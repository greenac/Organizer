from organize.fileFormatter import FileFormatter
from organize.organizerErros import WrongNameFormatException

class FileNamer:
    def __init__(self):
        self.punctuation = [
            ' ',
            '_',
            '.',
            '[',
            ']',
            ',',
            '/',
            '-',
            '{',
            '}',
            '|',
            '(',
            ')',
            '*',
            '!',
            '&',
            "'"
        ]
        self.fileFormatter = FileFormatter()

    def makeNewFileName(self, nameList, aFile, pathToFile):
        # check if aFile has name in it
        aFile = aFile.lower()
        firstName = nameList[0].lower()
        start = aFile.find(firstName) - 1
        if start >= 0:
            # firstName is found but not at beginning of aFile
            if aFile[start] not in self.punctuation:
                aFile = aFile.replace(firstName, '_' + firstName, 1)
        if len(nameList) > 1:
            # name list has first and last name
            lastName = nameList[1].lower()
            if firstName in aFile and lastName in aFile:
                endFirst = aFile.find(firstName) + len(firstName)
                startLast = aFile.find(lastName)
                if endFirst == startLast:
                    # first and last names are right next to each other
                    newFile = aFile.replace(lastName, '_' + lastName, 1)
                else:
                    # file contains first and last names. No changes needed
                    newFile = aFile
            elif firstName in aFile:
                # file contains first name only
                start = aFile.find(firstName)
                end = start + len(firstName)
                target = aFile[end]
                if target in self.punctuation:
                    newFile = aFile.replace(firstName, firstName + '_' + lastName, 1)
                else:
                    newFile = aFile.replace(firstName, firstName + '_' + lastName + '_', 1)
            else:
                # file does not contain name
                if self.fileFormatter.file_contains_format(aFile, pathToFile):
                    # file is in a movie format
                    parts = aFile.rpartition('.')
                    newFile = parts[0] + '_' + firstName + '_' + lastName + parts[1] + parts[2]
                else:
                    newFile = aFile + '_' + firstName + '_' + lastName
        else:
            if firstName in aFile:
                newFile = aFile
            elif self.fileFormatter.file_contains_format(aFile, pathToFile):
                parts = aFile.rpartition('.')
                newFile = parts[0] + '_' + firstName + parts[1] + parts[2]
            else:
                newFile = aFile + '_' + firstName
        newFile = self.replacePunctuation(newFile, pathToFile)
        return newFile

    def make_new_filename_multiple_names(self, names_list, file, file_path):
        for name_list in names_list:
            first_name = name_list[0]
            try:
                last_name = name_list[1]
            except IndexError:
                raise WrongNameFormatException('a name must have a first and last name')
            file = self.makeNewFileName(
                [first_name, last_name],
                file,
                file_path
            )
        return file

    def replacePunctuation(self, aFile, pathToFile):
        isMovie = False
        if self.fileFormatter.file_contains_format(aFile, pathToFile):
            length = aFile.rfind('.')
            isMovie = True
        else:
            length = len(aFile)
        newName = aFile
        if length != -1:
            i = 0
            while True:
                if newName[i] in self.punctuation:
                    newName = newName[:i] + '_' + newName[i + 1:]
                    try:
                        j = i + 1
                        while True:
                            if newName[j] in self.punctuation:
                                if isMovie:
                                    format_target = newName.rfind('.')
                                    if j == format_target:
                                        break
                                newName = newName[:j] + newName[j + 1:]
                                length -= 1
                                i = j
                                if j >= length:
                                    break
                            else:
                                break
                    except IndexError:
                        break
                i += 1
                if i >= length:
                    break
            if newName[0] == '_':
                newName = newName.replace('_', '', 1)
                length -= 1
            if isMovie:
                target = newName.rfind('.') - 1
                if newName[target] == '_':
                    newName = newName[:target] + newName[target + 1:]
            else:
                if newName[len(newName) - 1] == '_':
                    newName = newName[:len(newName) - 1] + newName[len(newName):]
        return newName

    def clean_name_for_raw_file(self, file, base_path):
        ext = self.fileFormatter.get_format(file, base_path)
        if ext:
            file = file.rsplit('.', 1)[0]
        for punctuation in self.punctuation:
            file = file.replace(punctuation, '_')
        to_remove = []
        i = len(file) - 1
        while i >= 0:
            if file[i] == '_' and (i == 0 or i == len(file) - 1 or file[i - 1] == '_'):
                to_remove.append(i)
            i -= 1
        for index in to_remove:
            file = file[:index] + file[index + 1:]
        if ext:
            file += '.' + ext
        return file.lower()





