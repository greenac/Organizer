import os
import random

class CreateTestFiles(object):
    def __init__(self):
        self.from_path = '/Volumes/Echo/.p/finished'
        self.to_path1 = '/Users/agreen/Desktop/t1'
        self.to_path2 = '/Users/agreen/Desktop/t2'
        self.to_path = None
        self.files = os.listdir(self.from_path)
        self.test_dir = set()
        self.max_num_to_create = 10
        self.dirs_to_choose = 50
        random.seed()

    def create(self):
        for i in range(self.dirs_to_choose):
            self.test_dir.add(self.choose_dir())
        for dir in list(self.test_dir):
            self.set_to_path()
            new_dir = os.path.join(self.to_path, dir)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            self.make_files_for_dir(dir)
        return None

    def set_to_path(self):
        if random.randint(0,100) % 2 == 0:
            self.to_path = self.to_path1
        else:
            self.to_path = self.to_path2
        return None

    def choose_dir(self):
        target = random.randint(0, len(self.files) - 1)
        target_dir = self.files[target]
        if target_dir in self.test_dir:
            return self.choose_dir()
        return target_dir

    def make_files_for_dir(self, dir):
        path = os.path.join(self.from_path, dir)
        new_path = os.path.join(self.to_path, dir)
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(new_path, file)
            with open(file_path, 'w') as f:
                f.write(file)
            f.close()
        return None
