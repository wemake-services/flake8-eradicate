# -*- coding: utf-8 -*-

from io import StringIO
from typing import Generator, Tuple

import attr
import pkg_resources
from eradicate import fix_file

pkg_name = 'flake8-eradicate'

#: We store the version number inside the `pyproject.toml`:
pkg_version: str = pkg_resources.get_distribution(pkg_name).version

STDIN = 'stdin'


@attr.attrs(frozen=True, auto_attribs=True, slots=True)
class _Options(object):
    """Represents ``eradicate`` option object."""

    aggressive: bool = False
    in_place: bool = False


class Checker(object):
    """Flake8 plugin to find commented out code."""

    name = pkg_name
    version = pkg_version
    _error_template = 'E800: Found commented out code:\n{0}'

    def __init__(self, tree, filename: str = STDIN) -> None:
        """
        Creates new checker instance.

        We only need a filename, since ``eradicate`` has its own logic to read
        file contents. And it is unhandy to pass it.
        But, without ``tree`` argument ``flake8`` does not call this plugin.

        When performance will be an issue - we can refactor it.
        """
        self.filename = filename

    def _error(self, traceback: str) -> str:
        return self._error_template.format(traceback)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """
        Runs the checker.

        ``fix_file()`` only mutates the buffer object.
        It is the only way to find out if some error happened.
        """
        if self.filename != STDIN:
            buffer = StringIO()
            fix_file(self.filename, _Options(), buffer)
            traceback = buffer.getvalue()

            if traceback:
                yield 1, 0, self._error(traceback), type(self)
