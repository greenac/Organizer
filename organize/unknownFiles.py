import os
import curses
from organize.names import Names
from organize.unknownFile import UnknownFile
from organize.addDirNameToFiles import AddDirNameToFiles
from organize.nameAdder import NameAdder

class UnknownFiles:
    def __init__(self, path, dirPaths, runLocal=False, namesNotToPrint=[]):
        self.path = path
        self.dirPaths = dirPaths
        self.names = Names()
        self.namesNotToPrint = set(namesNotToPrint)
        self.runLocal = runLocal
        self.unknownFiles = []
        self.nameAdder = NameAdder(None, path)
        self.changedFiles = {}

    def fetchUnknownFiles(self):
        if self.runLocal:
            self.names.getNamesFromFiles()
        else:
            self.names.getNamesFromFilesAndDirs(self.dirPaths)
        files = os.listdir(self.path)
        printList = []
        for aFile in files:
            shouldPrint = True
            for name in self.names.nameList:
                if aFile in self.namesNotToPrint or self.names.fileHasName(name, aFile):
                    shouldPrint = False
                    break
            printList.append(shouldPrint)
        counter = 0
        for shouldPrint in printList:
            if shouldPrint:
                unknownFile = UnknownFile(files[counter], counter)
                self.unknownFiles.append(unknownFile)
            counter += 1
        return None

    def printUnknownFiles(self):
        [print(unknownFile.index, '--', unknownFile.file_name) for unknownFile in self.unknownFiles]
        return None

    def stepThroughFiles(self):
        try:
            for unknownFile in self.unknownFiles:
                print('\nUnknown file:', unknownFile.file_name)
                if os.path.isdir(os.path.join(self.path, unknownFile.file_name)):
                    self.listFilesInDirectory(unknownFile.file_name)
                    choice = input('Add directory name to subfiles? y/n ')
                    self.addDirNamesToSubfiles(choice, unknownFile)
                names = input('Names to add to: ' + unknownFile.file_name + ' ? ').strip(' ').split(',')
                if names[0] == '':
                    continue
                choice = input('\nAdd ' + str(names) + ' to ' + unknownFile.file_name + ' y/n ')
                self.addNamesToFile(choice, unknownFile, names)
            self.printSummary()
        except KeyboardInterrupt:
            print("\n\noh no...I'm dying...agggrrr...anyway cold hearted...")
            self.printSummary()
        return None

    def stepThroughFilesInterface(self):
        try:
            for unknownFile in self.unknownFiles:
                print('\nUnknown file:', unknownFile.file_name)
                if os.path.isdir(os.path.join(self.path, unknownFile.file_name)):
                    self.listFilesInDirectory(unknownFile.file_name)
                    choice = input('Add directory name to subfiles? y/n ')
                    self.addDirNamesToSubfiles(choice, unknownFile)
                names = input('Names to add to: ' + unknownFile.file_name + ' ? ').strip(' ').split(',')
                if names[0] == '':
                    continue
                choice = input('\nAdd ' + str(names) + ' to ' + unknownFile.file_name + ' y/n ')
                self.addNamesToFile(choice, unknownFile, names)
            self.printSummary()
        except KeyboardInterrupt:
            print("\n\noh no...I'm dying...agggrrr...anyway cold hearted...")
            self.printSummary()
        return None

    def listFilesInDirectory(self, dir):
        print('\tsub-files:')
        files = os.listdir(os.path.join(self.path, dir))
        for i in range(len(files)):
            file = files[i]
            print('\t\t',i, ':', file)
        return None

    def addDirNamesToSubfiles(self, choice, unknownFile):
        choice = choice.lower()
        if choice == 'y' or choice == 'yes':
            nameAdder = AddDirNameToFiles(unknownFile.file_name, self.path)
            nameAdder.add()
        return None

    def addNamesToFile(self, choice, unknownFile, names):
        choice = choice.lower()
        if choice == 'y' or choice == 'yes':
            newName = self.nameAdder.renameFile(unknownFile, ','.join(names))
            self.changedFiles[unknownFile.file_name] = newName
        return None

    def printSummary(self):
        print("Here's the summary:")
        for oldName in self.changedFiles:
            newName = self.changedFiles[oldName]
            print('\t' + oldName, 'became --->', newName)
        return None
