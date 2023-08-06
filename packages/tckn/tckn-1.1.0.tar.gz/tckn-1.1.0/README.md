# tckn
[![PyPI version](https://badge.fury.io/py/tckn.svg)](https://badge.fury.io/py/tckn)
 
*tckn* is a library for generating and validating Republic of Turkey identity numbers.
It exposes two functions: `generate` and `validate`.

## Installation
```bash 
poetry add tckn
```
or
```bash
pip install tckn
```

## Usage
```python3
>>> import tckn
>>> tckn.generate()
'21862110720'
>>> tckn.validate('43650391326')
True
```
