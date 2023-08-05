# The `modulr` Python package

## Installation

```bash
pip install modulr
```

## Description

The `modulr` package has one function, `make_module`,
which saves class and/or function definitions of classes to a module (`.py` file).
The input objects (classes and/or functions) must defined in the current Python session.


### Usage

```python
from modulr import make_module

def func1(x):
    ...

def func2(x):
    ...

make_module([func1, func2], module_name='my_funcs.py')
```