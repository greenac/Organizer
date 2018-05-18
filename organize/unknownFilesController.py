import curses
import traceback
import os
from organize.unknownFiles import UnknownFiles
from organize.colors import Colors
from organize.directoryNamer import DirectoryNamer


class UnknownFilesController:
    def __init__(self, path, dir_paths, hide=None):
        self.VERTICAL_START_POINT = 2
        self.VERTICAL_SPACER = 1
        self.INDENT_SIZE = 4
        self.left_position = self.INDENT_SIZE
        self.line_x0 = 0
        self.vertical_position = 0
        self.vertical_user_start = 0
        self.screen = curses.initscr()
        self.screen_params = {}
        self.dir_namer = DirectoryNamer(path)
        self.unknown_files = UnknownFiles(path=path, dir_paths=dir_paths, excluded_names=hide)
        self.current_file_index = 0
        self.names = []
        self.phases = _UnknownPhases()
        self.current_phase = 0
        self.current_text = ''
        self.colors = Colors()
        self.first_time = True
        self.path = path
        self.all_names = []
        self.modes = _UnknownMode()
        self.mode = self.modes.entry
        self.setup()

    def setup(self):
        self.dir_namer.get_dirs()
        self.unknown_files.fetch_unknown_files()
        if self.unknown_files.number_of_unknowns() == 0:
            print("Couldn't find any unknown files...I have nothing to do here...avoir")
            return None
        self.screen.keypad(True)
        curses.start_color()
        for i in range(1, self.colors.count + 1):
            curses.init_pair(
                i,
                self.colors.curses_color(i),
                curses.COLOR_BLACK
            )
        curses.noecho()
        self.all_names = self.unknown_files.names.all_names_underscored()
        self.current_phase = self.phases.entry
        self.create_title()
        self.vertical_user_start = self.vertical_position
        return None

    def cleanup(self):
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        return None

    def reset(self, reset_full):
        self.print_blank_line()
        self.left_position = 2*self.INDENT_SIZE
        self.current_text = ''
        if reset_full:
            self.current_phase = self.phases.show_file_name
            self.vertical_position = self.vertical_user_start
            self.screen.move(self.vertical_position, self.left_position)
            self.screen.clrtobot()
            self.screen.refresh()
            self.increment_file_index()
        self.step_through()
        return None

    def increment_file_index(self):
        if self.mode == self.modes.directories:
            file_count = self.dir_namer.number_of_directories()
        elif self.mode == self.modes.files:
            file_count = self.unknown_files.number_of_unknowns()
        else:
            return None
        self.current_file_index += 1
        # if  self.current_file_index < file_count:
        #     self.step_through()
        # else:
        #     self.summary(on_exit=False)
        if self.current_file_index >= file_count:
            self.summary(on_exit=False)
        return None

    def summary(self, on_exit=True):
        counter = 0
        lines = []
        for old_name, new_name in self.unknown_files.changed_files.items():
            lines.append(str(counter) + '.) ' + old_name + ' became: ' + new_name)
            counter += 1
        if on_exit:
            print("All done...here is a summary on your unknown experience")
            [print(line) for line in lines]
        else:
            self.print_line(
                "All done...here is a summary on your unknown experience",
                left_position=self.left_position,
                vertical_position=self.vertical_position,
                color=self.colors.green
            )
            for line in lines:
                self.print_line(
                    line,
                    left_position=self.left_position,
                    vertical_position=self.vertical_position,
                    color=self.colors.cyan
                )
        return None

    def run(self):
        self.vertical_position = self.VERTICAL_START_POINT
        self.step_through()
        try:
            while True:
                event = self.screen.getch()
                if event == 127:
                    self.handle_backspace()
                elif event == 10:
                    self.handle_return()
                elif event == 9:
                    self.process_autocomplete()
                elif event == curses.KEY_RESIZE:
                    self.handle_resize()
                elif event == curses.KEY_RIGHT:
                    self.handle_arrow_press('right')
                elif event == curses.KEY_LEFT:
                    self.handle_arrow_press('left')
                else:
                    self.handle_key_press(event)
        except KeyboardInterrupt:
            self.cleanup()
            print("You've killed good unknown files...shame, shame!!")
            self.summary()
        except:
            self.cleanup()
            print(traceback.format_exc())
        return None

    def create_title(self):
        self.print_line('UNKNOWN FILES', color=self.colors.blue)
        return None

    def show_unknowns(self):
        y_pos = self.VERTICAL_START_POINT
        for unknown_file in self.unknown_files.files[:30]:
            info = str(unknown_file.index) + ' -- ' + unknown_file.file_name
            self.print_line(
                info,
                vertical_position=y_pos
            )
            y_pos += 1
        self.vertical_position = y_pos + self.VERTICAL_SPACER
        self.screen.refresh()
        return None

    def show_file_name(self, current_file):
        self.print_blank_line()
        self.print_line(
            'CURRENT FILE: ' + current_file.file_name,
            left_position=self.INDENT_SIZE,
            vertical_position=self.vertical_position,
            color=self.colors.magenta
        )
        return None

    # handle printing and file manipulation section
    def step_through(self):
        if self.mode == self.modes.entry:
            self.step_through_entry()
        elif self.mode == self.modes.directories:
            self.step_through_directories()
        else:
            self.step_through_files()
        return None

    def step_through_entry(self):
        self.print_line(
            'How Doing? What to do today...',
            vertical_position=self.vertical_position
        )
        self.print_line('Directories press: 1',
                        left_position=self.INDENT_SIZE,
                        vertical_position=self.vertical_position
                        )
        self.print_line(
            'Files press: 2',
            left_position=self.INDENT_SIZE,
            vertical_position=self.vertical_position
        )
        self.print_blank_line()
        return None

    def step_through_directories(self):
        current_file = self.dir_namer.file_at_index(self.current_file_index)
        if self.current_phase == self.phases.show_file_name:
            self.show_file_name(current_file)
            self.current_phase = self.phases.ask_add_dir_name_to_sub_files

        if self.current_phase == self.phases.ask_add_dir_name_to_sub_files:
                self.print_line(
                    'Add directory name: ' + current_file.file_name + ' to sub-files? y/n ',
                    left_position=self.INDENT_SIZE,
                    vertical_position=self.vertical_position,
                    color=self.colors.cyan
                )
                sub_files = self.dir_namer.sub_files_for_file_at_index(self.current_file_index)
                message = ''
                for i in range(len(sub_files)):
                    sub_file = sub_files[i]
                    increment_vertical = i != len(sub_files) - 1
                    message = str(i) + ' - ' + sub_file
                    self.print_line(
                        message,
                        left_position=2*self.INDENT_SIZE,
                        vertical_position=self.vertical_position,
                        color=self.colors.green,
                        increment_vertical=increment_vertical
                    )
                self.print_blank_line()
                message += ' '
                self.left_position = 2*self.INDENT_SIZE + len(message)
                self.line_x0 = self.left_position
        elif self.current_phase == self.phases.add_dir_name_to_sub_files:
            self.print_blank_line()
            files_before = self.dir_namer.sub_files_for_file_at_index(self.current_file_index)
            self.dir_namer.rename_directory_files(self.current_file_index)
            files_after = self.dir_namer.sub_files_for_file_at_index(self.current_file_index)
            for i in range(len(files_before)):
                self.print_moved_file(files_before[i], files_after[i])
            self.print_blank_line()
            self.print_line(
                'RENAMED...KEEP MOVING!!',
                vertical_position=self.vertical_position,
                increment_vertical=True
            )
            self.current_phase = self.phases.confirm_add_dir_name
        return None

    def step_through_files(self):
        current_file = self.unknown_files.file_at_index(self.current_file_index)
        if self.current_phase == self.phases.show_file_name:
            self.show_file_name(current_file)
            self.current_phase = self.phases.enter_names_for_file

        if self.current_phase == self.phases.enter_names_for_file:
            message = 'Enter names to add to ' + current_file.file_name + ' '
            self.print_line(
                    message,
                    left_position=self.INDENT_SIZE,
                    vertical_position=self.vertical_position,
                    color=self.colors.cyan,
                    increment_vertical=False
            )
            self.left_position = self.INDENT_SIZE + len(message)
            self.line_x0 = self.left_position
        elif self.current_phase == self.phases.ask_add_name_to_file:
            message = 'Add ' + str(self.names) + ' to: ' + current_file.file_name + '? '
            self.print_line(
                message,
                left_position=self.INDENT_SIZE,
                vertical_position=self.vertical_position,
                increment_vertical=False,
                color=self.colors.cyan
            )
            self.left_position = self.INDENT_SIZE + len(message)
            self.line_x0 = self.left_position
        elif self.current_phase == self.phases.add_name_to_file:
            new_name = self.unknown_files.add_names_to_file(current_file, self.names)
            self.print_moved_file(current_file.file_name, new_name)
            self.reset(reset_full=True)
        return None

    # handle input section
    def handle_return(self):
        if self.mode == self.modes.entry:
            reset_full = self.handle_entry_return_phase()
        elif self.mode == self.modes.directories:
            reset_full = self.handle_directories_return_phase()
        else:
            reset_full = self.handle_files_return_phase()
        self.reset(reset_full=reset_full)
        return None

    def handle_entry_return_phase(self):
        if self.current_text == '1':
            self.mode = self.modes.directories
        elif self.current_text == '2':
            self.mode = self.modes.files
        return True

    def handle_directories_return_phase(self):
        current_text = self.current_text.lower()
        reset_full = False
        if self.current_phase == self.phases.ask_add_dir_name_to_sub_files:
            self.vertical_position += 1
            if current_text == 'y' or current_text == 'yes':
                self.current_phase = self.phases.add_dir_name_to_sub_files
            elif self.current_file_index < len(self.dir_namer.all_directories()) - 1:
                reset_full = True
            else:
                self.summary(on_exit=False)
                return None
        elif self.current_phase == self.phases.confirm_add_dir_name:
            if self.current_file_index >= self.dir_namer.number_of_directories() - 1:
                self.current_phase = self.phases.enter_names_for_file
            else:
                self.current_phase = self.phases.show_file_name
            reset_full = True
        return reset_full

    def handle_files_return_phase(self):
        current_text = self.current_text.lower()
        reset_full = False
        if self.current_phase == self.phases.enter_names_for_file:
            if current_text == '':
                self.print_blank_line()
                self.current_phase = self.phases.show_file_name
                reset_full = True
            else:
                self.names = []
                for unclean_name in self.current_text.split(','):
                    if '_' in unclean_name:
                        unclean_name = unclean_name.replace(' ', '')
                        self.names.append(unclean_name)
                    else:
                        names = [part for part in unclean_name.split(' ') if part != '']
                        self.names.append('_'.join(names))
                self.print_blank_line()
                self.current_phase = self.phases.ask_add_name_to_file
        elif self.phases.ask_add_name_to_file:
            if current_text == 'y' or current_text == 'yes':
                self.print_blank_line()
                self.current_phase = self.phases.add_name_to_file
            else:
                self.current_phase = self.phases.show_file_name
                reset_full = True
        return reset_full

    def handle_backspace(self):
        x_position = self.left_position - self.line_x0 + 1
        #self.print_test(str(x_position))
        if x_position > 0 and len(self.current_text) > 0:
            self.left_position -= 1
            # check if cursor is outside of the current text
            if x_position > len(self.current_text):
                self.current_text = self.current_text[:len(self.current_text) - 1]
            else:
                self.current_text = self.current_text[:x_position] + self.current_text[x_position + 1:]
            self.screen.clrtoeol()
            self.print_line(
                self.current_text,
                self.line_x0,
                self.vertical_position,
                increment_vertical=False
            )
            self.screen.move(self.vertical_position, self.left_position)
            self.screen.refresh()
        return None

    def handle_arrow_press(self, direction):
        if direction == 'left':
            movement = -1
        else:
            movement = 1
        new_position = self.left_position + movement
        if (new_position >= self.line_x0 and
                        new_position + movement <= len(self.current_text) + self.line_x0 + 1):
            self.left_position = new_position
            self.screen.move(self.vertical_position, self.left_position)
            self.screen.refresh()
        return None

    def handle_key_press(self, event):
        new_char = chr(event)
        x = self.left_position - self.line_x0
        self.current_text = self.current_text[:x] + new_char + self.current_text[x:]
        self.print_line(
            self.current_text,
            left_position=self.line_x0,
            vertical_position=self.vertical_position,
            increment_vertical=False
        )
        self.left_position += 1
        self.screen.move(self.vertical_position, self.left_position)
        self.screen.refresh()
        return None

    def print_line(
            self,
            message,
            left_position=0,
            vertical_position=0,
            color=0,
            increment_vertical=True
    ):
        self.screen.addstr(vertical_position, left_position, message, curses.color_pair(color))
        self.screen.refresh()
        if increment_vertical:
            self.vertical_position += 1
        return None

    def print_moved_file(self, previous_name, after_name):
        self.print_line(
            'Moving: ' + previous_name + ' --> ' + after_name,
            left_position=self.INDENT_SIZE,
            vertical_position=self.vertical_position,
            color=self.colors.yellow
        )
        return None

    def print_blank_line(self):
        self.print_line('', left_position=0, vertical_position=self.vertical_position)
        return None

    def process_autocomplete(self):
        parts = self.current_text.split(',')
        current_text_parts = parts[len(parts) - 1].split(' ')
        if current_text_parts[0] == '':
            del current_text_parts[0]
        underscored_name = '_'.join(current_text_parts)
        matched_names = []
        for name in self.all_names:
            if len(underscored_name) <= len(name) and underscored_name == name[:len(underscored_name)]:
                matched_names.append(name)
        # add common letters to current_text
        letters_to_add = ''
        if len(matched_names) > 0:
            first_name = matched_names[0]
            for i in range(len(underscored_name), len(first_name)):
                letter = first_name[i]
                has_letter = True
                for j in range(1, len(matched_names)):
                    try:
                        if matched_names[j][i] != letter:
                            has_letter = False
                            break
                    except IndexError:
                        has_letter = False
                        break
                if has_letter:
                    letters_to_add += letter
                else:
                    break
            if letters_to_add != '':
                self.left_position += len(letters_to_add)
                self.current_text += letters_to_add
                left_start = self.left_position - len(self.current_text)
                self.print_line(
                    self.current_text,
                    left_position=left_start,
                    vertical_position=self.vertical_position,
                    increment_vertical=False
                )
        self.print_line(
            ', '.join(matched_names[:10]),
            left_position=self.INDENT_SIZE,
            vertical_position=self.vertical_position + 1,
            increment_vertical=False,
            color=self.colors.yellow
        )
        self.screen.clrtoeol()
        return None

    def handle_resize(self):
        terminal_size = self.terminal_size()
        return None

    def terminal_size(self):
        try:
            width, height = os.get_terminal_size[0], os.get_terminal_size[1]
            return {
                'width': width,
                'height': height
            }
        except OSError:
            return {
                'width': 100,
                'height': 50
            }

    def print_test(self, message):
        self.print_line(
            message,
            left_position=0,
            vertical_position=1,
            increment_vertical=False,
            color=self.colors.red
        )


class _UnknownPhases:
    def __init__(self):
        self.entry = 0
        self.show_file_name = 1
        self.ask_add_dir_name_to_sub_files = 2
        self.add_dir_name_to_sub_files = 3
        self.confirm_add_dir_name = 4
        self.enter_names_for_file = 5
        self.ask_add_name_to_file = 6
        self.add_name_to_file = 7
        self.exit = 8


class _UnknownMode:
    def __init__(self):
        self.entry = 0
        self.directories = 1
        self.files = 2
