from enum import Enum, Flag, auto
import functools


def print_class_and_method(func):
    """Decorator to print the class name and method signature."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        method_name = func.__name__
        method_signature = f"{method_name}({', '.join(map(str, args))}{', ' if kwargs else ''}{', '.join(f'{k}={v}' for k, v in kwargs.items())})"
        print(f"Calling {class_name}.{method_signature}")
        return func(self, *args, **kwargs)

    return wrapper


class TagRangeConf(Flag):
    '''
    SUB_FILTER - is for the filter substring we're looking for
    TAG_MARK_INDEXES - is for marking the indexes in the beginning of the line, with the filter revers tag conf (color as bg)
    '''
    SUB_FILTER_ONLY = auto()  # Typically would be 1 (2^0)
    SUB_FILTER_TO_END = auto()   # Typically would be 2 (2^1)
    TAG_MARK_INDEXES = auto()  # Typically would be 4 (2^2)


class LMFNotifType(Enum):
    SPECIFIC_FILTER_LINE_PRESSED = "SPECIFIC_FILTER_LINE_PRESSED"


class LMFNotifInfoKey(Enum):
    GLOBAL_LINE_IND = "GLOBAL_LINE_IND"