from enum import Enum
from inspect import stack
from sys import stdout
from datetime import datetime
class glog_flags(Enum):
    METHOD_PRINT = 0
    METHOD_FILE = 1
class glog_level(Enum):
    PLAIN = 0
    TRACE = 1
class glog():
    def __init__(self, flags = [glog_flags.METHOD_PRINT], filename = "bot.log", level = glog_level.PLAIN):
        if not flags: raise ValueError("no glog_flags given!")
        self.targets = []
        if glog_flags.METHOD_PRINT in flags:
            self.targets.append(stdout)
        if glog_flags.METHOD_FILE in flags:
            self.targets.append(open(filename, "a"))
        self.level = level
    def __del__(self):
        for target in self.targets:
            if not(target == stdout):
                target.close()
    def write(self, message):
        for target in self.targets:
            target.write("({2})@[{0}]: {1}\n".format(stack()[1].function if self.level == glog_level.TRACE else "glog", message, datetime.now()))