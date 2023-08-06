import re
from eorg import tokens
from eorg.tokens import Token
from eorg.const import (
    TYPE_ATTRIBUTE, TOKENS, METADATA, ESCAPE, image_extensions
)
from eorg.helper import parse_img_or_link, emphasis


class Document:
    pos = 0
    doc = []
    index = {}

    def __init__(self):
        self.doc = []
        self.index = {}

    def __getattr__(self, name, default=None):
        idx = self.index.get(name.upper(), [])
        if not idx:
            if default is not None:
                return default

            raise AttributeError(
                f"Attribute of {name} does not exist in document"
            )

        if len(idx) == 1:
            return self.doc[idx[0]].value

        return [self.doc[v].value for v in idx]

    def token(self):
        if self.doc:
            return self.doc[-1].token

        return ""

    def update(self, value):
        self.doc[-1].value += value

    def __iter__(self):
        self.pos = 0
        for item in self.doc:
            yield item

            self.pos += 1

    def previous(self, match):
        if self.pos is 0:
            return None

        if self.doc[self.pos - 1].token != match:
            return None

        return self.doc[self.pos - 1]

    def filter(self, value):
        """Only return types that are of intrest like source blocks"""
        for item in self.doc:
            if item.token == value:
                yield item

    def body(self):
        for item in self.doc:
            if item.token in METADATA:
                continue

            yield item

    def images(self):
        for item in self.__iter__():
            if item.token == tokens.IMAGE:
                yield item
                continue

            if item.token != tokens.LIST and item.token != tokens.RESULTS:
                continue

            if isinstance(item.value, list):
                for token in item.value:
                    if token.token == tokens.IMAGE:
                        yield token

    def __len__(self):
        return len(self.doc)

    def append(self, value):
        self.index.setdefault(value.token, []).append(len(self.doc))
        self.doc.append(value)


def parse_attrs(text):
    attrs = {}
    value_list = text.split(":")
    attrs["language"] = value_list.pop(0).strip()
    for row in value_list:
        values = row.strip().split(" ")
        attrs[values[0]] = values[1:]
    return attrs


def parsebody(text, rx):
    match = re.search(rx, text)
    if match:
        return False, None

    return rx, text + "\n"


def parseline(text, stream):
    attrs = None
    for key, token in TOKENS.items():
        match = re.search(token.start, text)
        if not match:
            continue

        value = text[match.end():]
        if token.type == TYPE_ATTRIBUTE:
            b, t = parseline(next(stream), stream)
            t.attrs = {token.key: value}
            return (token.end, t)

        if token.count is True:
            attrs = {"depth": len(match.group(0))}
        if key == tokens.META:
            return (
                token.end,
                Token(
                    token=match.group(0)[token.start_pos:token.end_pos],
                    value=value,
                ),
            )

        if key == tokens.IMAGE:
            return parse_img_or_link(text[0], iter(text[1:]))

        if key == tokens.SOURCE:
            return token.end, Token(token=key, attrs=parse_attrs(value))

        if key == tokens.TABLE:
            return token.end, Token(token=key, value=text + "\n")

        if key == tokens.BULLET:
            return token.end, Token(token=key, value=text + "\n")

        return token.end, Token(token=key, value=value, attrs=attrs)

    text = text.strip()
    if text == "":
        return False, Token(token=tokens.BLANK, value=text)

    return False, Token(token=tokens.LIST, value=text + " ")


def parse_results(txt):
    char = True
    tokenlist = []

    step = iter(txt)
    while char is not None:
        char = next(step, None)
        char, token = parse_img_or_link(char, step)
        if token:
            tokenlist.append(token)
        if not char:
            continue

        if len(tokenlist) == 0:
            tokenlist.append(Token(tokens.TEXT, char))
            continue

        if tokenlist[-1].token != tokens.TEXT:
            tokenlist.append(Token(tokens.TEXT, char))
            continue

        tokenlist[-1].value += char
    return tokenlist


def parse_text(txt):
    char = True
    tokenlist = []

    def append(value):
        char, token = value
        if token:
            tokenlist.append(token)
        return char

    step = iter(txt)
    while char is not None:
        char = next(step, None)
        char = append(emphasis(char, step, "*", tokens.BOLD))
        char = append(emphasis(char, step, "/", tokens.ITALIC))
        char = append(emphasis(char, step, "_", tokens.UNDERLINED))
        char = append(emphasis(char, step, "=", tokens.VERBATIM))
        char = append(emphasis(char, step, "~", "PRE"))
        char = append(parse_img_or_link(char, step))

        if not char:
            continue

        if len(tokenlist) == 0:
            tokenlist.append(Token(tokens.TEXT, char))
            continue

        if tokenlist[-1].token != tokens.TEXT:
            tokenlist.append(Token(tokens.TEXT, char))
            continue

        tokenlist[-1].value += char
    return tokenlist


def nextline(stream):
    line = next(stream)
    line = line.strip("\n")
    yield line


def parse(stream):
    doc = Document()
    block = False
    for line in stream:
        # for line in nextline(stream):
        line = line.strip("\n")

        if block is not False:
            block, token = parsebody(line, block)
            if block:
                doc.update(token)
            continue

        block, token = parseline(line, stream)
        if token:
            if doc.token() == tokens.LIST and token.token == tokens.LIST:
                doc.update(token.value)
                continue

            doc.append(token)

    for item in doc.filter(tokens.LIST):
        item.value = parse_text(item.value)
    for item in doc.filter(tokens.RESULTS):
        item.value = parse_results(item.value)
    return doc
