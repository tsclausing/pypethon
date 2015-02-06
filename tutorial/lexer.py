#
# The Lexer
#
from collections import namedtuple
import re

Pipe = namedtuple("Pipe", "value")
Name = namedtuple("Name", "value")
Integer = namedtuple("Integer", "value")


def lex(source) -> "tokens":
    """
    Lex the string and output a generator of tokens for `parse()`.
    """
    tokens = tokenize(source)
    # todo: after tokenizing whitespace and comments, drop them from the stream
    tokens = peekable(tokens)
    return tokens


def tokenize(source) -> "tokens":
    keywords = (
        (r"|", Pipe),
        # todo: =
        # todo: |=
    )
    patterns = (
        (r"^[a-zA-Z][a-zA-Z0-9]*", Name),
        (r"^\-?\d+", Integer),
        # todo: whitespace
        # todo: comments
    )
    position = 0
    while source:
        for pattern, constructor in patterns:
            match = re.match(pattern, source)
            if match:
                value = match.group()
                token = constructor(value)
                break
        for keyword, constructor in keywords:
            if source.startswith(keyword):
                token = constructor(keyword)
                break
        # todo: error if there is no token
        increment = len(token.value)
        position += increment
        source = source[increment:]
        yield token


def peekable(tokens):
    """
    Allows the consumer of `tokens` to "look ahead" one token and put it back.
    """
    for token in tokens:
        sent_back = yield token
        if sent_back and sent_back is token:
            yield True
            yield token

