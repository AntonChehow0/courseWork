import os


class PipeWorker():
    def __init__(self):
        pass

    def ReadPipe(self, FIFO):
        resultString = ""
        print("LOG: FIFO opened")
        with open(FIFO, "rb") as fifo:
            while True:
                data = fifo.read()
                resultString += data.decode("ascii", "ignore")
                if len(data) == 0:
                    print("LOG: Reader closed")
                    break

        resultString.rstrip()
        resultString.replace("\n", "")
        print("LOG: Прочитанно =" + str(len(resultString)))
        print(resultString)
        print("end read")

        return resultString

    def WriteToPipe(self, FIFO, writedString):
        ds = os.open(FIFO, os.O_WRONLY)
        os.write(ds, writedString)
        os.close(ds)
        # ds = os.open(FIFO, os.O_WRONLY | os.O_CREAT)
        # os.write(ds, writedString.encode())
        # os.close(ds)
