import os
from organize.names import Names


class SymLinker:
    def __init__(self, base_path):
        self.base_path = base_path
        self.names = Names(names_to_exclude=[
            '.DS_Store',
            '.organized',
            '.finished'
        ])
        self.link_counter = 1

    def setup(self):
        self.names.get_names_from_files_and_dirs(paths_list=[])
        return None

    def link(self):
        [self._link_helper(file, file, self.base_path) for file in os.listdir(self.base_path)
         if os.path.isdir(os.path.join(self.base_path, file))]
        self.link_counter = 1
        return None

    def _link_helper(self, name, dir, parent_path):
        dir_path = os.path.join(parent_path, dir)
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isdir(file_path):
                self._link_helper(name, file, dir_path)
                return None
            names = self.names.names_in_file(file)
            for p_name in names:
                underscored_name = self.names.underscored_name(p_name)
                link_path = os.path.join(self.base_path, underscored_name, file)
                if underscored_name != name and not os.path.exists(link_path):
                    name_path = os.path.join(self.base_path, underscored_name)
                    if not os.path.exists(name_path):
                        os.makedirs(name_path)
                    print(self.link_counter, ':linking files:\t', file_path, '\n\t\t\t', link_path, '\n')
                    os.symlink(file_path, link_path)
                    self.link_counter += 1
        return None

    def remove_links(self):
        [self._remove_links_helper(file, self.base_path) for file in os.listdir(self.base_path)
         if os.path.isdir(os.path.join(self.base_path, file))]
        self.link_counter = 1
        return None

    def _remove_links_helper(self, dir, base_path):
        dir_path = os.path.join(base_path, dir)
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isdir(file_path):
                self._remove_links_helper(file, dir_path)
            else:
                if os.path.islink(file_path):
                    print(self.link_counter, 'removing link:', file_path)
                    os.remove(file_path)
                    self.link_counter += 1
        return None
