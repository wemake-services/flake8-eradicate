import os
import tokenize
from typing import List

import pytest


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)
    return factory


@pytest.fixture(scope='session')
def get_file_tokens():
    """Fixture to generate tokens for a given filename."""
    def factory(filename: str) -> List[tokenize.TokenInfo]:
        with open(filename) as file_obj:
            return list(tokenize.generate_tokens(file_obj.readline))
    return factory


@pytest.fixture(scope='session')
def get_file_lines():
    """Fixture to read file into a sequence of lines for a given filename."""
    def factory(filename: str) -> List[str]:
        with open(filename) as file_obj:
            return file_obj.readlines()
    return factory
