#!/usr/bin/env python3
"""Merge the Sridevi Night 2019+ panel archive into the existing chart JSON."""
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from pathlib import Path
import json, re

SOURCE = "https://dpbossx.net/sridevi-night-panel-chart.php"
OUT = Path("dp777/data/charts/sridevi.json")
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DATE_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\s+to\s+\d{1,2}/\d{1,2}/\d{4}$")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "tr": self.row = []
        elif tag.lower() in ("td", "th") and self.row is not None: self.cell = []
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row); self.row = None

def parse_cell(raw):
    text = " ".join(raw.split())
    # Panel pages expose the open pana, jodi and close pana in that order.
    nums = re.findall(r"(?<!\d)\d{1,3}(?!\d)", text)
    if len(nums) >= 3:
        return nums[0].zfill(3), nums[1].zfill(2), nums[2].zfill(3)
    if re.fullmatch(r"[★☆*\s—-]+", text or "*"):
        marker = "***" if text else "***"
        return marker, "**", marker
    # Keep unknown text visible; never invent a number.
    return text or "***", "", ""

def main():
    req = Request(SOURCE, headers={"User-Agent":"Mozilla/5.0 DP777 archive importer"})
    html = urlopen(req, timeout=45).read().decode("utf-8", "replace")
    p = Parser(); p.feed(html)
    found = {}
    for cells in p.rows:
        if len(cells) < 8: continue
        date = cells[0].strip()
        if not DATE_RE.match(date): continue
        row = {"date": date}
        for day, raw in zip(DAYS, cells[1:8]):
            op, jo, cl = parse_cell(raw)
            row[f"{day} Open"], row[f"{day} Jodi"], row[f"{day} Close"] = op, jo, cl
        found[date] = row
    if not found: raise SystemExit("No Sridevi Night weekly rows parsed; existing archive left unchanged.")
    old = {"updated_at": "", "charts": {"sridevi": {"rows": []}}}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
    existing = {r.get("date"): r for r in old.get("charts",{}).get("sridevi",{}).get("rows",[]) if r.get("date")}
    # Existing records win on duplicate dates; newly recovered earlier weeks are added.
    merged = dict(found); merged.update(existing)
    def sortkey(item):
        m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", item["date"])
        return (int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else (0,0,0)
    rows = sorted(merged.values(), key=sortkey)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "charts": {"sridevi": {
            "title": "Sridevi Night historical records",
            "source": SOURCE,
            "rows": rows
        }}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Imported {len(found)} source weeks; merged archive now has {len(rows)} weeks.")

if __name__ == "__main__": main()
