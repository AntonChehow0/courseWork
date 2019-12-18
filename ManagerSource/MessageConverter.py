class MessageConverter():

    def __init__(self):
        pass

    def CheckMessage(self, stringMessage):
        return int(stringMessage.split(':')[0])

    def ParseToMessage(self, stringMess):
        if (stringMess == ""):
            print("Can't parse string")
            return
        allMessages = stringMess.split(".")
        usrList = []
        res = []
        for message in allMessages:
            for j in message.split(","):
                print(j)
                res = j.split(":")[1]
