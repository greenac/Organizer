import os
from organize.names import Names

class UnknownFiles:
    def __init__(self, path, dirPaths, runLocal=False, namesNotToPrint=[]):
        self.path = path
        self.dirPaths = dirPaths
        self.names = Names()
        self.namesNotToPrint = namesNotToPrint
        self.runLocal = runLocal

    def printFiles(self):
        if self.runLocal:
            self.names.getNamesFromFiles()
        else:
            self.names.getNamesFromFilesAndDirs(self.dirPaths)
        files = os.listdir(self.path)
        printList = []
        for aFile in files:
            shouldPrint = True
            for name in self.names.nameList:
                try:
                    self.namesNotToPrint.index(aFile)
                    shouldPrint = False
                    break
                except:
                    if self.names.fileHasName(name, aFile):
                        shouldPrint = False
                        break
            printList.append(shouldPrint)
        counter = 0
        self.names.nameList = []
        self.names.getNamesFromFile()
        for shouldPrint in list(printList):
            if shouldPrint:
                for name in self.names.nameList:
                    if self.names.fileHasName(name, files[counter], firstOnly=True):
                        printList[counter] = False
            counter += 1
        counter = 0
        for shouldPrint in printList:
            if shouldPrint:
                print(counter, '--', files[counter])
            counter += 1
        return None