class UknownColumn(Exception):
    def __init__(self, used_class):
        self.used_class = used_class
    def __str__(self):
        return 'Chosen field doesnt exists in class %s' % self.used_class


class EmptyArguments(Exception):
    def __str__(self):
        return 'You need to specify at least one field'