from dataclasses import dataclass


@dataclass
class CompanyInfo:
    cnpj: str | None = None
    name: str | None = None
    trading_name: str | None = None


@dataclass
class LogoSearchResult:
    url: str
    metadata: dict[str, str]
