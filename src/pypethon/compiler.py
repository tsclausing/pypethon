"""
The compiler composes each phase into a single compile() function to translate the source code into the target language.

Translator: http://en.wikipedia.org/wiki/Translator_(computing)
Compiler: http://en.wikipedia.org/wiki/Compiler
"""
from pypethon.lexer import lex
from pypethon.parser import parse
from pypethon.generator import generate


def compile(source: str):
    """
    >>> exec(compile("42"), {})
    42
    """
    return generate(parse(lex(source)))
