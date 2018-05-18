import os
import shutil
from organize.organizerFile import OrganizerFile

class DirectoryNamer:
    def __init__(self, path):
        self.path = path
        self.files = []

    def get_dirs(self):
        files = os.listdir(self.path)
        counter = 0
        self.files = []
        for file in files:
            if os.path.isdir(os.path.join(self.path, file)):
                self.files.append(OrganizerFile(file, counter))
        self.files.sort(key=lambda x: x.file_name)
        return None

    def rename_directory_files(self, index):
        file = self.file_at_index(index)
        sub_files = self.sub_files_for_file_at_index(index)
        for sub_file in sub_files:
            new_name = file.file_name + '_' + sub_file
            shutil.move(
                os.path.join(self.path, file.file_name, sub_file),
                os.path.join(self.path, file.file_name, new_name)
            )
        return None

    def number_of_directories(self):
        return len(self.files)

    def all_directories(self):
        return self.files

    def file_at_index(self, index):
        return self.files[index]

    def sub_files_for_file_at_index(self, index):
        return list(os.listdir(os.path.join(self.path, self.files[index].file_name)))
