#
# The Parser
#
from functools import singledispatch
from collections import namedtuple

from . import lexer

Pipe = namedtuple("Pipe", "left right")


def parse(tokens) -> "tree":
    """
    Parse the tokens and output a tree which represents the meaning of the token stream for `generate()`.
    """
    # From the linear stream of tokens, we need to create a tree of nodes and edges.
    # Each token type will either become a leaf node (no children) or a
    tree = parse_next(tokens)
    # todo: make sure there are no tokens left over after the tree is parsed!
    return tree


@singledispatch
def parse_next(root: "or tokens", tokens=None) -> "tree":
    """
    Returns a Pypethon Abstract Syntax Tree.
    """
    tokens = tokens or root
    return parse_next(next(tokens), tokens)


@parse_next.register(lexer.Name)
@parse_next.register(lexer.Integer)
def _(root, tokens):
    # "look ahead" for a Pipe, then immediately put the next_token back
    next_token = next(tokens, None)
    if isinstance(next_token, lexer.Pipe):
        return parse_pipe(root, tokens)
    elif next_token:
        tokens.send(next_token)
    return root


def parse_pipe(left, tokens):
    node = Pipe(
        left=left,
        right=parse_next(tokens),
    )
    # todo: enforce grammar for pipes
    return node


# todo: parse assignment (parent containing: name, value)
# todo: parse a pipe to a pipe ... "1|inc|inc|inc"
# todo: parse a pipe-equals (parent containing: name, pipe)
