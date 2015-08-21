import sys
import os
from organizer.organize import FindName

paths = ['/Users/agreen/.stage/finished/organized/',
         '/Volumes/Charlie/.p/',
         '/Volumes/Charlie/.p/finished/',
         '/Volumes/Echo/.p/',
         '/Volumes/Echo/.p/finished/'
]
words = []

for arg in sys.argv:
    if arg.find('.py') == -1:
        words.append(arg.lower())

finder = FindName(words, paths, False)
finder.searchDirForWords()
