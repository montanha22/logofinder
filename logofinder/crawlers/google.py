import asyncio
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from logofinder.crawlers.base import LogoSearchResult
from logofinder.crawlers.base import SeleniumCrawler

logger = logging.getLogger(__name__)


class GoogleImagesCrawler(SeleniumCrawler):
    _google_images_url = "https://www.google.com.br/imghp"

    def _search_first_image_url(self, driver: webdriver.Chrome, search_str: str) -> str:

        driver.get(self._google_images_url)

        # fill and submit search form
        form = driver.find_element(By.TAG_NAME, "form")
        search_bar = form.find_element(By.TAG_NAME, "input")
        search_bar.send_keys(search_str)
        form.submit()

        # find main div and click in the first image
        main_div = driver.find_element(By.CSS_SELECTOR, "div[role=main]")
        main_links = main_div.find_elements(By.TAG_NAME, "a")
        main_links[0].click()

        new_window = driver.find_element(By.ID, "islsp")

        try:
            WebDriverWait(driver, 5).until(
                lambda driver: not driver.find_element(By.ID, "islsp")
                .find_element(By.CSS_SELECTOR, "a[role=link]")
                .find_element(By.TAG_NAME, "img")
                .get_attribute("src")
                .startswith("data")
            )
        except TimeoutException as e:
            pass

        url = (
            new_window.find_element(By.CSS_SELECTOR, "a[role=link]")
            .find_element(By.TAG_NAME, "img")
            .get_attribute("src")
        )
        return url

    def search_logo_url(
        self, company_name: str, aux_keyword: str = "logomarca"
    ) -> LogoSearchResult | None:
        logger.info(f"crawling {company_name} logo")

        try:
            driver = self._driver_factory()
            url = self._search_first_image_url(
                driver,
                f"{company_name} {aux_keyword}",
            )
            driver.close()
            return LogoSearchResult(url, {"aux_keyword": aux_keyword})

        except Exception as e:
            logger.error(f"uncaught error {e} when searching {company_name} logo")
            return None
