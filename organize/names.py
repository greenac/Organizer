import os
import json

class Names:
    def __init__(
            self,
            fileName=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../files/names.txt'),
            cachedNameFile=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../files/cached_names.json'),
            completionFile=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../files/.shell_completion'),
            namesToExclude=[]
    ):
        self.fileName = fileName
        self.cachedNameFile = cachedNameFile
        self.completionFileName = completionFile
        self.nameList = []
        self.namesToExclude = namesToExclude

    def cleanUp(self):
        self.removeExcludedNames()
        self.nameList.sort()
        return None

    def removeExcludedNames(self):
        self.makeNameListUnique()
        for name in list(self.nameList):
            if name in self.namesToExclude:
                self.nameList.remove(name)
        return None

    def getNamesFromFile(self):
        namesFile = open(self.fileName, 'r')
        for name in namesFile:
            if name != '\n':
                self.nameList.append(name.lower().replace('\n', ''))
        namesFile.close()
        return None

    def getNamesFromCacheFile(self):
        with open(self.cachedNameFile, 'r') as cachedNamesFile:
            try:
                cacheNames = json.load(cachedNamesFile)
                self.nameList += cacheNames
            except ValueError:
                pass
        cachedNamesFile.close()
        return None

    def getNamesFromCompletionFile(self):
        names = []
        namesFile = open(self.completionFileName, 'r')
        for line in namesFile:
            if line != '\n':
                name = line.split('=')[0]
                names.append(name)
        namesFile.close()
        self.nameList = self.nameList + self.removeUnderscore(names)
        return None

    def getNamesFromDirs(self, pathsList):
        namesFromDirs = []
        for path in pathsList:
            try:
                namesForPath = list(os.listdir(path))
            except FileNotFoundError:
                continue
            for name in namesForPath:
                if not os.path.isdir(os.path.join(path, name)):
                    namesForPath.remove(name)
            namesFromDirs = namesFromDirs + namesForPath
        self.nameList += self.removeUnderscore(namesFromDirs)
        return None

    def getNamesFromFiles(self, shouldCleanUp=True):
        self.getNamesFromFile()
        self.getNamesFromCompletionFile()
        self.getNamesFromCacheFile()
        if shouldCleanUp:
            self.cleanUp()
        return None

    def getNamesFromFilesAndDirs(self, pathsList):
        self.getNamesFromFiles(shouldCleanUp=False)
        self.getNamesFromDirs(pathsList)
        self.cleanUp()
        return None

    def makeNameListUnique(self):
        self.nameList = list(set(self.nameList))
        return None

    def removeUnderscore(self, nameList):
        cleanNameList = []
        for name in nameList:
            cleanName = name.replace('_', ' ')
            cleanNameList.append(cleanName)
        return cleanNameList

    def fileHasName(self, name, aFile, caseSensitive=False, firstOnly=False):
        names = self.seperateNames(name)
        firstName = names[0]
        if firstOnly:
            if caseSensitive:
                if firstName in aFile:
                    return True
                return False
            else:
                if firstName.lower() in aFile.lower():
                    return True
                return False
        else:
            if len(names) == 1:
                return False
            else:
                lastName = names[1]
                if caseSensitive:
                    if firstName in aFile and lastName in aFile:
                        return True
                    return False
                else:
                    if firstName.lower() in aFile.lower() and lastName.lower() in aFile.lower():
                        return True
                    return False

    def seperateNames(self, name):
        if '_' in name:
            splitter = '_'
        else:
            splitter = ' '
        return name.split(splitter, 1)

    def hasFirstAndLastName(self, name):
        names = self.seperateNames(name)
        if len(names) == 2:
            return True
        else:
            return False

    def updateCachedNames(self, paths):
        self.getNamesFromFilesAndDirs(paths)
        with open(self.cachedNameFile, 'w') as cachedNamesFile:
            json.dump(self.nameList, cachedNamesFile)
        cachedNamesFile.close()
        return None

    def allNames(self):
        return self.nameList

    def allNamesUnderscored(self):
        return [name.replace(' ', '_') for name in self.nameList]