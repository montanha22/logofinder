import re

import pandas as pd
import spacy

from logofinder.models import CompanyInfo
from logofinder.processors.utils import remove_patterns
from logofinder.processors.utils import remove_words


def remove_useless_terms(series: pd.Series, stop_words: list[str]) -> pd.Series:

    ltda_regex = re.compile(r"\bltda\.{0,1}|ltd|limitada\b", flags=re.I)
    sa_regex = re.compile(r"\b(sa|s\.a\.{0,1}|s/a|s\sa)\b", flags=re.I)
    domain_regex = re.compile(r"\.com\b", flags=re.I)
    symbols_regex = re.compile(r"[.,-]")

    patterns_to_remove = [ltda_regex, sa_regex, domain_regex, symbols_regex]

    series = remove_patterns(series, patterns_to_remove)
    series = remove_words(series, stop_words)
    return series


class SearchByNameProcessor:
    def __init__(self):
        self._nlp_model = spacy.load("pt_core_news_md")
        self._stop_words = self._nlp_model.Defaults.stop_words

    def _is_valid(self, company: CompanyInfo):
        return company.name is not None or company.trading_name is not None

    def _validate_companies(self, companies: list[CompanyInfo]):
        invalid_companies = [c for c in companies if not self._is_valid(c)]
        if invalid_companies:
            raise ValueError(
                f"found {len(invalid_companies)} invalid companies data."
                f"First 5: {invalid_companies[:5]}"
            )

    def validate_and_process(self, companies: list[CompanyInfo]) -> list[str]:
        if not companies:
            return []

        self._validate_companies(companies)
        companies_df = pd.DataFrame(companies)
        names = remove_useless_terms(companies_df["name"], self._stop_words)
        return companies_df["trading_name"].fillna(names).tolist()
