import os
from organize.fileFormatter import FileFormatter


class FileCounter:
    def __init__(self, top_dirs):
        self.top_dirs = top_dirs
        self.file_formatter = FileFormatter()
        self.files = {}

    def count_files(self, dirs):
        counter = 0
        for topdir in dirs:
            print('******************* searching', topdir, '***************************')
            if os.path.isdir(topdir):
                files = os.listdir(topdir)
                for file in files:
                    file_path = os.path.join(topdir, file)
                    if os.path.isdir(file_path):
                        newFileNumber = self.countFiles([file_path])
                        print('\ncounter:', counter, '\nnew number:', newFileNumber, '\nnew counter:', counter + newFileNumber)
                        counter += newFileNumber
                    elif self.fileFormatter.file_contains_format(file, topdir):
                            counter += 1
                            print(counter, 'a movie:', file)
        print('------ returning', counter, '----------')
        return counter

    def count_names(self):
        for dir in self.top_dirs:
            if not os.path.isdir(dir):
                continue
            files = os.listdir(dir)
            for file in files:
                file_path = os.path.join(dir, file)
                if not os.path.isdir(file_path):
                    continue
                sub_files = os.listdir(file_path)
                for sub_file in sub_files:
                    sub_file_path = os.path.join(file_path, sub_file)
                    if os.path.isdir(sub_file_path):
                        sub_sub_files = self.get_relevant_files(sub_file_path)
                        self.add_files_for_name(file, sub_sub_files)
                    elif self.file_formatter.file_contains_format(sub_file, file_path):
                        self.add_files_for_name(file, [sub_file])
        return None

    def get_relevant_files(self, file_path):
        return [file for file in list(os.listdir(file_path))
                 if self.file_formatter.file_contains_format(file, file_path)]

    def add_files_for_name(self, name, files):
        if name in self.files:
            old_files = self.files[name]
            self.files[name] = files + old_files
        else:
            self.files[name] = files
        return None

    def print_results(self):
        names = list(self.files.keys())
        for i in range(len(names) - 1):
            target = i
            for j in range(i + 1, len(names)):
                if len(self.files[names[j]]) > len(self.files[names[target]]):
                    target = j
            if i != target:
                temp = names[i]
                names[i] = names[target]
                names[target] = temp
        max_num_length = len(str(len(names))) + 1
        max_name_length = max([len(name) for name in names]) + 1
        for i in range(len(names)):
            print(str(i + 1).ljust(max_num_length),
                  names[i].ljust(max_name_length),
                  'scenes:',
                  len(self.files[names[i]])
            )
        return None


top_dirs = [
    '/Volumes/Papa/.p/',
    '/Volumes/Papa/.organized/'
]

file_counter = FileCounter(top_dirs)
file_counter.count_names()
file_counter.print_results()
