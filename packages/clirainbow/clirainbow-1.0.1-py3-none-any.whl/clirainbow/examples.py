from clirainbow import Colorizer, ColorBracketOpenedButNotClosed
from colors import *


if __name__ == '__main__':
    c = Colorizer()

    c.print(
        '<hello> <world>',
        BRIGHT_RED_ON_MAGENTA,
        DIM_GREEN_ON_WHITE
    )

    c.print(
        '< >< >< >< >< >< >< >< >',
        BACK_RED,
        BACK_GREEN,
        BACK_BLUE,
        BACK_YELLOW,
        BACK_CYAN,
        BACK_MAGENTA,
        BACK_BLACK,
        BACK_WHITE
    )

    c.print(
        '<➜ > <colorizer> <git:(><master><)> <✗>',
        GREEN,
        CYAN,
        BLUE,
        RED,
        BLUE,
        YELLOW
    )

    try:
        c.print('<asdg')
    except ColorBracketOpenedButNotClosed as e:
        print(f'ERROR: {e}')
