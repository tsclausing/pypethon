"""
The Pypethon Tutorial!

See the README.md file for instructions.
"""
from .parser import parse
from .lexer import lex
from .generator import generate


#
# The Pypethon REPL!
#

def repl():
    """
    Runs a Pypethon Read-Eval-Print-Loop.
    """
    while True:
        # todo: implement a way to exit gracefully
        # todo: display error messages and keep going instead of blowing up
        print(evaluate(input("tutorial> ")))


def evaluate(source):
    """
    The "Eval" step in the REPL. Evaluation happens in two phases:

    * Compile: lex, parse, generate bytecode
    * Interpret: execute bytecode with Python's builtin `eval()`
    """
    return eval(
        generate(parse(lex(source))),
        # todo: write the standard library. currently, it only includes `inc`.
        {'__builtins__': {
            'inc': lambda n: n + 1,
            # todo: implement `dec` to decrement an integer
        }}
        # todo: add callable Integer data type (also requires change in generator.py)
        # then ...
        #   todo: implement `plus`
        #   todo: implement `minus`
        #   todo: implement `times`
    )


#
# This module may be run as a Python 3 script to start a REPL.
#

if __name__ == "__main__":
    repl()
