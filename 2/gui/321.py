#coding: utf-8
__author__ = 'tomar_000'
import sys

from PyQt4 import QtGui, QtCore

from gui.gui_window2 import Ui_MainWindow as UIMW


class MainWindow(QtGui.QMainWindow, UIMW):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.__setupConnections()
        self.statusBar().showMessage('Ready')

        self.action_Quit.setShortcut('Ctrl+Q')
        self.connect(self.action_Quit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

    def __setupConnections(self):
        self.connect(self.button_createOrder, QtCore.SIGNAL("clicked()"), self._reaction)

    def _reaction(self):
        text_orderName = self.line_orderName.text()
        text_orderCountry = self.line_orderCountry.text()
        text_orderDilivery = self.line_orderDilivery.text()
        if len(text_orderName):
            lvi = QtGui.QListWidgetItem(self.listWidget_Orders)
            lvi.setText(text_orderName+' | '+text_orderCountry+' | '+text_orderDilivery)
            self.line_orderName.clear()
            self.line_orderCountry.clear()
            self.line_orderDilivery.clear()

        self.statusBar().showMessage(unicode(text_orderName))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
