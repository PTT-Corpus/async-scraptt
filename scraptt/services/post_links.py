from __future__ import annotations

from datetime import datetime
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrapy.http.response.html import HtmlResponse


def get_post_links(response: HtmlResponse, selected_year: int | None = None):
    title_css = ".r-ent .title a"
    title_tags = (
        response.dom(".r-list-sep").prev_all(title_css)
        if response.url.endswith("index.html")
        else response.dom(title_css)
    )
    links = []
    for title_tag in list(title_tags.items()):
        url = title_tag.attr("href")
        timestamp = re.search(r"(\d{10})", url).group(1)
        year = datetime.fromtimestamp(int(timestamp)).year
        if selected_year and not selected_year <= year <= datetime.now().year:
            continue
        links.append(url)
    return links
