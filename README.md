# flake8-eradicate

[![wemake.services](https://img.shields.io/badge/-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.org/sobolevn/flake8-eradicate.svg?branch=master)](https://travis-ci.org/sobolevn/flake8-eradicate)
[![Coverage](https://coveralls.io/repos/github/sobolevn/flake8-eradicate/badge.svg?branch=master)](https://coveralls.io/github/sobolevn/flake8-eradicate?branch=master) [![Python Version](https://img.shields.io/pypi/pyversions/flake8-eradicate.svg)](https://pypi.org/project/flake8-eradicate/)
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


## Error codes

| Error code |        Description       |
|:----------:|:------------------------:|
|    E800    | Found commented out code |


## Output example

### Without aggressive mode

```diff
» flake8 tests/fixtures/incorrect.py
tests/fixtures/incorrect.py:1:1: E800: Found commented out code:
--- before/tests/fixtures/incorrect.py
+++ after/tests/fixtures/incorrect.py
@@ -1,23 +1,16 @@

 class Some(object):
-    # property_name = 1
-    # typed_property: int = 10
     other_property = 2


 # def function_name():
-#     return None


 # class CommentedClass(object):
 #     def __init__(self, prop: int) -> None:
-#         self.property = prop

 #     def __str__(self) -> str:
-#         return self.__class__.__name__

 #    def set_prop(self, prop: int):
-#        self.prop = prop

 #    def get_prop(self):
-#        return self.prop
```

### With aggresive mode

```diff
» flake8 --eradicate-aggressive tests/fixtures/incorrect.py
tests/fixtures/incorrect.py:1:1: E800: Found commented out code:
--- before/tests/fixtures/incorrect.py
+++ after/tests/fixtures/incorrect.py
@@ -1,23 +1,10 @@

 class Some(object):
-    # property_name = 1
-    # typed_property: int = 10
     other_property = 2


-# def function_name():
-#     return None


-# class CommentedClass(object):
-#     def __init__(self, prop: int) -> None:
-#         self.property = prop

-#     def __str__(self) -> str:
-#         return self.__class__.__name__

-#    def set_prop(self, prop: int):
-#        self.prop = prop

-#    def get_prop(self):
-#        return self.prop
```

## License

MIT.
