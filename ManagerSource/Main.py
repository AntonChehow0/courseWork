import os
import signal
import stat
import subprocess
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from ManagerSource.MessageConverter import MessageConverter
from ManagerSource.PipeWorker import PipeWorker
from UISource.PyUi.AddElementDialog import AddElementDialog
from UISource.PyUi.CustemQListWidget.QCustomQWidget import QCustomQWidget
from UISource.PyUi.MainForm import Ui_MainWindow
from UISource.PyUi.SendMsgDialog import SendMsgDialog


class MainWindow(QtWidgets.QMainWindow):
    MainPipePath = ''
    PipeName = "Pipe/GeneralPipe.p"
    PidFile = "Pipe/PidFile.txt"
    PipeMode = 0o666
    pathToClientProgram = ""
    dictUsers = {}
    _pipeworker = PipeWorker()
    _converter = MessageConverter()
    _listCounter = 0

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
        self.ui.sendMessageButton.clicked.connect(self.ButtonMsgClkicked)
        self.InitList()

    def ButtonMsgClkicked(self):
        self.dealog = SendMsgDialog(self.CallBackSendMsgHandlet)
        self.dealog.show()

    def TryDistinctData(self, PID):
        for key, value in self.dictUsers.items():
            if value.PID == PID:
                self.listWidget.takeItem(key)

    def AddToUi(self, usrData):
        for i in usrData:
            self.TryDistinctData(i.USER.PID)
            self._listCounter += 1
            self.dictUsers[self._listCounter] = i.USER
            myQCustomQWidget = QCustomQWidget()
            print("PID added  = ", i.USER.PID)
            myQCustomQWidget.SetPidValue(i.USER.PID)
            myQCustomQWidget.SetStatus(i.USER.STATUS)
            myQCustomQWidget.SetName(i.USER.Name)
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
        myQListWidgetItem = QListWidgetItem(self.listWidget)
        self.listWidget.setFixedHeight(500)
        self.listWidget.setFixedWidth(950)
        self.listWidget.addItem(myQListWidgetItem)

    def ButtonClicked(self):
        if self._listCounter == 0:
            return
        val = [x.row() for x in self.listWidget.selectedIndexes()]
        listItems = self.listWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))
        self._listCounter -= 1
        self.KillProcess(val[0])
        print(val)

    def KillProcess(self, index):
        usrData = self.dictUsers[index]
        os.kill(int(usrData.PID), 9)

    def ButtonAddClicked(self):
        self.dealog = AddElementDialog(self.CallBackHandler)
        self.dealog.show()

    def CallBackSendMsgHandlet(self, strTypeMsg, strComand):
        val = [x.row() for x in self.listWidget.selectedIndexes()]
        usrData = self.dictUsers[val[0]]
        os.kill(int(usrData.PID), signal.SIGUSR1)
        self._pipeworker.WriteToPipe(self.PipeName,
                                     "messageType:" + strTypeMsg + ",PID:" + usrData.PID + ",status:" + usrData.STATUS + ",userName:" + usrData.Name + ",msg:" + strComand)

    def CallBackHandler(self, str):
        print("call back recived" + str + "\n")
        self.pathToClientProgram = os.getcwd() + "/CClient/cmake-build-debug/CClient"  # "cmake-build-debug" + "/CClient &"
        subprocess.Popen(
            [self.pathToClientProgram, str, '1'])  # API PYTHON для вызова processa - системно вызывает exec
        # os.system(self.pathToClientProgram+" &")
        # os.execl(self.pathToClientProgram, "sa", "1", "1")

    def SignalUser1Handler(self, signum, stack):
        print("signaled!\n")
        readedString = self._pipeworker.ReadPipe(os.getcwd() + "/" + self.PipeName)
        usrs = self._converter.ParseToMessage(readedString)
        self.AddToUi(usrs)


def main():
    os.chdir("..")
    print(os.getpid())

    app = QtWidgets.QApplication([])
    application = MainWindow()
    signal.signal(signal.SIGUSR1, application.SignalUser1Handler)  # USR1 - for read from general named pipe
    timer = QTimer()
    timer.start(1)
    timer.timeout.connect(lambda: None)
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

