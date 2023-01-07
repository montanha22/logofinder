import re
from functools import partial

import pandas as pd
import spacy


def remove_words(sentence: str, words: list[str]):
    return " ".join([w for w in sentence.split() if w.lower() not in words])


def remove_useless_terms(series: pd.Series, stop_words: list[str]) -> pd.Series:

    ltda_regex = re.compile(r"\bltda\.{0,1}|ltd|limitada\b", flags=re.I)
    sa_regex = re.compile(r"\b(sa|s\.a\.{0,1}|s/a|s\sa)\b", flags=re.I)
    domain_regex = re.compile(r"\.com\b", flags=re.I)
    symbols_regex = re.compile(r"[.,-]")

    remove_patterns = [ltda_regex, sa_regex, domain_regex, symbols_regex]

    col = series.copy()
    for pattern in remove_patterns:
        col = col.str.replace(pattern, "")
    col = col.str.strip()

    col = col.apply(partial(remove_words, words=stop_words)).str.strip()

    return col


def get_pt_stop_words():
    nlp = spacy.load("pt_core_news_md")
    return nlp.Defaults.stop_words
