from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
FAILED_URLS_FILE = BASE_DIR / "failed_urls.json"

PTT_BASE_URL = "https://www.ptt.cc/bbs"

PTT_DOMAINS = ["ptt.cc", "www.ptt.cc"]

COOKIES = {"over18": "1"}
