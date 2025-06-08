# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QListView, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        if not MainMenu.objectName():
            MainMenu.setObjectName(u"MainMenu")
        MainMenu.resize(1280, 720)
        MainMenu.setMinimumSize(QSize(1280, 720))
        MainMenu.setMaximumSize(QSize(1280, 720))
        self.lineEdit = QLineEdit(MainMenu)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(70, 260, 201, 81))
        self.push_POST_request = QPushButton(MainMenu)
        self.push_POST_request.setObjectName(u"push_POST_request")
        self.push_POST_request.setGeometry(QRect(70, 370, 75, 91))
        self.push_GET_request = QPushButton(MainMenu)
        self.push_GET_request.setObjectName(u"push_GET_request")
        self.push_GET_request.setGeometry(QRect(180, 370, 75, 91))
        self.listView = QListView(MainMenu)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(420, 200, 561, 391))

        self.retranslateUi(MainMenu)

        QMetaObject.connectSlotsByName(MainMenu)
    # setupUi

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QCoreApplication.translate("MainMenu", u"Form", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainMenu", u"URL", None))
        self.push_POST_request.setText(QCoreApplication.translate("MainMenu", u"POST", None))
        self.push_GET_request.setText(QCoreApplication.translate("MainMenu", u"GET", None))
    # retranslateUi

