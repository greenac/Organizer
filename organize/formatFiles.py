from organize.fileNamer import FileNamer
from organize.names import Names
import os
import shutil


class FormatFiles:
    def __init__(self, base_path):
        self.base_path = base_path
        self.file_namer = FileNamer()
        self.files_to_ignore = {'.DS_Store'}
        self.namer = Names(names_to_exclude=[
            'random',
            'series',
            'finished'
        ])
        self.names = []

    def format(self):
        self._format_helper(self.base_path)
        return None

    def _setup(self):
        self.namer.get_names_from_files()
        self.names = self.namer.first_and_last_names()
        return None

    def _format_helper(self, base_path):
        files = os.listdir(base_path)
        for file in files:
            if file in self.files_to_ignore:
                continue
            print('file:', file)
            file_path = os.path.join(base_path, file)
            if os.path.isdir(file_path):
                self._format_helper(file_path)
            new_name = self.file_namer.clean_name_for_raw_file(file, base_path)
            new_path = os.path.join(base_path, new_name)
            print('Moving:', file_path, '\n', new_path, '\n')
            shutil.move(file_path, new_path)
        return None

    def add_names_no_spaces(self):
        self._setup()
        self._add_names_no_spaces_helper(self.base_path)
        return None

    def _add_names_no_spaces_helper(self, base_path):
        files = os.listdir(base_path)
        for file in files:
            file_path = os.path.join(base_path, file)
            if os.path.isdir(file_path):
                self._add_names_no_spaces_helper(file_path)
            else:
                for name in self.names:
                    indexes = self._all_indexes(file, name[0])
                    for i in indexes:
                        last_name_index = i + len(name[0])
                        try:
                            last_name = file[last_name_index:last_name_index + len(name[1])]
                        except IndexError:
                            continue
                        if last_name == name[1]:
                            new_file = file[:last_name_index] + '_' + file[last_name_index:]
                            last_name_index += 1
                            next_index = last_name_index + len(name[1])
                            if (next_index < len(new_file) - 1 and
                                        new_file[next_index] != '_' and
                                        new_file[next_index] != '.'):
                                    new_file = new_file[:next_index] + '_' + new_file[next_index:]
                            prev_index = i - 1
                            if prev_index >=0 and new_file[prev_index] != '_':
                                new_file = new_file[:i] + '_' + new_file[i:]
                            new_file_path = os.path.join(base_path, new_file)
                            print('moving:\t', file_path, '\n\t', new_file_path, '\n')
                            shutil.move(file_path, new_file_path)
                            file = new_file
                            file_path = new_file_path
        return None

    def _all_indexes(self, input_string, target):
        indexes = []
        i = 0
        while True:
            i = input_string.find(target, i)
            if i == -1:
                break
            indexes.append(i)
            i += len(target)
        return indexes
