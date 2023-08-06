from colors import DEFAULT_COLOR

COLOR_START, COLOR_END, CHAR = range(3)

OPENING_BRACKET = '<'
CLOSING_BRACKET = '>'


class ColorBracketOpenedButNotClosed(Exception):

    def __init__(self, position):
        super().__init__(
            f'Color bracket opened at position {position} was never closed')


def tokenize(string):
    i = 0
    tokens = []
    in_color = False
    while i < len(string):
        if string[i] == OPENING_BRACKET:
            if string[i:i + 2] == OPENING_BRACKET * 2:
                tokens.append((CHAR, OPENING_BRACKET))
                i += 1
            else:
                tokens.append((COLOR_START, OPENING_BRACKET))
                in_color = True
        elif string[i] == CLOSING_BRACKET:
            if not in_color or string[i:i + 2] == CLOSING_BRACKET * 2:
                tokens.append((CHAR, CLOSING_BRACKET))
                i += 1
            else:
                tokens.append((COLOR_END, CLOSING_BRACKET))
                in_color = False
        else:
            tokens.append((CHAR, string[i]))
        i += 1
    validate(tokens)
    return tokens


def validate(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i][0] == COLOR_START:
            stack.append((COLOR_START, i))
        if tokens[i][0] == COLOR_END:
            stack.pop()
        i += 1
    if stack:
        raise ColorBracketOpenedButNotClosed(stack[-1][1])
    return stack


def format_color_string(string, colors):
    tokens = tokenize(string)
    i = 0
    color_index = 0
    result = ''
    while i < len(tokens):
        token_type, token_value = tokens[i]
        if token_type == COLOR_START:
            i, parsed = parse_color(i + 1, tokens)
            parsed = colors[color_index] + parsed
            color_index += 1
        else:
            i, parsed = parse_normal(i, tokens)
            parsed = DEFAULT_COLOR + parsed
        result += parsed
    return result


def parse_color(i, tokens):
    parsed = ''
    while i < len(tokens) and tokens[i][0] != COLOR_END:
        parsed += tokens[i][1]
        i += 1
    return i + 1, parsed


def parse_normal(i, tokens):
    parsed = ''
    while i < len(tokens) and tokens[i][0] != COLOR_START:
        parsed += tokens[i][1]
        i += 1
    return i, parsed
