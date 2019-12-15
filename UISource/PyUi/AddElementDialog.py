import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QGridLayout, QLabel)


class AddElementDialog(QWidget):

    def __init__(self, callBack):
        super().__init__()
        self.initUI(callBack)

    def initUI(self, callBack):
        self.FormCallBack = callBack
        self.gridLayout = QGridLayout(self)
        self.btn = QPushButton('Ввод', self)
        self.btn.clicked.connect(self.buttonClick)
        font = QFont("Arial", 14)
        self.label = QLabel()
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Имя для терминала")
        self.lineEdit = QLineEdit(self)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.lineEdit, 1, 0)
        self.gridLayout.addWidget(self.btn, 2, 0)

    def buttonClick(self):
        self.FormCallBack(self.lineEdit.text())
        self.close()
