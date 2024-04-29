from __future__ import annotations

from dataclasses import dataclass
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyquery import PyQuery
    from scrapy.http.response.html import HtmlResponse

    from .html_parser import HTMLParserService


@dataclass
class PostContentService:
    html_parser_service: HTMLParserService

    def strip(self, content: PyQuery) -> str | None:
        cloned_content = (
            content.clone()
            .children()
            .remove('span[class^="article-meta-"]')
            .remove("div.push")
            .end()
            .html()
        )
        stripped_content = self.html_parser_service.strip_tags(cloned_content)
        return re.sub(r"※ 發信站.*|※ 文章網址.*|※ 編輯.*", "", stripped_content).strip(
            "\r\n-"
        )

    def get(self, response: HtmlResponse):
        content: PyQuery = response.dom("#main-content")
        if not content:
            return

        stripped_content = self.strip(content)
        if not stripped_content:
            return

        quotes = re.findall("※ 引述.*|\n: .*", stripped_content)
        for quote in quotes:
            stripped_content = stripped_content.replace(quote, "")

        return stripped_content.strip("\n ")
