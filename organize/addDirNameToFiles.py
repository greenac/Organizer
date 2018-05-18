import os
import shutil

class AddDirNameToFiles:
    def __init__(self, dir_name, path):
        self.dir_name = dir_name
        self.root_path = path

    def add(self, should_print=True):
        if should_print:
            print(self.dir_name)
        if self.dir_name[len(self.dir_name) - 1] == '/':
            self.dir_name = self.dir_name[:len(self.dir_name) - 1]
        dir_path = os.path.join(self.root_path, self.dir_name)
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            if should_print:
                print('# files:', len(files))
            self.add_to_files(
                self.root_path,
                self.dir_name,
                should_print=should_print
            )
        else:
            if should_print:
                print(self.dir_name + ' is not a directory')
        return None

    def add_to_files(self, base_path, file, should_print):
        file_path = os.path.join(base_path, file)
        if os.path.isdir(file_path):
            [self.add_to_files(file_path, new_file, should_print=should_print)
             for new_file in list(os.listdir(file_path))]
        else:
            new_path = os.path.join(base_path, self.dir_name) + '_' + file
            shutil.move(file_path, new_path)
            if should_print:
                print('old:', file_path, '\n', 'new:', new_path)
        return None
