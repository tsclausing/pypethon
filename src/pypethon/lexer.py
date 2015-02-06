"""
The lexer accepts a string of characters (source code) and returns a sequence of tokens.

Lexical Analysis: http://en.wikipedia.org/wiki/Lexical_analysis
"""
from collections import namedtuple
import re

from pypethon.exceptions import SyntaxException

Pipe = namedtuple("Pipe", "pos value")
Equal = namedtuple("Equal", "pos value")
PipeEqual = namedtuple("PipeEqual", "pos value")

Integer = namedtuple("Integer", "pos value")
Name = namedtuple("Name", "pos value")
Whitespace = namedtuple("Whitespace", "pos value")
Comment = namedtuple("Comment", "pos value")

KEYWORDS = (
    (r"|=", PipeEqual),
    (r"|", Pipe),
    (r"=", Equal),
)
PATTERNS = (
    (r"^\s", Whitespace),
    (r"^\-?\d+", Integer),
    (r"^[a-zA-Z][a-zA-Z0-9]*", Name),
    (r"^\#.*", Comment),
)


def lex(source) -> [namedtuple]:
    """
    >>> list(lex("= ans -42 | abs"))
    [Equal(pos=0, value='='), Name(pos=2, value='ans'), Integer(pos=6, value='-42'), Pipe(pos=10, value='|'), Name(pos=12, value='abs')]
    """
    tokens = tokenize(source)
    tokens = drop(tokens, Whitespace, Comment)
    tokens = peekable(tokens)
    return tokens


def tokenize(source):
    position = 0
    while source:
        token, source = pop_keyword_token(source, position) or pop_pattern_token(source, position)
        if token:
            yield token
            position += len(token.value)
        else:
            raise SyntaxException("Unknown character '%s' at index %d" % (source[0], position))


def pop_keyword_token(string, position):
    for keyword, constructor in KEYWORDS:
        if string.startswith(keyword):
            return constructor(position, keyword), string[len(keyword):]


def pop_pattern_token(string, position):
    for pattern, constructor in PATTERNS:
        match = re.match(pattern, string)
        if match:
            value = match.group()
            return constructor(position, value), string[len(value):]


def drop(tokens, *types):
    for token in tokens:
        if not isinstance(token, types):
            yield token


def peekable(tokens):
    for token in tokens:
        sent_back = yield token
        if sent_back and sent_back is token:
            yield True
            yield token
