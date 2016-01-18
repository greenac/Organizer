import os

class FileFormatter:
    def __init__(self):
        self.file_formats = {
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
        }

    def file_contains_format(self, file, base_path):
        if not os.path.isdir(os.path.join(base_path, file)):
            format_list = file.rsplit('.', 1)
            if len(format_list) > 1:
                if format_list[1].lower() in self.file_formats:
                    return True
        return False

    def get_format(self, file, base_path):
        if self.file_contains_format(file, base_path):
            return file.rsplit('.', 1)[1]
        return None