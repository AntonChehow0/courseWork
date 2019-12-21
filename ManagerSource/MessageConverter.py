from ManagerSource.Message import Message
from ManagerSource.User import User


class MessageConverter():

    def __init__(self):
        pass

    def CheckMessage(self, stringMessage):
        return int(stringMessage.split(':')[0])

    def ParseToMessage(self, stringMess):
        if stringMess == "":
            print("Can't parse string")
            return

        allMessages = stringMess.split(".")
        print(allMessages)
        msgList = []

        for message in allMessages:
            if message == "":
                continue
            res = []
            for j in message.split(","):
                if j == "":
                    continue
                res.append(str(j.split(":")[1]))
            print(res)
            msg = Message(User(res[3], res[1], res[2]), res[0], res[4])
            print(msg.USER.PID)
            msgList.append(msg)

        print("Count of element in lists = ", len(msgList))
        return msgList
