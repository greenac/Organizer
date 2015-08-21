import os
from organizer.organize import FileFormat


def countFiles(topdirs):
    print('******************* searching', topdir, '***************************')
    fileFormatter = FileFormat()
    counter = 0
    for topdir in topdirs:
        if os.path.isdir(topdir):
            if topdir[len(topdir) - 1] != '/':
                topdir = topdir + '/'
            files = os.listdir(topdir)
            for aFile in files:
                if os.path.isdir(topdir + aFile):
                    newFileNumber = countFiles(topdir + aFile)
                    print('\ncounter:', counter, '\nnew number:', newFileNumber, '\nnew counter:', counter + newFileNumber)
                    counter += newFileNumber
                else:
                    extList = aFile.rsplit('.', 1)
                    try:
                        ext = extList[1]
                        if ext in fileFormatter.fileFormats:
                            counter += 1
                            print(counter, 'a movie:', aFile)
                    except:
                        counter = counter
    print('------ returning', counter, '----------')
    return counter


topPaths = ['/Volumes/Charlie/.p/', '/Volumes/Echo/.p/']
counter = countFiles(topPaths)
print('there are', counter, 'movies')
    