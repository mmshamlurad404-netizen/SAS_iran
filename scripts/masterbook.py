"""Parse the audited 200-service Iranian AI SaaS masterbook (v3 docx).

Produces data/masterbook.json with structured BMC and P&L data.
"""
from __future__ import annotations

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / ".monkeycode-tmp-files" / "cfcf94bb-Iran_AI_SaaS_200_Services_Business_Model_Masterbook-v3-1.docx"
OUT = ROOT / "data" / "masterbook.json"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SEGMENTS = {
    "Prosumer, Micro-Seller & B2B2C (School/Platform Packs)",
    "Enterprise, Industrial & Institutional B2B",
    "Core Iranian SME, Bazaar, Clinic & Agency B2B",
}


def _text(el) -> str:
    return "".join(t.text or "" for t in el.iter(W + "t")).strip()


def read_docx(path: Path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    seq = []
    tables = []
    for child in body:
        if child.tag == W + "p":
            txt = _text(child)
            if txt:
                seq.append(("p", txt))
        elif child.tag == W + "tbl":
            rows = []
            for tr in child.findall(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    parts = [_text(p) for p in tc.findall(W + "p")]
                    cells.append(" ".join(p for p in parts if p).strip())
                rows.append(cells)
            tables.append(rows)
            seq.append(("t", len(tables) - 1))
    return seq, tables


def num(s: str) -> float:
    s = str(s).strip().replace(",", "").replace("$", "").replace("%", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        v = float(s)
    except ValueError:
        return 0.0
    return -v if neg else v


def split_pl(rows):
    out = {}
    for r in rows[1:]:
        if len(r) < 3:
            continue
        label = r[0]
        out[label] = {
            "label": label,
            "basis": r[1] if len(r) > 1 else "",
            "toman": num(r[2]) if len(r) > 2 else 0.0,
            "usd": num(r[3]) if len(r) > 3 else 0.0,
        }
    return out


def parse_service(sid, title, cls, bmc_rows, pl_rows, sector):
    bmc = {}
    for r in bmc_rows:
        if len(r) >= 2 and r[0] and r[0][0].isdigit():
            bmc[int(r[0][0])] = r[1]

    fields = {}
    for part in cls.split(" | "):
        if part.startswith("Auditor Classification:"):
            fields["tier"] = part.split("Tier:", 1)[-1].strip()
        elif part.startswith("Advisory Verdict:"):
            fields["verdict"] = part.split(":", 1)[1].strip()
        elif part.startswith("Buyer:"):
            fields["buyer_raw"] = part.split(":", 1)[1].strip()
        elif part.startswith("Engine:"):
            fields["engine"] = part.split("Engine:", 1)[-1].strip()

    buyer_raw = fields.get("buyer_raw", "")
    buyer, segment = buyer_raw, ""
    for seg in SEGMENTS:
        suffix = f" ({seg})"
        if buyer_raw.endswith(suffix):
            buyer, segment = buyer_raw[: -len(suffix)].strip(), seg
            break
    if not segment:
        m = re.match(r"^(.*)\s+\(([^()]*)\)$", buyer_raw)
        if m:
            buyer, segment = m.group(1).strip(), m.group(2).strip()

    b1 = bmc.get(1, "")
    replaces = ""
    m = re.search(r"Replaces/mitigates:\s*(.*?)\.\s*Audited Month-12", b1)
    if m:
        replaces = m.group(1).strip()
    active = None
    m = re.search(r"active base:\s*(\d+)\s+paying accounts\s*\(([^)]*)\)", b1)
    if m:
        active = {
            "accounts": int(m.group(1)),
            "mix": m.group(2).strip(),
        }
    churn = None
    m = re.search(r"with\s+([\d.]+)%\s+monthly churn", b1)
    if m:
        churn = float(m.group(1))

    b2 = bmc.get(2, "")
    eliminated = driver = ""
    m = re.search(r"Eliminates '(.*?)' at (.*?) of manual/penalty cost\.", b2)
    if m:
        eliminated, eliminated_cost_ratio = m.group(1), m.group(2)
    else:
        eliminated_cost_ratio = ""
    m = re.search(r"Powered by (.*?) and hosted 100% inside Iran", b2)
    if m:
        driver = m.group(1).strip()
    m = re.search(r"data centers so (.*?)\.$", b2)
    sovereignty = m.group(1).strip() if m else ""

    b3 = bmc.get(3, "")
    gtm = ""
    m = re.search(r"Primary GTM via (.*?) plus ([\d.]+) FTE B2B Inside Sales Closers", b3)
    sales_fte = None
    if m:
        gtm, sales_fte = m.group(1).strip(), float(m.group(2))
    partner_pct = partner_share = partner_cogs = 0
    m = re.search(
        r"Models a (\d+)% partner/marketplace commission on (\d+)% of revenue \(([\d,]+) T/mo in COGS\)",
        b3,
    )
    if m:
        partner_pct = int(m.group(1))
        partner_share = int(m.group(2))
        partner_cogs = num(m.group(3))

    b4 = bmc.get(4, "")
    support_fte = None
    m = re.search(r"([\d.]+) FTE dedicated support specialists handle (.*?)\.$", b4)
    if m:
        support_fte = float(m.group(1))
        support_scope = m.group(2).strip()

    b5 = bmc.get(5, "")
    prices = {}
    m = re.search(r"Starter: ([\d,]+) T/mo \| Growth: ([\d,]+) T/mo \| Pro/Ent: ([\d,]+) T/mo", b5)
    if m:
        prices = {
            "starter": num(m.group(1)),
            "growth": num(m.group(2)),
            "pro": num(m.group(3)),
        }
    usage_price = None
    m = re.search(r"Usage packs \(([\d,]+) T/mo avg\)", b5)
    if m:
        usage_price = num(m.group(1))
    billing_model = ""
    m = re.search(r"Monthly Toman billing \(([^)]*)\)", b5)
    if m:
        billing_model = m.group(1).strip()
    m = re.search(r"Gross Billed MRR:\s*([\d,]+) T/mo", b5)
    gross_mrr = num(m.group(1)) if m else 0.0
    m = re.search(r"Net Collected MRR after ([\d.]+)% DSO/bad-debt provision:\s*([\d,]+) T/mo", b5)
    dso_pct = float(m.group(1)) if m else 0.0
    net_mrr = num(m.group(2)) if m else 0.0
    m = re.search(r"ARPU:\s*([\d,]+) T/mo", b5)

    b6 = bmc.get(6, "")
    gpu_nodes = gpu_cost = nin_cost = 0.0
    stack = dataset = ""
    m = re.search(r"Domestic GPU: ([\d.]+)x RTX 6000 Ada 48GB node incl\. 25% peak buffer \(([\d,]+) T/mo\) \+ NIN CPU/DB servers \(([\d,]+) T/mo\)", b6)
    if m:
        gpu_nodes = float(m.group(1))
        gpu_cost = num(m.group(2))
        nin_cost = num(m.group(3))
    m = re.search(r"Stack:\s*(.*?)\. Dataset:\s*(.*?)\.$", b6)
    if m:
        stack, dataset = m.group(1).strip(), m.group(2).strip()

    b7 = bmc.get(7, "")
    activity_accuracy = activity_connectors = activity_billing = ""
    m = re.search(
        r"Maintaining LoRA accuracy on (.*?); keeping (.*?) connectors live across NIN/BGP routing shifts; enforcing (.*?)\.$",
        b7,
    )
    if m:
        activity_accuracy, activity_connectors, activity_billing = (
            m.group(1).strip(),
            m.group(2).strip(),
            m.group(3).strip(),
        )

    b8 = bmc.get(8, "")
    dist_partners = infrastructure = ""
    m = re.search(r"Distribution & API partners:\s*(.*?)\. Infrastructure:\s*(.*?)\.$", b8)
    if m:
        dist_partners, infrastructure = m.group(1).strip(), m.group(2).strip()

    b9 = bmc.get(9, "")
    standalone_cost = standalone_ebitda = standalone_margin = 0.0
    standalone_usd = 0.0
    portfolio_cost = portfolio_ebitda = portfolio_margin = 0.0
    m = re.search(
        r"Standalone All-In Cost:\s*([\d,]+) T/mo \(\$([\d,.]+)\) -> Standalone EBITDA:\s*(-?[\d,]+) T/mo \((-?[\d.]+)%\)\. "
        r"Shared-Engine Portfolio Cost \(splitting core dev/office across 3 sibling tools\):\s*([\d,]+) T/mo -> "
        r"Portfolio EBITDA:\s*(-?[\d,]+) T/mo \((-?[\d.]+)%\)\.",
        b9,
    )
    if m:
        standalone_cost = num(m.group(1))
        standalone_usd = num(m.group(2))
        standalone_ebitda = num(m.group(3))
        standalone_margin = float(m.group(4))
        portfolio_cost = num(m.group(5))
        portfolio_ebitda = num(m.group(6))
        portfolio_margin = float(m.group(7))

    pl = split_pl(pl_rows)
    pl_ebitda = pl.get("EBITDA (STANDALONE vs. SHARED-ENGINE)", {})
    ebitda_basis = pl_ebitda.get("basis", "")
    be_customers = cac = payback = ltv_cac = 0.0
    m = re.search(r"BE:\s*(\d+)\s*cust", ebitda_basis)
    if m:
        be_customers = int(m.group(1))
    m = re.search(r"CAC:\s*([\d,]+) T \(([\d.]+) mo\)", ebitda_basis)
    if m:
        cac = num(m.group(1))
        payback = float(m.group(2))
    m = re.search(r"LTV:CAC:\s*([\d.]+)x", ebitda_basis)
    if m:
        ltv_cac = float(m.group(1))

    pl_rows_out = []
    for key in [
        "Revenue — Tier 1 (Starter)",
        "Revenue — Tier 2 (Growth)",
        "Revenue — Tier 3 (Pro / Ent / B2B2C Pack)",
        "Revenue — Metered Usage & Overage",
        "GROSS BILLED REVENUE (MRR)",
        "Less: Bad Debt & DSO Inflation Lag",
        "COGS — Domestic GPU (+25% Buffer)",
        "COGS — NIN CPU, DB & BGP Relay",
        "COGS — SMS & Shaparak Gateway",
        "COGS — Partner / Channel Commissions",
        "AUDITED GROSS PROFIT & MARGIN",
        "OPEX — Tech Payroll (incl. Tamin/Eidi/Sanavat)",
        "OPEX — B2B Sales Closers & Support Payroll",
        "OPEX — Marketing, Tehran Office & Tax/Legal",
        "EBITDA (STANDALONE vs. SHARED-ENGINE)",
    ]:
        if key in pl:
            pl_rows_out.append(pl[key])

    return {
        "id": sid,
        "sector": sector,
        "title": title,
        "tier": fields.get("tier", ""),
        "verdict": fields.get("verdict", ""),
        "buyer": buyer,
        "segment": segment,
        "engine": fields.get("engine", ""),
        "bmc": bmc,
        "replaces": replaces,
        "eliminated": eliminated,
        "eliminated_cost_ratio": eliminated_cost_ratio,
        "driver": driver,
        "sovereignty": sovereignty,
        "gtm": gtm,
        "sales_fte": sales_fte,
        "partner_pct": partner_pct,
        "partner_share": partner_share,
        "partner_cogs": partner_cogs,
        "support_fte": support_fte,
        "support_scope": support_scope,
        "active": active,
        "churn": churn,
        "prices": prices,
        "usage_price": usage_price,
        "billing_model": billing_model,
        "gross_mrr": gross_mrr,
        "dso_pct": dso_pct,
        "net_mrr": net_mrr,
        "gpu_nodes": gpu_nodes,
        "gpu_cost": gpu_cost,
        "nin_cost": nin_cost,
        "stack": stack,
        "dataset": dataset,
        "activity_accuracy": activity_accuracy,
        "activity_connectors": activity_connectors,
        "activity_billing": activity_billing,
        "dist_partners": dist_partners,
        "infrastructure": infrastructure,
        "standalone_cost": standalone_cost,
        "standalone_usd": standalone_usd,
        "standalone_ebitda": standalone_ebitda,
        "standalone_margin": standalone_margin,
        "portfolio_cost": portfolio_cost,
        "portfolio_ebitda": portfolio_ebitda,
        "portfolio_margin": portfolio_margin,
        "be_customers": be_customers,
        "cac": cac,
        "payback": payback,
        "ltv_cac": ltv_cac,
        "pl": pl_rows_out,
    }


def main():
    seq, tables = read_docx(DOCX)
    services = []
    sector = ""
    sector_ranges = {}
    for i, item in enumerate(seq):
        if item[0] == "p":
            txt = item[1]
            m = re.match(r"^Sector ([A-Z]):\s*(.*?)\s*\(Services #(\d+)[–-]#(\d+)\)", txt)
            if m:
                sector = f"{m.group(1)}: {m.group(2)}"
                sector_ranges[sector] = (int(m.group(3)), int(m.group(4)))
            m = re.match(r"^Service\s*#(\d+):\s*(.*)$", txt)
            if m:
                sid = int(m.group(1))
                title = m.group(2).strip()
                cls = seq[i + 1][1] if seq[i + 1][0] == "p" else ""
                bmc = tables[seq[i + 2][1]]
                pl = tables[seq[i + 3][1]]
                services.append(parse_service(sid, title, cls, bmc, pl, sector))

    services.sort(key=lambda s: s["id"])
    assert len(services) == 200, len(services)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"sectors": sector_ranges, "services": services}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} with {len(services)} services")
    missing = [s["id"] for s in services if not s["gtm"] or not s["driver"] or not s["dataset"]]
    print("missing fields:", missing)


if __name__ == "__main__":
    main()
