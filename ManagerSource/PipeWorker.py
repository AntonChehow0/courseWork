class PipeWorker():
    def __init__(self):
        pass

    def ReadPipe(self, FIFO):
        resultString = ""
        with open(FIFO) as fifo:
            print("FIFO opened")
            while True:
                data = fifo.read()
                resultString += data
                if len(data) == 0:
                    print("Writer closed")
                    break
                print('Read: "{0}"'.format(data))
        return resultString

    def WriteToPipe(self, FIFO, writedString):
        with open(FIFO) as fifo:
            print("Fifo opened")
            fifo.write(writedString)
