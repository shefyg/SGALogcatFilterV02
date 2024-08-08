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


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def calculate_luminance(rgb):
    """Calculate the relative luminance of an RGB color."""
    r, g, b = [x / 255.0 for x in rgb]

    # Apply sRGB conversion formula
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # Calculate luminance
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance


def get_contrast_color(hex_color):
    """Return black or white based on the luminance of the background color."""
    rgb = hex_to_rgb(hex_color)
    luminance = calculate_luminance(rgb)

    # Use a threshold of 0.5 for luminance to decide the contrast color
    return 'black' if luminance > 0.5 else 'white'

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
    FILTER_CREATED = "FILTER_CREATED"


class LMFNotifInfoKey(Enum):
    GLOBAL_LINE_IND = "GLOBAL_LINE_IND"