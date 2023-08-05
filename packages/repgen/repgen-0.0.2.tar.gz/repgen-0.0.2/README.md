---
title:  repgen: A Simple Python Report Generation Library
author: Libor Wagner <libor.wagner@cvut.cz>
date:   2018-11-22
---

# repgen: A Simple Python Report Generation Library

## Installation

Requirements:

  - [jinja2](http://jinja.pocoo.org)

Optional, needed to run the example:

  - [numpy](http://www.numpy.org)
  - [tabulate](https://pypi.org/project/tabulate/)
  - [matplotlib](https://matplotlib.org)

Unstall using pip:

```shell
$ pip install https://github.com/liborw/repgen.git
```

## Usage

 - The following example will produce the ultimate answer in about 7.5 milion years, but also shows the simples usage of this library.

```python

import time
from repgen import generate

"""!
What is the answer to life the universe and everything? {{ the_answer }}
"""

time.sleep(7.5e+6*3.154e+7)

data = dict()
data['the_answer'] = 7*6

print(generate(data=data))


```

  - For more examples see the [examples](examples/) directory.

## Similar tools

 - [pweawe]()
