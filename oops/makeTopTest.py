import os
import shutil


def makeFiles(path, fNames, dNames):
    if path[len(path) - 1:] != '/':
        path += '/'
    try:
        shutil.rmtree(path + dNames[0])
    except:
        print('did not delete root dir\n')
    for dirName in dNames:
        newPath = path + dirName
        try:
            os.mkdir(newPath)
            print('making dir: ' + newPath)
        except:
            print('could not make dir: ' + newPath)
        names = fNames[dirName]
        for fName in names:
            f = open(newPath + fName, 'w')
            f.close()


path = '/Volumes/Charlie/test/'
dNames = ['top_dir/', 'top_dir/a_dir/', 'top_dir/b_dir/', 'top_dir/a_dir/a_below/']
fNames = {dNames[0]: ['athing.mp4', 'bthing.wmv'],
          dNames[1]: ['athing.mp4', 'cthing.avi', 'dthing.mp4'],
          dNames[2]: ['athing.mp4', 'bthing.wmv'],
          dNames[3]: ['dthing.mp4', 'emovie.wmv']}
makeFiles(path, fNames, dNames)

