# Dict Pretty Printer

[pypi homepage](https://pypi.org/project/dict-pretty-printer/)

## Install

```bash
pip3 install dict-pretty-printer
```

only python3 supported.

## Usage

API Scheme:

- function name: dict_pretty_printer.pretty_print
- input param:

    - data_obj: dict object to be converted to pretty string
    - display_callback: convert and pass partial results to this function in streaming mode

- return:
    - if display_callback is None, return the result as a string
    - if display_callback is not None, return None to avoid OOM.

#### convert dict object to a pretty string

exmample:

```python
from dict_pretty_printer import pretty_print

dict_obj = {'key%s' % i: i/100.0 for i in range(10)}
text = pretty_print(dict_obj)
print(text)
```

output:

```bash
{
    "key0": 0,
    "key1": 0.01,
    "key2": 0.02,
    "key3": 0.03,
    "key4": 0.04,
    "key5": 0.05,
    "key6": 0.06,
    "key7": 0.07,
    "key8": 0.08,
    "key9": 0.09,
}
```

#### convert in streaming mode

example:

```bash
import sys
from dict_pretty_printer import pretty_print

data_obj = {i: tuple(range(i)) for i in range(5)}
pretty_print(data_obj, sys.stdout.write)
```

output:

```bash
{
    0: (
    ),
    1: (
        0,
    ),
    2: (
        0,
        1,
    ),
    3: (
        0,
        1,
        2,
    ),
    4: (
        0,
        1,
        2,
        3,
    ),
}
```

## Enhancement of Existing formantting

for example,

if the expected output of the streaming example above is:

```bash
{
    0: (),
    1: (0,),
    2: (0,1,),
    3: (0,1,2,),
    4: (0,1,2,3,),
}
```

simply
modify 'is_multi_line_mode' function of 'ArrayLikeFormatter' class to return 'False' instead of 'True'

you can further imporve the output by implementing a more complicated logic in 'is_multi_line_mode' function. for example, return False if there are less than 5 elements in the object, and return True if there are more than 5 elements.


## Adding New plugins to support more data types

refer to the existing examples in [formatter](src/dict_pretty_printer/formatter/) module

1. define a subclass of 'BaseFormatter'
2. rewrite 'is_multi_line_mode', 'ele_generator', 'format_element' method if necessary

    the framework will call ele_generator to loop through the object and pass the yield element to format_element one by one.

3. rewrite 'obj_start', 'obj_end' and 'record_ending' to what you want.

    the obj_start and obj_end for list is '[' and ']' by default, the obj_start and obj_end for dict or set is '{' and '}' by default.

    ',' is widely used as the record_ending.


## Cyclic Reference Tolerance

the package is designed for strong Cyclic Reference Tolerance by default and the process speed drops a little.

you can enhance the functionality by adding a switch flag in 'format_obj' method in [formatter/__init__.py][src/dict_pretty_printer/formatter/__init__.py]

and remove the cache from memory at the end of the process to avoid memory leak.


## Setup DEV ENV

```bash
$ pip3 install -r requirements-dev.txt
```

## Packaging Steps


#### Unittest

```bash
make test
```

#### testing before release

```bash
$ make build
$ make install
```

run examples:

```bash
$ python3 examples/console_based.py
```

#### release to pypi

```bash
$ make build
$ make upload
```
