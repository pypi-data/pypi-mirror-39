# DataCI

data oriented unittest framework


## Install

```bash
$ pip3 install dataci
```


## Usage


## Setup DEV ENV

```bash
$ pip3 install -r requirements-dev.txt
```

or simply

```bash
$ make dev-setup
```

## Packaging Steps


#### Unittest

```bash
$ make test
```

#### Testing before release

```bash
$ make build
$ make install
```

#### Run examples

```bash
$ cd examples
$ PYTHONPATH=. pytest tests.py
```

#### Release to pypi

```bash
$ make build
$ make upload
```
