from __future__ import annotations

from typing import TYPE_CHECKING

from scrapy.exporters import JsonItemExporter as _JsonItemExporter

from .utils import make_file_path

if TYPE_CHECKING:
    from io import BufferedWriter

    from scrapy.exporters import BaseItemExporter

    from scraptt.interfaces import Post
    from scraptt.spiders import PttSpider


class JsonItemExporter(_JsonItemExporter):
    def start_exporting(self):
        self._beautify_newline()

    def finish_exporting(self):
        self._beautify_newline()


class JsonPipeline:
    def open_spider(self, spider: PttSpider) -> None:
        self.exporters_list: dict[str, tuple[BaseItemExporter, BufferedWriter]] = {}

    def _exporter_for_item(self, item: Post, spider: PttSpider):
        file_path = make_file_path(item, spider._arguments.data_dir)

        if file_path not in self.exporters_list:
            file = open(f"{file_path}.json", "wb")
            exporter = JsonItemExporter(file, encoding="utf-8", indent=4)
            exporter.start_exporting()
            self.exporters_list[file_path] = (exporter, file)

        return self.exporters_list[file_path][0]

    def process_item(self, item: Post, spider: PttSpider):
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item

    def close_spider(self, spider: PttSpider) -> None:
        for exporter, file in self.exporters_list.values():
            exporter.finish_exporting()
            file.close()
