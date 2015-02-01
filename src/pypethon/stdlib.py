"""
Pypethon builtins.
"""
from pypethon.types import Integer


def build():
    return {
        '__builtins__': {
            # REPL
            'quit': lambda status: exit(status),
            'help': help,

            # Integers
            'Integer': Integer,

            # Integer Operations
            'abs': abs,
            'inc': lambda n: n + 1,
            'dec': lambda n: n - 1,
            'minus': lambda n: lambda i: Integer(n - i),  # 1 | minus | 1
            'plus': lambda n: lambda i: Integer(n + i),  # 1 | plus | 1
            'times': lambda n: lambda i: Integer(n * i),  # 1 | times | 1
        }
    }
