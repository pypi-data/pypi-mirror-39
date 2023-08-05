from eorg import tokens
from collections import namedtuple

TYPE_SINGLE = 0
TYPE_BLOCK = 1
TYPE_ATTRIBUTE = 2
TokenStruct = namedtuple(
    "TokenStruct",
    ["start", "end", "type", "start_pos", "end_pos", "count", "key"],
)
TokenStruct.__new__.__defaults__ = ("", False, TYPE_SINGLE, 2, None, False, "")

ESCAPE = ["\n"]


METADATA = [
    "TITLE",
    "AUTHOR",
    "EMAIL",
    "DESCRIPTION",
    "KEYWORDS",
    "FILETAGS",
    "DATE",
    "HTML_DOCTYPE",
    "SETUPFILE",
]
t_META = r"^[#]\+(" + "|".join(METADATA) + ")\:"
t_BLANK_LINE = "^\s*$"
t_COMMENT_BEGIN = r"^\#\+BEGIN_COMMENT"
t_COMMENT_END = r"^\#\+END_COMMENT"
t_EXAMPLE_BEGIN = r"^\#\+BEGIN_EXAMPLE"
t_EXAMPLE_END = r"^\#\+END_EXAMPLE"
t_SRC_BEGIN = r"^\#\+BEGIN_SRC\s+"
t_SRC_END = r"^\#\+END_SRC"
t_TABLE_START = r"^\s*\|"
t_TABLE_END = r"^(?!\s*\|).*$"
t_RESULTS_START = r"^\#\+RESULTS:"
t_CAPTIONS = r"^\#\+CAPTION:"
t_NAME = r"^\#\+NAME:"
# t_IMG = r"^\[\[(\w|\.|-|_|/)+\]\]$"
t_IMG = r"^\[\["
t_IMG_END = r"\]\]"
t_RESULTS_END = r"^\:..*"
t_END_LABELS = r"^(?!\[|\#).*"
t_BULLET_START = r"^\s*[\+|\-|0-9\.]"
t_BULLET_END = r"^\s*(?![\+|\-|0-9]).*$"

t_HEADER = r"^\*+"
t_META_OTHER = r"^[#]\+[A-Z\_]+\:"

# Start regex, End regex, skip start, skip end, count matches
TOKENS = {
    tokens.META: TokenStruct(start=t_META, end_pos=-1),
    tokens.COMMENT: TokenStruct(
        start=t_COMMENT_BEGIN, end=t_COMMENT_END, type=TYPE_BLOCK, end_pos=-1
    ),
    tokens.EXAMPLE: TokenStruct(
        start=t_EXAMPLE_BEGIN, end=t_EXAMPLE_END, type=TYPE_BLOCK, end_pos=-1
    ),
    tokens.IMAGE: TokenStruct(start=t_IMG, end_pos=-2),
    tokens.CAPTION: TokenStruct(
        start=t_CAPTIONS, type=TYPE_ATTRIBUTE, key="caption"
    ),
    tokens.SOURCE: TokenStruct(start=t_SRC_BEGIN, end=t_SRC_END),
    tokens.TABLE: TokenStruct(
        start=t_TABLE_START, end=t_TABLE_END, start_pos=0
    ),
    tokens.BULLET: TokenStruct(
        start=t_BULLET_START, end=t_BULLET_END, start_pos=0
    ),
    tokens.RESULTS: TokenStruct(start=t_SRC_BEGIN, end=t_SRC_END),
    tokens.HEADER: TokenStruct(start=t_HEADER, start_pos=1, count=True),
    tokens.META_OTHER: TokenStruct(
        start=t_META_OTHER, start_pos=2, end_pos=-1
    ),
}


class Token:
    __slots__ = ["token", "value"]

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"Token(token={self.token}, value={self.value})"


image_extensions = (".jpg", ".jpeg", ".png", ".svg")
