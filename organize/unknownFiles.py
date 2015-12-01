import os
import curses
from organize.names import Names
from organize.unknownFile import UnknownFile
from organize.addDirNameToFiles import AddDirNameToFiles
from organize.nameAdder import NameAdder

class UnknownFiles:
    def __init__(self, path, dir_paths, run_local=False, excluded_names=[]):
        self.path = path
        self.dir_paths = dir_paths
        self.names = Names()
        self.excluded_names = set(excluded_names)
        self.run_local = run_local
        self.files = []
        self.name_adder = NameAdder(None, path)
        self.changed_files = {}

    def fetch_unknown_files(self):
        if self.run_local:
            self.names.getNamesFromFiles()
        else:
            self.names.getNamesFromFilesAndDirs(self.dir_paths)
        files = os.listdir(self.path)
        printList = []
        for aFile in files:
            shouldPrint = True
            for name in self.names.nameList:
                if aFile in self.excluded_names or self.names.fileHasName(name, aFile):
                    shouldPrint = False
                    break
            printList.append(shouldPrint)
        counter = 0
        for shouldPrint in printList:
            if shouldPrint:
                unknownFile = UnknownFile(files[counter], counter)
                self.files.append(unknownFile)
            counter += 1
        return None

    def file_at_index(self, index):
        return self.files[index]

    def print_unknown_files(self):
        [print(unknownFile.index, '--', unknownFile.file_name) for unknownFile in self.files]
        return None

    def step_through_files(self):
        try:
            for unknownFile in self.files:
                print('\nUnknown file:', unknownFile.file_name)
                if os.path.isdir(os.path.join(self.path, unknownFile.file_name)):
                    self.list_files_in_directory(unknownFile.file_name)
                    choice = input('Add directory name to subfiles? y/n ')
                    self.add_dir_names_to_sub_files(choice, unknownFile)
                names = input('Names to add to: ' + unknownFile.file_name + ' ? ').strip(' ').split(',')
                if names[0] == '':
                    continue
                choice = input('\nAdd ' + str(names) + ' to ' + unknownFile.file_name + ' y/n ')
                self.add_names_to_file(choice, unknownFile, names)
            self.print_summary()
        except KeyboardInterrupt:
            print("\n\noh no...I'm dying...agggrrr...anyway cold hearted...")
            self.print_summary()
        return None

    def list_files_in_directory(self, dir):
        print('\tsub-files:')
        files = os.listdir(os.path.join(self.path, dir))
        for i in range(len(files)):
            file = files[i]
            print('\t\t',i, ':', file)
        return None

    def sub_files_for_file_index(self, fileIndex):
        unknownFile = self.files[fileIndex]
        return list(os.listdir(os.path.join(self.path, unknownFile.file_name)))

    def add_dir_names_to_sub_files(self, unknownFile):
        name_adder = AddDirNameToFiles(unknownFile.file_name, self.path)
        name_adder.add(should_print=False)
        return None

    def add_names_to_file(self, unknown_file, names):
        new_name = self.name_adder.renameFile(
            unknown_file,
            ','.join(names),
            should_print=False
        )
        self.changed_files[unknown_file.file_name] = new_name
        return new_name

    def is_file_dir(self, file_index):
        return os.path.isdir(os.path.join(self.path, self.files[file_index].file_name))

    def number_of_unknowns(self):
        return len(self.files)

    def print_summary(self):
        print("Here's the summary:")
        for oldName in self.changed_files:
            newName = self.changed_files[oldName]
            print('\t' + oldName, 'became --->', newName)
        return None
