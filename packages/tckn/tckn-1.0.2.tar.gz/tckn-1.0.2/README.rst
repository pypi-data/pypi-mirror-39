tckn
====

*tckn* is a library for generating and validating Republic of Turkey identity numbers.
It exposes two functions: `generate` and `validate`.

Usage
-----
>>> import tckn
>>> tckn.generate()
'21862110720'
>>> tckn.validate('43650391326')
True

