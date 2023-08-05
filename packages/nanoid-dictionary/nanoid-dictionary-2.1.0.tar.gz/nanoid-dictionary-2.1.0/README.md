# Nano ID dictionary

Predefined character sets to use with [Nano ID](https://github.com/puyuan/py-nanoid).

## Installation

Install Nano ID dictionary using pip:

```
pip install nanoid-dictionary
```

## Usage

Nano ID dictionary has `alphabet_std` and `human_alphabet` alphabets.

The dictionary also provides many useful sets of strings and functions to use:

* `lookalikes`;
* `lowercase`;
* `numbers`;
* `uppercase`;
* `prevent_misreadings(unsafe_chars, string)`.

`prevent_misreadings(unsafe_chars, string)` accepts a string and removes all the characters that look similar. You can pass your own optional character set if you want.

```python
from nanoid_dictionary import *

alphabet_std # => _-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
human_alphabet # => _-23456789abcdefghijkmnpqrstuvwxyzABCDEFGHIJKMNPQRSTUVWXYZ

lookalikes # => 1l0o
lowercase # => abcdefghijklmnopqrstuvwxyz
numbers # => 0123456789
prevent_misreadings(lookalikes, 'a1l0o') # => a
uppercase # => ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

## Thanks to

* Andrey Sitnik for [Nano ID](https://github.com/ai/nanoid);
* Stanislav Lashmanov for [Nano ID dictionary](https://github.com/CyberAP/nanoid-dictionary).
