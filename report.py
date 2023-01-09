from glob import glob

import pandas as pd

from logofinder.helpers import Company
from logofinder.helpers import SearchData
from logofinder.helpers import render_logos_report


def generate_report():

    dfs = []
    for filepath in glob("results/20230108*.csv"):
        df = pd.read_csv(filepath)
        dfs.append(df)

    results = pd.concat(dfs).drop_duplicates(["name", "crawler"], keep="last")

    companies = []
    for name, group in results.groupby("name"):
        searchs = []
        for _, row in group.iterrows():
            searchs.append(SearchData(**row[["url", "crawler", "metadata"]]))
        companies.append(Company(name, searchs))

    render_logos_report(companies, "report.html")


if __name__ == "__main__":
    generate_report()
