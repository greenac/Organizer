import curses
from organize.unknownFiles import UnknownFiles


class UnknownFilesController:
    def __init__(self, path, dir_paths, hide=[]):
        self.screen = curses.initscr()
        self.TOP_START_POINT = 2
        self.VERTICAL_SPACER = 1
        self.left_position = 0
        self.top_position = self.TOP_START_POINT
        self.screen_params = {}
        self.unknown_files = UnknownFiles(path=path, dirPaths=dir_paths, namesNotToPrint=hide)
        self.phases = [
            'show-file-name',
            'add-dir-name-to-sub-files',
            'add-name-to-file'
        ]
        self.setup()

    def setup(self):
        self.screen.keypad(True)
        curses.noecho()
        self.unknown_files.fetchUnknownFiles()
        return None

    def create_title(self):
        self.screen.addstr(0, 0, 'UNKNOWN FILES')
        return None

    def show_unknowns(self):
        y = self.TOP_START_POINT
        for unknown_file in self.unknown_files.unknownFiles:
            info = str(y) + ' -- ' + unknown_file.file_name
            self.screen.addstr(y, 0, info)
            y += 1
        self.top_position = y + self.VERTICAL_SPACER
        return None

    def step_through(self):

    def run(self):
        try:
            while True:
                self.create_title()
                self.show_unknowns()
                new_char = ' '
                event = self.screen.getch()
                increment_left = False
                if event == 127:
                    self.handle_backspace()
                elif event == 10:
                    self.handle_return()
                    new_char = ''
                    self.screen.clear()
                else:
                    increment_left = True
                    new_char = chr(event)
                self.screen.addstr(
                    self.top_position + self.VERTICAL_SPACER,
                    self.left_position,
                    new_char
                )
                if increment_left:
                    self.left_position += 1
        except KeyboardInterrupt:
            self.screen.keypad(False)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        return None

    def handle_backspace(self):
        if self.left_position > 0:
            self.left_position -= 1
        elif self.top_position > self.TOP_START_POINT:
            self.top_position -= 1
            self.left_position = self.screen_params[self.top_position]
        return None

    def handle_return(self):
        self.screen_params[self.top_position] = self.left_position
        self.top_position += 1
        if len(self.screen_params) - 1 > self.top_position:
            self.left_position = self.screen_params[self.top_position]
        else:
            self.left_position = 0
        return None
