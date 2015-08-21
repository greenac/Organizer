import os
import shutil

# topDir = "/Users/acgreen1226/Documents/.Downloads/finished/organized/"
topDir = '/Volumes/Charlie/.p/finished/'

for dir in os.listdir(topDir):
    subDir = topDir + dir
    if os.path.isdir(subDir):
        subDir += '/'
        for aFile in os.listdir(subDir):
            if not os.path.isdir(subDir + aFile):
                newFile = aFile.replace('__', ' - ')
                newFile = newFile.replace('___', ' - ')
                newFile = newFile.replace('friend_s', "friend's")
                if aFile != newFile:
                    shutil.move(subDir + aFile, subDir + newFile)
                    print('replacing:', aFile, '\nwith:', newFile)
