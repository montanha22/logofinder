from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader

BASE_PATH = Path(__file__).parent


@dataclass
class SearchData:
    url: str
    crawler: str
    metadata: dict


@dataclass
class Company:
    name: str
    logo_searchs: list[SearchData]


def render_logos_report(companies: list[Company], output_path: str) -> str:
    loader = FileSystemLoader(BASE_PATH / "static")
    env = Environment(loader=loader)

    template = env.get_template("template.html")
    output = template.render(companies=companies)

    with open(output_path, "w+") as f:
        f.write(output)
