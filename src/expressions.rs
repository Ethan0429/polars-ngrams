#![allow(clippy::unused_unit)]

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

#[derive(Deserialize)]
pub struct NgramKwargs {
    n: usize,
    include_whitespace: bool,
}

fn list_string_dtype(_: &[Field]) -> PolarsResult<Field> {
    Ok(Field::new(
        PlSmallStr::from_static("ngrams"),
        DataType::List(Box::new(DataType::String)),
    ))
}

#[polars_expr(output_type_func=list_string_dtype)]
fn ngrams(inputs: &[Series], kwargs: NgramKwargs) -> PolarsResult<Series> {
    let s = &inputs[0];
    let ca = s.str()?;

    let n = kwargs.n;
    if n < 1 {
        polars_bail!(ComputeError: "n must be greater than 0");
    }
    let include_whitespace = kwargs.include_whitespace;

    let out = ca
        .into_iter()
        .map(|opt_str| match opt_str {
            None => None,
            Some(s) => {
                if s.len() < n {
                    return None;
                }
                let chars: Vec<char> = if !include_whitespace {
                    s.chars().filter(|c| !c.is_whitespace()).collect()
                } else {
                    s.chars().collect()
                };

                if chars.len() < n {
                    return None;
                }

                let ngrams: Vec<String> = chars
                    .windows(n)
                    .map(|window| window.iter().collect())
                    .collect();

                Some(Series::new("ngram".into(), ngrams))
            },
        })
        .collect::<ListChunked>();

    Ok(out.into_series())
}
