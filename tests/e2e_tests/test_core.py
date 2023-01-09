from logofinder import crawl_logos
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.models import CompanyInfo


def test_crawling_coca_cola_logo_with_core_crawl_logos():
    crawler = GoogleImagesCrawler()
    companies = [CompanyInfo(name="coca cola")]
    result_df = crawl_logos(crawler, companies)
    assert (
        result_df["url"].iloc[0]
        == "https://logodownload.org/wp-content/uploads/2014/04/coca-cola-logo-1-1.png"
    )
