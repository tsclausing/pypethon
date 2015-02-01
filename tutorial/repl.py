"""
The Pypethon Tutorial!

See the README.md file for instructions.
"""
from functools import singledispatch
from collections import namedtuple
import ast


#
# The Pypethon REPL!
#

def repl():
    """
    Runs a Pypethon Read-Eval-Print-Loop.
    """
    while True:
        print(evaluate(input("tutorial> ")))


def evaluate(source):
    """
    The "Eval" step in the REPL. Evaluation happens in two phases:

    * Compile: lex, parse, generate bytecode
    * Interpret: execute bytecode with Python's builtin `eval()`
    """
    return eval(generate(parse(lex(source))))


#
# The Pypethon Compiler!
#


def lex(string) -> "tokens":
    """
    Lex the string and output a generator of tokens for `parse()`.
    """
    pass


def parse(tokens) -> "tree":
    """
    Parse the tokens and output a tree which represents the meaning of the token stream for `generate()`.
    """
    pass


def generate(tree) -> "bytecode":
    """
    With the help of `translate()` below, generate Python bytecode for the Python's `eval()`.

    https://docs.python.org/3/library/functions.html#compile
    """
    return compile(
        source=ast.fix_missing_locations(ast.Expression(body=translate(tree))),
        filename="<input>",
        mode="eval"
    )


@singledispatch
def translate(node):
    """
    Recursively translate a Pypethon Abstract Syntax Tree into a Python Abstract Syntax Tree for Python's `compile()`.
    """
    raise NotImplementedError('translate(%r)' % node)


#
# This module may be run as a Python 3 script to start a REPL.
#

if __name__ == "__main__":
    repl()
