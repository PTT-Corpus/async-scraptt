from __future__ import annotations

import json
from typing import TYPE_CHECKING

from scrapy.signalmanager import dispatcher

from scraptt.config import FAILED_URLS_FILE

if TYPE_CHECKING:
    from scrapy.http.response.html import HtmlResponse

error_post_signal = object()


def process_error_post(errors: list[HtmlResponse], board: str):
    urls = list(map(lambda error: error.url, errors))
    if FAILED_URLS_FILE.exists():
        with open(FAILED_URLS_FILE) as file:
            data = json.load(file)
            if data.get(board):
                filtered = list(filter(lambda url: url not in data[board], urls))
                data[board].extend(filtered)
            else:
                data[board] = urls
    else:
        data = {board: urls}

    with open(FAILED_URLS_FILE, "w") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


dispatcher.connect(process_error_post, signal=error_post_signal)
