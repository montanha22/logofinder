from typing import Any
from unittest.mock import Mock
from unittest.mock import call

import pandas as pd
import pytest

from logofinder import crawl_logos
from logofinder.core import CrawlerRaisedAnException
from logofinder.crawlers.base import LogoCrawler
from logofinder.models import CompanyInfo
from logofinder.models import LogoSearchResult


@pytest.fixture
def companies():
    return [
        CompanyInfo(name="fake1"),
        CompanyInfo(name="fake2"),
        CompanyInfo(name="fake3"),
    ]


class FakeProcessor:
    def validate_and_process(self, data: list):
        return data


class FakeCrawler(LogoCrawler):
    def __init__(self, raises: bool):
        self._raises = raises

    @property
    def default_processor(self):
        return FakeProcessor()

    def search_logo_url(self, data: Any) -> LogoSearchResult | None:
        if self._raises:
            raise Exception("error")

        return LogoSearchResult(f"fake_url: {data}", {})


def test_craw_logos_return(companies):
    crawler = FakeCrawler()
    result_df = crawl_logos(crawler, companies)

    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == len(companies)
    assert set(result_df.columns) == {"cnpj", "name", "url", "metadata", "crawler"}


def test_craw_logos_return_when_no_companies():
    crawler = FakeCrawler()
    result_df = crawl_logos(crawler, [])

    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 0
    assert set(result_df.columns) == {"cnpj", "name", "url", "metadata", "crawler"}


def test_crawl_logos_when_crawlers_raises_an_exception(companies):
    crawler = FakeCrawler(raises=True)

    with pytest.raises(CrawlerRaisedAnException) as exc_info:
        crawl_logos(crawler, companies)

    assert exc_info.type is CrawlerRaisedAnException
