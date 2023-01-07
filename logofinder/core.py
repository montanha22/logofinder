import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from tqdm import tqdm

from logofinder.crawlers.base import LogoCrawler


def crawl_logos(
    crawler: LogoCrawler,
    company_names: list[str],
    n_threads: int = None,
    show_progress: bool = False,
) -> pd.DataFrame:

    n_threads = n_threads or os.cpu_count()

    results = []

    executor = ThreadPoolExecutor(n_threads)
    search_results = list(
        tqdm(
            executor.map(crawler.search_logo_url, company_names),
            total=len(company_names),
            disable=not show_progress,
        )
    )

    for search_result, company_name in zip(search_results, company_names):
        url, metadata = None, None

        if search_result is not None:
            url = search_result.url
            metadata = search_result.metadata

        results.append(
            {
                "name": company_name,
                "url": url,
                "metadata": metadata,
                "crawler": crawler.__class__.__name__,
            }
        )

    results_df = pd.DataFrame(results)
    return results_df
