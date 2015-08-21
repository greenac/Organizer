import os
import shutil

# path = '/Volumes/Charlie/.p/finished/'
#path = '/Users/acgreen1226/Documents/.Downloads/finished/'
path = '/Volumes/Delta/.p2/finished/'
targetName = 'angelica_sage'
targetPath = path + targetName
newName = 'angelica_saige'

print('searching: ' + targetPath)
if os.path.exists(targetPath) and os.path.isdir(targetPath):
    targetPath += '/'
    files = os.listdir(targetPath)
    for oldFile in files:
        if not os.path.isdir(targetPath + oldFile):
            newFile = oldFile.replace(targetName, newName)
            print('\nreplacing:', oldFile, '\nwith:', newFile)
            shutil.move(targetPath + oldFile, targetPath + newFile)
    shutil.move(targetPath, path + newName)
    print('\nmoving directory:', targetName, ' to:', newName)
else:
    print('Target Path Does Not Exist Or Is Not A Directory: ' + targetPath)