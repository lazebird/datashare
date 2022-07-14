import os.path
import time


class log:
    _instance = None
    logpath = None

    def __new__(self, *args, **kw):  # single instance
        if self._instance is None:
            self._instance = object.__new__(self, *args, **kw)
        return self._instance

    def __init__(self, logpath=None):
        if not logpath and not self.logpath:
            logpath = "D:/pyscript.log" if os.path.isdir("D:/") else "/tmp/pyscript.log"
        if logpath:
            self.logpath = logpath

    def info(self, s):
        try:
            f = open(self.logpath, "a")
            f.write(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + "[Info] " + s + "\n")
            f.close()
        except:
            print(s)

    def err(self, s):
        try:
            f = open(self.logpath, "a")
            f.write(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + "[Error] " + s + "\n")
            f.close()
        except:
            print(s)


def info(s):
    log().info(s)


def err(s):
    log().err(s)
