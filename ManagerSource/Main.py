import os
import signal
import stat
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from ManagerSource.MessageConverter import MessageConverter
from ManagerSource.PipeWorker import PipeWorker
from UISource.PyUi.AddElementDialog import AddElementDialog
from UISource.PyUi.CustemQListWidget.QCustomQWidget import QCustomQWidget
from UISource.PyUi.MainForm import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    MainPipePath = ''
    PipeName = "Pipe/GeneralPipe.p"
    PidFile = "Pipe/PidFile.txt"
    PipeMode = 0o666
    pathToClientProgram = ""
    dict = {}
    _pipeworker = PipeWorker()
    _converter = MessageConverter()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listWidget = QListWidget(self)
        self.MainPipePath = os.getcwd() + "/" + self.PipeName
        try:
            os.mkfifo(self.MainPipePath, stat.S_IFIFO)  # stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            os.chmod(self.MainPipePath, self.PipeMode)
            print("Pipe created")
        except IOError:
            print("Pipe already exist")
        # self.AddToDictonary()
        file = open(self.PidFile, "w")
        file.write(str(os.getpid()))
        file.close()

        self.ui.DelleteButton.clicked.connect(self.ButtonClicked)
        self.ui.addElementButton.clicked.connect(self.ButtonAddClicked)
        self.InitList()

    def AddToUi(self, usrData):
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

    def AddToDictonary(self):
        readedString = self._pipeworker.ReadPipe(self.MainPipePath)
        self._converter.ParseToMessage(readedString)

    def InitList(self):
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



    def ButtonClicked(self):
        print(self.listWidget.SelectRows)
        readedString = self._pipeworker.ReadPipe(os.getcwd() + "/" + self.PipeName)
        print(readedString)

    def ButtonAddClicked(self):
        self.dealog = AddElementDialog(self.CallBackHandler)
        self.dealog.show()

    def CallBackHandler(self, str):
        print("call back recived" + str + "\n")
        self.pathToClientProgram = os.getcwd() + "/CClient/cmake-build-debug/CClient"  # "cmake-build-debug" + "/CClient &"
        # subprocess.Popen([self.pathToClientProgram, '-c', 'd',])#API PYTHON для вызова processa
        # os.system(self.pathToClientProgram+" &")
        os.execl(self.pathToClientProgram, "sa")

    def SignalCatcher(self, signum, stack):
        print("signaled!\n")
        readedString = self._pipeworker.ReadPipe(os.getcwd() + "/" + self.PipeName)
        usrs = self._converter.ParseToMessage(readedString)
        self.AddToUi("das")


def main():
    os.chdir("..")
    print(os.getpid())

    app = QtWidgets.QApplication([])
    application = MainWindow()
    signal.signal(signal.SIGUSR1, application.SignalCatcher)  # USR1 - for read from general named pipe
    timer = QTimer()
    timer.start(1)
    timer.timeout.connect(lambda: None)
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

