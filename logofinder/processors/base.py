from typing import Protocol

from logofinder.models import CompanyInfo


class CompanyDataProcessor(Protocol):
    def validate_and_process(self, companies: list[CompanyInfo]) -> list:
        ...
