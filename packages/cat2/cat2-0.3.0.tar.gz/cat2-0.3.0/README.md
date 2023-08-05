<h1>cat2</h1>

[![PyPI version](https://badge.fury.io/py/cat2.svg)](https://badge.fury.io/py/cat2)

<h2>Print file contents like a boss</h2>

<h3>CLI useage:</h3>

<img src="https://i.ibb.co/28GdxcN/Screen-Shot-2018-12-02-at-00-45-47.png">

<h3>Programmatic usage:</h3>

```python

from cat2 import Cat2, Cat2Exception

# line_from and line_to are optional parameters
cat2_file = Cat2(file_path, line_from, line_to)

# cat2_file is an iterator object
for line in cat2_file:
	print(line)
	print(cat2_file.line_number)
	print(cat2_file.is_bytes)

```
