from __future__ import annotations

from typing import TYPE_CHECKING

from ckip2tei import generate_tei_xml_async

from .utils import make_file_path

if TYPE_CHECKING:
    from scraptt.interfaces import Post
    from scraptt.spiders import PttSpider


class CkipPipeline:
    """
    The CkipPipeline object implements CKIP Chinese NLP tools on the scraped item,
    and writes the result to XML.
    """

    async def process_item(self, item: Post, spider: PttSpider) -> None:
        file_path = make_file_path(item, spider._arguments.data_dir)
        item["board"] = f"{item['board']}-ptt"
        tei_xml = await generate_tei_xml_async(item, "ptt")

        with open(f"{file_path}.xml", "w", encoding="utf-8") as file:
            file.write(tei_xml)
