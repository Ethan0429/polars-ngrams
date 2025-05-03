# polars-ngrams

A Polars extension that provides n-gram functionality for string columns, implemented in Rust for high performance.

## Overview

`polars-ngrams` adds the capability to compute n-grams (sequences of n consecutive characters) from string columns in Polars DataFrames. The implementation is written in Rust using the Polars plugin system for optimal performance.

## Features

- Generate n-grams of any length (n ≥ 1)
- Option to include or exclude whitespace characters
- Native Rust implementation for high performance
- Seamless integration with Polars expressions

## Install

### Requirements

- Python>=3.9
- Rust toolchain
- Maturin

### Building from source

To install `polars-ngrams`, you can clone this repository and build from source. You must have the above requirements to build the wheel. I recommend using `uv` if you don't already have it, but it's not required. You can follow the instructions below to build from source after cloning the repository to your local machine.

> [!IMPORTANT]
> Note that this package lists `polars-lts-cpu>=1.27.1` as its Polars dependency. If you want to use regular Polars (which is most likely), then you can change the dependency accordingly. Same for if you want a different version of Polars.

```bash
# after cloning repo...
cd polars-ngrams
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
maturin develop --release
```

#### Adding to project

If the build is successful, the output will be under `./target/wheels/*.whl`. From here, you can include the plugin in your project by installing the wheel directly to your project's environment. 

```bash
pip install /path/to/wheel # e.g. target/wheels/polars_ngrams-0.1.0-cp39-abi3-linux_x86_64.whl
```


## Usage

```python
import polars as pl
import polars_ngrams as pn

# Create a sample DataFrame
df = pl.DataFrame({"text": ["hello world", "polars is fast"]})

# Generate trigrams (n=3 by default)
df_with_trigrams = df.with_columns(trigrams=pn.ngrams(pl.col("text")))

# Generate custom n-grams (e.g., bigrams)
df_with_bigrams = df.with_columns(bigrams=pn.ngrams(pl.col("text"), n=2))

# Include whitespace in n-grams
df_with_ws = df.with_columns(
    trigrams=pn.ngrams(pl.col("text"), include_whitespace=True)
)
```

### `ngrams`

```python
def ngrams(
    expr: IntoExprColumn, n: int = 3, include_whitespace: bool = False
) -> pl.Expr:
    """
    Compute n-grams for each string value in a column.

    This function breaks down a string into a list of substrings of length n.

    Parameters
    ----------
    expr : IntoExprColumn
        The input string column or expression to compute n-grams from.
    n : int, default=3
        The size of each n-gram (number of characters). Must be at least 1.
    include_whitespace : bool, default=False
        Whether to include whitespace characters in the n-grams.
        If False, all whitespace is removed before n-gramming.

    Returns
    -------
    polars.Expr
        A list column containing the n-grams for each string.

    Examples
    --------
    >>> import polars as pl
    >>> import polars_ngrams as pt
    >>> df = pl.DataFrame({"text": ["hello world", "polars is fast"]})
    >>> df.with_columns(trigrams=pt.ngrams(pl.col("text")))
    shape: (2, 2)
    ┌────────────────┬─────────────────────────┐
    │ text           ┆ trigrams                │
    │ ---            ┆ ---                     │
    │ str            ┆ list[str]               │
    ╞════════════════╪═════════════════════════╡
    │ hello world    ┆ ["hel", "ell", ... "ld"]│
    │ polars is fast ┆ ["pol", "ola", ... "st"]│
    └────────────────┴─────────────────────────┘
    """
```