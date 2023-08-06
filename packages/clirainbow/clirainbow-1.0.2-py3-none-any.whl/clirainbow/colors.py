from colorama import Fore, Back, Style


def get(key, obj, default):
    if key is None:
        return default
    else:
        return obj.__dict__.get(key.upper(), default)


def _fore(color):
    default = Fore.RESET
    return get(color, Fore, default)


def _back(color):
    default = Back.RESET
    return get(color, Back, default)


def _style(_style):
    default = Style.NORMAL
    return get(_style, Style, default)


def Color(fore=None, back=None, style=None):
    return _fore(fore) + _back(back) + _style(style)


DEFAULT_COLOR = Color()

colors = 'black red green yellow blue magenta cyan white'.split()

brigthnesses = 'bright dim'.split()


def define_color(name, *args, **kwargs):
    globals()[name] = Color(*args, **kwargs)


def color_name(format_string, *args):
    return format_string.format(*map(str.upper, args))


def define_fore_color(color):
    name = color_name('{}', color)
    define_color(name, color)


def define_back_color(color):
    name = color_name('BACK_{}', color)
    define_color(name, back=color)


def define_fore_on_back_color(fore_color, back_color):
    name = color_name('{}_ON_{}', fore_color, back_color)
    define_color(name, fore_color, back_color)


def define_fore_color_with_brightness(fore_color, brightness):
    name = color_name('{}_{}', brightness, fore_color)
    define_color(name, fore_color, style=brightness)


def define_back_color_with_brightness(back_color, brightness):
    name = color_name('{}_BACK_{}', brightness, back_color)
    define_color(name, back=back_color, style=brightness)


def define_fore_color_on_back_color_with_brightness(fore_color, back_color, brightness):
    name = color_name('{}_{}_ON_{}', brightness, fore_color, back_color)
    define_color(name, fore_color, back_color, brightness)


def populate_color_namespace():
    for fore_color in colors:
        define_fore_color(fore_color)
        for back_color in colors:
            define_back_color(back_color)
            define_fore_on_back_color(fore_color, back_color)
            for brightness in brigthnesses:
                define_fore_color_with_brightness(fore_color, brightness)
                define_back_color_with_brightness(back_color, brightness)
                define_fore_color_on_back_color_with_brightness(
                    fore_color, back_color, brightness)


populate_color_namespace()
