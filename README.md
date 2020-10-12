# flake8-eradicate

[![wemake.services](https://img.shields.io/badge/-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://github.com/sobolevn/flake8-eradicate/workflows/test/badge.svg?branch=master&event=push)](https://github.com/sobolevn/flake8-eradicate/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/sobolevn/flake8-eradicate/branch/master/graph/badge.svg)](https://codecov.io/gh/sobolevn/flake8-eradicate)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-eradicate.svg)](https://pypi.org/project/flake8-eradicate/)
[![PyPI version](https://badge.fury.io/py/flake8-eradicate.svg)](https://pypi.org/project/flake8-eradicate/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

`flake8` plugin to find commented out (or so called "dead") code.

This is quite important for the project in a long run.
Based on [`eradicate`](https://github.com/myint/eradicate) project.


## Installation

```bash
pip install flake8-eradicate
```

It is also a valuable part of [`wemake-python-styleguide`](https://github.com/wemake-services/wemake-python-styleguide).


## Usage

Run your `flake8` checker [as usual](http://flake8.pycqa.org/en/latest/user/invocation.html).
Commented code should raise an error.

Example:

```bash
flake8 your_module.py
```


## Options

- `--eradicate-aggressive` to enable aggressive mode from `eradicate`, can lead to false positives
- `--eradicate-whitelist` to overwrite the whitelist from `eradicate` (`#` separated list)
- `--eradicate-whitelist-extend` to extend the whitelist from `eradicate` (`#` separated list)


## Error codes

| Error code |        Description       |
|:----------:|:------------------------:|
|    E800    | Found commented out code |


## Output example

Here's how output looks like (we are using [`wemake` formatter](https://wemake-python-stylegui.de/en/latest/pages/formatter.html)):

![flake8-eradicate output](https://raw.githubusercontent.com/sobolevn/flake8-eradicate/master/eradicate.png)


## License

MIT.
