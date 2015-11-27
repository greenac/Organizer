import os
import shutil

class AddDirNameToFiles:
    def __init__(self, dir_name, path):
        self.dir_name = dir_name
        self.root_path = path

    def add(self):
        print(self.dir_name)
        if self.dir_name[len(self.dir_name) - 1] == '/':
            self.dir_name = self.dir_name[:len(self.dir_name) - 1]
        dir_path = os.path.join(self.root_path, self.dir_name)
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            print('# files:', len(files))
            for file in files:
                old_path = os.path.join(dir_path, file)
                new_path = os.path.join(dir_path, self.dir_name) + '_' + file
                shutil.move(old_path, new_path)
                print('old:', old_path, '\n', 'new:', new_path)
        else:
            print(self.dir_name + ' is not a directory')
        return None
