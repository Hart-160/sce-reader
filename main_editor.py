import ctypes
import os
import sys
import json
import copy
import logging

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from dialogue_sections import DialogueSections
from ui_editor import Ui_SCETranslateEditor
from generate_tmp import *
from utilities import *

def rename(path_name,new_name):
    #应对出现重复文件的情况
    try:
        os.rename(path_name,new_name)
    except Exception as e:
        if e.args[0] ==17: #重命名
            fname, fename = os.path.splitext(new_name)
            rename(path_name, fname+"-1"+fename)

class Configs:
    #记录配置用
    PREFERRED_SCE_PATH = 'PreferredSCEPath'
    PREFERRED_TEMPLATE_PATH = 'PreferredTemplatePath'
    FONT_SIZE = 'FontSize'
    X_VALUE = 'XValue'
    Y_VALUE = 'YValue'
    WIDTH = 'Width'
    HEIGHT = 'Height'
    IS_MAXIMIZED = 'IsMaximized'
    
    def config_creator():
        data = {
            Configs.PREFERRED_SCE_PATH:'',
            Configs.PREFERRED_TEMPLATE_PATH:'',
            Configs.FONT_SIZE:20,
            Configs.X_VALUE:410,
            Configs.Y_VALUE:240,
            Configs.WIDTH:900,
            Configs.HEIGHT:600,
            Configs.IS_MAXIMIZED:False
        }
        with open('settings\\setting_editor.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info('Config File Created')

    def config_reader(parameter):
        with open('settings\\setting_editor.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
        logging.info('Config File Read')
        return data[parameter]

    def config_editor(parameter, input):
        with open('settings\\setting_editor.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
        data[parameter] = input
        with open('settings\\setting_editor.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info('Config File Edited')

class TranslateEditor(QMainWindow, Ui_SCETranslateEditor):
    if getattr(sys, 'frozen', False):
        root = sys._MEIPASS
    else:
        root, _ = os.path.split(os.path.abspath(sys.argv[0]))
        
    error_message = Signal(int) #告知GUI出现错误，弹出提示框

    #原文会出现的不太好打出来的特殊字符
    SPECIAL_SYMBOLS = [
        '♪', '☆', '「', '」', '『', '』', '♡', '〇', '℃', '■', '★'
    ]

    def __init__(self):
        super(TranslateEditor, self).__init__()
        
        self.move(Configs.config_reader(Configs.X_VALUE), Configs.config_reader(Configs.Y_VALUE))
        self.resize(Configs.config_reader(Configs.WIDTH), Configs.config_reader(Configs.HEIGHT))
        logging.info('Window Size Set from Config File')
        
        icon = QPixmap()
        icon.loadFromData(B64_Images.get_b64_icon(B64_Images.READER_ICON_B64))
        self.setWindowIcon(icon)
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.choose_sce.clicked.connect(self.select_sce)
        self.template_generate.clicked.connect(self.generateTemplate)
        self.open_template.clicked.connect(self.select_template)
        self.clear_template.clicked.connect(self.clear_template_table)
        self.save_template.clicked.connect(self.save_file_button)
        self.template_loader.itemChanged.connect(self.change_text)
        self.template_loader.currentCellChanged.connect(self.trackSrc)

        self.error_message.connect(self.pop_error)

        QShortcut(QKeySequence(self.tr("Ctrl+S")), self, self.save_file_button)

        self.sce_table = self.sce_loader
        self.template_table = self.template_loader
        self.src_talk = []
        self.dst_talk = []
        self.saved = True
        self.font_size = 20
        
        logging.info('Application Started')

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')[0] #拖拽多文件只取第一个地址
        filePath = filePath.replace('file:///', '', 1) #去除文件地址前缀的特定字符
        if filePath.endswith('.sce'):
            self.sce_route.setText(filePath)
            if self.template_route.text() == '':
                self.template_route.setText(os.path.split(filePath)[0] + '/[TEMPLATE] ' + os.path.split(filePath)[1][:-4] + '.txt')
            Configs.config_editor(Configs.PREFERRED_SCE_PATH, os.path.split(filePath)[0])
            logging.info('Choose SCE file by dropEvent: ' + filePath)
            self.load_sce_table_from_srcTalk()
            self.font_size = Configs.config_reader(Configs.FONT_SIZE)
            TranslateEditor.setFontSize(self, self.font_size)
            if self.dst_talk == []:
                self.template_route.setText(os.path.split(filePath)[0] + '/[TEMPLATE] ' + os.path.split(filePath)[1][:-4] + '.txt')
                self.template_table.clearContents()
                self.load_template_list_from_table()
            elif self.is_empty_text():
                self.template_route.setText(os.path.split(filePath)[0] + '/[TEMPLATE] ' + os.path.split(filePath)[1][:-4] + '.txt')
                self.template_table.clearContents()
                self.load_template_list_from_table()
            else:
                res = QMessageBox.question(self, '警告', '是否清空当前模板？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if res == QMessageBox.Yes:
                    self.template_route.setText(os.path.split(filePath)[0] + '/[TEMPLATE] ' + os.path.split(filePath)[1][:-4] + '.txt')
                    self.template_table.clearContents()
                    self.load_template_list_from_table()

        if filePath.endswith('.txt'):
            self.template_route.setText(filePath)
            Configs.config_editor(Configs.PREFERRED_TEMPLATE_PATH, os.path.split(filePath)[0])
            logging.info('Choose Template file by dropEvent: ' + filePath)
            if self.dst_talk == []:
                self.template_table.clearContents()
                self.load_template_list_from_file()
            else:
                res = QMessageBox.question(self, '警告', '是否清空当前模板？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if res == QMessageBox.Yes:
                    self.template_table.clearContents()
                    self.load_template_list_from_file()
            self.font_size = Configs.config_reader(Configs.FONT_SIZE)
            TranslateEditor.setTemplateFontSize(self, self.font_size)
        else:
            return

    def wheelEvent(self, event):
        # 捕捉鼠标滚轮事件
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers == Qt.ControlModifier:
            # 如果按下了 Ctrl 键
            delta = event.angleDelta().y()
            font = self.sce_loader.font()
            font.setPixelSize(self.font_size)
 
            # 根据滚轮方向调整字体大小
            if delta > 0:
                if self.font_size < 60:
                    self.font_size += 2
                    TranslateEditor.setFontSize(self, self.font_size)
            else:
                if self.font_size > 20:
                    self.font_size -= 2
                    TranslateEditor.setFontSize(self, self.font_size)

            Configs.config_editor(Configs.FONT_SIZE, self.font_size)
            
        else:
            # 如果没有按下 Ctrl 键，则使用默认滚轮事件处理
            super().wheelEvent(event)

    def trackSrc(self, currentRow, currentColumn, previousRow, previousColumn):
        if currentColumn >= 3:
            return
        srcrow = self.sce_table.rowCount()
        if currentRow < len(self.dst_talk):
            srcrow = min(srcrow, self.dst_talk[currentRow]['Index'])
            srcItem = self.sce_table.item(srcrow - 1, 1)
            self.sce_table.setCurrentItem(srcItem)

        currentItem = self.template_table.item(currentRow, currentColumn)
        self.template_table.editItem(currentItem)
        self.template_table.blockSignals(True)
        if currentItem:
            currentItem.setText(currentItem.text().split("\n")[0].rstrip().lstrip())
        self.template_table.blockSignals(False)

    def setFontSize(self, font_size):
        self.font_size = font_size
        if(not self.sce_loader):
            return
        font = self.sce_loader.font()
        font.setPixelSize(self.font_size)
        self.sce_loader.setFont(font)
        self.template_loader.setFont(font)
        self.template_loader.horizontalHeader().setFont(font)
        self.sce_loader.horizontalHeader().resizeSection(0, self.font_size * 7)
        
        self.template_loader.horizontalHeader().resizeSection(0, self.font_size * 2 + 20)
        self.template_loader.horizontalHeader().resizeSection(1, self.font_size * 7)
        self.template_loader.horizontalHeader().resizeSection(3, self.font_size * 3 + 40)

        for row in range(self.sce_loader.rowCount()):
            text = self.sce_loader.item(row, 1).text()
            height = len(text.split('\n'))
            self.sce_loader.setRowHeight(row, 40 + (20 + self.font_size) * height)
        for row in range(self.template_loader.rowCount()):
            text = self.template_loader.item(row, 1).text()
            height = len(text.split('\n'))
            self.template_loader.setRowHeight(row, 40 + (20 + self.font_size) * height)

    def setTemplateFontSize(self, font_size):
        self.font_size = font_size
        if(not self.template_loader):
            return
        font = self.template_loader.font()
        font.setPixelSize(self.font_size)
        self.template_loader.setFont(font)
        self.template_loader.horizontalHeader().setFont(font)
        self.template_loader.horizontalHeader().resizeSection(0, self.font_size * 2 + 20)
        self.template_loader.horizontalHeader().resizeSection(1, self.font_size * 7)
        self.template_loader.horizontalHeader().resizeSection(3, self.font_size * 3 + 40)

        for row in range(self.template_loader.rowCount()):
            text = self.template_loader.item(row, 1).text()
            height = len(text.split('\n'))
            self.template_loader.setRowHeight(row, 40 + (20 + self.font_size) * height)

    def select_sce(self):
        #选择sce文件
        config_sce_path = Configs.config_reader(Configs.PREFERRED_SCE_PATH)
        if config_sce_path == '':
            config_sce_path = r"C:\\"
        scePath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择SCE文件",
            config_sce_path,
            "文件类型 (*.sce)"
        )
        if scePath == '':
            return
        self.sce_route.setText(scePath)
        if self.template_route.text() == '':
            self.template_route.setText(os.path.split(scePath)[0] + '/[TEMPLATE] ' + os.path.split(scePath)[1][:-4] + '.txt')
        Configs.config_editor(Configs.PREFERRED_SCE_PATH, os.path.split(scePath)[0])
        logging.info('Choose SCE file by select_sce: ' + scePath)
        self.load_sce_table_from_srcTalk()
        self.font_size = Configs.config_reader(Configs.FONT_SIZE)
        TranslateEditor.setFontSize(self, self.font_size)
        if self.dst_talk == []:
            self.template_route.setText(os.path.split(scePath)[0] + '/[TEMPLATE] ' + os.path.split(scePath)[1][:-4] + '.txt')
            self.template_table.clearContents()
            self.load_template_list_from_table()
        elif self.is_empty_text():
            self.template_route.setText(os.path.split(scePath)[0] + '/[TEMPLATE] ' + os.path.split(scePath)[1][:-4] + '.txt')
            self.template_table.clearContents()
            self.load_template_list_from_table()
        else:
            res = QMessageBox.question(self, '警告', '是否清空当前模板？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.template_route.setText(os.path.split(scePath)[0] + '/[TEMPLATE] ' + os.path.split(scePath)[1][:-4] + '.txt')
                self.template_table.clearContents()
                self.load_template_list_from_table()

    def load_sce_table_from_srcTalk(self):
        #从sce加载列表显示在左侧表格
        if self.sce_route.text() == '':
            return
        
        ev_li = DialogueSections.sce_handler(self.sce_route.text())
        self.src_talk = ev_li
        self.sce_table.setRowCount(len(ev_li))
        
        for i in range(len(ev_li)):
            talker_id = ''
            for idx, chara in enumerate(chara_li):
                if ev_li[i]['Talker'] == chara['FirstName']:
                    talker_id = chara['ID']
                    break
            if talker_id != '':
                iconpath = "image/icon/char/{}.png".format(talker_id)
                iconpath = os.path.join(self.root, iconpath)
                icon = QTableWidgetItem(QIcon(iconpath), ev_li[i]['Talker'])
                self.sce_table.setItem(i, 0, icon)
            else:
                self.sce_table.setItem(i, 0, QTableWidgetItem(ev_li[i]['Talker']))
            self.sce_table.setItem(i, 1, QTableWidgetItem(ev_li[i]['Body']))
            height = len(ev_li[i]['Body'].split('\n')) - 1
            self.sce_table.setRowHeight(i, 72 + 20 * height)
            
        self.sce_table.setCurrentItem(self.sce_table.item(0, 1))
        self.saved = True
        self.setWindowTitle('SCE Translate Editor')
        logging.info('SCE Table Loaded')
    
    def is_empty_text(self) -> bool:
        #判断dst_talk是否无文本
        for talk in self.dst_talk:
            for char in talk['Body']:
                if char in TranslateEditor.SPECIAL_SYMBOLS:
                    talk['Body'] = talk['Body'].replace(char, '')
            if talk['Body'] != '':
                return False
        return True
    
    def generateTemplate(self):
        #生成翻译模板
        sce = self.sce_route.text()
        if sce == '':
            QMessageBox.critical(self, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('No SCE file input')
        else:
            TemplateUtils.sce_to_template(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEMPLATE] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self, '任务完成', '模板已成功生成！', QMessageBox.Ok, QMessageBox.Ok)
            logging.info('Template File Generated by Button')
            
    def load_template_list_from_table(self):
        #加载模板列表
        self.template_table.horizontalHeader().setVisible(True)
        if self.sce_route.text() == '':
            return
        if self.dst_talk != []:
            self.dst_talk = []
        for talk in self.src_talk:
            if not '\n' in talk['Body']:
                talk['Start'] = True
                talk['End'] = True
                talk['Body'] = ''
                self.dst_talk.append(talk)
            else:
                body = talk['Body'].split('\n')
                for i in range(len(body)):
                    new_talk = {'Index':talk['Index'], 'EventType':talk['EventType'], 'Talker':'', 'Body':''}
                    for char in body[i]:
                        if char in TranslateEditor.SPECIAL_SYMBOLS:
                            new_talk['Body'] += char
                    if i == 0:
                        new_talk['Talker'] = talk['Talker']
                        new_talk['Start'] = True
                    if i == len(body) - 1:
                        new_talk['End'] = True
                    self.dst_talk.append(new_talk)
        logging.info('dst_talk created from src_talk')
        self.load_template_table_from_dstTalk()
    
    def load_template_table_from_dstTalk(self):
        self.template_table.setRowCount(len(self.dst_talk))
        for i in range(len(self.dst_talk)):
            talk = self.dst_talk[i]
            if 'Start' in talk and self.dst_talk[i]['EventType'] == 'Dialogue':
                column1_item = QTableWidgetItem(str(self.dst_talk[i]['Index']))
            elif self.dst_talk[i]['EventType'] == 'Title' or self.dst_talk[i]['EventType'] == 'Subtitle':
                column1_item = QTableWidgetItem(str(self.dst_talk[i]['Index']))
            else:
                column1_item = QTableWidgetItem('')
            column1_item.setFlags(Qt.ItemIsSelectable)
            self.template_table.setItem(i, 0, column1_item)
            
            if 'Start' in talk:
                self.template_table.setItem(i, 1, QTableWidgetItem(self.dst_talk[i]['Talker']))
            else:
                column2_item = QTableWidgetItem('')
                column2_item.setFlags(Qt.ItemIsSelectable)
                self.template_table.setItem(i, 1, column2_item)
                
            self.template_table.setItem(i, 2, QTableWidgetItem(self.dst_talk[i]['Body']))
            height = len(self.dst_talk[i]['Body'].split('\n')) - 1
            self.template_table.setRowHeight(i, 72 + 20 * height)
            
            if 'End' in talk and self.dst_talk[i]['EventType'] == 'Dialogue':
                column4_item = QTableWidgetItem('')
                column4_item.setFlags(Qt.ItemIsSelectable)
                self.template_table.setItem(i, 3, column4_item)
                
                line_ctrl = QWidget()
                layout = QHBoxLayout(line_ctrl)
                if self.dst_talk[i]['EventType'] == 'Dialogue':
                    button_add = QPushButton('+', line_ctrl)
                    button_add.setFixedSize(35, 35)
                    layout.addWidget(button_add)
                    button_add.clicked.connect(self.add_line)
                    
                if not 'Start' in talk:
                    button_remove = QPushButton('-', line_ctrl)
                    button_remove.setFixedSize(35, 35)
                    layout.addWidget(button_remove)
                    button_remove.clicked.connect(self.remove_line)

                self.template_table.setCellWidget(i, 3, line_ctrl)
                
            elif self.dst_talk[i]['EventType'] == 'Title' or self.dst_talk[i]['EventType'] == 'Subtitle':
                column4_item = QTableWidgetItem('')
                column4_item.setFlags(Qt.ItemIsSelectable)
                self.template_table.setItem(i, 3, column4_item)
                
            else:
                column4_item = QTableWidgetItem('\\N')
                column4_item.setFlags(Qt.ItemIsSelectable)
                self.template_table.setItem(i, 3, column4_item)
        
        self.font_size = Configs.config_reader(Configs.FONT_SIZE)
        TranslateEditor.setTemplateFontSize(self, self.font_size)
        self.template_table.setCurrentItem(self.template_table.item(0, 2))
        self.saved = True
        self.setWindowTitle('SCE Translate Editor')
        logging.info('Template Table Loaded')
    
    def add_line(self):
        button = self.sender()
        if button:
            tablecell = button.parent()
            row = self.template_table.indexAt(tablecell.pos()).row()
            new_talk = copy.deepcopy(self.dst_talk[row])
            if 'Start' in new_talk:
                del new_talk['Start']
            del self.dst_talk[row]['End']
            new_talk['End'] = True
            new_talk['Body'] = ''
            self.dst_talk.insert(row + 1, new_talk)
            
            self.template_table.clearContents()
            self.template_table.setRowCount(0)
            self.load_template_table_from_dstTalk()
            self.template_table.setCurrentItem(self.template_table.item(row + 1, 2))
            self.template_table.editItem(self.template_table.item(row + 1, 2))
                
    def remove_line(self):
        button = self.sender()
        if button:
            tablecell = button.parent()
            row = self.template_table.indexAt(tablecell.pos()).row()
            if row > 0:
                self.dst_talk[row - 1]['End'] = True
            self.dst_talk.pop(row)

            self.template_table.clearContents()
            self.template_table.setRowCount(0)
            self.load_template_table_from_dstTalk()
            self.template_table.setCurrentItem(self.template_table.item(row-1, 2))
            self.template_table.editItem(self.template_table.item(row-1, 2))
    
    def select_template(self):
        if os.path.exists(self.template_route.text()) and self.dst_talk[0]['Body'] == '':
            templatePath = self.template_route.text()
        else:
            if self.dst_talk != []:
                res = QMessageBox.question(self, '警告', '是否清空当前模板？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if res == QMessageBox.No:
                    return
                self.dst_talk = []
            config_template_path = Configs.config_reader(Configs.PREFERRED_TEMPLATE_PATH)
            if config_template_path == '':
                config_template_path = r"C:\\"
            templatePath, _  = QFileDialog.getOpenFileName(
                self,             
                "选择翻译模板文件",
                config_template_path,
                "文件类型 (*.txt)"
            )
            if templatePath == '':
                return
        self.template_route.setText(templatePath)
        Configs.config_editor(Configs.PREFERRED_TEMPLATE_PATH, os.path.split(templatePath)[0])
        logging.info('Choose Template file by select_template: ' + templatePath)
        self.template_table.clearContents()
        self.load_template_list_from_file()
    
    def load_template_list_from_file(self):
        if self.template_route.text() == '':
            return
        
        if self.dst_talk != []:
            self.dst_talk = []
        
        self.template_table.horizontalHeader().setVisible(True)
        with open(self.template_route.text(), 'r', encoding='utf-8') as f:
            template_li = f.readlines()
        index_count = 1
        for line in template_li:
            talk = {}
            talk['Index'] = index_count
            talker = line.split(':', 1)[0]
            if talker == 'Title':
                event_type = 'Title'
            elif talker == 'Subtitle':
                event_type = 'Subtitle'
            else:
                event_type = 'Dialogue'
            talk['EventType'] = event_type
            
            body = line.split(':', 1)[1]
            body = body.replace('\n', '')
            if not '\\N' in body:
                talk['Talker'] = talker
                talk['Body'] = body
                talk['Start'] = True
                talk['End'] = True
                self.dst_talk.append(talk)
            else:
                body = body.split('\\N')
                for i in range(len(body)):
                    new_talk = {'Index':index_count, 'EventType':event_type, 'Talker':talker, 'Body':body[i]}
                    if i == 0:
                        new_talk['Talker'] = talker
                        new_talk['Start'] = True
                    if i == len(body) - 1:
                        new_talk['End'] = True
                    self.dst_talk.append(new_talk)
            index_count += 1
        
        logging.info('dst_talk loaded from template file')
        self.load_template_table_from_dstTalk()
        self.font_size = Configs.config_reader(Configs.FONT_SIZE)
        TranslateEditor.setTemplateFontSize(self, self.font_size)
    
    def save_file(self, file_path):
        output = ''
        
        for talk in self.dst_talk:
            if 'Start' in talk:
                output += talk['Talker']
                output += (':')
            output +=talk['Body']
            if 'End' in talk and talk['EventType'] == 'Dialogue':
                output += '\n'
            elif talk['EventType'] == 'Title' or talk['EventType'] == 'Subtitle':
                output += '\n'
            else:
                output += '\\N'
        
        output = output.rstrip()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output)
            
    def save_file_button(self):
        if self.template_route.text() == '':
            QMessageBox.critical(self, '发生错误', '模板路径不存在！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('No Template file input')
        else:
            self.save_file(self.template_route.text())
            self.saved = True
            self.setWindowTitle('SCE Translate Editor')
            logging.info('Template File Saved')

    def change_text(self, item):
        if item.column() == 2:
            row = item.row()
            self.dst_talk[row]['Body'] = item.text()
            if row < self.template_table.rowCount() - 1:
                nextItem = self.template_table.item(row + 1, item.column())
                self.template_table.setCurrentItem(nextItem)
                self.template_table.editItem(nextItem)
        
        self.saved = False
        self.setWindowTitle('SCE Translate Editor - [未保存]')
        self.save_file(os.path.join(os.getcwd(), 'settings/[Auto-Save].txt'))

    def clear_template_table(self):
        if self.dst_talk == []:
            QMessageBox.critical(self, '发生错误', '模板已为空！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('Template already empty before clear_template_table()')
        else:
            reply = QMessageBox.question(self, '警告', '是否清空模板？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.template_table.clearContents()
                self.template_table.setRowCount(0)
                if self.src_talk != []:
                    for i in range(len(self.dst_talk)):
                        self.dst_talk[i]['Body'] = ''
                    self.load_template_table_from_dstTalk()
                    self.sce_table.setCurrentItem(self.sce_table.item(0, 1))
                    self.template_table.setCurrentItem(self.template_table.item(0, 2))
                else:
                    self.template_loader.horizontalHeader().setVisible(False)
                    self.template_route.setText('')
                    self.dst_talk = []
                self.saved = True
                self.setWindowTitle('SCE Translate Editor')
                logging.info('Template Table Cleared by Button')

    def check_save(self) -> bool:
        if self.saved:
            logging.info('Exit with Changes Saved')
            return True
        
        reply = QMessageBox.question(self, '警告', '修改尚未保存，是否保存？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.No:
            logging.info('Changes Discarded Right Before Exit')
            return True
        elif reply == QMessageBox.Yes:
            self.save_file_button()
            logging.info('Changes Saved Right Before Exit')
            return True
        elif reply == QMessageBox.Cancel:
            logging.info('Exit Cancelled')
            return False
        
    def closeEvent(self, event):
        if not self.check_save():
            event.ignore()
            return
        Configs.config_editor(Configs.X_VALUE, QMainWindow.frameGeometry(self).x())
        Configs.config_editor(Configs.Y_VALUE, QMainWindow.frameGeometry(self).y())
        Configs.config_editor(Configs.WIDTH, QMainWindow.frameGeometry(self).width())
        Configs.config_editor(Configs.HEIGHT, QMainWindow.frameGeometry(self).height())
        Configs.config_editor(Configs.IS_MAXIMIZED, self.isMaximized())
        logging.info('Window Info Saved')
        event.accept()

    def pop_error(self, status_code:int):
        if status_code == -1:
            QMessageBox.critical(self, 'D4DJ ASS AUTOMATION', '发生未知错误！<br>请将settings/log.txt发送给广间！', QMessageBox.Ok, QMessageBox.Ok)

if __name__ == '__main__':
    
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    if sys.platform.startswith('win'):
        ctypes.windll.user32.SetProcessDPIAware()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    if not os.path.exists('settings'):
        os.makedirs('settings')
        
    logging.basicConfig(filename='settings\\log.txt', filemode='w', level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    
    if not os.path.exists('settings\\setting_editor.json'):
        Configs.config_creator()
    
    app = QApplication(sys.argv)
    stats = TranslateEditor()
    
    def handle_exception(exc_type, exc_value, exc_traceback):
        #GUI部分的log输出，sys的excepthook有三个参数
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)) # 重点
        stats.error_message.emit(-1)
    sys.excepthook = handle_exception

    if Configs.config_reader(Configs.IS_MAXIMIZED):
        stats.showMaximized()
    stats.show()
    app.exec_()
