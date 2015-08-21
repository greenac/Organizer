import os
import shutil

topLevelPath = '/Users/acgreen1226/Documents/.Downloads/finished/organized/'
targetPath = '/Users/acgreen1226/Documents/.Downloads/finished/'

topFiles = os.listdir(topLevelPath)

for topFile in topFiles:
    dirPath = topLevelPath + topFile
    if os.path.isdir(dirPath):
        files = os.listdir(dirPath)
        dirPath = dirPath + '/'
        for aFile in files:
            src = dirPath + aFile
            dst = targetPath + aFile
            shutil.move(src, dst)
        shutil.rmtree(dirPath)