from pathlib import Path
import re
from typing import Optional

from pydantic import (
    BaseModel,
    model_validator,
)

from scraptt.config import DATA_DIR


class SpiderArguments(BaseModel):
    boards: list[str]
    fetch_all: Optional[bool] = None
    scrape_from: Optional[int] = None
    index_from: Optional[int] = None
    index_to: Optional[int] = None
    data_dir: Optional[Path]

    @model_validator(mode="before")
    @classmethod
    def convert_boards(self, values: dict):
        index_from: int = values.get("index_from")
        index_to: int = values.get("index_to")
        if index_from and index_to is None:
            raise ValueError("Provide `index_to` with `index_from`.")
        if index_from is None and index_to:
            raise ValueError("Provide `index_from` with `index_to`.")
        if all([index_from, index_to]):
            if int(index_from) > int(index_to):
                raise ValueError(
                    "The value of `index_from` cannot be greater than `index_to`."
                )

        data_dir: str = values.get("data_dir")
        boards: str = values.get("boards")
        values["boards"] = re.split(r"\s*,\s*", boards.strip()) if boards else None
        values["data_dir"] = Path(data_dir) if data_dir else DATA_DIR
        return values
