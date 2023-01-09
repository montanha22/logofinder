import logging
import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from tqdm import tqdm

from logofinder.crawlers.base import LogoCrawler
from logofinder.models import CompanyInfo
from logofinder.processors.base import CompanyDataProcessor

logger = logging.getLogger(__name__)


class CrawlerRaisedAnException(BaseException):
    ...


def crawl_logos(
    crawler: LogoCrawler,
    companies: list[CompanyInfo],
    company_data_processor: CompanyDataProcessor = None,
    n_threads: int = None,
    show_progress: bool = False,
):
    company_data_processor = company_data_processor or crawler.default_processor
    n_threads = n_threads or os.cpu_count()

    processed_companies_data = company_data_processor.validate_and_process(companies)

    try:
        executor = ThreadPoolExecutor(n_threads)
        search_results = list(
            tqdm(
                executor.map(crawler.search_logo_url, processed_companies_data),
                total=len(processed_companies_data),
                disable=not show_progress,
            )
        )
    except Exception as e:
        msg = (
            f"uncaught exception when searching logo: [{e}]."
            "The crawler shouldn't raise an Exception."
        )
        logger.error(msg)
        raise CrawlerRaisedAnException

    results = []
    for search_result, info in zip(search_results, companies):
        url, metadata = None, None

        if search_result is not None:
            url = search_result.url
            metadata = search_result.metadata

        results.append(
            {
                "cnpj": info.cnpj,
                "name": info.name,
                "url": url,
                "metadata": metadata,
                "crawler": crawler.__class__.__name__,
            }
        )

    results_df = pd.DataFrame(columns=["cnpj", "name", "url", "metadata", "crawler"])

    if results:
        results_df = pd.DataFrame(results)

    return results_df
