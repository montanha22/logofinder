import pytest

from logofinder.crawlers.google import GoogleImagesCrawler

SKIP_SLOW_TESTS = False


@pytest.mark.skipif(SKIP_SLOW_TESTS, reason="slow")
@pytest.mark.asyncio
async def test_crawling_coca_cola_logo():
    crawler = GoogleImagesCrawler()
    url = await crawler.search_logo_url("coca cola")
    assert isinstance(url, str)
    assert (
        url
        == "https://logodownload.org/wp-content/uploads/2014/04/coca-cola-logo-1-1.png"
    )
