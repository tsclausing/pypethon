"""
Translates a parsed Pypethon AST into a Python executable code object.

Code Generation: http://en.wikipedia.org/wiki/Code_generation_(compiler)
"""
import ast
from functools import singledispatch

from pypethon import lexer
from pypethon import parser


def generate(tree):
    """
    >>> from pypethon.lexer import lex
    >>> from pypethon.parser import parse
    >>> from pypethon.stdlib import build
    >>> state = build()
    >>> exec(generate(parse(lex("|= plus5 inc | inc | inc | inc | inc"))), state)
    >>> exec(generate(parse(lex("= ans 33 | inc | inc | inc | inc | plus5"))), state)
    >>> exec(generate(parse(lex("ans"))), state)
    42
    """
    return compile(
        source=ast.fix_missing_locations(
            ast.Interactive(body=[wrap(translate(tree))])
        ),
        filename="Pypethon",
        mode="single",
    )


@singledispatch
def translate(node):
    """
    Recursively transform a Pypethon AST node into a Python AST node.
    """
    raise NotImplementedError('Python AST Generation Error: translate(%r)' % node)


@translate.register(parser.Assignment)
def _(node):
    return ast.Assign(
        targets=[translate(node.name, assign=True)],
        value=translate(node.expression),
    )


@translate.register(parser.Function)
def _(node):
    return ast.FunctionDef(
        name=node.name.value,
        args=ast.arguments(
            args=[ast.arg(arg='input')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[ast.Return(
            # inject the implied 'input' pipe and translate
            value=translate(parser.Pipe(
                left=lexer.Name(0, 'input'),
                right=node.expression,
            )))
        ],
        decorator_list=[],
        returns=None,
    )


@translate.register(parser.Pipe)
def _(node, args=None):
    if isinstance(node.right, parser.Pipe):
        # in the pipe!
        return translate(
            node.right,
            args=ast.Call(
                func=translate(node.right.left),
                args=[args or translate(node.left)],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        )
    else:
        # end of the pipe!
        return ast.Call(
            func=translate(node.right),
            args=[args or translate(node.left)],
            keywords=[],
            starargs=None,
            kwargs=None,
        )


@translate.register(lexer.Name)
def _(node, assign=False):
    return ast.Name(
        lineno=1,
        col_offset=node.pos,
        id=node.value,
        ctx=ast.Store() if assign else ast.Load(),
    )


@translate.register(lexer.Integer)
def _(node):
    return ast.Num(
        lineno=1,
        col_offset=node.pos,
        n=int(node.value)
    )


@singledispatch
def wrap(node):
    """
    Wrap a Python AST node in an Expr or Stmt, or nothing.
    """
    return node


@wrap.register(ast.Num)
@wrap.register(ast.Name)
@wrap.register(ast.Call)
def _(node):
    return ast.Expr(node)
