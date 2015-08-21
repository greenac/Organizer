import sys
import shutil

cut_limit = 4
star_name_list = ['holly', 'michaels']
star_name = '_'.join(star_name_list)
stars_names = ''
try:
    arguments = sys.argv
    del arguments[0]
    args = []
    current_arg = ''
    for i in range(0, len(arguments)):
        arg = arguments[i]
        if i == len(arguments) - 1:
            if arg != ' ':
                current_arg += arg
                args.append(current_arg)
        elif ',' in arg:
            current_arg += arg.replace(',', '')
            args.append(current_arg)
            current_arg = ''
        else:
            if arg != ' ':
                current_arg += arg + '_'
    if len(args) < cut_limit:
        raise Exception()
    else:
        args.insert(cut_limit, star_name)
        cut_plus = cut_limit + 1
        if len(args) > cut_plus:
            base_args = args[:cut_plus]
            stars_names = '_'.join(args[cut_plus:])
            args = base_args
            args.append(stars_names)
except Exception as exception:
    print(exception)
    print(
        'Error: must Enter old file, studio name, month, day, year, file name, and optional stars names(if more than one).\nThere are currently: ' + str(
            len(args)) + ' arguments:', args)
    sys.exit(0)

base_path = '/Volumes/Charlie/.p/' + star_name + '/'
old_file = args.pop(0)
ext = old_file.rsplit('.')[1]
new_file = ''
counter = 0
for arg in args:
    new_file += arg
    if counter != len(args) - 1:
        new_file += '_'
    counter += 1
new_file += '.' + ext
new_file = new_file.lower()

src = base_path + old_file
dst = base_path + new_file

shutil.move(src, dst)
print('Moved: ' + old_file + '\nTo: ' + new_file)
