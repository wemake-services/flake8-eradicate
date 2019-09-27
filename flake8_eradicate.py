# -*- coding: utf-8 -*-

from typing import Any, Iterable, Tuple

import attr
import pkg_resources
from eradicate import filter_commented_out_code
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
    _error_template = 'E800: Found commented out code'

    options: Any  # type: ignore

    def __init__(self, physical_line) -> None:
        """
        Creates new checker instance.

        When performance will be an issue - we can refactor it.
        """
        self._physical_line = physical_line
        self._options = _Options(aggressive=self.options.eradicate_aggressive)

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
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = options

    def __iter__(self) -> Iterable[Tuple[int, str]]:
        """Runs on each step of flake8."""
        if not self._is_equal_source():
            yield (1, self._error_template)

    def _is_equal_source(self) -> bool:
        filtered_source = ''.join(filter_commented_out_code(
            self._physical_line, self._options,
        ))

        return self._physical_line == filtered_source
