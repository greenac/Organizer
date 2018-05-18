import os
import subprocess
import bisect
import organize.organizerErros as OrganizerExceptions
from organize.balanceConstants import BalanceConstants
from organize.balanceFile import BalanceFile
from organize.directoryMover import DirectoryMover

class BalanceTree(object):
    def __init__(self, disk_path, root_path, files_to_exclude=None):
        self.disk_path = disk_path
        self.root_path = root_path
        self._files_to_exclude = files_to_exclude
        self._constants = BalanceConstants()
        self.files = os.listdir(root_path)
        self._disk_info = self.set_disk_info()
        self.used_space = self._disk_info[self._constants.used_space]
        self.index = 0

    def set_disk_info(self):
        df = subprocess.Popen(["df", self.disk_path], stdout=subprocess.PIPE)
        output = df.communicate()[0].decode('utf-8')
        results = output.split('\n')
        labels = [label.lower() for label in results[0].split(' ') if label != '']
        values = [value for value in results[1].split(' ') if value != '']
        free_space = int(values[self._find_index(labels, 'available')])*self._constants.block_size
        used_space = int(values[self._find_index(labels, 'used')])*self._constants.block_size
        disk_info = {
            self._constants.free_space: free_space,
            self._constants.used_space: used_space,
            self._constants.total_space: free_space + used_space
        }
        return disk_info

    def _find_index(self, target_list, target):
        try:
            index = target_list.index(target)
        except Exception:
            raise OrganizerExceptions.NoValueInListException(str(target) + ' is not a label of disk info')
        return index

    def used_space_ratio(self):
        return self.used_space/self._disk_info[self._constants.total_space]

    def free_space(self):
        return self._disk_info[self._constants.total_space] - self.used_space

    def projected_used_space_ratio(self, file_size):
        used_space = self.used_space + file_size
        return used_space/self._disk_info[self._constants.total_space]

    def projected_free_space(self, file_size):
        return self._disk_info[self._constants.total_space] - self.used_space - file_size

    def able_to_add_dir(self, dir_path):
        return os.path.getsize(dir_path) < self.free_space()

    def _pop_file(self, file_index):
        file_name = self.files.pop(file_index)
        file = BalanceFile(
            path=os.path.join(self.root_path, file_name),
            file_name=file_name
        )
        self.used_space -= file.size
        return file

    def pop_first_file(self):
        return self._pop_file(0)

    def pop_last_file(self):
        return self._pop_file(len(self.files) - 1)

    def _get_file(self, index):
        file = self.files[index]
        path = os.path.join(self.root_path, file)
        return BalanceFile(path=path, file_name=file)

    def first_file(self):
        return self._get_file(0)

    def last_file(self):
        return self._get_file(len(self.files) - 1)

    def add_file(self, balance_file):
        try:
            index_info = self._insertion_index(balance_file.file_name)
        except OrganizerExceptions.NoValueInListException as e:
            print(e)
        destination_path = os.path.join(self.root_path, balance_file.file_name)
        # TODO Add error handling in case moving dirs fails when handling is added to DirectoryMover
        dir_mover = DirectoryMover(balance_file.path, destination_path)
        dir_mover.move_single_dir(dir_mover.src_path, dir_mover.dst_path)
        if not index_info[self._constants.has_file]:
            print('inserting:', balance_file.file_name, 'into:', self.root_path)
            self.files.insert(index_info[self._constants.file_index], balance_file.file_name)
        self.used_space += balance_file.size
        return None

    def _file_path(self, file):
        return os.path.join(self.root_path, file)

    def _insertion_index(self, file_name):
        index = bisect.bisect_left(self.files, file_name)
        if index <= len(self.files):
            insert_info = {
                    self._constants.has_file: False,
                    self._constants.file_index: index
                }
            try:
                if self.files[index] == file_name:
                    insert_info[self._constants.has_file] = True
            except IndexError:
                pass
            return insert_info
        raise OrganizerExceptions.NoValueInListException(
            'Could not find insertion index in files list for: ' + file_name
        )

    def projected_size(self, balance_file):
        return self.used_space + balance_file.size
