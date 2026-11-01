"""Parse the sourced canvases (data/sourced-canvases-100.md) into structured data.

Writes data/sourced_canvases.json (per service id 1-100) and
data/iran-ai-saas-sourced-100.csv. The markdown file is the single source of
truth for these services; edit it and rerun build_v3.py.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC = DATA / "sourced-canvases-100.md"
OUT = DATA / "sourced_canvases.json"
CSV_OUT = DATA / "iran-ai-saas-sourced-100.csv"
SECTION_KEYS = {
    "1": "canvas",
    "2": "cost_model",
    "3": "revenue",
    "4": "sensitivities",
    "5": "risks",
    "6": "unverified",
}
def plain(text: str) -> str:
    """Strip light markdown (bold, links) for the Word export."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", text)
    text = text.replace("\\[", "[").replace("\\]", "]")
    return text.strip()


def to_blocks(md_text: str) -> list:
    """Markdown -> [{'t':'table','h':[...],'r':[[...]]} | {'t':'p','x':str} | {'t':'li','x':str}]."""
    blocks, lines, i = [], md_text.strip().splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [plain(c) for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+:?|:?-+:?", c.replace(" ", "")) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                blocks.append({"t": "table", "h": rows[0], "r": rows[1:]})
            continue
        if re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            blocks.append({"t": "li", "x": plain(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", line))})
        elif line.strip():
            blocks.append({"t": "p", "x": plain(line)})
        i += 1
    return blocks


def num(s: str) -> float | None:
    s = s.replace(",", "").replace("−", "-").replace("+", "")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def parse_scenarios(block: str) -> dict:
    out = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] not in ("Conservative", "Base", "Optimistic"):
            continue
        cust = re.findall(r"[\d,]+(?:\.\d+)?", cells[1])
        be_txt = cells[2]
        out[cells[0].lower()] = {
            "customers_m12": num(cust[0]) if len(cust) > 0 else None,
            "customers_m24": num(cust[1]) if len(cust) > 1 else None,
            "break_even_month": None if re.search(r"not|none|never", be_txt, re.I) else (num(be_txt) if re.search(r"\d", be_txt) else None),
            "peak_cash_m": num(cells[3]),
            "mrr_m24_m": num(cells[4]),
            "profit_m24_m": num(cells[5]),
        }
    return out


def parse() -> dict:
    text = SRC.read_text(encoding="utf-8")
    parts = re.split(r"^(?=## Service #\d+:)", text, flags=re.M)[1:]
    result = {}
    for part in parts:
        m = re.match(r"## Service #(\d+): (.+)", part)
        sid, title = int(m.group(1)), m.group(2).strip()
        body = part[m.end():]
        chunks = re.split(r"^### (\d)\. .*$", body, flags=re.M)
        verdict_md = chunks[0].strip()
        sections = {}
        for i in range(1, len(chunks), 2):
            sections[SECTION_KEYS[chunks[i]]] = chunks[i + 1].strip()
        scen = parse_scenarios(sections["revenue"])
        result[sid] = {
            "id": sid,
            "title": title,
            "verdict_md": verdict_md,
            "scenarios": scen,
            "sections_md": sections,
            "verdict_blocks": to_blocks(verdict_md),
            "sections_blocks": {k: to_blocks(v) for k, v in sections.items()},
        }
    return result


def write_all() -> dict:
    data = parse()
    assert sorted(data) == list(range(1, 101)), "expected services 1-100"
    OUT.write_text(json.dumps({str(k): v for k, v in data.items()}, ensure_ascii=False), encoding="utf-8")
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "id", "service",
            "base_customers_m12", "base_customers_m24", "base_break_even_month",
            "base_peak_cash_m_toman", "base_mrr_m24_m_toman", "base_profit_m24_m_toman",
            "conservative_break_even_month", "conservative_profit_m24_m_toman",
            "optimistic_break_even_month", "optimistic_profit_m24_m_toman",
        ])
        for sid in sorted(data):
            sc = data[sid]["scenarios"]
            b, c, o = sc.get("base", {}), sc.get("conservative", {}), sc.get("optimistic", {})
            w.writerow([
                sid, data[sid]["title"],
                b.get("customers_m12"), b.get("customers_m24"), b.get("break_even_month"),
                b.get("peak_cash_m"), b.get("mrr_m24_m"), b.get("profit_m24_m"),
                c.get("break_even_month"), c.get("profit_m24_m"),
                o.get("break_even_month"), o.get("profit_m24_m"),
            ])
    return data


if __name__ == "__main__":
    d = write_all()
    print(f"wrote {OUT.name} and {CSV_OUT.name} for {len(d)} services")
