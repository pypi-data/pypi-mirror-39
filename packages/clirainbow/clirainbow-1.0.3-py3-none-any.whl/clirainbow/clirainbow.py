from colorama import init
# noinspection PyUnresolvedReferences
from clirainbow.formatter import format_color_string, ColorBracketOpenedButNotClosed, MoreBracketsThanColors, MoreColorsThanBrackets


class Colorizer:

    def __init__(self):
        init(autoreset=True)

    def format(self, string, *colors):
        return format_color_string(string, colors)

    def print(self, string, *colors):
        f_string = self.format(string, *colors)
        print(f_string)
