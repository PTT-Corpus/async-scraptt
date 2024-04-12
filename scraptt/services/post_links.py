from __future__ import annotations

from datetime import datetime
import re
from typing import TYPE_CHECKING

from scrapy.http import Request
from twisted.internet.defer import DeferredList

from scraptt.config import COOKIES

if TYPE_CHECKING:
    from pyquery import PyQuery
    from scrapy.core.engine import ExecutionEngine
    from scrapy.http.response.html import HtmlResponse


class PostLinkService:
    def _get_title_tags(self, response: HtmlResponse) -> PyQuery:
        title_css = ".r-ent .title a"
        if response.url.endswith("index.html"):
            return response.dom(".r-list-sep").prev_all(title_css)
        return response.dom(title_css)

    def get(
        self,
        response: HtmlResponse,
        scrapy_engine: ExecutionEngine,
        selected_year: int | None = None,
    ):
        title_tags = self._get_title_tags(response)
        links = []
        for title_tag in list(title_tags.items()):
            url = title_tag.attr("href")
            timestamp = re.search(r"(\d{10})", url).group(1)
            year = datetime.fromtimestamp(int(timestamp)).year
            if selected_year and not selected_year <= year <= datetime.now().year:
                continue

            links.append(scrapy_engine.download(Request(url, cookies=COOKIES)))

        return DeferredList(links)
