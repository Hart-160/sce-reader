import ctypes
import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from dialogue_sections import DialogueSections
from ui_reader import Ui_SCEReader
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

class Reader(QMainWindow, Ui_SCEReader):
    if getattr(sys, 'frozen', False):
        root = sys._MEIPASS
    else:
        root, _ = os.path.split(os.path.abspath(sys.argv[0]))

    def __init__(self):
        super(Reader, self).__init__()
        icon = QPixmap()
        icon.loadFromData(B64_Images.get_b64_icon(B64_Images.READER_ICON_B64))
        self.setWindowIcon(icon)
        self.setupUi(self)

        self.choose_sce.clicked.connect(self.select_sce)
        self.template_generate.clicked.connect(self.generateTemplate)

        self.sce_table = self.sce_loader
        self.src_talk = []

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
            self.load_sce_list()
        else:
            return

    def select_sce(self):
        #选择sce文件
        scePath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择SCE文件",
            os.getcwd(),
            "文件类型 (*.sce)"
        )
        if scePath == '':
            return
        self.sce_route.setText(scePath)
        self.load_sce_list()

    def load_sce_list(self):
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
            
        self.sce_table.setCurrentCell(0,0)
        
    def generateTemplate(self):
        #生成翻译模板
        sce = self.sce_route.text()
        if sce == '':
            QMessageBox.critical(self, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            TemplateUtils.sce_to_template(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEMPLATE] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self, '任务完成', '模板已成功生成！', QMessageBox.Ok, QMessageBox.Ok)

if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    if sys.platform.startswith('win'):
        ctypes.windll.user32.SetProcessDPIAware()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    stats = Reader()
    stats.show()
    app.exec_()
