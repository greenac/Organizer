import shutil
import os
from organize.fileFormatter import FileFormatter


class MoveToRoot:
    def __init__(self, root_path, dir_to_exclude):
        self.root_path = root_path
        self.formatter = FileFormatter()
        self.dir_to_exclude = set(dir_to_exclude)

    def move(self):
        files = os.listdir(self.root_path)
        self._move_helper(self.root_path, files)
        return None

    def _move_helper(self, root_path, files):
        for file in files:
            if file not in self.dir_to_exclude:
                file_path = os.path.join(root_path, file)
                if os.path.isdir(file_path):
                    self._move_helper(file_path, list(os.listdir(file_path)))
                    print('removing directory:', file_path, 'with contents')
                    [print('\t', deleted_file) for deleted_file in list(os.listdir(file_path))]
                    shutil.rmtree(file_path)
                else:
                    if (self.formatter.file_contains_format(file, file_path) and
                                root_path != self.root_path):
                        new_path = os.path.join(self.root_path, file)
                        print('moving:', file_path, 'to:', new_path)
                        shutil.move(file_path, new_path)
        return None
