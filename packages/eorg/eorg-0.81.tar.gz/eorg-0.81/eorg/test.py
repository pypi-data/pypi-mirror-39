import os
import pytest
from io import StringIO
from eorg.parser import parse
from eorg.parser import parse_text


text = StringIO(
    """
test
#+BEGIN_EXAMPLE
*I'm bold text*
/I'm italic text/
_I'm underlined text_
#+END_EXAMPLE"""
)

result = parse(text)
print(result.doc)
