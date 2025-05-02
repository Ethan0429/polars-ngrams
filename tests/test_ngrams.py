import polars as pl
from polars_ngrams import ngrams


def test_standard_trigrams():
    df = pl.DataFrame(
        {
            "text": [
                "hello world",  # standard case
                "",  # empty string
                "hi",  # string shorter than n
                "🌍🌎🌏",  # emoji
                "über café",  # non-ascii
                None,  # null value
            ]
        }
    )

    result = df.with_columns(trigrams=ngrams(pl.col("text")))
    assert result.get_column("trigrams").to_list() == [
        ["hel", "ell", "llo", "low", "owo", "wor", "orl", "rld"],
        None,
        None,
        ["🌍🌎🌏"],
        ["übe", "ber", "erc", "rca", "caf", "afé"],
        None,
    ]


def test_different_n_values():
    df = pl.DataFrame(
        {
            "text": [
                "hello world",  # standard case
                "",  # empty string
                "hi",  # string shorter than n
                "🌍🌎🌏",  # emoji
                "über café",  # non-ascii
                None,  # null value
            ]
        }
    )

    result = df.with_columns(bigrams=ngrams(pl.col("text"), n=2))
    assert result.get_column("bigrams").to_list() == [
        ["he", "el", "ll", "lo", "ow", "wo", "or", "rl", "ld"],
        None,
        ["hi"],
        ["🌍🌎", "🌎🌏"],
        ["üb", "be", "er", "rc", "ca", "af", "fé"],
        None,
    ]


def test_whitespace_inclusion():
    df = pl.DataFrame(
        {
            "text": [
                "hello world",  # standard case
                "",  # empty string
                "hi",  # string shorter than n
                "🌍🌎🌏",  # emoji
                "über café",  # non-ascii
                None,  # null value
            ]
        }
    )

    result = df.with_columns(
        trigrams_ws=ngrams(pl.col("text"), n=3, include_whitespace=True)
    )
    assert result.get_column("trigrams_ws").to_list() == [
        ["hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"],
        None,
        None,
        ["🌍🌎🌏"],
        ["übe", "ber", "er ", "r c", " ca", "caf", "afé"],
        None,
    ]
