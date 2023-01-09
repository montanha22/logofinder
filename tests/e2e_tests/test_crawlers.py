import pytest

from logofinder.crawlers.base import LogoSearchResult
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.crawlers.officialsite import OfficialWebsiteCrawler

SKIP_SLOW_TESTS = False


@pytest.mark.skipif(SKIP_SLOW_TESTS, reason="slow")
def test_crawling_coca_cola_logo_with_google_images_crawler():
    crawler = GoogleImagesCrawler()
    result = crawler.search_logo_url("coca cola")
    assert isinstance(result, LogoSearchResult)
    assert (
        result.url
        == "https://logodownload.org/wp-content/uploads/2014/04/coca-cola-logo-1-1.png"
    )


@pytest.mark.skipif(SKIP_SLOW_TESTS, reason="slow")
def test_crawling_claro_logo_with_official_site_crawler():
    crawler = OfficialWebsiteCrawler()
    result = crawler.search_logo_url("claro")
    assert isinstance(result, LogoSearchResult)
    assert (
        result.url
        == "https://www.claro.com.br/files/104379/300x300/a3cbcc941a/assinatura-claro.png/m/filters:quality(100)"
    )
