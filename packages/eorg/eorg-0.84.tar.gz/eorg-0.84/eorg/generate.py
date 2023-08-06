import re
from html import escape
from io import StringIO
from eorg import tokens
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def src(doc, code, cls="", root=True):
    try:
        lexer = get_lexer_by_name(code.attrs.get("language", "shell"))
    except ClassNotFound as e:
        lexer = get_lexer_by_name("text")
    return highlight(code.value, lexer, HtmlFormatter(linenos=True))


def img(doc, item, cls="", root=True):
    text = ""
    if item.attrs:
        caption = item.attrs.get('caption')
        if caption:
            text = f'<p class="center-align">{caption}</p>'
    return f'<img{cls} style="margin:auto;" src="{item.value[0]}" alt="{item.value[1]}" />{text}'


def link(doc, item, cls="", root=True):
    return f'<a {cls} style="margin:auto;" href="{item.value[0]}">{item.value[1]}</a>'


def parse_list_html(doc, token, cls="", root=True):
    response = StringIO()
    response.write(f"<p{cls}>")

    for item in token.value:
        response.write(handle_token(doc, item, False))
    response.write(f"</p>")
    response.seek(0)
    return response.read()


def parse_bullets_html(doc, token, cls="", root=True):
    response = StringIO()
    bullet = 'ul'
    if token.value[0].isdigit():
        bullet = 'ol'

    response.write(f"<{bullet}{cls}>")
    for row in token.value.split("\n"):
        if row:
            text = ''
            if row[0] in ['-', '+']:
                text = re.sub(r'^\s*[-|+]+\s*', '', row, 1)

            if row[0].isdigit():
                text = re.sub(r'^\s*[0-9]+\.*\s*', '', row, 1)

            response.write(f"<li class=\"collection-item\">{text}</li>")

    response.write(f"</{bullet}>")
    response.seek(0)
    return response.read()


def parse_text_html(doc, token, cls="", root=True):
    return f"{token.value}"


def results(doc, results, cls="", root=True):
    result = ""
    for token in results.value:
        if token.token is tokens.IMAGE:
            result += img(doc, token, cls, root=root)
            return result
        result += "<blockquote%s>%s</blockquote>\n" % (
            cls,
            escape(token.value).replace("\n", "<br />"),
        )
    return result


def blockquote(doc, token, cls="", root=True):
    return "<blockquote%s>%s</blockquote>\n" % (
        cls,
        escape(token.value).replace("\n", "<br />"),
    )


def header(doc, item, cls="", root=True):
    depth = 1
    if item.attrs:
        depth = item.attrs.get("depth", depth)
    depth += 1
    return "<h%s%s>%s</h%s>\n" % (depth, cls, item.value, depth)


def table(doc, item, cls="", root=True):
    tbl = "<tbody>"
    tblhead = ""
    newrow = None
    for row in item.value.split("\n"):
        if newrow:
            if row.startswith("|-"):
                tblhead += (
                    "<thead><th>"
                    + "</th><th>".join(newrow)
                    + "</th></thead>\n"
                )
            else:
                tbl += f"<tr><td>" + "</td><td>".join(newrow) + "</td></tr>\n"
        newrow = filter(None, row.split("|"))
        if row.startswith("|-"):
            newrow = None

    tbl += "</tbody>"
    return "<table%s>%s%s</table>\n" % (cls, tblhead, tbl)


builddoc = {
    tokens.HEADER: (header, None),
    tokens.IMAGE: (img, "materialboxed center-align responsive-img"),
    tokens.LINK: (link, None),
    tokens.BOLD: ("b", None),
    tokens.UNDERLINED: ("u", None),
    tokens.ITALIC: ("i", None),
    tokens.VERBATIM: ("code", None),
    tokens.LIST: (parse_list_html, "flow-text"),
    tokens.TEXT: (parse_text_html, "flow-text"),
    tokens.BULLET: (parse_bullets_html, "browser-default"),
    tokens.SOURCE: (src, None),
    tokens.EXAMPLE: (blockquote, None),
    tokens.RESULTS: (results, None),
    tokens.TABLE: (table, "responsive-table striped"),
}


def handle_token(doc, item, root=False):
    response = StringIO()
    match = builddoc.get(item.token)

    if not match:
        return ""

    tag, cls = match
    if cls:
        cls = f' class="{cls}"'
    else:
        cls = ""
    if callable(tag):
        return tag(doc, item, cls, root=root)

    else:
        return "<%s%s>%s</%s>\n" % (tag, cls, item.value, tag)


def html(doc):
    response = StringIO()
    for item in doc:
        response.write(handle_token(doc, item, True))
    response.seek(0)
    return response
