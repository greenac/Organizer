import os
import shutil
from organize.fileNamer import FileNamer

class NameAdder:
    def __init__(self, args, path):
        self.arguments = args
        self.path = path
        self.files = os.listdir(path)

    def renameFiles(self):
        counter = 0
        for arg in self.arguments:
            if counter % 2 == 0:
                names = arg.split('_', 1)
                firstName, lastName = names[0], names[1]
            else:
                indexes = [int(i) for i in arg.split(',')]
                nameList = [firstName, lastName]
                for index in indexes:
                    oldFileName = self.files[index]
                    newFileName = FileNamer().makeNewFileName(nameList, oldFileName, self.path)
                    if newFileName != oldFileName:
                        shutil.move(self.path + oldFileName, self.path + newFileName)
                        print('moving: ' + oldFileName + ' -----> to: ' + newFileName + '\n')
            counter += 1
        return None