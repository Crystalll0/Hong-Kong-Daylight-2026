# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from pathlib import Path
from urllib.request import Request, urlopen

URL = (
    "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
    "?dataType=SRS&year=2026&rformat=csv"
)

FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "hko-sunrise-sunset-2026.csv"
)


def fetch():
    if FILE.exists():
        print(f"Using saved file: {FILE.name}")
        return

    request = Request(
        URL,
        headers={"User-Agent": "SD5913 student daylight project"},
    )

    with urlopen(request, timeout=60) as response:
        raw = response.read()

    FILE.parent.mkdir(exist_ok=True)
    FILE.write_bytes(raw)
    print(f"Saved {len(raw)} bytes to data/{FILE.name}")


if __name__ == "__main__":
    fetch()