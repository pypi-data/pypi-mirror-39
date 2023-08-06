BLANK = 0
META = 1
META_OTHER = 2
HEADER = 5
BOLD = 10
ITALIC = 11
UNDERLINED = 12
VERBATIM = 13
LIST = 20
TEXT = 21
IMAGE = 22
LINK = 23
CAPTION = 24
BULLET = 25
SOURCE = 50
EXAMPLE = 51
RESULTS = 52
COMMENT = 53
TABLE = 54


class Token:
    __slots__ = ["token", "value", "attrs"]

    def __init__(self, token, value="", attrs=None):
        self.token = token
        self.value = value
        self.attrs = attrs

    def __repr__(self):
        return f'Token(token="{self.token}", value="{self.value}", attrs="{self.attrs}")'
