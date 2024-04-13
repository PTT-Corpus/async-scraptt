from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scraptt.interfaces import Post


def make_file_path(item: Post, data_dir: str) -> str:
    board = item["board"]
    date = datetime.fromtimestamp(item["created_at"])
    formatted_date = date.strftime("%Y%m%d_%H%M")
    dir_path = f"{data_dir}/{board}/{date.year}"
    file_path = f"{dir_path}/{formatted_date}_{item['id']}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    return file_path
