import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from ui_reader import Ui_SCEReader
from dictionary import chara_li
from dialogue_sections import DialogueSections

class Reader(QMainWindow, Ui_SCEReader):
    if getattr(sys, 'frozen', False):
        root = sys._MEIPASS
    else:
        root, _ = os.path.split(os.path.abspath(sys.argv[0]))

    def __init__(self):
        super(Reader, self).__init__()
        self.setWindowIcon(QIcon('image/icon/RD.ico'))
        self.setupUi(self)

        self.choose_sce.clicked.connect(self.select_sce)

        self.sce_table = self.sce_loader
        self.src_talk = []

    def select_sce(self):
        #选择sce文件
        scePath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择SCE文件",
            r"c:\\",
            "文件类型 (*.sce)"
        )
        self.sce_route.setText(scePath)
        self.load_sce_list()

    def load_sce_list(self):
        #从sce加载列表显示在左侧表格
        if self.sce_route.text() == '':
            self.sce_table.setRowCount(0)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stats = Reader()
    stats.show()
    app.exec_()
