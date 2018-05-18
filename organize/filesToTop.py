import os
import shutil
from organize.printFormatter import PrintFormatter
from organize.fileFormatter import FileFormatter
from organize.fileNamer import FileNamer

class FilesToTop:
    def __init__(self, rootPath, exceptedDirs=[], delSamples=False):
        self.exceptedDirs = exceptedDirs
        self.rootPath = rootPath
        self.deleteSamples = delSamples
        self.printFormatter = PrintFormatter()

    def makeNewFile(self, nameList, aFile, pathToFile, fileNumber):
        if FileFormatter().file_contains_format(aFile, pathToFile):
            newFile = FileNamer().makeNewFileName(nameList, aFile, pathToFile)
            if newFile != aFile:
                src = pathToFile + aFile
                dst = pathToFile + newFile
                shutil.move(src, dst)
            print(fileNumber, '-- from: ' + aFile + '\n' + str(fileNumber) + ' -- to:   ' + newFile + '\n')
        elif not os.path.isdir(pathToFile + aFile):
            os.remove(pathToFile + aFile)
            print(fileNumber, '-- removing file: ' + aFile + '\n')
            newFile = None
        else:
            print('File is a dir: ' + pathToFile + aFile)
            newFile = None
        return newFile

    def addNameToAllFilesInDir(self, nameList, topDir, currentDirPath):
        files = os.listdir(currentDirPath)
        currentDirPath = self.addSlashToDir(currentDirPath)
        counter = 1
        for aFile in files:
            filePath = os.path.join(currentDirPath, aFile)
            if os.path.isdir(filePath) and 'keep_dir_together' not in aFile.lower():
                self.addNameToAllFilesInDir(nameList, topDir, filePath)
            else:
                newFile = self.makeNewFile(nameList, aFile, currentDirPath, counter)
                if newFile is not None:
                    counter += 1
                    topPath = topDir + newFile
                    if topDir != currentDirPath:
                        if not os.path.exists(topPath):
                            shutil.move(currentDirPath + newFile, topPath)
                            print('Moving file: ' + currentDirPath + newFile)
                            print('To: ' + topPath + '\n')
                        else:
                            message = currentDirPath + newFile + ' exisits in: ' + topDir
                            print(self.printFormatter.acrossScreenWithName('*', message))
        if len(os.listdir(currentDirPath)) == 0:
            shutil.rmtree(currentDirPath)
            print('Removing dir: ' + currentDirPath + '\n')
        else:
            print('Not removing dir: ' + currentDirPath + '\n')
        return None

    def addSlashToDir(self, dirPath):
        if dirPath[len(dirPath) - 1:] != '/':
            dirPath += '/'
        return dirPath

    def moveFilesToTop(self):
        files = os.listdir(self.rootPath)
        for aFile in files:
            dirPath = os.path.join(self.rootPath, aFile)
            if os.path.isdir(dirPath) and aFile.lower() not in self.exceptedDirs:
                print('\n' + self.printFormatter.acrossScreenWithName('-', aFile) + '\n')
                dirPath = self.addSlashToDir(dirPath)
                self.addNameToAllFilesInDir(aFile.split('_', 1), dirPath, dirPath)
        return None