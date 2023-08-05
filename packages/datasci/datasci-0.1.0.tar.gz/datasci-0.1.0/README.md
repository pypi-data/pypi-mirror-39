# `datasci`

[![Latest version on PyPI](https://badge.fury.io/py/datasci.svg)](https://pypi.org/project/datasci/)

Install from PyPI:

```sh
pip install datasci
```

Install in development mode:

```sh
pip install -e .
```


## Features

### Jupyter notebook initialization

```pycon
%run -m datasci.notebook.init
```

### Pandas helpers

```python
import pandas as pd
df = pd.DataFrame(...)

from datasci.pandas import drop_na_columns, drop_uninformative_columns
df_without_na = drop_na_columns(df)
df_informative = drop_uninformative_columns(df)
```


## Testing

```sh
python setup.py test
```


## License

Copyright 2018 Christopher Brown.
[MIT Licensed](https://chbrown.github.io/licenses/MIT/#2018).
