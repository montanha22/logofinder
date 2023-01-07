import abc
from dataclasses import dataclass
from typing import Callable

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}


@dataclass
class LogoSearchResult:
    url: str
    metadata: dict[str, str]


class LogoCrawler(abc.ABC):
    @abc.abstractmethod
    def search_logo_url(self, company_name: str) -> LogoSearchResult | None:
        pass


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
