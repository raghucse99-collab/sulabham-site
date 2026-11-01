#!/usr/bin/env python3
"""Refresh the Radha Night weekly archive from its public Pana chart page."""
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import json, re
from pathlib import Path

SOURCE = "https://sara777.com/radha-night/pana.html"
OUT = Path("dp777/data/charts/radha-night.json")
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DATE_RE = re.compile(r"^\\d{1,2}/\\d{1,2}/\\d{4}\\s+to\\s+\\d{1,2}/\\d{1,2}/\\d{4}$")

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "tr":
            self.row = []
        elif tag.lower() in ("td", "th") and self.row is not None:
            self.cell = []
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None

def parse_cell(value):
    value = " ".join(value.split())
    if not value or re.fullmatch(r"[★☆*\\s—-]+", value):
        marker = value or ""
        return marker, marker, marker
    parts = value.split()
    if len(parts) >= 3 and all(re.fullmatch(r"\\d{1,3}", x) for x in parts[:3]):
        return tuple(x.zfill(3) if i != 1 else x.zfill(2) for i, x in enumerate(parts[:3]))
    # Do not guess or split a malformed/unreadable source cell.
    return value, "", ""

def main():
    request = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (compatible; DP777ChartUpdater/1.0)"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    parser = TableParser()
    parser.feed(html)
    rows, seen = [], set()
    for cells in parser.rows:
        if len(cells) < 8:
            continue
        date = cells[0].strip()
        if not DATE_RE.match(date) or date in seen:
            continue
        seen.add(date)
        row = {"date": date}
        for day, raw in zip(DAYS, cells[1:8]):
            opened, jodi, closed = parse_cell(raw)
            row[f"{day} Open"] = opened
            row[f"{day} Jodi"] = jodi
            row[f"{day} Close"] = closed
        rows.append(row)
    if not rows:
        raise SystemExit("No weekly Radha Night rows found; refusing to overwrite the archive.")
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "charts": {
            "radha-night": {
                "title": "Radha Night historical records",
                "source": SOURCE,
                "rows": rows
            }
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\\n", encoding="utf-8")
    print(f"Saved {len(rows)} Radha Night weekly rows to {OUT}")

if __name__ == "__main__":
    main()
