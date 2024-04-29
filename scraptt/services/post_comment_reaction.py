from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrapy.http.response.html import HtmlResponse


class PostCommentReactionService:
    def count(self, response: HtmlResponse):
        push_tags = response.css('span[class*="push-tag"]::text').getall()
        total_comments = [push_tag.strip() for push_tag in push_tags]
        counter = Counter(total_comments)
        return {
            "推 (pos)": counter["推"],
            "噓 (neg)": counter["噓"],
            "→ (neu)": counter["→"],
        }
