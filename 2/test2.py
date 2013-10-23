import sys
import shutil
from test import Ui_MainWindow as UIMW
from PyQt4 import QtCore, QtGui
import urllib2 as ulib
#import  QFileDialog.py
#from PyQt4 import QtGui
#from PyQt4 import QtCore


class MyWindow(QtGui.QMainWindow, UIMW):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.__setupConnections()

    def __setupConnections(self):
        self.connect(self.addphoto, QtCore.SIGNAL("clicked()"), self._addphotoClicked)
        self.connect(self.addphotoandtag, QtCore.SIGNAL("clicked()"), self._addphotoandtagClicked)
        self.connect(self.removephoto, QtCore.SIGNAL("clicked()"), self._removephotoClicked)
        self.connect(self.searchphoto, QtCore.SIGNAL("clicked()"), self._searchphotoClicked)
        self.connect(self.cancel, QtCore.SIGNAL("clicked()"), self._cancelClicked)
        self.connect(self.actionImport_Photos, QtCore.SIGNAL("triggered()"), self._actionImport_Photos)
        self.connect(self.actionExit, QtCore.SIGNAL("triggered()"), self._actionExit)
        self.connect(self.listView, QtCore.SIGNAL("triggered()"), self._listView)

    def _addphotoClicked(self):
        shutil.copytree('/home/waseem/My Pictures/yemen 2008/2008/1',
                        '/home/waseem/test')

    def _addphotoandtagClicked(self):
        pass

    def _searchphotoClicked(self):
        pass

    def _removephotoClicked(self):
        pass

    def _FinishClicked(self):
        pass

    def _cancelClicked(self):
        pass

    def _actionImport_Photos(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Import Photo',
                                                     '/home/')#, tr('Images (*.png *.xpm *.jpg)'));
        #self.items=[]
        self.item.append(QlistViewitem(self.tree, 'filename'))
        # file=open(filename)
        #data = file.read()
        #print data
        #self.photosdisplay.read(data)

    def _actionExit(self):
        pass

    def _listView(self):
        pass

#class Import_Photos(QtGui.QMainWindow, UIMW):

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
