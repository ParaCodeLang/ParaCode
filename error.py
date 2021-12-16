from enum import Enum, auto
from util import LogColor

class InterpreterError(Exception):
    def __init__(self, m, node=None, type=None, message=None, cont=False, name=None, classnames=None, object=None):
        super().__init__(m)
        self.node = node
        self.type = type
        self.message = message
        self.cont = cont
        self.name = name
        self.classnames = classnames
        self.object = object

class ErrorType(Enum):
    Exception = auto()
    Syntax = auto()
    DoesNotExist = auto()
    TypeError = auto()
    MultipleDefinition = auto()
    ArgumentError = auto()
    MacroExpansionError = auto()

class Error():
    def __init__(self, type, location, message, filename, name="Exception"):
        self.type = type
        self.filename = filename
        self.message = message
        self.location = location
        self.name = name

    @property
    def location_filename(self):
        if self.filename is None:
            return '<none>'

        return self.filename

    @property
    def location_row(self):
        if self.location is None:
            return 0

        return self.location[1]

    @property
    def location_col(self):
        if self.location is None:
            return 0

        return self.location[0]

    def __repr__(self):
        nstr = f"{self.location_filename}:{self.location_row}:{self.location_col}: {LogColor.Error}{self.name}:{LogColor.Default}"
        # nstr = f"{self.location_filename}:{self.location_row}:{self.location_col}: {LogColor.Error}{self.type.name} error:{LogColor.Default}"
        # if self.type == ErrorType.Exception:
        #     nstr = f"{self.location_filename}:{self.location_row}:{self.location_col}: {LogColor.Error}{self.name}:{LogColor.Default}"
        return f"{LogColor.Bold}{nstr}{LogColor.Default} {self.message}"
    __str__ = __repr__
        
class ErrorList():
    def __init__(self):
        self.errors = []

    def clear_errors(self):
        self.errors = []
    
    def push_error(self, error):
        self.errors.append(error)
        
    def print_errors(self):
        for error in self.errors:
            print(error)
        
    def get_errors(self):
        return self.errors
