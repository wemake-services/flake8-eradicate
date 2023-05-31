import subprocess
from collections import namedtuple

from flake8_eradicate import Checker


def test_correct_fixture(absolute_path):
    """End-to-End test to check that correct code works."""
    filename = absolute_path('fixtures', 'correct.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--show-source',
            '--select',
            'E8',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 0


def test_incorrect_fixture(absolute_path):
    """End-to-End test to check that incorrect code raises warning."""
    filename = absolute_path('fixtures', 'incorrect.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--show-source',
            '--select',
            'E8',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 7
    assert b'# property_name = 1' in stdout
    assert b'# typed_property: int = 10' in stdout


def test_incorrect_fixture_aggressive(absolute_path):
    """End-to-End test to check that incorrect code raises warning."""
    filename = absolute_path('fixtures', 'incorrect.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--eradicate-aggressive',
            '--isolated',
            '--show-source',
            '--select',
            'E8',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(b'E800') == 13
    assert b'# property_name = 1' in stdout
    assert b'# typed_property: int = 10' in stdout
    assert b'# def function_name():' in stdout
    assert b'# class CommentedClass(object):' in stdout


def test_incorrect_fixture_whitelist(absolute_path):
    """End-to-End test to check that incorrect code raises warning."""
    filename = absolute_path('fixtures', 'incorrect.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--eradicate-whitelist',
            'just#overwrite',
            '--isolated',
            '--show-source',
            '--select',
            'E8',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 9
    assert b'# property_name = 1' in stdout
    assert b'# typed_property: int = 10' in stdout
    assert b'# fmt: on' in stdout
    assert b'# fmt: off' in stdout


def test_incorrect_fixture_whitelist_extend(absolute_path):
    """End-to-End test to check that incorrect code raises warning."""
    filename = absolute_path('fixtures', 'incorrect.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--eradicate-whitelist-extend',
            'return',
            '--isolated',
            '--show-source',
            '--select',
            'E8',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 4
    assert b'# property_name = 1' in stdout
    assert b'return' not in stdout
    assert b'# typed_property: int = 10' in stdout


def test_lines_with_commented_out_code_incorrect_fixture_output(
    absolute_path,
    get_file_lines,
    get_file_tokens,
):
    """Verify central underlying method is returning correct output."""
    filename = absolute_path('fixtures', 'incorrect.py')

    OptionsStub = namedtuple(
        'Options',
        'eradicate_aggressive eradicate_whitelist eradicate_whitelist_extend',
    )
    Checker.options = OptionsStub(
        eradicate_aggressive=True,
        eradicate_whitelist=False,
        eradicate_whitelist_extend=False,
    )

    checker = Checker(
        tree=None,
        lines=get_file_lines(filename),
        file_tokens=get_file_tokens(filename),
    )
    output = list(checker._lines_with_commented_out_code())
    assert output == [3, 4, 9, 10, 14, 15, 16, 18, 19, 21, 22, 24, 25]


def test_lines_with_commented_out_code_file_no_comment(
    absolute_path,
    get_file_tokens,
    get_file_lines,
):
    """Make sure file without comment are ignored."""
    filename = absolute_path('fixtures', 'correct_no_comment.py')

    OptionsStub = namedtuple(
        'Options',
        'eradicate_aggressive eradicate_whitelist eradicate_whitelist_extend',
    )
    Checker.options = OptionsStub(
        eradicate_aggressive=True,
        eradicate_whitelist=False,
        eradicate_whitelist_extend=False,
    )

    checker = Checker(
        tree=None,
        lines=get_file_lines(filename),
        file_tokens=get_file_tokens(filename),
    )
    output = list(checker._lines_with_commented_out_code())
    assert output == []
