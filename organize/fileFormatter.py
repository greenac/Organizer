import os

class FileFormatter:
    def __init__(self):
        self.file_formats = [
            'mp4',
            'wmv',
            'avi',
            'mpg',
            'mpeg',
            'mov',
            'asf',
            'mkv',
            'flv',
            'm4v',
            'rmvb'
        ]

    def file_contains_format(self, file, path_to_file):
        if not os.path.isdir(path_to_file + file):
            format_list = file.rsplit('.', 1)
            if len(format_list) > 1:
                if format_list[1].lower() in self.file_formats:
                    return True
        return False
