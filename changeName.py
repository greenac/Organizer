import os
import shutil
import sys
import organize.organizerErros as OrganizerExceptions

def rename(base_path, name, change_to_name):
    try:
        files = os.listdir(base_path)
    except OSError:
        print(current_name, 'is not in', base_path)
        return
    for file in files:
        file_path = os.path.join(base_path, file)
        try:
            sub_files = os.listdir(file_path)
            rename(file_path, name, change_to_name)
            continue
        except OSError:
            pass
        new_name = file.replace(name, change_to_name)
        new_file_path = os.path.join(base_path, new_name)
        if file_path != new_file_path:
            print('name:', name, 'new name', new_name)
            print('moving:', file_path, '\nto:', new_file_path, '\n')
            shutil.move(file_path, new_file_path)
    return None

args = sys.argv
try:
    del args[0]
    current_name = args.pop(0).lower()
    future_name = args.pop(0).lower()
except IndexError:
    raise OrganizerExceptions.CommandLineArgumentException('Not enough arguments given')

base_paths = [
    '/Volumes/Papa/.p',
    '/Volumes/Papa/.organized'
]

for base_path in base_paths:
    rename(base_path, current_name, future_name)
    target_path = os.path.join(base_path, current_name)
    if os.path.isdir(target_path):
        new_path = os.path.join(base_path, future_name)
        print('moving dir: ', target_path, '\nto:', new_path)
        shutil.move(target_path, new_path)
