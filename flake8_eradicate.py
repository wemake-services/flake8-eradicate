# -*- coding: utf-8 -*-

import tokenize
from typing import Iterable, Tuple

import pkg_resources
from eradicate import filter_commented_out_code
from flake8.options.manager import OptionManager

#: This is a name that we use to install this library:
pkg_name = 'flake8-eradicate'

#: We store the version number inside the `pyproject.toml`:
pkg_version = pkg_resources.get_distribution(pkg_name).version

STDIN = 'stdin'


class _Options:
    """Represents ``eradicate`` option object."""

    aggressive = False
    in_place = False

    def __init__(self, aggressive=False) -> None:
        self.aggressive = aggressive


class Checker(object):
    """Flake8 plugin to find commented out code."""

    name = pkg_name
    version = pkg_version
    _error_template = 'E800: Found commented out code'

    options = None

    def __init__(self, physical_line, tokens) -> None:
        """
        Creates new checker instance.

        When performance will be an issue - we can refactor it.
        """
        self._physical_line = physical_line
        self._tokens = tokens
        self._options = _Options(
            aggressive=self.options.eradicate_aggressive,  # type: ignore
        )

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
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = options

    def __iter__(self) -> Iterable[Tuple[int, str]]:
        """Runs on each step of flake8."""
        if self._contains_commented_out_code():
            yield (1, self._error_template)

    def _contains_commented_out_code(self) -> bool:
        """
        Check if the current physical line contains commented out code.

        This test relies on eradicate function to remove commented out code
        from a physical line.

        Physical lines might appear like commented code although they are part
        of a multi-line docstring (e.g. a `# noqa: DAR201` comment to suppress
        flake8 warning about missing returns in the docstring).
        To prevent this false-positive, the tokens of the physical line are
        checked for a comment. The eradicate function is only invokes,
        when the tokens indicate a comment in the physical line.

        """
        comment_in_line = any(
            token_type == tokenize.COMMENT
            for token_type, _, _, _, _ in self._tokens
        )

        if comment_in_line:
            filtered_source = ''.join(filter_commented_out_code(
                self._physical_line,
                self._options,
            ))
            return self._physical_line != filtered_source
        return False
