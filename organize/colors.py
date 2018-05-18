import curses

class Colors:
    def __init__(self):
        self.white = 1
        self.green = 2
        self.blue = 3
        self.red = 4
        self.cyan = 5
        self.magenta = 6
        self.yellow = 7
        self.black = 8
        self.count = 8

    def curses_color(self, color):
        if color == self.green:
            return curses.COLOR_GREEN
        elif color == self.blue:
            return curses.COLOR_BLUE
        elif color == self.red:
            return curses.COLOR_RED
        elif color == self.cyan:
            return curses.COLOR_CYAN
        elif color == self.magenta:
            return curses.COLOR_MAGENTA
        elif color == self.yellow:
            return curses.COLOR_YELLOW
        elif color == self.black:
            return curses.COLOR_BLACK
        else:
            return curses.COLOR_WHITE
