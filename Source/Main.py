import os, sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout

from MainForm.PyUi.CustemQListWidget.QCustomQWidget import QCustomQWidget
from MainForm.PyUi.MainForm import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listWidget = QListWidget(self)
        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.SetPidValue("123")
        myQCustomQWidget.SetStatus("Normal")

        myQListWidgetItem = QListWidgetItem(self.listWidget)
        # Set size hint
        self.listWidget.setFixedHeight(500)
        self.listWidget.setFixedWidth(950)

        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.listWidget.addItem(myQListWidgetItem)
        self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.ui.DelleteButton.clicked.connect(self.ButtonClicked)

    def ButtonClicked(self):
        print(self.listWidget.SelectRows)





def main():
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

