import os

class PrintFormatter:
    def __init__(self):
        self.size = self._terminal_size()

    def _terminal_size(self):
        try:
            return os.get_terminal_size()[0]
        except OSError:
            return 100

    def acrossScreen(self, char):
        size = self.size - 1
        line = ''
        for i in range(0, size):
            line += char
        return line

    def acrossScreenWithName(self, char, name):
        name = ' ' + name + ' '
        size = self.size - len(name)
        if size > 2:
            line = ''
            for i in range(0, int(size/2)):
                line += char
            line += name
            for i in range(0, int(size/2)):
                line += char
            return line
        return name