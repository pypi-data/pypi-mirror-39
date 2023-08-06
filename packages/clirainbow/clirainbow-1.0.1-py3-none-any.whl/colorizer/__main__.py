from colorizer import Colorizer
from colors import *


def main():
    c = Colorizer()
    c.print(
        'Welcome to <C><O><L><O><R><I><Z><E><R>',
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_BLUE,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_BLUE,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_BLUE
    )


if __name__ == '__main__':
    main()
