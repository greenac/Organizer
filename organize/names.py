import os
class Names:
    def __init__(self, fileName='files/names.txt', completionFile='files/.shell_completion', namesToExclude=[]):
        self.fileName = fileName
        self.completionFileName = completionFile
        self.nameList = []
        self.namesToExclude = namesToExclude

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
                self.nameList.append(name.replace('\n', ''))
        namesFile.close()
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
            namesForPath = os.listdir(path)
            for name in list(namesForPath):
                if not os.path.isdir(path + name):
                    namesForPath.remove(name)
            namesFromDirs = namesFromDirs + namesForPath
        self.nameList = self.nameList + self.removeUnderscore(namesFromDirs)
        return None

    def getNamesFromFiles(self):
        self.getNamesFromFile()
        self.getNamesFromCompletionFile()
        self.removeExcludedNames()
        return None

    def getNamesFromFilesAndDirs(self, pathsList):
        self.getNamesFromFile()
        self.getNamesFromCompletionFile()
        self.getNamesFromDirs(pathsList)
        self.removeExcludedNames()
        return None

    def makeNameListUnique(self):
        i = 0
        cont = True
        while cont:
            name = self.nameList.pop(i)
            size = self.removeRepeatName(name) + 1
            self.nameList.insert(i, name)
            i += 1
            if i >= size:
                cont = False
        return None

    def removeRepeatName(self, name):
        self.nameList.reverse()
        if name in list(self.nameList):
            self.nameList.remove(name)
            self.removeRepeatName(name)
        self.nameList.reverse()
        return len(self.nameList)

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