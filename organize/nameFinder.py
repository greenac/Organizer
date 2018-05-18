import os

class NameFinder:
    def __init__(self, wordsList, searchPaths, areWordsSolo):
        self.wordsToFind = wordsList
        self.searchPaths = searchPaths
        self.areSolo = areWordsSolo

    def searchDirForWords(self):
        print('searching for: ' + ' '.join(self.wordsToFind))
        for path in self.searchPaths:
            if os.path.isdir(path):
                if path[len(path) - 1] != '/':
                    path += '/'
                files = os.listdir(path)
                for file in files:
                    fPath = path + file
                    if os.path.isdir(fPath):
                        name = file.replace('_', ' ')
                        self.checkForWords(fPath, name)
        return None

    def checkForWords(self, path, name):
        if os.path.isdir(path):
            if path[len(path) - 1] != '/':
                path += '/'
            files = os.listdir(path)
            for aFile in files:
                fPath = path + aFile
                self.checkForWords(fPath, name)
        else:
            fParts = path.rsplit('/', 1)
            if len(fParts) > 1:
                mFile = fParts[1]
                if self.hasWords(mFile):
                    print(name + '\n' + path + '\n')
        return None

    def hasWords(self, file):
        hasWords = False
        for word in self.wordsToFind:
            try:
                i = file.index(word)
                if self.areSolo:
                    hasWords = True
                else:
                    if self.checkStart(file, i) and self.checkEnd(file, i + len(word)):
                        hasWords = True
            except:
                hasWords = False
                break
        return hasWords


    def checkStart(self, file, start):
        isClean = False
        if start - 1 >= 0:
            target = file[start - 1]
            if target == '.' or target == '_':
                isClean = True
        else:
            isClean = True
        return isClean

    def checkEnd(self, file, end):
        clean = False
        if end < len(file):
            target = file[end]
            if target == '.' or target == '_':
                clean = True
        return clean