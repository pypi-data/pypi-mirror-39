# sentenceslug
a module to generate relatively easy to remember slugs

## Installation
```bash
pip install sentenceslug

```
## Usage

```python
In [1]: from sentenceslug import *

In [2]: sentence_slug()
Out[2]: 'Improve_That_Last_Day'

In [3]: sentence_slug_digits()
Out[3]: 'Start_His_National_Town_377'

In [4]: simple_slug()
Out[4]: 'NationalCar'

In [5]: simple_slug_digits()
Out[5]: 'LegalSystem305'

In [6]: nsa_codeword()
Out[6]: 'POORUSE'

In [7]: make_slug(simple=True, digits=5, delimiter="-")
Out[7]: 'Short-Good-83933'

```

## Changelog

### V1.1 2018-12-05
    - Python 3 Changes

    