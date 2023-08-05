import doctest
from typing import Callable, Iterable


def add_docstring(func: Callable, desc: str, example_args: Iterable) -> None:
    """

    Examples:
        >>> def my_add(*args): return sum(args)
        >>> add_docstring(my_add, 'sum any numbers', [2, 3])
        >>> my_add.__doc__
        'sum any numbers\\nExamples:\\n    >>> my_add([2, 3])\\n    5\\n'
    """
    docstring = (f"""{desc}
Examples:
    >>> {func.__name__ + '(' + str(example_args) + ')'}
    {eval('func(*example_args)')}
""")

    func.__doc__ = docstring


if __name__ == '__main__':
    doctest.testmod(verbose=True)
