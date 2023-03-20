# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reader.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_SCEReader(object):
    def setupUi(self, SCEReader):
        if not SCEReader.objectName():
            SCEReader.setObjectName(u"SCEReader")
        SCEReader.resize(450, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SCEReader.sizePolicy().hasHeightForWidth())
        SCEReader.setSizePolicy(sizePolicy)
        SCEReader.setMinimumSize(QSize(450, 0))
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
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
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


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.sce_loader = QTableWidget(self.centralwidget)
        if (self.sce_loader.columnCount() < 2):
            self.sce_loader.setColumnCount(2)
        self.sce_loader.setObjectName(u"sce_loader")
        sizePolicy.setHeightForWidth(self.sce_loader.sizePolicy().hasHeightForWidth())
        self.sce_loader.setSizePolicy(sizePolicy)
        self.sce_loader.setMinimumSize(QSize(0, 0))
        self.sce_loader.setMaximumSize(QSize(16777215, 16777215))
        self.sce_loader.setFont(font)
        self.sce_loader.setIconSize(QSize(60, 60))
        self.sce_loader.setColumnCount(2)
        self.sce_loader.horizontalHeader().setVisible(False)
        self.sce_loader.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.sce_loader)

        SCEReader.setCentralWidget(self.centralwidget)

        self.retranslateUi(SCEReader)

        QMetaObject.connectSlotsByName(SCEReader)
    # setupUi

    def retranslateUi(self, SCEReader):
        SCEReader.setWindowTitle(QCoreApplication.translate("SCEReader", u"SCE Reader", None))
        self.label.setText(QCoreApplication.translate("SCEReader", u"SCE\u6587\u4ef6\uff1a", None))
        self.choose_sce.setText(QCoreApplication.translate("SCEReader", u"\u8f7d\u5165\u6587\u4ef6", None))
    # retranslateUi

