import re
from urllib.parse import urljoin
from urllib.parse import urlparse

from logofinder.crawlers.base import LogoSearchResult
from logofinder.crawlers.base import RequestsCrawler
from logofinder.processors.search_by_name import SearchByNameProcessor


class OfficialWebsiteCrawler(RequestsCrawler):
    TIMEOUT = 5

    def search_logo_url(self, company_name: str) -> LogoSearchResult | None:
        self.logger.info(f"crawling {company_name} logo")
        try:
            website = self._find_website(company_name)
            url = self._find_website_logo(website)

            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                url = urljoin(website, url)

            return LogoSearchResult(url, {"company_website": website})

        except Exception as e:
            self.logger.error(f"uncaught error {e} when searching {company_name} logo")
            return None

    @property
    def default_processor(self) -> SearchByNameProcessor:
        return SearchByNameProcessor()

    def _find_website(self, company_name: str) -> str:
        soup = self._get_soup(
            "https://www.google.com/search",
            params={"q": f"{company_name}"},
            timeout=self.TIMEOUT,
        )

        links = []
        for result in soup.find_all("div", attrs={"class": "g"}):
            link = result.find("a", href=True)
            links.append(link.attrs.get("href"))

        if not links:
            return

        return links[0]

    def _find_website_logo(self, domain: str) -> str:
        soup = self._get_soup(domain, timeout=self.TIMEOUT)
        LOGO_REGEX = re.compile(r"logo", re.I)

        attrs = ["alt", "src", "id", "class"]
        imgs = []
        for attr in attrs:
            new_imgs = soup.find_all("img", attrs={attr: LOGO_REGEX})
            imgs.extend(new_imgs)

        imgs = sorted(imgs, key=lambda img: (img.sourceline, img.sourcepos))

        if not imgs:
            return

        return [img.attrs.get("src") for img in imgs][0]
