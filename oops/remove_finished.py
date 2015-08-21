import os
import shutil

topDir = '/Volumes/Charlie/.p/finished/'

dirs = os.listdir(topDir)

for dir in dirs:
    dirPath = topDir + dir
    if os.path.isdir(dirPath):
        dirPath += '/'
        files = os.listdir(dirPath)
        for aFile in files:
            if '_finished' in aFile.lower():
                newFile = aFile.replace('_finished', '')
                shutil.move(dirPath + aFile, dirPath + newFile)
                print('\nReplaceing:', aFile, '\nWith:', newFile)
        
  