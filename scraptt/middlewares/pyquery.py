from __future__ import annotations

from typing import TYPE_CHECKING

from pyquery import PyQuery

from scraptt.config import PTT_BASE_URL

if TYPE_CHECKING:
    from scrapy.http.request import Request
    from scrapy.http.response.html import HtmlResponse

    from scraptt.spiders import PttSpider


class PyQueryMiddleware:
    """
    The PyQueryMiddleware object injects PyQuery object into Scrapy `response`.
    """

    def process_response(
        self, request: Request, response: HtmlResponse, spider: PttSpider
    ) -> HtmlResponse:
        response.dom = PyQuery(response.text).make_links_absolute(PTT_BASE_URL)
        return response
