import os
import shutil

topDir = '/Volumes/Charlie/.p/'

excDir = ['finished', 'series', 'random']

dirs = os.listdir(topDir)

for dir in dirs:
    dirPath = topDir + dir
    if os.path.isdir(dirPath):
        dirPath += '/'
        files = os.listdir(dirPath)
        for aFile in files:
            if aFile[0] == '_':
                newFile = aFile[1:]
                shutil.move(dirPath + aFile, dirPath + newFile)
                print('\nMoving:', aFile, '\nTo:', newFile)