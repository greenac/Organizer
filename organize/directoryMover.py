import os
import shutil
import datetime
from organize.printFormatter import PrintFormatter

class DirectoryMover:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path
        self.files = os.listdir(self.src_path)
        self.print_formatter = PrintFormatter()
        self.moved_files = {}

    def move_dirs(self):
        for file_name in self.files:
            source_path = self.src_path + file_name
            destination_path = self.dst_path + file_name
            self.move_single_dir(source_path, destination_path)
            print(self.print_formatter.acrossScreen('-') + '\n')
        return None

    def move_single_dir(self, src_path, dst_path):
        if os.path.isdir(src_path):
            file_name = src_path.split('/').pop()
            self.moved_files[file_name] = []
            if os.path.isdir(dst_path):
                print("Directory named " + file_name + " exists in target directory ...Moving individual files...\n")
                target_files = os.listdir(src_path)
                for target_file in target_files:
                    sourceFile = os.path.join(src_path, target_file)
                    if os.path.exists(os.path.join(dst_path, target_file)):
                        print("Pre-existing file: " + target_file + " already exists in " + dst_path + "\n")
                    else:
                        shutil.move(sourceFile, dst_path)
                        print("Moving: " + sourceFile + "\nTo: " + dst_path + target_file + "\n")
                        self._add_file_to_moved_files(file_name, target_file)
            else:
                print("No Directory named: " + file_name + " exists in " + self.dst_path)
                print('Creating: ' + os.path.join(self.dst_path, file_name) + '\n')
                print("Moving: " + src_path + "\nTo: " + dst_path + "\n")
                names = os.listdir(src_path)
                for name in names:
                    self._add_file_to_moved_files(file_name, name)
                    print("Moving: " + src_path + name + "\nTo: " + dst_path + name + "\n")
                shutil.move(src_path, dst_path)
        return None

    def _del_empty_dirs(self):
        self.files = os.listdir(self.src_path)
        for aFile in self.files:
            path = self.src_path + aFile
            if os.path.isdir(path):
                dirFiles = os.listdir(path)
                size = len(dirFiles)
                shouldRemove = False
                if size == 0:
                    shouldRemove = True
                if size == 1:
                    if dirFiles[0] == ".DS_Store":
                        shouldRemove = True
                if shouldRemove:
                    shutil.rmtree(path)
                    print("Deleting: " + path)
        return None

    def _add_file_to_moved_files(self, dirName, fileName):
        try:
            self.moved_files[dirName].append(fileName)
        except KeyError:
            self.moved_files[dirName] = [fileName]
            pass
        return None

    def save_recently_moved_names(self):
        with open('files/.latest.txt', 'a') as namesFile:
            namesFile.write('\n\n' + 'MOVE DATE: ' +  self._timestamp() + '\n\n')
            for name in sorted(self.moved_files.keys()):
                header = '\n---------------------------------- ' + name + ' ----------------------------------------\n'
                namesFile.write(header)
                for entry in self.moved_files[name]:
                    namesFile.write(entry + '\n')
        namesFile.close()
        return None

    def _timestamp(self):
        date = datetime.datetime.now()
        return "%d-%d-%d %d:%d:%d" % (date.year, date.month, date.day, date.hour, date.minute, date.second)