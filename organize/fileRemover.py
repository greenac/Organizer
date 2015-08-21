import os

class FileRemover:
    def __init__(self, path, targets, caseSens=False):
        self.targets = targets
        self.caseSens = caseSens
        self.path = path

    def removeFiles(self, path):
        files = os.listdir(path)
        for aFile in list(files):
            filePath = path + aFile
            if os.path.isdir(filePath):
                if self.shouldDeleteFile(filePath):
                    self.deleteFile(filePath, isDir=True)
                else:
                    if filePath[len(filePath) - 1:] != '/':
                        filePath += '/'
                    self.removeFiles(filePath)
            else:
                if self.shouldDeleteFile(filePath):
                    self.deleteFile(filePath)
        return None

    def shouldDeleteFile(self, path):
        delFile = False
        if self.caseSens:
            for target in self.targets:
                if target in path:
                    delFile = True
                    break
        else:
            for target in self.targets:
                if target.lower() in path.lower():
                    delFile = True
                    break
        return delFile

    def deleteFile(self, path, isDir=False):
        if isDir:
            shutil.rmtree(path)
        else:
            os.remove(path)
        print('Removing File: ' + path)
        return None
