import os
import json


class Names:
    def __init__(
            self,
            file_name=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../files/names.txt'),
            cached_file_name=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../files/cached_names.json'),
            names_to_exclude=None
    ):
        self.file_name = file_name
        self.cached_name_file = cached_file_name
        self.names_to_exclude = names_to_exclude if names_to_exclude else []
        self.name_list = []

    def cleanup(self):
        self.remove_excluded_names()
        self.name_list.sort()
        return None

    def remove_excluded_names(self):
        self.make_name_list_unique()
        for name in list(self.name_list):
            if name in self.names_to_exclude:
                self.name_list.remove(name)
        return None

    def get_names_from_file(self):
        names_file = open(self.file_name, 'r')
        for name in names_file:
            if name != '\n':
                name = name.replace('_', ' ')
                self.name_list.append(name.lower().replace('\n', ''))
        names_file.close()
        return None

    def get_names_from_cached_file(self):
        with open(self.cached_name_file, 'r') as cached_file:
            try:
                cached_names = json.load(cached_file)
                self.name_list += cached_names
            except ValueError:
                pass
        cached_file.close()
        return None

    def get_names_from_dirs(self, paths_list):
        names_from_dirs = []
        for path in paths_list:
            try:
                names_for_path = list(os.listdir(path))
            except FileNotFoundError:
                continue
            for name in names_for_path:
                if not os.path.isdir(os.path.join(path, name)):
                    names_for_path.remove(name)
            names_from_dirs += names_for_path
        self.name_list += self.remove_underscore(names_from_dirs)
        return None

    def get_names_from_files(self, should_clean_up=True, use_current_cache=True):
        self.get_names_from_file()
        if use_current_cache:
            self.get_names_from_cached_file()
        if should_clean_up:
            self.cleanup()
        return None

    def get_names_from_files_and_dirs(self, paths_list, use_current_cache=True):
        self.get_names_from_files(should_clean_up=False)
        self.get_names_from_dirs(paths_list)
        self.cleanup()
        return None

    def make_name_list_unique(self):
        self.name_list = list(set(self.name_list))
        return None

    def remove_underscore(self, name_list):
        return [name.replace('_', ' ') for name in name_list]

    def file_has_name(self, name, file, is_case_sensitive=False, first_only=False):
        names = self.separate_names(name)
        first_name = names[0]
        if first_only:
            if is_case_sensitive:
                if first_name in file:
                    return True
                return False
            else:
                if first_name.lower() in file.lower():
                    return True
                return False
        else:
            if len(names) == 1:
                return False
            else:
                last_name = names[1]
                if is_case_sensitive:
                    if first_name in file and last_name in file:
                        return True
                    return False
                else:
                    if first_name.lower() in file.lower() and last_name.lower() in file.lower():
                        return True
                    return False

    def file_has_name_2(self, name, file):
        if name.find(' ') >= 0:
            name = name.replace(' ', '_')
        return name in file

    def separate_names(self, name):
        if '_' in name:
            splitter = '_'
        else:
            splitter = ' '
        return name.split(splitter, 1)

    def has_fist_and_last_name(self, name):
        names = self.separate_names(name)
        if len(names) == 2:
            return True
        else:
            return False

    def update_cached_names(self, paths, should_print=False, use_current_cache=True):
        self.get_names_from_dirs(paths)
        self.get_names_from_files(use_current_cache=use_current_cache)
        with open(self.cached_name_file, 'w') as cached_file:
            json.dump(self.name_list, cached_file)
        cached_file.close()
        return None

    def all_names(self):
        return self.name_list

    def all_names_underscored(self):
        return [name.replace(' ', '_') for name in self.name_list]

    def underscored_name(self, name):
        return name.replace(' ', '_')

    def first_and_last_names(self):
        return [name.split(' ') for name in self.name_list]

    def names_in_file(self, file):
        return [name for name in self.name_list if self.file_has_name_2(name, file)]
