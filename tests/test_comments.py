# -*- coding: utf-8 -*-

import subprocess


def test_correct_fixture(absolute_path):
    """End-to-End test to check that correct code works."""
    filename = absolute_path('fixtures', 'correct.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'E8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 0


def test_incorrect_fixture(absolute_path):
    """End-to-End test to check that incorrect code raises warning."""
    filename = absolute_path('fixtures', 'incorrect.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'E8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'E800') == 1
