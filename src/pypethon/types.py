"""
Data Types for Pypethon.
"""


class Integer(int):
    """
    Callable integers!
    """
    def __call__(self, func):
        return func(self)
