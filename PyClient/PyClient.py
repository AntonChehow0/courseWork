import os

from ManagerSource.PipeWorker import PipeWorker


def main():
    os.chdir("..")
    p = "/home/suvorovm/uni/OS/courseWork/Pipe/GeneralPipe.ps"
    w = PipeWorker()
    w.WriteToPipe(p, "хуйня ваш PIP")


if __name__ == '__main__':
    main()
