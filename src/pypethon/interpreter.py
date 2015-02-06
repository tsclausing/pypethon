"""
The interpreter returns the evaluated result of compiling source code.

Interpreter: http://en.wikipedia.org/wiki/Interpreter_(computing)
"""
from pypethon.compiler import compile


def evaluate(source: str, namespace: dict):
    """
    >>> from pypethon.stdlib import build
    >>> evaluate("42", build())
    42
    """
    return exec(compile(source), namespace) if source else None
