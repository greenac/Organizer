from organizer.organize import Names
import os
import sys
from subprocess import call

for arg in sys.argv:
    if arg.find('.py') == -1:
        state = arg.lower()
        break

fPath_names = 'files/.shell_completion'
fPath_files = 'files/.file_names'
worked = True

if state == 'on':
    dirs = ['/Users/agreen/.stage/finished/organized/', '/Volumes/Charlie/.p/', '/Volumes/Charlie/.p/finished/',
            '/Volumes/Echo/.p/', '/Volumes/Echo/.p/finished/']

    paths = []

    for adir in dirs:
        try:
            if os.path.isdir(adir):
                paths.append(adir)
        except:
            print('could not find', adir)

    namer = Names(namesToExclude=['finished'])
    namer.getNamesFromFilesAndDirs(paths)
    file = open(fPath_names, 'w')
    for name in namer.nameList:
        underScoredName = name.replace(' ', '_')
        line = underScoredName + '="' + underScoredName + '"\n'
        file.write(line)
    file.close()
elif state == 'off':
    file = open(fPath_names, 'r')
    for line in file:
        name = line.split('=')[0]
        cmd = 'unset $' + name
        suc = call(cmd, shell=True)
        if suc != 0:
            print('Error: could not unset $', name)
    file.close()
    file = open(fPath_names, 'w')
    file.write('')
    file.close()
else:
    worked = False
    print('Error: must enter on or off argument')

if worked:
    success = call('source /Users/agreen/.bash_profile', shell=True)

    if success == 0 and state == 'on':
        print('autocomplete has been turned on...')
    elif success == 0 and state == 'off':
        print('autocomplete has been turned off...')
    else:
        print('Error in running autocomplete...state = ' + state)
