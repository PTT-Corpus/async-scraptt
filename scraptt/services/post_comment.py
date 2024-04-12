from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyquery import PyQuery
    from scrapy.http.response.html import HtmlResponse


PUSH_TAG_WATERMARK = {"推": "pos", "噓": "neg", "→": "neu"}


class PostCommentService:
    def _create_dto(self, push_tag_item: tuple[int, PyQuery]):
        index, value = push_tag_item
        return {
            "type": value(".push-tag").text(),
            "author": value(".push-userid").text().split(" ")[0],
            "content": value(".push-content").text().lstrip(" :").strip(),
            "order": index + 1,
        }

    def get(self, response: HtmlResponse):
        push_tag: PyQuery = response.dom(".push")
        return list(
            map(lambda value: self._create_dto(value), enumerate(push_tag.items()))
        )
