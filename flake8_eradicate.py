# -*- coding: utf-8 -*-

from io import StringIO
from typing import Any, Generator, Tuple

import attr
import pkg_resources
from eradicate import fix_file
from flake8.options.manager import OptionManager

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

    options: Any  # type: ignore

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

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """
        ``flake8`` api method to register new plugin options.

        See :class:`.Configuration` docs for detailed options reference.

        Arguments:
            parser: ``flake8`` option parser instance.

        """
        parser.add_option(
            '--eradicate-aggressive',
            default=False,
            help=(
                'Enables aggressive mode for eradicate; '
                'this may result in false positives'
            ),
            action='store_true',
            type=None,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = options

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """
        Runs the checker.

        ``fix_file()`` only mutates the buffer object.
        It is the only way to find out if some error happened.
        """
        if self.filename != STDIN:
            buffer = StringIO()
            options = _Options(aggressive=self.options.eradicate_aggressive)
            fix_file(self.filename, options, buffer)
            traceback = buffer.getvalue()

            if traceback:
                yield 1, 0, self._error(traceback), type(self)
