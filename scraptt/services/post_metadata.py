from __future__ import annotations

import re
from typing import (
    TYPE_CHECKING,
    TypedDict,
)

if TYPE_CHECKING:
    from scrapy.http.response.html import HtmlResponse


META_TAG = '//*[@id="main-content"]/div/span[@class="article-meta-tag"]'


class PostMetadata(TypedDict):
    id: str
    board: str
    title: str
    author: str
    created_at: int


class PostMetadataService:
    def _strip_items(self, data: list[str]):
        return list(map(lambda value: value.strip(), data))

    def _get_metadata_header(self, response: HtmlResponse):
        keys = self._strip_items(response.xpath(f"{META_TAG}/text()").getall())
        values = self._strip_items(
            response.xpath(f"{META_TAG}/following-sibling::*/text()").getall()
        )
        return dict(zip(keys, values, strict=True))

    def get(self, response: HtmlResponse) -> PostMetadata:
        board = re.search(
            r"www\.ptt\.cc\/bbs\/([\w\d\-_]{1,30})\/", response.url
        ).group(1)
        post_id = response.url.split("/")[-1].split(".html")[0]
        created_at = re.search(r"(\d{10})", response.url).group(1)
        header = self._get_metadata_header(response)
        title = header.get("標題", "無標題")
        author = header.get("作者", "匿名")
        return PostMetadata(
            id=post_id,
            board=board,
            title=title,
            author=author,
            created_at=int(created_at),
        )
