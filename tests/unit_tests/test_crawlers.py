from logofinder.crawlers.base import LogoCrawler
from logofinder.crawlers.google import GoogleImagesCrawler


def test_crawler_log():
    crawler = GoogleImagesCrawler()
    crawler.logger.critical("critical error")
