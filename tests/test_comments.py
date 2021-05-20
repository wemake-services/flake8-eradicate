# -*- coding: utf-8 -*-

import subprocess
import sys
from collections import namedtuple

from flake8_eradicate import Checker

PY_GTE_36 = sys.version_info >= (3, 6)


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

    assert stdout.count(b'E800') == 6 + int(PY_GTE_36)
    assert b'# property_name = 1' in stdout
    if PY_GTE_36:
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
    assert stdout.count(b'E800') == 12 + int(PY_GTE_36)
    assert b'# property_name = 1' in stdout
    if PY_GTE_36:
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

    assert stdout.count(b'E800') == 6 + int(PY_GTE_36) * 3
    assert b'# property_name = 1' in stdout
    if PY_GTE_36:
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

    assert stdout.count(b'E800') == 3 + int(PY_GTE_36)
    assert b'# property_name = 1' in stdout
    assert b'return' not in stdout
    if PY_GTE_36:
        assert b'# typed_property: int = 10' in stdout


def test__lines_with_commented_out_code_incorrect_fixture_output(absolute_path):
    filename = absolute_path('fixtures', 'incorrect.py')

    OptionsStub = namedtuple('Options', 'eradicate_aggressive eradicate_whitelist eradicate_whitelist_extend')
    Checker.options = OptionsStub(eradicate_aggressive=True, eradicate_whitelist=False, eradicate_whitelist_extend=False)

    checker = Checker(tree=None, filename=filename)
    output = list(checker._lines_with_commented_out_code())
    if PY_GTE_36:
        assert output == [3, 4, 9, 10, 14, 15, 16, 18, 19, 21, 22, 24, 25]
    else:
        assert output == [3, 9, 10, 14, 15, 16, 18, 19, 21, 22, 24, 25]
