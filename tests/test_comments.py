# -*- coding: utf-8 -*-

import subprocess
import sys

PY36 = sys.version_info >= (3, 6)


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

    assert stdout.count(b'E800') == 6 + int(PY36)
    assert b'# property_name = 1' in stdout
    if PY36:
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
    assert stdout.count(b'E800') == 12 + int(PY36)
    assert b'# property_name = 1' in stdout
    if PY36:
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

    assert stdout.count(b'E800') == 6 + int(PY36) * 3
    assert b'# property_name = 1' in stdout
    if PY36:
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

    assert stdout.count(b'E800') == 3 + int(PY36)
    assert b'# property_name = 1' in stdout
    assert b'return' not in stdout
    if PY36:
        assert b'# typed_property: int = 10' in stdout
