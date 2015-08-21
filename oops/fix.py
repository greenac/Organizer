import sys
import os
import shutil

sPath = "/Users/acgreen1226/Documents/python/organizer/"
dPath = "/Users/acgreen1226/Documents/.Downloads/finished_test/"
files = os.listdir(sPath)
target = "REPEATED_DIR"
for aFile in files:
    if target in aFile:
        newName = aFile.split(target)[1]
        s = sPath + aFile
        d = dPath + newName
        print("SOURCE -- " + s)
        print("DESTINATION -- " + d + "\n")
        shutil.move(s, d)
