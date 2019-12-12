# -*- coding: utf-8 -*-

"""
Some docs string in a module.

Some code example here:

>>> x = (1 / 2) * 2
>>> min(x, 0)
0

"""

class Some(object):
    """
    Docstring inside a class.

    Contains some code:

        instance = Some()
        print('Test', instance.other_property)

    """

    #: Doc comment with some code: property_name = 1
    property_name = 1

    # Regular comment with some code: other_property: int = 2
    other_property: int = 2

    def some_method(self) -> None:
        """Comment inside a method."""
        print('not True and not False')

        # Some logics: count(numbers) or print(False)
        print(12 + 23 / 3)


def some_function():
    """
    Test for noqa comments in docstrings.

    This function has a multi-line doc string, but no return value is
    stipulated, while the function defines a return. This would raise DAR201
    flake8 violation. To suppress this raise violation the following noqa
    comment is defined in the docstring.

    # noqa: DAR201

    This noqa comment should not be detected as commented out code. `eradicate`
    itself does not raise this as a violation.

    """
    return "something"
