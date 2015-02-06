"""
The parser accepts a sequence of tokens (from lexer.lex) and returns a RomanNumeral abstract syntax tree.

Parsing: http://en.wikipedia.org/wiki/Parsing
"""
from collections import namedtuple
from functools import singledispatch

from pypethon import lexer

Assignment = namedtuple("Assignment", "name, expression")
Function = namedtuple("Function", "name, expression")
Pipe = namedtuple("Pipe", "left, right")


def parse(tokens):
    """
    >>> from pypethon.lexer import lex

    >>> parse(lex("= ans -42 | abs"))
    Assignment(name=Name(pos=2, value='ans'), expression=Pipe(left=Integer(pos=6, value='-42'), right=Name(pos=12, value='abs')))

    >>> parse(lex("|= correct abs | inc"))
    Function(name=Name(pos=3, value='correct'), expression=Pipe(left=Name(pos=11, value='abs'), right=Name(pos=17, value='inc')))
    """
    tree = ast(tokens)
    # todo: enforce anything at the tree level?
    enforce_no_remaining_tokens(tokens)
    return tree


#
# AST Building
#


@singledispatch
def ast(root: "or tokens", tokens=None):
    """
    Returns a Pypethon Abstract Syntax Tree.
    """
    tokens = tokens or root
    return ast(next(tokens), tokens)


@ast.register(lexer.Name)
@ast.register(lexer.Integer)
def _(root, tokens):
    # "look ahead" for a Pipe, then immediately put the next_token back
    next_token = next(tokens, None)
    if isinstance(next_token, lexer.Pipe):
        return parse_pipe(root, tokens)
    elif next_token:
        tokens.send(next_token)
    return root


@ast.register(lexer.Equal)
def _(root, tokens):
    node = Assignment(
        name=ast(tokens),
        expression=ast(tokens),
    )
    # TODO: enforce grammar
    return node


@ast.register(lexer.PipeEqual)
def _(root, tokens):
    node = Function(
        name=ast(tokens),
        expression=ast(tokens),
    )
    # TODO: enforce grammar
    return node


def parse_pipe(left, tokens):
    node = Pipe(
        left=left,
        right=ast(tokens),
    )
    # TODO: enforce grammar
    return node


#
# Parser Rules
#

def enforce_no_remaining_tokens(tokens):
    unexpected_token = next(tokens, False)
    if unexpected_token:
        raise SyntaxError("Unexpected %s at position %d" % (unexpected_token.value, unexpected_token.pos))
