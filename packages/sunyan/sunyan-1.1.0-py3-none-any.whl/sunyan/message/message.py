import wasabi as wb
from wasabi import Printer

class message:

    __slots__ = ('msg')

    def __init__(self):
        self.msg = Printer()

    def text(self,info):
        self.msg.text(info)

    def good(self,info):
        self.msg.good(info)

    def fail(self,info):
        self.msg.fail(info)

    def warn(self,info):
        self.msg.warn(info)

    def divider(self,info="Heading",char='-'):
        self.msg.divider(info, char=char)

    def load(self,info="Successfully loaded!"):
        self.msg.good(info)

    def color(self,info,fg='white',bg='grey',bold=True):
        formatted = wb.color(info, fg=fg, bg=bg, bold=bold)
        return formatted

    def indent(self,info,indent):
        wrapped = wb.wrap(info, indent=indent)
        return wrapped

import time

def load():
    time.sleep(3)

if __name__ == '__main__':
     msg = message()
     msg.text('sunyan')
     msg.warn('sunyan')
     msg.good('sunyan')
     msg.fail('sunyan')
     msg.divider(info='sunyan',char='-')
     sunyan = msg.color('sunyan',fg='white',bg='grey',bold=True)
     print(sunyan)
     sunyan = msg.indent('sunyan',indent=4)
     print(sunyan)
     load()
     msg.load(info='Successfully loaded!')
