import re
from functools import partial

import pandas as pd


def _remove_words(sentence: str, words: list[str]):
    return " ".join([w for w in sentence.split() if w.lower() not in words])


def remove_words(series: pd.Series, words: list[str]):
    return series.apply(partial(_remove_words, words=words)).str.strip()


def remove_patterns(series: pd.Series, patterns: list[re.Pattern]):
    col = series.copy()
    for pattern in patterns:
        col = col.str.replace(pattern, "")
    col = col.str.strip()
    return col
