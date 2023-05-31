import tokenize
from importlib import metadata as importlib_metadata
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
)

from eradicate import Eradicator
from flake8.options.manager import OptionManager

#: This is a name that we use to install this library:
pkg_name = 'flake8-eradicate'

#: We store the version number inside the `pyproject.toml`:
pkg_version = importlib_metadata.version(pkg_name)


class Checker(object):
    """Flake8 plugin to find commented out code."""

    name = pkg_name
    version = pkg_version

    _error_template = 'E800 Found commented out code'

    options: ClassVar[Optional[Dict[str, Any]]] = None  # type: ignore

    def __init__(
        self,
        tree,  # that's the hack we use to trigger this check
        file_tokens: List[tokenize.TokenInfo],
        lines: Sequence[str],
    ) -> None:
        """
        ``flake8`` plugin constructor.

        Arguments:
            file_tokens: all tokens for this file.
            lines: all file lines.

        """
        self._file_tokens = file_tokens
        self._lines = lines
        self._options = {
            'aggressive': self.options.eradicate_aggressive,  # type: ignore
        }

        self._eradicator = Eradicator()

        whitelist = self.options.eradicate_whitelist  # type: ignore
        whitelist_ext = self.options.eradicate_whitelist_extend  # type: ignore

        if whitelist_ext:
            self._eradicator.update_whitelist(
                whitelist_ext.split('#'),
                extend_default=True,
            )
        elif whitelist:
            self._eradicator.update_whitelist(
                whitelist.split('#'),
                extend_default=False,
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
        parser.add_option(
            '--eradicate-whitelist',
            default=False,
            help=(
                'String of "#" separated comment beginnings to whitelist '
                'for eradicate. '
                'Single parts are interpreted as regex. '
                'OVERWRITING the default whitelist: {0}'
            ).format(Eradicator.DEFAULT_WHITELIST),
            action='store',
            parse_from_config=True,
        )
        parser.add_option(
            '--eradicate-whitelist-extend',
            default=False,
            help=(
                'String of "#" separated comment beginnings to whitelist '
                'for eradicate. '
                'Single parts are interpreted as regex. '
                'Overwrites --eradicate-whitelist. '
                'EXTENDING the default whitelist: {0} '
            ).format(Eradicator.DEFAULT_WHITELIST),
            action='store',
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = options

    def run(self) -> Iterator[Tuple[int, int, str, Type['Checker']]]:
        """Runs on each step of flake8."""
        for line_no in self._lines_with_commented_out_code():
            yield line_no, 0, self._error_template, type(self)

    def _lines_with_commented_out_code(self) -> Iterable[int]:
        """
        Yield the physical line number that contain commented out code.

        This test relies on eradicate function to remove commented out code
        from a physical line.

        Physical lines might appear like commented code although they are part
        of a multi-line docstring (e.g. a `# noqa: DAR201` comment to suppress
        flake8 warning about missing returns in the docstring).
        To prevent this false-positive, the tokens of the physical line are
        checked for a comment. The eradicate function is only invokes,
        when the tokens indicate a comment in the physical line.
        """
        comment_in_file = any(
            token.type == tokenize.COMMENT
            for token in self._file_tokens
        )

        if comment_in_file:
            for line_no, line in enumerate(self._lines):
                filtered_source = ''.join(
                    self._eradicator.filter_commented_out_code(
                        line,
                        aggressive=self._options['aggressive'],
                    ),
                )
                if line != filtered_source:
                    yield line_no + 1
