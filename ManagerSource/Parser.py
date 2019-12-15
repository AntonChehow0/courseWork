class PipeWorker():
    def __init__(self):
        pass

    def CheckMessage(self,stringMessage):
        return int(stringMessage.split(':')[0])
