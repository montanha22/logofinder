from dataclasses import dataclass
from enum import Enum
from typing import Literal

import uvicorn
from fastapi import FastAPI

from logofinder import crawl_logos
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.crawlers.officialsite import OfficialWebsiteCrawler

app = FastAPI()


class Crawlers(Enum):
    google_images = "google_images"
    official_website = "official_website"


crawlers_factories = {
    Crawlers.google_images: GoogleImagesCrawler,
    Crawlers.official_website: OfficialWebsiteCrawler,
}


@dataclass
class GetLogosResponse:
    name: str
    url: str


@app.get("/get-logo", response_model=list[GetLogosResponse])
def get_companies_logos_url(names: str, crawler: Crawlers):
    names = [name.strip() for name in names.split(",")]
    crawler_ = crawlers_factories.get(crawler)()
    return crawl_logos(crawler_, names)[["name", "url"]].to_dict("records")


if __name__ == "__main__":
    uvicorn.run(app)
