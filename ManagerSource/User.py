class User():
    Name = ""
    PID = "-1"
    STATUS = ""
    MSG = ""

    def __init__(self, name, pid, status, msg):
        self.Name = name
        self.PID = pid
        self.STATUS = status
        self.MSG = msg
        pass
