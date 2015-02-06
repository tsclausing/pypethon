#
# The (Python bytecode) Code Generator
#
from functools import singledispatch
import ast

from .lexer import Integer
from .lexer import Name
from .parser import Pipe


def generate(tree) -> "bytecode":
    """
    With the help of `translate()` below, generate Python bytecode for the Python's `eval()`.

    https://docs.python.org/3/library/functions.html#compile
    """
    return compile(
        source=ast.fix_missing_locations(
            ast.Interactive(body=[wrap(translate(tree))])
        ),
        filename="<input>",
        mode="single"
    )


@singledispatch
def translate(node):
    """
    Recursively translate a Pypethon Abstract Syntax Tree into a Python Abstract Syntax Tree for Python's `compile()`.
    """
    raise NotImplementedError('translate(%r)' % node)


@translate.register(Integer)
def _(node):
    return ast.Num(
        n=int(node.value),
    )


@translate.register(Name)
def _(node):
    return ast.Name(
        id=node.value,
        ctx=ast.Load(),
    )


@translate.register(Pipe)
def _(node):
    return ast.Call(
        # the right node of a Pipe is a callable name
        func=translate(node.right),
        # the left node of a Pipe is the argument
        args=[translate(node.left)],
        keywords=[], starargs=None, kwargs=None,
    )


# todo: generate PipeEquals
# todo: generate Assignment


@singledispatch
def wrap(node):
    """
    Wrap a Python AST nodes if necessary.
    """
    return node


@wrap.register(ast.Num)
@wrap.register(ast.Name)
@wrap.register(ast.Call)
def _(node):
    return ast.Expr(node)
