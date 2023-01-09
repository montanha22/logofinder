import abc
import logging
from typing import Any
from typing import Callable

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from logofinder.models import LogoSearchResult
from logofinder.processors.base import CompanyDataProcessor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}


class LogoCrawler(abc.ABC):
    """Abstract class for crawlers suited for crawling company logos."""

    @abc.abstractmethod
    def search_logo_url(self, data: Any) -> LogoSearchResult | None:
        """crawls for company logo.
        this methods takes a generic data (defined by each crawler) and
        should return an `LogoSearchResult` object as response.
        It can also return None if the crawler couldn't find
        any logo. The method shoudn't raise any exception, if the crawler stops
        unexpectedly it should log the error and return None."""
        pass

    @abc.abstractproperty
    def default_processor(self) -> CompanyDataProcessor:
        pass

    @property
    def logger(self):
        return logging.getLogger(f"crawlers.{self.__class__.__name__}")


class SeleniumCrawler(LogoCrawler):
    def __init__(self, driver_factory: Callable[[], webdriver.Chrome] = None) -> None:
        if driver_factory is None:
            driver_factory = self._create_default_driver

        self._driver_factory = driver_factory

    def _create_default_driver(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return webdriver.Chrome(options=options)


class RequestsCrawler(LogoCrawler):
    def _get_soup(self, url: str, **kwargs: dict) -> BeautifulSoup:
        response = requests.get(url, headers=HEADERS, **kwargs)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
