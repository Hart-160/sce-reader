# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_SCETranslateEditor(object):
    def setupUi(self, SCEReader):
        if not SCEReader.objectName():
            SCEReader.setObjectName(u"SCEReader")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SCEReader.sizePolicy().hasHeightForWidth())
        SCEReader.setSizePolicy(sizePolicy)
        SCEReader.setMinimumSize(QSize(980, 0))
        SCEReader.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        SCEReader.setFont(font)
        self.centralwidget = QWidget(SCEReader)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMaximumSize(QSize(80, 30))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.sce_route = QLineEdit(self.centralwidget)
        self.sce_route.setObjectName(u"sce_route")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sce_route.sizePolicy().hasHeightForWidth())
        self.sce_route.setSizePolicy(sizePolicy3)
        self.sce_route.setMaximumSize(QSize(16777215, 30))
        self.sce_route.setFont(font)

        self.horizontalLayout.addWidget(self.sce_route)

        self.choose_sce = QPushButton(self.centralwidget)
        self.choose_sce.setObjectName(u"choose_sce")
        sizePolicy2.setHeightForWidth(self.choose_sce.sizePolicy().hasHeightForWidth())
        self.choose_sce.setSizePolicy(sizePolicy2)
        self.choose_sce.setMinimumSize(QSize(90, 30))
        self.choose_sce.setMaximumSize(QSize(90, 30))
        self.choose_sce.setFont(font)

        self.horizontalLayout.addWidget(self.choose_sce)

        self.template_generate = QPushButton(self.centralwidget)
        self.template_generate.setObjectName(u"template_generate")
        sizePolicy2.setHeightForWidth(self.template_generate.sizePolicy().hasHeightForWidth())
        self.template_generate.setSizePolicy(sizePolicy2)
        self.template_generate.setMinimumSize(QSize(90, 30))
        self.template_generate.setMaximumSize(QSize(90, 30))
        self.template_generate.setFont(font)

        self.horizontalLayout.addWidget(self.template_generate)

        self.horizontalLayout.setStretch(1, 10)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.sce_loader = QTableWidget(self.centralwidget)
        if (self.sce_loader.columnCount() < 2):
            self.sce_loader.setColumnCount(2)
        self.sce_loader.setObjectName(u"sce_loader")
        sizePolicy.setHeightForWidth(self.sce_loader.sizePolicy().hasHeightForWidth())
        self.sce_loader.setSizePolicy(sizePolicy)
        self.sce_loader.setMinimumSize(QSize(470, 630))
        self.sce_loader.setMaximumSize(QSize(16777215, 16777215))
        self.sce_loader.setFont(font)
        self.sce_loader.setIconSize(QSize(60, 60))
        self.sce_loader.setColumnCount(2)
        self.sce_loader.horizontalHeader().setVisible(False)
        self.sce_loader.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.sce_loader)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setMaximumSize(QSize(80, 30))
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.template_route = QLineEdit(self.centralwidget)
        self.template_route.setObjectName(u"template_route")
        sizePolicy3.setHeightForWidth(self.template_route.sizePolicy().hasHeightForWidth())
        self.template_route.setSizePolicy(sizePolicy3)
        self.template_route.setMaximumSize(QSize(16777215, 30))
        self.template_route.setFont(font)

        self.horizontalLayout_2.addWidget(self.template_route)

        self.open_template = QPushButton(self.centralwidget)
        self.open_template.setObjectName(u"open_template")
        sizePolicy2.setHeightForWidth(self.open_template.sizePolicy().hasHeightForWidth())
        self.open_template.setSizePolicy(sizePolicy2)
        self.open_template.setMinimumSize(QSize(60, 30))
        self.open_template.setMaximumSize(QSize(60, 30))
        self.open_template.setFont(font)

        self.horizontalLayout_2.addWidget(self.open_template)

        self.save_template = QPushButton(self.centralwidget)
        self.save_template.setObjectName(u"save_template")
        sizePolicy2.setHeightForWidth(self.save_template.sizePolicy().hasHeightForWidth())
        self.save_template.setSizePolicy(sizePolicy2)
        self.save_template.setMinimumSize(QSize(60, 30))
        self.save_template.setMaximumSize(QSize(60, 30))
        self.save_template.setFont(font)

        self.horizontalLayout_2.addWidget(self.save_template)

        self.clear_template = QPushButton(self.centralwidget)
        self.clear_template.setObjectName(u"clear_template")
        sizePolicy2.setHeightForWidth(self.clear_template.sizePolicy().hasHeightForWidth())
        self.clear_template.setSizePolicy(sizePolicy2)
        self.clear_template.setMinimumSize(QSize(60, 30))
        self.clear_template.setMaximumSize(QSize(60, 30))
        self.clear_template.setFont(font)

        self.horizontalLayout_2.addWidget(self.clear_template)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.template_loader = QTableWidget(self.centralwidget)
        if (self.template_loader.columnCount() < 4):
            self.template_loader.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.template_loader.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.template_loader.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.template_loader.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.template_loader.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.template_loader.horizontalHeader().resizeSection(0, 50)
        self.template_loader.horizontalHeader().resizeSection(1, 100)
        self.template_loader.horizontalHeader().resizeSection(2, 300)
        self.template_loader.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.template_loader.horizontalHeader().resizeSection(3, 100)
        self.template_loader.setObjectName(u"template_loader")
        sizePolicy.setHeightForWidth(self.template_loader.sizePolicy().hasHeightForWidth())
        self.template_loader.setSizePolicy(sizePolicy)
        self.template_loader.setMinimumSize(QSize(470, 630))
        self.template_loader.setMaximumSize(QSize(16777215, 16777215))
        self.template_loader.setFont(font)
        self.template_loader.setIconSize(QSize(60, 60))
        self.template_loader.setColumnCount(4)
        self.template_loader.horizontalHeader().setVisible(False)
        self.template_loader.horizontalHeader().setDefaultSectionSize(50)
        self.template_loader.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.template_loader)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        SCEReader.setCentralWidget(self.centralwidget)

        self.retranslateUi(SCEReader)

        QMetaObject.connectSlotsByName(SCEReader)
    # setupUi

    def retranslateUi(self, SCEReader):
        SCEReader.setWindowTitle(QCoreApplication.translate("SCEReader", u"SCE Translate Editor", None))
        self.label.setText(QCoreApplication.translate("SCEReader", u"SCE\u6587\u4ef6\uff1a", None))
        self.choose_sce.setText(QCoreApplication.translate("SCEReader", u"\u8f7d\u5165\u6587\u4ef6", None))
        self.template_generate.setText(QCoreApplication.translate("SCEReader", u"\u6a21\u677f\u751f\u6210", None))
        self.label_2.setText(QCoreApplication.translate("SCEReader", u"\u6a21\u677f\u6587\u4ef6\uff1a", None))
        self.open_template.setText(QCoreApplication.translate("SCEReader", u"\u6253\u5f00", None))
        self.save_template.setText(QCoreApplication.translate("SCEReader", u"\u4fdd\u5b58", None))
        self.clear_template.setText(QCoreApplication.translate("SCEReader", u"\u6e05\u7a7a", None))
        ___qtablewidgetitem = self.template_loader.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SCEReader", u"\u884c\u6570", None));
        ___qtablewidgetitem1 = self.template_loader.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SCEReader", u"\u8bf4\u8bdd\u4eba", None));
        ___qtablewidgetitem2 = self.template_loader.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SCEReader", u"\u7ffb\u8bd1\u6587\u672c", None));
        ___qtablewidgetitem3 = self.template_loader.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SCEReader", u"\u6362\u884c", None));
    # retranslateUi

