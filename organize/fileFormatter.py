import os

class FileFormatter:
    def __init__(self):
        self.fileFormats = ['mp4', 'wmv', 'avi', 'mpg', 'mpeg', 'mov', 'asf', 'mkv', 'flv', 'm4v', 'rmvb']

    def fileContainsFormat(self, aFile, pathToFile):
        if not os.path.isdir(pathToFile + aFile):
            formatList = aFile.rsplit('.', 1)
            if len(formatList) > 1:
                if formatList[1].lower() in self.fileFormats:
                    return True
        return False