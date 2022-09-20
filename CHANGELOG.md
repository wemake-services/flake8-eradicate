# Version history

We follow Semantic Versions since the `0.1.0` release.


## 1.4.0

### Features

- Drops `python3.6` support
- Switches from `pkg_resources` to `importlib_metadata`

### Misc

- Uses `poetry@1.2`


## 1.3.0

### Features

- Adds `flake8@5.0` support


## 1.2.1

### Bugfixes

- Adds `setuptools` in the dependencies


## 1.2.0

### Features

- Adds `flake8@4.0.0` support
- Adds `python3.10` support


## 1.1.0

### Features

- Improves performance on long files #210


## 1.0.0

### Features

- Adds `python3.9` support
- Now using new `eradicate` API
- Adds `--eradicate-whitelist` and `--eradicate-whitelist-append` options

### Misc

- Moves to Github Actions


## 0.4.0

### Features

- Adds `python3.5` support


## 0.3.0

### Features

- Adds `python3.8` support


## 0.2.4

### Bugfixes

- Fixes that some lines inside the docstrings were marked as commented out code


## 0.2.3

### Bugfixes

- Fixed `argparse` bug, see [#76](https://github.com/sobolevn/flake8-eradicate/issues/76)


## 0.2.2

### Bugfixes

- Now `eradicate-aggressive` is parsed from config


## 0.2.1

### Features

- Updates to `flake8 >= 3.7`
- Updates `attrs < 20`
- Fixes plugin to work with `stdin`

### Misc

- Changes how we use `flake8`, moves from `pytest-flake8` to native CLI


## Version 0.2.0

### Features

- Adds `aggressive` configuration option
- Upgrades `eradicate` to `1.0`


## Version 0.1.2

### Misc

- Improves readme
- Improves tests


## Version 0.1.1

### Bugfixes

- Relies on `attrs` explicitly, see [#2](https://github.com/sobolevn/flake8-eradicate/issues/2)

### Misc

- Improves readme
- Improves tests


## Version 0.1.0

- Initial release
