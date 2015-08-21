import os

class BalanceFile(object):
    def __init__(self, path, file_name):
        self.path = path
        self.name = file_name
        self.size = os.path.getsize(path)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'path': self.path,
            'file_name': self.file_name,
            'size': self.size
        }

    def base_path(self):
        paths = self.path.rsplit('/', 1)
        if len(paths) == 1:
            return paths[1]
        raise ValueError