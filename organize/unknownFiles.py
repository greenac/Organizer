import os
from organize.names import Names
from organize.organizerFile import OrganizerFile
from organize.addDirNameToFiles import AddDirNameToFiles
from organize.nameAdder import NameAdder

class UnknownFiles:
    def __init__(self, path, dir_paths, run_local=False, excluded_names=None):
        self.path = path
        self.dir_paths = dir_paths
        self.names = Names()
        self.excluded_names = set(excluded_names) if excluded_names else set([])
        self.run_local = run_local
        self.files = []
        self.name_adder = NameAdder(None, path)
        self.changed_files = {}

    def fetch_unknown_files(self):
        if self.run_local:
            self.names.get_names_from_file()
        else:
            self.names.get_names_from_files_and_dirs(self.dir_paths)
        files = os.listdir(self.path)
        printList = []
        for aFile in files:
            shouldPrint = True
            for name in self.names.all_names():
                if aFile in self.excluded_names or self.names.file_has_name(name, aFile):
                    shouldPrint = False
                    break
            printList.append(shouldPrint)
        counter = 0
        for shouldPrint in printList:
            if shouldPrint:
                organizer_file = OrganizerFile(files[counter], counter)
                self.files.append(organizer_file)
            counter += 1
        return None

    def file_at_index(self, index):
        return self.files[index]

    def print_unknown_files(self):
        [print(organizer_file.index, '--', organizer_file.file_name) for organizer_file in self.files]
        return None

    def list_files_in_directory(self, dir):
        print('\tsub-files:')
        files = os.listdir(os.path.join(self.path, dir))
        for i in range(len(files)):
            file = files[i]
            print('\t\t',i, ':', file)
        return None

    def sub_files_for_file_index(self, fileIndex):
        organizer_file = self.files[fileIndex]
        return list(os.listdir(os.path.join(self.path, organizer_file.file_name)))

    def add_dir_names_to_sub_files(self, organizer_file):
        name_adder = AddDirNameToFiles(organizer_file.file_name, self.path)
        name_adder.add(should_print=False)
        return None

    def add_names_to_file(self, unknown_file, names):
        new_name = self.name_adder.rename_file(
            unknown_file.file_name,
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
