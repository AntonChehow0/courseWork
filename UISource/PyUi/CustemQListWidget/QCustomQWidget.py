from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget


class QCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        font = QFont("Arial", 18)

        self.firstColumn = QVBoxLayout()
        self.secondColumn = QVBoxLayout()
        self.thirdColumn = QVBoxLayout()

        self.SetLabels()
        # Устанавливаем шрифты
        self.SetFonts(font)

        self.firstColumn.addWidget(self.textUpQLabelPIDProcess)
        self.firstColumn.addWidget(self.textDownQLabelValuePIDProcess)
        self.secondColumn.addWidget(self.textQlabelStatus)
        self.secondColumn.addWidget(self.textQlabeleStatusValue)

        self.thirdColumn.addWidget(self.textQLabelNameProcess)
        self.thirdColumn.addWidget(self.textValueNameProcess)

        self.firstColumn.setContentsMargins(1, 0, 15, 0)
        self.secondColumn.setContentsMargins(0, 0, 15, 0)
        self.thirdColumn.setContentsMargins(0, 0, 15, 0)

        self.allQHBoxLayout = QHBoxLayout()

        self.allQHBoxLayout.addLayout(self.firstColumn, 0)
        self.allQHBoxLayout.addLayout(self.secondColumn, 1)
        self.allQHBoxLayout.addLayout(self.thirdColumn, 2)
        self.setContentsMargins(15, 0, 15, 0)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.SetColors()
        self.textQlabelStatus.setText("Статус")
        self.textUpQLabelPIDProcess.setText("PID")
        self.textQLabelNameProcess.setText("Имя")

    def SetColors(self):
        self.textUpQLabelPIDProcess.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabelValuePIDProcess.setStyleSheet('''
            color: rgb(0, 0, 0);
        ''')
        self.textQlabelStatus.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textQLabelNameProcess.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')

    def SetLabels(self):
        self.textUpQLabelPIDProcess = QLabel()
        self.textDownQLabelValuePIDProcess = QLabel()
        self.textQlabelStatus = QLabel()
        self.textQlabeleStatusValue = QLabel()
        self.textQLabelNameProcess = QLabel()
        self.textValueNameProcess = QLabel()

    def SetFonts(self, font):
        self.textUpQLabelPIDProcess.setFont(font)
        self.textDownQLabelValuePIDProcess.setFont(font)
        self.textQlabelStatus.setFont(font)
        self.textQlabeleStatusValue.setFont(font)
        self.textQLabelNameProcess.setFont(font)
        self.textValueNameProcess.setFont(font)

    def SetPidValue(self, text):
        self.textDownQLabelValuePIDProcess.setText(text)

    def SetStatus(self, text):
        self.textQlabeleStatusValue.setText(text)

    def SetName(self, text):
        self.textValueNameProcess.setText(text)
