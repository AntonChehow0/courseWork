from ManagerSource.User import User


class Message():
    MSG_TYPE = ""
    USER = User("no", "no", "no")
    MSG = ""

    def __init__(self, User, type, msg):
        self.USER = User
        self.MSG_TYPE = type
        self.MSG = msg
        pass
