# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_window_test.ui'
#
# Created: Thu Oct 24 01:46:52 2013
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
        MainWindow.setEnabled(True)
        MainWindow.resize(661, 392)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(999999, 999999))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        MainWindow.setAcceptDrops(False)
        MainWindow.setAccessibleDescription(_fromUtf8(""))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 160, 135, 74))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line_orderName = QtGui.QLineEdit(self.layoutWidget)
        self.line_orderName.setObjectName(_fromUtf8("line_orderName"))
        self.verticalLayout.addWidget(self.line_orderName)
        self.line_orderCountry = QtGui.QLineEdit(self.layoutWidget)
        self.line_orderCountry.setObjectName(_fromUtf8("line_orderCountry"))
        self.verticalLayout.addWidget(self.line_orderCountry)
        self.line_orderDilivery = QtGui.QLineEdit(self.layoutWidget)
        self.line_orderDilivery.setObjectName(_fromUtf8("line_orderDilivery"))
        self.verticalLayout.addWidget(self.line_orderDilivery)
        self.button_createOrder = QtGui.QPushButton(self.centralwidget)
        self.button_createOrder.setGeometry(QtCore.QRect(80, 240, 131, 31))
        self.button_createOrder.setObjectName(_fromUtf8("button_createOrder"))
        self.dateTime_Order = QtGui.QDateTimeEdit(self.centralwidget)
        self.dateTime_Order.setEnabled(True)
        self.dateTime_Order.setGeometry(QtCore.QRect(50, 280, 194, 22))
        self.dateTime_Order.setObjectName(_fromUtf8("dateTime_Order"))

        self.listView = QtGui.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 80, 256, 61))
        self.listView.setObjectName(_fromUtf8("listView"))

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 10, 256, 61))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(280, 10, 371, 61))
        self.tableView.setObjectName(_fromUtf8("tableView"))

        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(280, 80, 371, 61))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(5)

        self.columnView = QtGui.QColumnView(self.centralwidget)
        self.columnView.setGeometry(QtCore.QRect(280, 150, 256, 192))
        self.columnView.setObjectName(_fromUtf8("columnView"))

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 170, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 190, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 210, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 661, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_loadFromFile = QtGui.QAction(MainWindow)
        self.action_loadFromFile.setObjectName(_fromUtf8("action_loadFromFile"))
        self.action_uploadToFile = QtGui.QAction(MainWindow)
        self.action_uploadToFile.setObjectName(_fromUtf8("action_uploadToFile"))
        self.menu.addAction(self.action_Quit)
        self.menu_2.addAction(self.action_loadFromFile)
        self.menu_2.addAction(self.action_uploadToFile)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление заказами", None))

        self.line_orderName.setText(_translate("MainWindow", "Имя заказа", None))
        self.line_orderCountry.setText(_translate("MainWindow", "Страна доставки", None))
        self.line_orderDilivery.setText(_translate("MainWindow", "Время доставки", None))

        self.button_createOrder.setText(_translate("MainWindow", "Создать заказ", None))

        self.label.setText(_translate("MainWindow", "Имя", None))
        self.label_2.setText(_translate("MainWindow", "Страна", None))
        self.label_3.setText(_translate("MainWindow", "Дата", None))

        self.menu.setTitle(_translate("MainWindow", "Меню", None))
        self.menu_2.setTitle(_translate("MainWindow", "Импорт, Экспорт", None))

        self.action_Quit.setText(_translate("MainWindow", "Выход", None))
        self.action.setText(_translate("MainWindow", "Сохранить в файл", None))
        self.action_loadFromFile.setText(_translate("MainWindow", "Загрузить из файла", None))
        self.action_uploadToFile.setText(_translate("MainWindow", "Сохранить в файл", None))

