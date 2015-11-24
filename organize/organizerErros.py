class Error(Exception):
    pass

class CommandLineArgumentException(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class UnknownArgumentExeption(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BalanceArgsException(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NoValueInListException(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongNameFormatException(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)