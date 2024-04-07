from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

PTT_BASE_URL = "https://www.ptt.cc/bbs"

COOKIES = {"over18": "1"}
