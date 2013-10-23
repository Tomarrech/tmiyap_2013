# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try1.ui'
#
# Created: Thu Oct 10 12:47:02 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(509, 262)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 30, 221, 71))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(340, 30, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton_1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(320, 80, 91, 31))
        self.pushButton_1.setObjectName(_fromUtf8("pushButton_1"))
        self.close_Button = QtGui.QPushButton(self.centralwidget)
        self.close_Button.setGeometry(QtCore.QRect(360, 170, 91, 31))
        self.close_Button.setObjectName(_fromUtf8("close_Button"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_1 = QtGui.QAction(MainWindow)
        self.action_1.setObjectName(_fromUtf8("action_1"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.menu.addAction(self.action_1)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.lineEdit.setText(_translate("MainWindow", "box1", None))
        self.pushButton_1.setText(_translate("MainWindow", "PushButton", None))
        self.close_Button.setText(_translate("MainWindow", "Close", None))
        self.menu.setTitle(_translate("MainWindow", "блах-блах", None))
        self.action_1.setText(_translate("MainWindow", "блах1", None))
        self.action_2.setText(_translate("MainWindow", "блах2", None))

