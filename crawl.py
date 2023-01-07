from datetime import datetime

import pandas as pd

from logofinder import crawl_logos
from logofinder.crawlers.google import GoogleImagesCrawler
from logofinder.crawlers.officialsite import OfficialWebsiteCrawler
from logofinder.preprocessing import get_pt_stop_words
from logofinder.preprocessing import remove_useless_terms


def get_now_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def load_and_preprocess_companies_dataset() -> pd.DataFrame:
    rename_dict = {"Razão Social": "corporate name", "Nome fantasia": "trading name"}
    comp = (
        pd.read_csv("empresas.csv").rename(rename_dict, axis=1).drop_duplicates("CNPJ")
    )

    stop_words = get_pt_stop_words()
    comp["revised name"] = remove_useless_terms(comp["corporate name"], stop_words)
    comp["search name"] = comp["trading name"].fillna(comp["revised name"])
    return comp


def main():
    companies = load_and_preprocess_companies_dataset()
    names = companies["search name"].tolist()

    now_ts = get_now_timestamp()

    google_crawler = GoogleImagesCrawler()
    website_crawler = OfficialWebsiteCrawler()

    google_df = crawl_logos(google_crawler, names, 5)
    website_df = crawl_logos(website_crawler, names, 20)

    google_df = pd.concat([companies, google_df], axis=1)
    website_df = pd.concat([companies, website_df], axis=1)

    google_df.to_csv(f"results/{now_ts}_google_images.csv")
    website_df.to_csv(f"results/{now_ts}_official_site.csv")


if __name__ == "__main__":
    main()
