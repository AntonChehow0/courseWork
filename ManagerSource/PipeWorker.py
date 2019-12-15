import os


class PipeWorker():
    def __init__(self):
        pass

    def ReadPipe(self, FIFO):
        resultString = ""
        print(FIFO)
        ds = os.open(FIFO,  os.O_RDONLY | os.O_NONBLOCK)
        strn= os.read(ds, 100)
        os.close(ds)
        print("Descrioter  = {0} "  +  str(ds))
        #print(strn.decode("ascii", "ignore"))
        # with open(FIFO, "r") as fifo:
        #     print("FIFO opened")
        #     while True:
        #         data = fifo.read()
        #         resultString += data#.decode("ascii", "ignore")
        #         if len(data) == 0:
        #             print("Writer closed")
        #             break
        #         print('Read: "{0}"'.format(data))

        print(len(strn))
        print(str(strn.decode("ascii", "ignore")))
        print("end read")
        return resultString

    def WriteToPipe(self, FIFO, writedString):
        with open(FIFO) as fifo:
            print("Fifo opened")
            fifo.write(writedString)
