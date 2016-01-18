import os
import shutil
from organize.printFormatter import PrintFormatter


class Organizer:
    def __init__(self, names, top_level_path, target_folder_path, files_to_exclude):
        self.top_level_dir_path = top_level_path
        self.target_folder_path = target_folder_path
        self.fileNames = os.listdir(top_level_path)
        self.names = names
        self.dirNames = []
        self.printFormatter = PrintFormatter()
        self.repeatedDirName = "REPEATED_DIRECTORY"
        self.dirs_to_move = {}
        self.files_to_exclude = set(files_to_exclude)

    def newDirName(self, name):
        nameList = self.names.separate_names(name)
        if len(nameList) == 2:
            dirName = nameList[0] + "_" + nameList[1]
        else:
            dirName = nameList[0]
        return dirName

    def doesNameListHaveRepeatedFirstName(self, name):
        hasSameFirstName = False
        names = self.names.seperateNames(name)
        if self.names.hasFirstAndLastName(name):
            for aName in self.names.nameList:
                splitNames = self.names.seperateNames(aName)
                counter = 0
                if len(splitNames) == 2:
                    if splitNames[0] == names[0] and splitNames[1] != names[1]:
                        hasSameFirstName = True
                        break
                else:
                    if splitNames[0] == names[0]:
                        counter += 1
                        if counter == 2:
                            hasSameFirstName = True
                            break
        else:
            counter = 0
            for aName in self.names.nameList:
                splitNames = self.names.seperateNames(aName)
                if len(splitNames) == 1:
                    if splitNames[0] == names[0]:
                        counter += 1
                        if counter == 2:
                            hasSameFirstName = True
                            break
        return hasSameFirstName

    def directoryAlreadyCreatedForFirstName(self, name):
        firstName = self.names.seperateNames(name)[0]
        dirName = self.repeatedDirName
        for aDir in self.dirNames:
            if firstName in aDir:
                dirName = aDir
                break
        return dirName

    def makeNewDirectoryPath(self, name, repeat=False):
        newDirName = self.newDirName(name)
        if repeat:
            newDirName = newDirName + "_repeat/"
        newDirPath = os.path.join(self.target_folder_path, newDirName)
        return newDirPath

    def makeNewDirectory(self, name, repeat=False):
        newDirPath = self.makeNewDirectoryPath(name, repeat)
        if os.path.isdir(newDirPath):
            return False
        else:
            os.mkdir(newDirPath)
            self.dirNames.append(self.newDirName(name) + "/")
            return True

    def filesForFirstAndLastName(self, name):
        files = []
        for aFile in self.fileNames:
            if self.names.file_has_name(name, aFile):
                files.append(aFile)
        for aFile in files:
            self.fileNames.remove(aFile)
        return files

    def filesForFirstName(self, name):
        firstName = self.names.separate_names(name)[0]
        files = []
        for aFile in self.fileNames:
            if firstName.lower() in aFile.lower():
                files.append(aFile)
        for aFile in files:
            self.fileNames.remove(aFile)
        return files

    def moveFilesForFirstAndLastName(self):
        self.printNumberOfFiles()
        files = []
        for name in self.names.all_names():
            if self.names.has_fist_and_last_name(name):
                files = self.filesForFirstAndLastName(name)
            else:
                files = self.filesForFirstName(name)
            if len(files) > 0:
                dirPath = self.makeNewDirectoryPath(name)
                newDir = self.makeNewDirectory(name)
                printNames = []
                for aFile in files:
                    src = os.path.join(self.top_level_dir_path, aFile)
                    dst = os.path.join(dirPath, aFile)
                    if src != dst:
                        shutil.move(src, dst)
                        printNames.append(aFile)
                self.printInfo(name, printNames, dirPath, newDir)
        self.printNumberOfFiles()
        return None

    def move_files(self):
        files = os.listdir(self.top_level_dir_path)
        to_move = {}
        for file in files:
            if file not in self.files_to_exclude:
                names_in_file = [name for name in self.names.all_names()
                                 if self.names.file_has_name(name, file)]
                ranking_name = self.ranker.rank(names_in_file)
                if ranking_name:
                    if ranking_name in self.dirs_to_move:
                        files_for_name = self.dirs_to_move[ranking_name]
                        files_for_name.append(file)
                        to_move[ranking_name] = files_for_name
                    else:
                        to_move[ranking_name] = [file]
        for dir_name, files in to_move:
            is_new = self.makeNewDirectory(dir_name)
            dir_path = self.makeNewDirectoryPath(dir_name)
            printNames = []
            for file in files:
                src = os.path.join(self.top_level_dir_path, file)
                dst = os.path.join(dir_path, file)
                if src != dst:
                    #shutil.move(src, dst)
                    printNames.append(file)
            self.printInfo(dir_name, printNames, dir_path, is_new)
        return None


    def moveFilesForFirstName(self):
        self.printNumberOfFiles()
        for name in self.names.nameList:
            files = self.filesForFirstName(name)
            if len(files) > 0:
                firstName = self.names.seperateNames(name)[0]
                # if there are repeated first names in namelist, makes new directory for first name only and moves files into it
                if self.doesNameListHaveRepeatedFirstName(name):
                    dirPath = self.makeNewDirectoryPath(firstName, True)
                    isNewDir = self.makeNewDirectory(firstName, True)
                    names = []
                    for aFile in files:
                        src = os.path.join(self.top_level_dir_path, aFile)
                        dst = os.path.join(dirPath, aFile)
                        if src != dst:
                            shutil.move(src, dst)
                            names.append(aFile)
                    if len(names) > 0:
                        self.printInfo('Fist Name Only -- Repeated -- ' + name, names, dirPath, isNewDir)
                # if there are not repeated first names in namelist, will move files into folder with same first name
                else:
                    dirPath = self.makeNewDirectoryPath(name)
                    isNewDir = self.makeNewDirectory(name)
                    names = []
                    for aFile in files:
                        src = os.path.join(self.top_level_dir_path, aFile)
                        dst = os.path.join(dirPath, aFile)
                        if src != dst:
                            shutil.move(src, dst)
                            names.append(aFile)
                    if len(names) > 0:
                        self.printInfo('Fist Name Only -- ' + name, names, dirPath, isNewDir)
        self.printNumberOfFiles()
        return None

    def printInfo(self, name, files, dst, isNewDirectory):
        print(self.printFormatter.acrossScreenWithName('-', name))
        if isNewDirectory:
            print('\nMaking New Directory: ' + dst)
        else:
            print('\nNot Making New Directory...Directory Exists: ' + dst)
        print("\nFiles Moved:")
        counter = 1
        for aFile in files:
            print(counter, '--', aFile)
            counter += 1
        print("\nMoved to: " + dst + '\n')
        return None

    def printNumberOfFiles(self):
        numOfFiles = len(self.fileNames)
        if numOfFiles > 0:
            title = 'Files in root directory: ' + str(numOfFiles)
            print('\n' + self.printFormatter.acrossScreenWithName('*', title) + '\n')
        return None
