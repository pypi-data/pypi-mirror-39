from eorg import tokens
from eorg.tokens import Token
from eorg.const import ESCAPE, image_extensions


def emphasis(char, step, end, tag):
    if not char or char != end:
        return char, None

    char = next(step, None)
    r = ""
    while char and char not in [end] + ESCAPE:
        r += char
        char = next(step, None)
    return False, Token(tag, r)


def parse_img_or_link(char, step):
    if char != "[":
        return char, None

    char = next(step, None)

    if char != "[":
        return char, None

    char = next(step, None)

    path = ""
    while char not in ["]"] + ESCAPE:
        path += char
        char = next(step, None)
    char = next(step, None)
    alt = ""
    if char == "[":
        char = next(step, None)
        while char not in ["]"] + ESCAPE:
            alt += char
            char = next(step, None)
        char = next(step, None)

    if path.startswith('file:'):
        path = path[5:]
    if path.endswith(image_extensions):
        return False, Token(tokens.IMAGE, [path, alt])

    return False, Token(tokens.LINK, [path, alt])
