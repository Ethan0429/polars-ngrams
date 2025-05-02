from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from polars_ngrams._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_ngrams.typing import IntoExprColumn

LIB = Path(__file__).parent


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

    Notes
    -----
    This function uses a native implementation for better performance.
    """
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="ngrams",
        kwargs={
            "n": n,
            "include_whitespace": include_whitespace,
        },
        is_elementwise=True,
    )
