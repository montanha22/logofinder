from dataclasses import dataclass
from enum import Enum

import uvicorn
from fastapi import FastAPI

from logofinder import crawl_logos
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.crawlers.officialsite import OfficialWebsiteCrawler
from logofinder.models import CompanyInfo

app = FastAPI(title="Logofinder")


class Crawlers(Enum):
    google_images = "google_images"
    official_website = "official_website"


crawlers_factories = {
    Crawlers.google_images: GoogleImagesCrawler,
    Crawlers.official_website: OfficialWebsiteCrawler,
}
n_threads_by_crawler = {
    Crawlers.google_images: 5,
}


@dataclass
class GetLogosResponse:
    name: str
    url: str | None


@app.get(
    "/api/v0/get-logos-by-name", response_model=list[GetLogosResponse], tags=["Logo"]
)
def get_companies_logos_urls_by_name(names: str, crawler: Crawlers):
    names = [name.strip() for name in names.split(",")]
    companies = [CompanyInfo(name=name) for name in names]

    crawler_ = crawlers_factories.get(crawler)()
    n_threads = n_threads_by_crawler.get(crawler)

    logos_df = crawl_logos(crawler=crawler_, companies=companies, n_threads=n_threads)
    logos_df = logos_df[["name", "url"]]

    return logos_df.to_dict("records")


if __name__ == "__main__":
    uvicorn.run(app)
