#!/usr/bin/python
# coding=utf-8
from testapp_ui import TestAppUI
from qt import *
import sys
class HelloApplication(QApplication):
    def __init__(self, args):
        """
            В конструкторе мы делаем всё, что необходимо для запска нашего приложения, которое
            создаёт QApplication в __init__ методе, затем добваляет наши виджеты и, наконец,
            запускает exec_loop
        """
        QApplication.__init__(self,args)
        # Мы передаём None т.к. этот виджет верхнего уровня
        self.maindialog = TestApp(None)
        self.setMainWidget(self.maindialog)
        self.maindialog.show()
        self.exec_loop()


class TestApp(TestAppUI):
    def __init__(self,parent):
        # Запускаем родительский конструктор и присоединяем слоты к методам
        TestAppUI.__init__(self,parent)
        self._connectSlots()
        # Изначально список пуст, так что кнопка удаления не должна работать
        # Сделаем её неактивной
        self.deletebutton.setEnabled(False)
    def _connectSlots(self):
        # Устанавливаем обработчики сингналов на кнопки
        self.connect(self.addbutton,SIGNAL("clicked()"),self._slotAddClicked)
        self.connect(self.lineedit,SIGNAL("returnPressed()"),self._slotAddClicked)
        self.connect(self.deletebutton,SIGNAL("clicked()"),self._slotDeleteClicked)
    def _slotAddClicked(self):
        # Читаем тескт из lineedit,
        text = self.lineedit.text()
        # если lineedit не пуст,
        if len(text):
            # вставим новый элемент в список ...
            lvi = QListViewItem(self.listview)
            # с текстом из lineedit ...
            lvi.setText(0,text)
            # и очистим lineedit.
            self.lineedit.clear()
            # Кнопка удаления м.б. выключена, так что включим её.
            self.deletebutton.setEnabled(True)
    def _slotDeleteClicked(self):
        # Удаляем выбранный элемент из списка
        self.listview.takeItem(self.listview.currentItem())
        # Check if the list is empty - if yes, disable the deletebutton.
        # Если список после этого оказался пустым, то сделаем кнопку удаления неактивной
        if self.listview.childCount() == 0:
            self.deletebutton.setEnabled(False)
if __name__ == "__main__":
    app = HelloApplication(sys.argv)