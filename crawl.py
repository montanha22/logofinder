from datetime import datetime

import pandas as pd

from logofinder import crawl_logos
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.crawlers.officialsite import OfficialWebsiteCrawler
from logofinder.models import CompanyInfo


def get_now_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def load_and_preprocess_companies_dataset() -> pd.DataFrame:
    rename_dict = {
        "Razão Social": "name",
        "Nome fantasia": "trading_name",
        "CNPJ": "cnpj",
    }
    companies = (
        pd.read_csv("empresas.csv").rename(rename_dict, axis=1).drop_duplicates("cnpj")
    )
    return companies


def main():
    companies_df = load_and_preprocess_companies_dataset()
    companies = [CompanyInfo(**c) for c in companies_df.to_dict("records")]

    now_ts = get_now_timestamp()

    google_crawler = GoogleImagesCrawler()
    website_crawler = OfficialWebsiteCrawler()

    google_df = crawl_logos(google_crawler, companies, n_threads=5, show_progress=True)
    website_df = crawl_logos(
        website_crawler, companies, n_threads=20, show_progress=True
    )

    google_df.to_csv(f"results/{now_ts}_google_images.csv")
    website_df.to_csv(f"results/{now_ts}_official_site.csv")


if __name__ == "__main__":
    main()
