import os
import shutil
from organize.fileNamer import FileNamer
import organize.organizerErros as OrganizerErrors
class NameAdder:
    def __init__(self, args, path):
        self.arguments = args
        self.path = path
        self.files = os.listdir(path)

    def rename_files(self):
        i = 0
        while i < len(self.arguments):
            names = self.arguments[i]
            numbers = self.arguments[i + 1]
            names_list = self._handle_names(names)
            for index in self._handle_numbers(numbers):
                old_name = self.files[index]
                new_name = FileNamer().make_new_filename_multiple_names(
                    names_list,
                    old_name,
                    self.path
                )
                shutil.move(
                    os.path.join(self.path, old_name),
                    os.path.join(self.path, new_name)
                )
                #print('moving:', old_name, '-----> to:', new_name, '\n')
            i += 2
        return None

    def rename_file(self, file_name, names, should_print=True):
        new_name = FileNamer().make_new_filename_multiple_names(
            self._handle_names(names),
            file_name,
            self.path
        )
        shutil.move(
            os.path.join(self.path, file_name),
            os.path.join(self.path, new_name)
        )
        if should_print:
            print('moving:', file_name, '-----> to:', new_name, '\n')
        return new_name

    def _handle_names(self, names):
        names_list = names.split(',')
        if len(names_list) == 1:
            return [self._separate_names(names)]
        else:
            return [self._separate_names(name) for name in names_list]

    def _separate_names(self, names):
        names_list = names.split('_')
        first_name = names_list[0]
        try:
            last_name = names_list[1]
        except IndexError:
            raise OrganizerErrors.WrongNameFormatException('Name must have first and last name')
        return [first_name, last_name]

    def _handle_numbers(self, numbers):
        return [int(number) for number in numbers.split(',')]