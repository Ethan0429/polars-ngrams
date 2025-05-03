import polars as pl
from polars_ngrams import ngrams

pl.Config.set_fmt_str_lengths(100)
pl.Config.set_fmt_table_cell_list_len(100)
pl.Config.set_tbl_width_chars(100)
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_formatting("UTF8_FULL")

df = pl.LazyFrame({"text": ["hello world", "polars is fast"]})

print("creating ngrams")

result_df = df.with_columns(
    trigrams=ngrams(pl.col("text").str.normalize().str.to_lowercase(), n=3),
    ngrams_with_whitespace=ngrams(
        pl.col("text").str.normalize().str.to_lowercase(),
        n=4,
        include_whitespace=True,
    ),
)
print(result_df.collect(engine="streaming"))
