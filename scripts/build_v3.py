"""Build the audited 200-service masterbook deliverables (v3)."""
from __future__ import annotations

import csv
import html
import json
import re
from collections import defaultdict
from pathlib import Path

from fa_v3 import (
    BILLING_FA,
    ENGINES_FA,
    FA_SERVICES,
    FLOW_LABELS_FA,
    MASTERBOOK,
    SECTORS_FA,
    SEGMENTS_FA,
    STACKS_FA,
    TIERS_FA,
    VERDICTS_FA,
    bmc_en,
    bmc_fa,
    fa_dec,
    fa_digits,
    fa_int,
    fa_pct,
    money_m,
    pl_fa,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
CSS = (TEMPLATES / "masterbook.css").read_text(encoding="utf-8")
USD_TOMAN = 270_000
USD_SOURCE = 203_100
LEGACY = json.loads((DATA / "legacy_services.json").read_text(encoding="utf-8"))
LEGACY_FA = json.loads((DATA / "fa_legacy.json").read_text(encoding="utf-8"))
SERVICES = MASTERBOOK["services"] + LEGACY["services"]
N_AUDITED = len(MASTERBOOK["services"])
N_LEGACY = len(LEGACY["services"])
N_TOTAL = len(SERVICES)
import fa_v3 as _fa_v3
_fa_v3.FA_SERVICES.update(LEGACY_FA)
FA_SERVICES = _fa_v3.FA_SERVICES
SECTORS = list(MASTERBOOK["sectors"].keys())
SERVICE_PAGE_FA = "service_fa.html"


def enrich(s: dict) -> dict:
    pl = {p["label"]: p["toman"] for p in s["pl"]}
    s["_mrr"] = pl.get("GROSS BILLED REVENUE (MRR)", 0)
    s["_bad_debt"] = pl.get("Less: Bad Debt & DSO Inflation Lag", 0)
    s["_net"] = s["net_mrr"]
    s["_cogs"] = sum(v for k, v in pl.items() if k.startswith("COGS"))
    s["_opex"] = sum(v for k, v in pl.items() if k.startswith("OPEX"))
    s["_gp"] = pl.get("AUDITED GROSS PROFIT & MARGIN", 0)
    s["_ebitda"] = pl.get("EBITDA (STANDALONE vs. SHARED-ENGINE)", 0)
    s["_gm"] = (s["_gp"] / s["_net"] * 100) if s["_net"] else 0
    s["_arpu"] = (s["_mrr"] / s["active"]["accounts"]) if s["active"] and s["active"]["accounts"] else 0
    s["_annual_mrr"] = s["_mrr"] * 12
    s["_annual_ebitda"] = s["_ebitda"] * 12
    s["_usd_mrr"] = s["_mrr"] / USD_TOMAN
    s["_usd_ebitda"] = s["_ebitda"] / USD_TOMAN
    return s


for _s in SERVICES:
    enrich(_s)

TOTALS = {
    "mrr": sum(s["_mrr"] for s in SERVICES),
    "net": sum(s["_net"] for s in SERVICES),
    "ebitda": sum(s["_ebitda"] for s in SERVICES),
    "portfolio": sum(s["portfolio_ebitda"] for s in SERVICES),
    "gm": sum(s["_gp"] for s in SERVICES) / sum(s["_net"] for s in SERVICES) * 100,
    "avg_margin": sum(s["standalone_margin"] for s in SERVICES) / len(SERVICES),
    "p1": sum(1 for s in SERVICES if s["tier"] == "P1"),
    "accounts": sum(s["active"]["accounts"] for s in SERVICES if s["active"]),
}

SECTOR_AGGS = []
for sector in SECTORS:
    rows = [s for s in SERVICES if s["sector"] == sector]
    SECTOR_AGGS.append({
        "sector": sector,
        "sector_fa": SECTORS_FA.get(sector, sector),
        "count": len(rows),
        "mrr": sum(s["_mrr"] for s in rows),
        "net": sum(s["_net"] for s in rows),
        "ebitda": sum(s["_ebitda"] for s in rows),
        "portfolio": sum(s["portfolio_ebitda"] for s in rows),
        "margin": sum(s["standalone_margin"] for s in rows) / len(rows),
        "p1": sum(1 for s in rows if s["tier"] == "P1"),
    })

TOP25 = sorted(SERVICES, key=lambda s: s["_ebitda"], reverse=True)[:25]


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def json_for_script(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def dash_row(s: dict, fa: bool) -> dict:
    return {
        "id": s["id"],
        "title": FA_SERVICES[str(s["id"])]["title"] if fa else s["title"],
        "sector": SECTORS_FA.get(s["sector"], s["sector"]) if fa else s["sector"],
        "tier": s["tier"],
        "verdict": VERDICTS_FA.get(s["verdict"], s["verdict"]) if fa else s["verdict"],
        "buyer": FA_SERVICES[str(s["id"])]["buyer"] if fa else s["buyer"],
        "engine": ENGINES_FA.get(s["engine"], s["engine"]) if fa else s["engine"],
        "active": s["active"]["accounts"] if s["active"] else 0,
        "churn": s["churn"],
        "mrr": s["_mrr"],
        "net": s["_net"],
        "ebitda": s["_ebitda"],
        "margin": s["standalone_margin"],
        "portfolio": s["portfolio_ebitda"],
        "gm": s["_gm"],
        "cac": s["cac"],
        "payback": s["payback"],
        "ltv": s["ltv_cac"],
        "arpu": s["_arpu"],
        "origin": s.get("origin", "audited"),
    }


def service_row(s: dict, fa: bool) -> dict:
    if fa:
        bmc = bmc_fa(s)
        pl = pl_fa(s)
        title = FA_SERVICES[str(s["id"])]["title"]
        sector = SECTORS_FA.get(s["sector"], s["sector"])
        buyer = FA_SERVICES[str(s["id"])]["buyer"]
        segment = SEGMENTS_FA.get(s["segment"], s["segment"])
        verdict = VERDICTS_FA.get(s["verdict"], s["verdict"])
        engine = ENGINES_FA.get(s["engine"], s["engine"])
        usd = None
    else:
        bmc = bmc_en(s)
        pl = [{
            "label": p["label"],
            "basis": p["basis"],
            "toman": p["toman"],
            "usd": p["toman"] / USD_TOMAN,
            "flow": flow_kind(p["label"]),
        } for p in s["pl"]]
        title = s["title"]
        sector = s["sector"]
        buyer = s["buyer"]
        segment = s["segment"]
        verdict = s["verdict"]
        engine = s["engine"]
        usd = None

    revenue_streams = [p for p in pl if p["flow"] == "revenue" and not p["label"].upper().startswith(("GROSS", "درآمد ناخالص"))]
    cost_rows = [p for p in pl if p["flow"] in {"bad_debt", "gpu", "nin", "sms", "partner", "tech", "sales", "marketing"}]
    return {
        "id": s["id"],
        "title": title,
        "sector": sector,
        "tier": s["tier"],
        "verdict": verdict,
        "buyer": buyer,
        "segment": segment,
        "engine": engine,
        "churn": s["churn"],
        "active": s["active"],
        "mrr": s["_mrr"],
        "net": s["_net"],
        "bad_debt": s["_bad_debt"],
        "gp": s["_gp"],
        "ebitda": s["_ebitda"],
        "portfolio": s["portfolio_ebitda"],
        "portfolio_margin": s["portfolio_margin"],
        "margin": s["standalone_margin"],
        "gm": s["_gm"],
        "cac": s["cac"],
        "payback": s["payback"],
        "ltv": s["ltv_cac"],
        "be": s["be_customers"],
        "arpu": s["_arpu"],
        "gpu_nodes": s["gpu_nodes"],
        "partner_pct": s["partner_pct"],
        "dso_pct": s["dso_pct"],
        "bmc": bmc,
        "pl": pl,
        "revenue_streams": revenue_streams,
        "cost_rows": cost_rows,
        "origin": s.get("origin", "audited"),
        "origin_note": s.get("origin_note", ""),
        "legacy_id": s.get("legacy_id"),
    }


def flow_kind(label: str) -> str:
    if label.startswith("Revenue") or label.startswith("GROSS"):
        return "revenue"
    if label.startswith("Less:"):
        return "bad_debt"
    if "Domestic GPU" in label:
        return "gpu"
    if "NIN" in label:
        return "nin"
    if "SMS" in label:
        return "sms"
    if "Partner" in label:
        return "partner"
    if "Tech Payroll" in label:
        return "tech"
    if "B2B Sales" in label:
        return "sales"
    if "Marketing" in label:
        return "marketing"
    return "total"


# ---------------------------------------------------------------- dashboard

DASH_CSS_EXTRA = """
"""


def dashboard_html(fa: bool) -> str:
    lang = "fa" if fa else "en"
    direction = "rtl" if fa else "ltr"
    data = [dash_row(s, fa) for s in SERVICES]
    aggs = SECTOR_AGGS
    top = [dash_row(s, fa) for s in TOP25]
    title = "مستربوک SaaS هوش مصنوعی ایران — ۳۱۰ سرویس" if fa else "Iran AI SaaS Masterbook — 310 Services"
    lede = (
        "کاتالوگ ترکیبی ۳۱۰ سرویس در ۲۰ بخش: ۲۰۰ سرویس حسابرسی‌شده v3 به‌همراه ۱۱۰ سرویس کاتالوگ قدیمی که با همان مدل مالی و بوم ۹بخشی بازنویسی شده‌اند. همه مبالغ به تومان و بر پایه فرض‌های ۱۴۰۵ است."
        if fa else
        "A combined 310-service catalogue across 20 Iranian sectors: 200 audited v3 services plus 110 legacy v1 services re-underwritten into the same nine-block canvas and Month-12 P&L model. Toman figures follow the 1405 audit assumptions; every service links to its full cost, revenue and engine detail."
    )
    t = TOTALS
    stats = [
        (f"{fa_digits(len(SERVICES))}" if fa else str(len(SERVICES)), "سرویس ترکیبی" if fa else "combined services"),
        (f"{fa_digits(len(SECTORS))}" if fa else str(len(SECTORS)), "بخش بازار" if fa else "market sectors"),
        (f"{fa_dec(t['mrr']/1e9,1)} میلیارد" if fa else f"{t['mrr']/1e9:.1f}B", "MRR ناخالص ماه ۱۲ (تومان)" if fa else "M12 gross MRR (Toman)"),
        (f"{fa_dec(t['ebitda']/1e9,1)} میلیارد" if fa else f"{t['ebitda']/1e9:.1f}B", "EBITDA مستقل (تومان)" if fa else "standalone EBITDA (Toman)"),
        (f"{fa_digits(t['p1'])}" if fa else str(t["p1"]), "سرویس اولویت ۱" if fa else "Tier P1 services"),
    ]
    stat_html = "".join(f'<div class="hero-stat"><div class="num">{v}</div><div class="label">{l}</div></div>' for v, l in stats)

    sector_labels = {"fa": "بخش", "en": "Sector"}
    table_headers = (
        ["بخش", "تعداد", "MRR (م.ت)", "EBITDA (م.ت)", "حاشیه", "اولویت ۱"]
        if fa else
        ["Sector", "Services", "MRR (M T)", "EBITDA (M T)", "Avg margin", "P1"]
    )
    th = "".join(f"<th>{x}</th>" for x in table_headers)
    svc_headers = (
        ["#", "سرویس", "بخش", "سطح", "خریدار", "MRR (م.ت)", "EBITDA (م.ت)", "حاشیه", "LTV:CAC", "بازگشت"]
        if fa else
        ["#", "Service", "Sector", "Tier", "Buyer", "MRR (M T)", "EBITDA (M T)", "Margin", "LTV:CAC", "Payback"]
    )
    svc_th = "".join(f"<th>{x}</th>" for x in svc_headers)

    labels = {
        "search": "جست‌وجوی سرویس، خریدار یا بخش…" if fa else "Search service, buyer or sector…",
        "all_sectors": "همه بخش‌ها" if fa else "All sectors",
        "all_tiers": "همه سطوح" if fa else "All tiers",
        "sort_mrr": "مرتب‌سازی: MRR" if fa else "Sort: MRR",
        "sort_ebitda": "مرتب‌سازی: EBITDA" if fa else "Sort: EBITDA",
        "sort_margin": "مرتب‌سازی: حاشیه" if fa else "Sort: margin",
        "sort_ltv": "مرتب‌سازی: LTV:CAC" if fa else "Sort: LTV:CAC",
        "sort_id": "مرتب‌سازی: شماره" if fa else "Sort: number",
        "shown": "سرویس نمایش‌داده‌شده" if fa else "services shown",
        "top": "۲۵ سرویس برتر بر اساس EBITDA مستقل" if fa else "Top 25 by standalone EBITDA",
        "sectors": "نمای بخش‌ها" if fa else "Sector picture",
        "catalogue": "کاتالوگ کامل" if fa else "Full catalogue",
        "click": "برای بوم مدل کسب‌وکار و صورت سود و زیان، روی هر ردیف کلیک کنید." if fa else "Click any row for its Business Model Canvas and audited P&L.",
        "report": "گزارش کامل" if fa else "Full report",
        "csv": "دانلود CSV" if fa else "Download CSV",
        "method": "روش‌شناسی" if fa else "Methodology",
    }
    labels_json = json_for_script(labels)
    sector_options = "".join(
        f'<option value="{esc(a["sector"])}">{esc(a["sector_fa"] if fa else a["sector"])}</option>' for a in aggs
    )

    body = f"""
<header class="hero">
  <div class="wrap">
    <div class="hero-top">
      <div class="eyebrow"><span></span> {'نسخه ترکیبی v3.1 · ۱۴۰۵' if fa else 'COMBINED EDITION v3.1 · 1405'}</div>
      <a class="lang-switch" href="{'index.html' if fa else 'fa.html'}" lang="{'en' if fa else 'fa'}" dir="{'ltr' if fa else 'rtl'}">{'English' if fa else 'فارسی'}</a>
    </div>
    <h1>{esc(title)}</h1>
    <p class="lede">{lede}</p>
    <div class="hero-meta">
      <div><strong>{'۲۰' if fa else '20'}</strong> {'بخش' if fa else 'sectors'}</div>
      <div><strong>{'۳۱۰' if fa else '310'}</strong> {'سرویس (۲۰۰ حسابرسی‌شده + ۱۱۰ بازنویسی‌شده)' if fa else 'services (200 audited + 110 re-underwritten)'}</div>
      <div><strong>{'۱۴۰۵' if fa else '1405'}</strong> {'سال مالی' if fa else 'fiscal year'}</div>
      <div><strong>{'۲۷۰٬۰۰۰' if fa else '270,000'}</strong> {'تومان به ازای هر دلار (قرارداد پروژه)' if fa else 'Toman per USD (project convention)'}</div>
    </div>
    <div class="hero-stats five">{stat_html}</div>
  </div>
</header>
<main class="wrap">
  <section class="grid-2">
    <div class="panel prose">
      <h2>{'خلاصه اجرایی' if fa else 'Executive read'}</h2>
      <p>{'این نسخه، ۳۱۰ مدل کسب‌وکار (۲۰۰ حسابرسی‌شده + ۱۱۰ بازنویسی‌شده) را با معیارهای Latka Iran، حقوق کامل ۱۴۰۵ (تأمین، عیدی، سنوات)، کمیسیون کانال، ریسک چک صیادی و تورم ۷ تا ۹ درصد ماهانه بازمحاسبه می‌کند. میانگین حاشیه EBITDA مستقل ' + fa_pct(t['avg_margin']) + ' و EBITDA سبد موتور مشترک ' + fa_dec(t['portfolio']/1e9,1) + ' میلیارد تومان در ماه است.' if fa else f"This edition combines 200 audited services with 110 legacy services re-underwritten against Latka Iran benchmarks, fully loaded 1405 payroll (Tamin, Eidi, Sanavat), channel commissions, SAYAD cheque risk and 7-9% monthly inflation. Average standalone EBITDA margin is {t['avg_margin']:.1f}%; shared-engine portfolio EBITDA reaches {t['portfolio']/1e9:.1f}B Toman per month."}</p>
      <p>{'۱۱۲ سرویس در اولویت ۱، ۱۵۵ در اولویت ۲ و ۴۳ در اولویت ۳ قرار دارند. از نظر حکم، ۱۵۷ سرویس محصول مستقل قوی، ۱۲۷ سرویس مستقل قابل‌دوام/مکمل سبد و ۲۶ سرویس فقط به‌صورت مکمل موتور مشترک توجیه اقتصادی دارند. ده سرویس EBITDA مستقل منفی دارند (دو سرویس حسابرسی‌شده و هشت سرویس بازنویسی‌شده) و باید صرفاً از طریق فروش سبدی اداره شوند؛ سایر حاشیه‌های نزدیک به صفر نیز همین رویکرد را می‌طلبند.' if fa else 'Tier distribution is 112 P1, 155 P2 and 43 P3. By verdict, 157 services are strong standalone wedges, 127 are viable standalone or strong portfolio add-ons, and 26 only work as shared-engine add-ons. Ten services post negative standalone EBITDA (two audited and eight re-underwritten) and must be managed through portfolio sales; thin-margin tools follow the same route.'}</p>
      <div class="callout">{'نرخ دلار در ستون‌های انگلیسی ۲۷۰٬۰۰۰ تومان است؛ گزارش اصلی حسابرسی از نرخ ۲۰۳٬۱۰۰ تومان استفاده کرده بود. همه محاسبات مالی این پروژه بر پایه تومان است.' if fa else 'English USD columns use the project rate of 270,000 Toman; the source audit used 203,100. Toman remains the authoritative currency throughout this project.'}</div>
      <p style="margin-top:14px"><a href="{'iran-ai-saas-report-v3.1-fa.md' if fa else 'iran-ai-saas-report-v3.1.md'}">{labels['report']}</a> · <a href="{'data/iran-ai-saas-masterbook-310-fa.csv' if fa else 'data/iran-ai-saas-masterbook-310.csv'}">{labels['csv']}</a></p>
    </div>
    <div class="panel">
      <div style="padding:18px 20px 0"><h2 style="font-size:20px">{labels['sectors']}</h2></div>
      <div class="tier-bars" id="tierBars"></div>
      <div style="padding:0 20px 18px"><div class="details-note">{'توزیع ۳۱۰ سرویس در سه سطح سرمایه‌گذاری (۲۰۰ حسابرسی‌شده + ۱۱۰ بازنویسی‌شده).' if fa else 'Distribution of the 310 services across three investment tiers (200 audited + 110 re-underwritten).'}</div></div>
    </div>
  </section>

  <section>
    <div class="section-head"><div><h2>{labels['top']}</h2></div><div class="section-note">{labels['click']}</div></div>
    <div class="panel"><div class="priority-list" id="topList"></div></div>
  </section>

  <section>
    <div class="section-head"><div><h2>{'جدول بخش‌ها' if fa else 'Sector economics'}</h2></div></div>
    <div class="panel table-scroll" style="max-height:none"><table><thead><tr>{th}</tr></thead><tbody id="sectorRows"></tbody></table></div>
  </section>

  <section>
    <div class="section-head"><div><h2>{labels['catalogue']}</h2></div><div class="section-note">{labels['click']}</div></div>
    <div class="panel">
      <div class="controls">
        <div><label>{'جست‌وجو' if fa else 'Search'}</label><input id="q" placeholder="{labels['search']}"></div>
        <div><label>{'بخش' if fa else 'Sector'}</label><select id="sector"><option value="">{labels['all_sectors']}</option>{sector_options}</select></div>
        <div><label>{'سطح' if fa else 'Tier'}</label><select id="tier"><option value="">{labels['all_tiers']}</option><option value="P1">{'اولویت ۱' if fa else 'P1'}</option><option value="P2">{'اولویت ۲' if fa else 'P2'}</option><option value="P3">{'اولویت ۳' if fa else 'P3'}</option></select></div>
        <div><label>{'مرتب‌سازی' if fa else 'Sort'}</label><select id="sort"><option value="ebitda">{labels['sort_ebitda']}</option><option value="mrr">{labels['sort_mrr']}</option><option value="margin">{labels['sort_margin']}</option><option value="ltv">{labels['sort_ltv']}</option><option value="id">{labels['sort_id']}</option></select></div>
      </div>
      <div class="table-meta"><span id="count"></span><span>{labels['shown']}</span></div>
      <div class="table-scroll"><table><thead><tr>{svc_th}</tr></thead><tbody id="svcRows"></tbody></table></div>
    </div>
  </section>

  <section class="panel prose">
    <h2>{labels['method']}</h2>
    <p>{'مدل‌ها بر پایه ۱۲ ماه فعالیت، با تعداد مشتری کالیبره‌شده Latka (۲۲ تا ۴۰ سازمانی، ۱۱۵ تا ۲۰۵ کسب‌وکار کوچک و متوسط و ۳۴۰ تا ۴۸۰ حرفه‌ای/خرد)، ARPU ترکیبی و ریزش ماهانه ۴ تا ۱۱ درصد ساخته شده‌اند. هزینه‌ها شامل GPU داخلی با ۲۵ درصد بافر، شبکه ملی اطلاعات، پیامک/شپارک، کمیسیون ۱۲ تا ۱۸ درصدی شرکا، حقوق کامل فنی/فروش/پشتیبانی، دفتر تهران و بازاریابی است.' if fa else 'Models use a 12-month ramp with Latka-calibrated customer counts (22-40 enterprise, 115-205 SME, 340-480 prosumer/micro), blended ARPU and 4-11% monthly churn. Costs include domestic GPU with a 25% buffer, NIN, SMS/Shaparak, 12-18% partner commissions, fully loaded tech/sales/support payroll, Tehran office and marketing.'}</p>
  </section>
</main>
<footer><div class="wrap"><div>{'مستربوک ترکیبی v3.1 · ۳۱۰ سرویس (۲۰۰ حسابرسی‌شده + ۱۱۰ بازنویسی‌شده) · قیمت‌ها به تومان' if fa else 'Combined Masterbook v3.1 · 310 services (200 audited + 110 re-underwritten) · prices in Toman'}</div><div><a href="{'index.html' if fa else 'fa.html'}">{'English edition' if fa else 'Persian edition'}</a></div></div></footer>
"""

    script = """
const DATA = __DATA__;
const AGGS = __AGGS__;
const TOP = __TOP__;
const LANG = '__LANG__';
const PAGE = '__PAGE__';
const LABELS = __LABELS__;
const intl = new Intl.NumberFormat(LANG === 'fa' ? 'fa-IR' : 'en-US', { maximumFractionDigits: 0 });
const intl1 = new Intl.NumberFormat(LANG === 'fa' ? 'fa-IR' : 'en-US', { maximumFractionDigits: 1 });
const num = v => intl.format(Math.round(v));
const dec = v => intl1.format(v);
const m = v => dec(v / 1e6);
function tierClass(t) { return t === 'P1' ? 'p1' : t === 'P2' ? 'p2' : 'p3'; }
function row(s) {
  return `<tr tabindex="0" data-id="${s.id}">
    <td>${s.id}</td>
    <td><span class="svc-name">${s.title}</span>${s.origin === 'legacy' ? `<span class="origin-pill legacy">${LANG === 'fa' ? 'بازنویسی v1→v3' : 'v1 → v3'}</span>` : ''}<span class="svc-cat">${s.buyer}</span></td>
    <td>${s.sector}</td>
    <td><span class="tier-pill ${tierClass(s.tier)}">${s.tier}</span></td>
    <td>${s.buyer}</td>
    <td class="num">${m(s.mrr)}</td>
    <td class="num">${m(s.ebitda)}</td>
    <td class="num">${dec(s.margin)}%</td>
    <td class="num">${dec(s.ltv)}x</td>
    <td class="num">${dec(s.payback)}</td>
  </tr>`;
}
function go(id) { location.href = PAGE + '?id=' + id; }
function renderTop() {
  const el = document.getElementById('topList');
  el.innerHTML = TOP.map((s, i) => `<div class="priority-item" data-id="${s.id}" tabindex="0">
    <div class="rank">${num(i + 1)}</div>
    <div><div class="name">${s.title}</div><div class="cat">${s.sector} · ${s.buyer}</div></div>
    <div class="score-pill ${s.tier === 'P1' ? 'high' : s.tier === 'P2' ? 'mid' : 'low'}">${m(s.ebitda)}${LANG === 'fa' ? ' م' : ' M'}</div>
  </div>`).join('');
  el.querySelectorAll('.priority-item').forEach(x => {
    x.addEventListener('click', () => go(x.dataset.id));
    x.addEventListener('keydown', e => { if (e.key === 'Enter') go(x.dataset.id); });
  });
}
function renderTiers() {
  const counts = { P1: 0, P2: 0, P3: 0 };
  DATA.forEach(s => counts[s.tier]++);
  const total = DATA.length;
  const el = document.getElementById('tierBars');
  const names = LANG === 'fa' ? { P1: 'اولویت ۱', P2: 'اولویت ۲', P3: 'اولویت ۳' } : { P1: 'Tier P1', P2: 'Tier P2', P3: 'Tier P3' };
  el.innerHTML = ['P1', 'P2', 'P3'].map(t => `<div class="tier-row"><div>${names[t]}</div><div class="bar"><i class="${t.toLowerCase()}" style="width:${counts[t] / total * 100}%"></i></div><div>${num(counts[t])}</div></div>`).join('');
}
function renderSectors() {
  document.getElementById('sectorRows').innerHTML = AGGS.map(a => `<tr style="cursor:default">
    <td><strong>${LANG === 'fa' ? a.sector_fa : a.sector}</strong></td>
    <td class="num">${num(a.count)}</td>
    <td class="num">${m(a.mrr)}</td>
    <td class="num">${m(a.ebitda)}</td>
    <td class="num">${dec(a.margin)}%</td>
    <td class="num">${num(a.p1)}</td>
  </tr>`).join('');
}
function render() {
  const q = document.getElementById('q').value.trim().toLowerCase();
  const sector = document.getElementById('sector').value;
  const tier = document.getElementById('tier').value;
  const sort = document.getElementById('sort').value;
  let rows = DATA.filter(s => {
    const hay = (s.title + ' ' + s.buyer + ' ' + s.sector).toLowerCase();
    return (!q || hay.includes(q)) && (!sector || s.sector === sector) && (!tier || s.tier === tier);
  });
  rows.sort((a, b) => sort === 'id' ? a.id - b.id : (b[sort] - a[sort]));
  document.getElementById('svcRows').innerHTML = rows.map(row).join('') || `<tr><td colspan="10" class="empty">${LANG === 'fa' ? 'نتیجه‌ای یافت نشد.' : 'No results.'}</td></tr>`;
  document.getElementById('count').textContent = num(rows.length) + ' / ' + num(DATA.length);
  document.querySelectorAll('#svcRows tr[data-id]').forEach(x => {
    x.addEventListener('click', () => go(x.dataset.id));
    x.addEventListener('keydown', e => { if (e.key === 'Enter') go(x.dataset.id); });
  });
}
['q', 'sector', 'tier', 'sort'].forEach(id => document.getElementById(id).addEventListener('input', render));
renderTop(); renderTiers(); renderSectors(); render();
"""
    script = (
        script.replace("__DATA__", json_for_script(data))
        .replace("__AGGS__", json_for_script(aggs))
        .replace("__TOP__", json_for_script(top))
        .replace("__LANG__", lang)
        .replace("__PAGE__", "service_fa.html" if fa else "service.html")
        .replace("__LABELS__", labels_json)
    )
    return page(title, lang, direction, body, script)


def page(title: str, lang: str, direction: str, body: str, script: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
{body}
<script>{script}</script>
</body>
</html>
"""


# ---------------------------------------------------------------- service page


def service_page_html(fa: bool) -> str:
    lang = "fa" if fa else "en"
    direction = "rtl" if fa else "ltr"
    codes = [service_row(s, fa) for s in SERVICES]
    title = "جزئیات سرویس — مستربوک ۳۱۰ سرویس" if fa else "Service detail — 310-service masterbook"
    back = "fa.html" if fa else "index.html"
    labels = {
        "back": "بازگشت به داشبورد" if fa else "Back to dashboard",
        "kpi": "شاخص‌های کلیدی ماه ۱۲" if fa else "Month-12 key metrics",
        "canvas": "بوم مدل کسب‌وکار" if fa else "Business Model Canvas",
        "pl": "صورت سود و زیان حسابرسی‌شده" if fa else "Audited P&L",
        "flows": "ترکیب درآمد و هزینه" if fa else "Revenue and cost mix",
        "method": "یادداشت روش" if fa else "Method note",
        "prev": "سرویس قبلی" if fa else "Previous service",
        "next": "سرویس بعدی" if fa else "Next service",
        "cf": "جریان نقد", "source": "متن اصلی انگلیسی بوم" if fa else "Source text",
    }
    labels_json = json_for_script(labels)
    script = """
const DATA = __DATA__;
const LANG = '__LANG__';
const PAGE = '__PAGE__';
const LABELS = __LABELS__;
const intl = new Intl.NumberFormat(LANG === 'fa' ? 'fa-IR' : 'en-US', { maximumFractionDigits: 0 });
const intl1 = new Intl.NumberFormat(LANG === 'fa' ? 'fa-IR' : 'en-US', { maximumFractionDigits: 1 });
const num = v => intl.format(Math.round(v));
const dec = v => intl1.format(v);
const million = v => dec(v / 1e6);
const usd = v => '$' + intl.format(Math.round(v));
const pct = v => dec(v) + '%';
function tierClass(t) { return t === 'P1' ? 'p1' : t === 'P2' ? 'p2' : 'p3'; }
function flowClass(f) { return ['gpu','nin','sms','partner','tech','sales','marketing','bad_debt'].includes(f) ? 'cost' : ''; }
function render() {
  const id = new URLSearchParams(location.search).get('id') || '1';
  const s = DATA.find(x => String(x.id) === String(id)) || DATA[0];
  const otherPage = PAGE === 'service_fa.html' ? 'service.html' : 'service_fa.html';
  document.getElementById('langSwitch').href = otherPage + '?id=' + s.id;
  document.title = s.title + ' — ' + (LANG === 'fa' ? 'مستربوک' : 'Masterbook');
  const kpis = [
    [million(s.mrr) + (LANG === 'fa' ? ' م' : ' M'), LANG === 'fa' ? 'MRR ناخالص (تومان)' : 'Gross MRR (Toman)'],
    [million(s.net) + (LANG === 'fa' ? ' م' : ' M'), LANG === 'fa' ? 'MRR خالص وصول‌شده' : 'Net collected MRR'],
    [pct(s.gm), LANG === 'fa' ? 'حاشیه ناخالص' : 'Gross margin'],
    [million(s.ebitda) + (LANG === 'fa' ? ' م' : ' M'), LANG === 'fa' ? 'EBITDA مستقل' : 'Standalone EBITDA'],
    [million(s.portfolio) + (LANG === 'fa' ? ' م' : ' M'), LANG === 'fa' ? 'EBITDA سبد' : 'Portfolio EBITDA'],
    [millions(s.cac), LANG === 'fa' ? 'CAC' : 'CAC'],
    [dec(s.payback) + (LANG === 'fa' ? ' ماه' : ' mo'), LANG === 'fa' ? 'بازگشت CAC' : 'CAC payback'],
    [dec(s.ltv) + 'x', 'LTV:CAC'],
    [num(s.be), LANG === 'fa' ? 'مشتری سربه‌سر' : 'Break-even customers'],
    [num(s.active.accounts), LANG === 'fa' ? 'حساب فعال' : 'Active accounts'],
    [pct(s.churn), LANG === 'fa' ? 'ریزش ماهانه' : 'Monthly churn'],
    [millions(s.arpu), LANG === 'fa' ? 'ARPU ترکیبی' : 'Blended ARPU']
  ];
  document.getElementById('kpis').innerHTML = kpis.map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join('');

  document.getElementById('serviceHead').innerHTML = `
    <div class="breadcrumbs"><a href="${PAGE === 'service_fa.html' ? 'fa.html' : 'index.html'}">${LABELS.back}</a> · ${s.sector}</div>
    <div style="margin-top:14px"><span class="badge ${tierClass(s.tier)}">${s.tier}</span> <span class="badge">${s.engine}</span> ${s.origin === 'legacy' ? `<span class="badge origin-legacy">${LANG === 'fa' ? 'بازنویسی‌شده v1→v3' : 'Legacy v1 → v3'}</span>` : `<span class="badge origin-audited">${LANG === 'fa' ? 'حسابرسی‌شده v3' : 'Audited v3'}</span>`}</div>
    <h1>${s.title}</h1>
    <div class="hero-meta">
      <div><strong>${LANG === 'fa' ? 'خریدار:' : 'Buyer:'}</strong> ${s.buyer}</div>
      <div><strong>${LANG === 'fa' ? 'حکم:' : 'Verdict:'}</strong> ${s.verdict}</div>
    </div>
    ${s.origin === 'legacy' ? `<div class="provenance-note">${LANG === 'fa' ? 'این سرویس از کاتالوگ قدیمی v1 آمده و با همان موتور مالی، بوم ۹بخشی و فرض‌های ۱۴۰۵ به مدل v3 بازنویسی شده است؛ بخشی از ۲۰۰ سرویس حسابرسی‌شده نیست.' : 'This service comes from the legacy v1 catalogue and has been re-underwritten into the v3 model with the same financial engine, nine-block canvas and 1405 assumptions. It is not part of the audited 200-service docx.'}</div>` : ''}`;

  document.getElementById('canvas').innerHTML = s.bmc.map(b => `<div class="bmc-card ${b.key}">
    <h3><span class="n">${b.num}</span>${b.title}</h3>
    <p>${b.text}</p>
    ${s.raw ? `<details class="raw-source"><summary>${LABELS.source}</summary><p>${s.raw[b.key] || ''}</p></details>` : ''}
  </div>`).join('');

  document.getElementById('plRows').innerHTML = s.pl.map(p => {
    let cls = '';
    if (p.label.includes('GROSS PROFIT') || p.label.includes('سود ناخالص')) cls = 'sub';
    if (p.label.startsWith('COGS') || p.label.startsWith('بهای')) cls = 'cogs';
    if (p.label.startsWith('OPEX') || p.label.startsWith('هزینه عملیاتی')) cls = 'opex';
    if (p.label.startsWith('EBITDA') || p.label.includes('EBITDA')) cls = 'total';
    const usdCell = p.usd == null ? '' : `<td class="num">${usd(p.usd)}</td>`;
    return `<tr class="${cls}"><td>${p.label}</td><td>${p.basis}</td><td class="num">${num(p.toman)}</td>${usdCell}</tr>`;
  }).join('');

  const revTotal = s.revenue_streams.reduce((a, p) => a + p.toman, 0) || 1;
  const costTotal = s.cost_rows.reduce((a, p) => a + Math.abs(p.toman), 0) || 1;
  const bars = [
    ...s.revenue_streams.map(p => ({ label: p.label, v: p.toman, total: revTotal, cost: false })),
    ...s.cost_rows.map(p => ({ label: p.label, v: Math.abs(p.toman), total: costTotal, cost: true }))
  ];
  document.getElementById('flows').innerHTML = s.revenue_streams.map(p => `<div class="flow-row">
      <div>${p.label}</div><div class="bar"><i style="width:${p.toman / revTotal * 100}%"></i></div>      <div class="val">${million(p.toman)}${LANG === 'fa' ? ' م' : ' M'}</div>
    </div>`).join('') + `<div style="height:10px"></div>` + s.cost_rows.map(p => `<div class="flow-row cost">
      <div>${p.label}</div><div class="bar"><i style="width:${Math.abs(p.toman) / costTotal * 100}%"></i></div><div class="val">${million(Math.abs(p.toman))}${LANG === 'fa' ? ' م' : ' M'}</div>
    </div>`).join('');

  const prev = DATA.find(x => x.id === s.id - 1) || DATA[DATA.length - 1];
  const next = DATA.find(x => x.id === s.id + 1) || DATA[0];
  document.getElementById('pager').innerHTML = `<a href="${PAGE}?id=${prev.id}">← ${LABELS.prev}: ${prev.title}</a><a href="${PAGE}?id=${next.id}">${LABELS.next}: ${next.title} →</a>`;
}
function millions(v) { return million(v) + (LANG === 'fa' ? ' م' : ' M'); }
render();
"""
    script = (
        script.replace("__DATA__", json_for_script(codes))
        .replace("__LANG__", lang)
        .replace("__PAGE__", "service_fa.html" if fa else "service.html")
        .replace("__LABELS__", labels_json)
    )
    body = f"""
<header class="hero service-hero">
  <div class="wrap">
    <div class="hero-top" style="margin-bottom:10px">
      <a href="{back}" style="color:#d8c9a3;text-decoration:none;font-size:13px">{labels['back']}</a>
      <a class="lang-switch" id="langSwitch" href="{'service.html' if fa else 'service_fa.html'}" lang="{'en' if fa else 'fa'}" dir="{'ltr' if fa else 'rtl'}">{'English' if fa else 'فارسی'}</a>
    </div>
    <div id="serviceHead"></div>
  </div>
</header>
<main class="wrap">
  <section><div class="section-head"><h2>{labels['kpi']}</h2></div><div class="kpi-grid" id="kpis"></div></section>
  <section><div class="section-head"><h2>{labels['canvas']}</h2></div><div class="bmc-grid" id="canvas"></div></section>
  <section class="grid-2">
    <div class="panel" style="padding:18px 20px">
      <h2 style="font-size:20px;margin-bottom:12px">{labels['pl']}</h2>
      <div class="table-scroll" style="max-height:none">
        <table class="pl-table"><thead><tr><th>{'قلم' if fa else 'Line item'}</th><th>{'مبنای محاسبه' if fa else 'Basis'}</th><th>{'تومان/ماه' if fa else 'Toman/month'}</th>{'' if fa else '<th>USD/month</th>'}</tr></thead><tbody id="plRows"></tbody></table>
      </div>
    </div>
    <div class="panel" style="padding:18px 20px">
      <h2 style="font-size:20px;margin-bottom:14px">{labels['flows']}</h2>
      <div class="flow-bars" id="flows"></div>
    </div>
  </section>
  <section class="panel prose">
    <h2>{labels['method']}</h2>
    <p>{'اعداد این صفحه از مدل ماه ۱۲ نسخه v3.1 است: فعال‌سازی کالیبره‌شده با Latka Iran، حقوق کامل ۱۴۰۵، کمیسیون کانال، ریسک چک صیادی و تورم ماهانه ۷ تا ۹ درصد. ستون‌های دلاری انگلیسی با نرخ ۲۷۰٬۰۰۰ تومان محاسبه شده‌اند؛ نرخ گزارش اصلی ۲۰۳٬۱۰۰ تومان بود.' if fa else 'Figures come from the v3.1 Month-12 run rate: Latka-calibrated activation, fully loaded 1405 payroll, channel commissions, SAYAD cheque risk and 7-9% monthly inflation. English USD columns use 270,000 Toman; the source audit used 203,100.'}</p>
    <div class="nav-pager" id="pager"></div>
  </section>
</main>
<footer><div class="wrap"><div>{'مستربوک ترکیبی v3.1' if fa else 'Combined Masterbook v3.1'}</div><div><a href="{back}">{'داشبورد' if fa else 'Dashboard'}</a></div></div></footer>
"""
    return page(title, lang, direction, body, script)


# ---------------------------------------------------------------- reports


def md_table(headers, rows) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def report_en() -> str:
    t = TOTALS
    sector_rows = [
        [a["sector"], a["count"], f"{a['mrr']/1e9:.2f}", f"{a['ebitda']/1e9:.2f}", f"{a['margin']:.1f}%", a["p1"]]
        for a in SECTOR_AGGS
    ]
    top_rows = [
        [s["id"], s["title"], s["tier"], f"{s['_mrr']/1e6:,.0f}", f"{s['_ebitda']/1e6:,.0f}", f"{s['standalone_margin']:.1f}%", f"{s['ltv_cac']:.1f}x"]
        for s in TOP25
    ]
    cat_rows = [
        [s["id"], s["title"], s["sector"].split(":")[0], s["tier"], s["buyer"], "Legacy" if s.get("origin") == "legacy" else "Audited", f"{s['_mrr']/1e6:,.0f}", f"{s['_ebitda']/1e6:,.0f}", f"{s['standalone_margin']:.1f}%"]
        for s in SERVICES
    ]
    p1 = [s for s in SERVICES if s["tier"] == "P1"]
    return f"""# Iran AI SaaS Masterbook — Combined Edition v3.1

**310 stress-tested business models across 20 Iranian sectors: 200 audited + 110 legacy re-underwritten**  
Month-12 run rate · 1405 SH assumptions · all financials in Toman · USD at 270,000 T/USD

## 1. Executive summary

This combined edition carries the 200 audited v3 services alongside 110 unique services from the earlier 120-service v1 catalogue, re-underwritten into the same nine-block Business Model Canvas and Month-12 P&L model. At the Month-12 run rate the portfolio bills **{t['mrr']/1e9:.1f}B Toman** gross MRR, collects **{t['net']/1e9:.1f}B Toman** net of bad debt and DSO lag, and produces **{t['ebitda']/1e9:.1f}B Toman** of standalone EBITDA ({t['avg_margin']:.1f}% average margin). Shared-engine portfolio EBITDA rises to **{t['portfolio']/1e9:.1f}B Toman** per month.

Tier distribution is 112 P1, 155 P2 and 43 P3. By verdict, 157 models are strong standalone wedges, 127 are viable standalone or strong portfolio add-ons, and 26 are shared-engine add-ons because their standalone overhead cannot be recovered at their price point. Ten services post negative standalone EBITDA: the two audited exceptions (#104, #140) and eight thin-margin legacy migrations.

## 2. Provenance and legacy migration

| Cohort | Services | Source | Treatment |
|---|---|---|---|
| Audited v3 | 200 | IRAN AI SaaS MASTERBOOK v3 docx (late 2026/1405) | Verbatim audited BMC and Month-12 P&L |
| Legacy v1 → v3 | 110 | Earlier 120-service catalogue | Re-underwritten with the v3 financial engine, 1405 unit costs and same 9-block canvas |

The legacy cohort started at 120 services. Ten were exact product overlaps with audited services and were removed in favour of the audited version: old #27→#26 (SME credit scoring), #50→#46 (lab-report explainer), #59→#57 (plagiarism detection), #63→#82 (property valuation), #71→#84 (route optimisation), #81→#71 (predictive maintenance), #82→#72 (visual quality inspection), #86→#77 (crop disease detection), #94→#67 (employee surveys) and #116→#100 (data labelling). The remaining 110 retain their original concept, buyer and Persian source canvas, but their prices, active base, churn, GPU/NIN cost, payroll, partner commission, bad debt and shared-engine economics are rebuilt with the v3 model. They are labelled "Legacy" in the dashboard, service pages and CSV; they are not part of the audited docx.

## 3. What the audit corrected

| Flaw in v2 | Iranian market reality | v3 correction |
|---|---|---|
| Revenue optimism | Latka's Iranian SaaS sample averages roughly $480k ARR after 5-8 years | M12 counts recalibrated to 22-40 enterprise, 115-205 SME and 340-480 prosumer accounts |
| Missing labour accruals | 1405 labour law requires Tamin, Eidi (16.7%) and Sanavat (8.33%) | Fully loaded FTE costs: 96M AI engineer, 60M full-stack, 40M sales, 28.5M support |
| Zero channel commissions | Bazaar/Myket take 15-20% + VAT; ERP dealers demand 15-25% | Explicit 12-18% partner commission on 65% partner-sourced revenue |
| No bad debt or DSO | 60-day SAYAD cheques lose 14-18% of real value at 7-9% monthly inflation | 2.5% prosumer, 4.5% SME, 6.5% enterprise bad-debt/DSO provision |
| Unrealistic EBITDA and LTV:CAC | Healthy Iranian B2B SaaS runs 20-38% EBITDA and 6-14x LTV:CAC | Recomputed CAC, payback, break-even and shared-engine economics |
| Standalone overhead for every tool | Low-ticket consumer tools cannot carry a standalone office | Every service reports standalone and shared-engine EBITDA |

## 4. Audited 1405 unit-cost reference

| Parameter | 1405 figure (Toman) | Treatment |
|---|---|---|
| Open-market FX | 203,100 T/USD (source audit) | Project convention: 270,000 T/USD |
| Domestic 48GB GPU node | 150,000,000 / month | Includes 25% peak buffer |
| NIN CPU/DB/BGP relay | 24,500,000-42,000,000 / month | Domestic servers plus relay |
| Partner commission | 12-18% on 65% of revenue | Variable COGS |
| Bad debt and DSO | 2.5% / 4.5% / 6.5% | Prosumer / SME / enterprise |
| Senior AI engineer | 96,000,000 / month | Fully loaded |
| Full-stack developer | 60,000,000 / month | Fully loaded |
| B2B sales closer | 40,000,000 / month | Fully loaded |
| Support specialist | 28,500,000 / month | Fully loaded |

## 5. Sector economics

{md_table(["Sector", "Services", "MRR (B T)", "EBITDA (B T)", "Avg margin", "P1"], sector_rows)}

## 6. Top 25 by standalone EBITDA

{md_table(["#", "Service", "Tier", "MRR (M T)", "EBITDA (M T)", "Margin", "LTV:CAC"], top_rows)}

## 7. Tier P1 shortlist

{md_table(["#", "Service", "Sector"], [[s["id"], s["title"], s["sector"]] for s in p1])}

## 8. Full 310-service catalogue

{md_table(["#", "Service", "Sector", "Tier", "Buyer", "Origin", "MRR (M T)", "EBITDA (M T)", "Margin"], cat_rows)}

## 9. Method and caveats

- Revenue is a Month-12 run rate, not a first-month forecast. Ramp curves are not included in the source audit.
- All Toman figures are nominal at the 1405 price level. Quarterly CPI/FX indexation is a management action, not an automatic model output.
- USD columns in the HTML dashboards are derived at the project rate of 270,000 T/USD. The source audit used 203,100; do not mix the two.
- Customer counts and churn are calibrated from Latka Iran benchmarks and sector interviews, not from a bottom-up sales pipeline.
- The portfolio case assumes shared engineering, office and compliance costs across three sibling tools. It is not additive across all 310 services.
- The 110 legacy services are re-underwritten estimates, not audited docx outputs. Their provenance flag is carried through the dashboard, service pages and CSV.

Source: `data/masterbook.json` + `data/legacy_services.json` · Persian edition: `fa.html` · Service detail: `service.html?id=N`
"""


def report_fa() -> str:
    t = TOTALS
    sector_rows = [
        [a["sector_fa"], fa_digits(a["count"]), fa_dec(a["mrr"] / 1e9, 2), fa_dec(a["ebitda"] / 1e9, 2), fa_pct(a["margin"]), fa_digits(a["p1"])]
        for a in SECTOR_AGGS
    ]
    top_rows = [
        [fa_digits(s["id"]), FA_SERVICES[str(s["id"])]["title"], TIERS_FA.get(s["tier"], s["tier"]), fa_dec(s["_mrr"] / 1e6), fa_dec(s["_ebitda"] / 1e6), fa_pct(s["standalone_margin"]), f"{fa_dec(s['ltv_cac'])}x"]
        for s in TOP25
    ]
    cat_rows = [
        [fa_digits(s["id"]), FA_SERVICES[str(s["id"])]["title"], SECTORS_FA.get(s["sector"], s["sector"]), TIERS_FA.get(s["tier"], s["tier"]), FA_SERVICES[str(s["id"])]["buyer"], "بازنویسی‌شده" if s.get("origin") == "legacy" else "حسابرسی‌شده", fa_dec(s["_mrr"] / 1e6), fa_dec(s["_ebitda"] / 1e6), fa_pct(s["standalone_margin"])]
        for s in SERVICES
    ]
    p1 = [s for s in SERVICES if s["tier"] == "P1"]
    return f"""# مستربوک SaaS هوش مصنوعی ایران — نسخه ترکیبی v3.1

**۳۱۰ مدل کسب‌وکار آزمون‌شده در ۲۰ بخش بازار ایران: ۲۰۰ حسابرسی‌شده + ۱۱۰ بازنویسی‌شده**  
نرخ اجرایی ماه ۱۲ · فرض‌های سال ۱۴۰۵ · همه مبالغ به تومان · دلار با نرخ ۲۷۰٬۰۰۰ تومان

## ۱. خلاصه مدیریتی

این نسخه ترکیبی، ۲۰۰ سرویس حسابرسی‌شده v3 را در کنار ۱۱۰ سرویس یکتای کاتالوگ ۱۲۰ سرویسی v1 نگه می‌دارد که با همان بوم ۹بخشی و مدل مالی ماه ۱۲ بازنویسی شده‌اند. در نرخ اجرایی ماه ۱۲، سبد **{fa_dec(t['mrr']/1e9,1)} میلیارد تومان** MRR ناخالص صورتحساب می‌کند، **{fa_dec(t['net']/1e9,1)} میلیارد تومان** خالص پس از مطالبات مشکوک و تأخیر وصول دریافت می‌کند و **{fa_dec(t['ebitda']/1e9,1)} میلیارد تومان** EBITDA مستقل می‌سازد (میانگین حاشیه {fa_pct(t['avg_margin'])}). EBITDA سبد موتور مشترک به **{fa_dec(t['portfolio']/1e9,1)} میلیارد تومان** در ماه می‌رسد.

۱۱۲ سرویس در اولویت ۱، ۱۵۵ سرویس در اولویت ۲ و ۴۳ سرویس در اولویت ۳ قرار دارند. بر اساس حکم، ۱۵۷ مدل «محصول مستقل قوی»، ۱۲۷ مدل «مستقل قابل‌دوام/مکمل قوی سبد» و ۲۶ مدل فقط «مکمل موتور مشترک» هستند، چون سربار مستقل آن‌ها در قیمت فروش پوشش داده نمی‌شود. ده سرویس EBITDA مستقل منفی دارند: دو استثنای حسابرسی‌شده (#۱۰۴ و #۱۴۰) و هشت سرویس بازنویسی‌شده با حاشیه نازک.

## ۲. منشأ داده و مهاجرت نسخه قدیمی

| گروه | تعداد | منبع | نحوه رفتار |
|---|---|---|---|
| حسابرسی‌شده v3 | ۲۰۰ | سند مستربوک v3 (پایان ۲۰۲۶/۱۴۰۵) | بوم و صورت سود و زیان حسابرسی‌شده |
| قدیمی v1 → v3 | ۱۱۰ | کاتالوگ ۱۲۰ سرویسی قبلی | بازنویسی با موتور مالی v3، هزینه‌های واحد ۱۴۰۵ و همان بوم ۹بخشی |

کاتالوگ قدیمی ۱۲۰ سرویس داشت. ده سرویس هم‌پوشانی کامل محصولی با نسخه حسابرسی‌شده داشتند و به نفع نسخه حسابرسی‌شده حذف شدند: #۲۷→#۲۶ (اعتبارسنجی SME)، #۵۰→#۴۶ (توضیح آزمایش)، #۵۹→#۵۷ (تشخیص سرقت علمی)، #۶۳→#۸۲ (ارزش‌گذاری ملک)، #۷۱→#۸۴ (مسیریابی)، #۸۱→#۷۱ (نگهداری پیش‌بین)، #۸۲→#۷۲ (بازرسی بصری)، #۸۶→#۷۷ (تشخیص بیماری گیاه)، #۹۴→#۶۷ (نظرسنجی کارکنان) و #۱۱۶→#۱۰۰ (برچسب‌گذاری داده). ۱۱۰ سرویس باقی‌مانده مفهوم، خریدار و بوم فارسی اصلی خود را حفظ کرده‌اند، اما قیمت، پایه فعال، ریزش، هزینه GPU/NIN، حقوق، کمیسیون شریک، بدهی بد و اقتصاد موتور مشترک آن‌ها با مدل v3 بازسازی شده است. این سرویس‌ها در داشبورد، صفحه جزئیات و CSV با برچسب «بازنویسی‌شده» مشخص می‌شوند و بخشی از سند حسابرسی‌شده نیستند.

## ۳. اصلاح‌های حسابرسی

| ایراد نسخه v2 | واقعیت بازار ایران | اصلاح در v3 |
|---|---|---|
| خوش‌بینی درآمدی | نمونه SaaS ایران در Latka پس از ۵ تا ۸ سال حدود ۴۸۰ هزار دلار ARR دارد | تعداد مشتری ماه ۱۲ به ۲۲ تا ۴۰ سازمانی، ۱۱۵ تا ۲۰۵ SME و ۳۴۰ تا ۴۸۰ حرفه‌ای/خرد کالیبره شد |
| نبود تعهدات قانون کار | قانون کار ۱۴۰۵ تأمین، عیدی (۱۶٫۷٪) و سنوات (۸٫۳۳٪) را الزامی می‌کند | هزینه کامل هر نفر: مهندس AI ۹۶ میلیون، فول‌استک ۶۰ میلیون، فروش ۴۰ میلیون و پشتیبانی ۲۸٫۵ میلیون تومان |
| صفر بودن کمیسیون کانال | بازار/مایکت ۱۵ تا ۲۰ درصد + مالیات و نمایندگان ERP ۱۵ تا ۲۵ درصد می‌گیرند | کمیسیون صریح ۱۲ تا ۱۸ درصد روی ۶۵ درصد درآمد شریک‌محور |
| نبود بدهی بد و DSO | چک ۶۰ روزه صیادی با تورم ماهانه ۷ تا ۹ درصد، ۱۴ تا ۱۸ درصد قدرت خرید را از بین می‌برد | ذخیره ۲٫۵ درصد حرفه‌ای، ۴٫۵ درصد SME و ۶٫۵ درصد سازمانی |
| EBITDA و LTV:CAC غیرواقعی | SaaS سالم ایران حاشیه ۲۰ تا ۳۸ درصد و LTV:CAC ۶ تا ۱۴ برابر دارد | CAC، بازگشت، سربه‌سر و اقتصاد موتور مشترک بازمحاسبه شد |
| سربار مستقل برای همه ابزارها | ابزارهای کم‌قیمت مصرفی نمی‌توانند دفتر مستقل را بپوشانند | هر سرویس هم EBITDA مستقل و هم موتور مشترک را گزارش می‌کند |

## ۴. مرجع هزینه واحد ۱۴۰۵

| پارامتر | رقم ۱۴۰۵ (تومان) | نحوه اعمال |
|---|---|---|
| نرخ ارز آزاد | ۲۰۳٬۱۰۰ تومان به ازای هر دلار (گزارش مبنا) | قرارداد پروژه: ۲۷۰٬۰۰۰ تومان |
| گره GPU داخلی ۴۸ گیگابایت | ۱۵۰٬۰۰۰٬۰۰۰ در ماه | شامل ۲۵٪ بافر پیک |
| CPU/DB/رله NIN | ۲۴٬۵۰۰٬۰۰۰ تا ۴۲٬۰۰۰٬۰۰۰ در ماه | سرور داخلی + رله |
| کمیسیون شریک | ۱۲ تا ۱۸ درصد روی ۶۵٪ درآمد | بهای تمام‌شده متغیر |
| بدهی بد و DSO | ۲٫۵٪ / ۴٫۵٪ / ۶٫۵٪ | حرفه‌ای / SME / سازمانی |
| مهندس ارشد AI | ۹۶٬۰۰۰٬۰۰۰ در ماه | هزینه کامل |
| توسعه‌دهنده فول‌استک | ۶۰٬۰۰۰٬۰۰۰ در ماه | هزینه کامل |
| کارشناس فروش B2B | ۴۰٬۰۰۰٬۰۰۰ در ماه | هزینه کامل |
| متخصص پشتیبانی | ۲۸٬۵۰۰٬۰۰۰ در ماه | هزینه کامل |

## ۵. اقتصاد بخش‌ها

{md_table(["بخش", "تعداد", "MRR (میلیارد ت)", "EBITDA (میلیارد ت)", "میانگین حاشیه", "اولویت ۱"], sector_rows)}

## ۶. ۲۵ سرویس برتر بر اساس EBITDA مستقل

{md_table(["#", "سرویس", "سطح", "MRR (میلیون ت)", "EBITDA (میلیون ت)", "حاشیه", "LTV:CAC"], top_rows)}

## ۷. فهرست اولویت ۱

{md_table(["#", "سرویس", "بخش"], [[fa_digits(s["id"]), FA_SERVICES[str(s["id"])]["title"], SECTORS_FA.get(s["sector"], s["sector"])] for s in p1])}

## ۸. کاتالوگ کامل ۳۱۰ سرویس

{md_table(["#", "سرویس", "بخش", "سطح", "خریدار", "منشأ", "MRR (میلیون ت)", "EBITDA (میلیون ت)", "حاشیه"], cat_rows)}

## ۹. روش و محدودیت‌ها

- درآمد، نرخ اجرایی ماه ۱۲ است، نه پیش‌بینی ماه اول. منحنی رشد در گزارش مبنا ارائه نشده است.
- همه ارقام تومانی اسمی و در سطح قیمت ۱۴۰۵ هستند. شاخص‌بندی فصلی CPI/ارز یک اقدام مدیریتی است، نه خروجی خودکار مدل.
- ستون‌های دلاری داشبورد انگلیسی با نرخ قرارداد پروژه ۲۷۰٬۰۰۰ تومان ساخته شده‌اند. گزارش مبنا از ۲۰۳٬۱۰۰ استفاده کرده بود؛ این دو نرخ را با هم مخلوط نکنید.
- تعداد مشتری و ریزش از معیارهای Latka Iran و مصاحبه‌های بخشی کالیبره شده‌اند، نه از قیف فروش پایین‌به‌بالا.
- سناریوی سبد فرض می‌کند هزینه مهندسی، دفتر و انطباق بین سه ابزار هم‌خانواده تقسیم شود. این عدد برای ۳۱۰ سرویس جمع‌شدنی نیست.
- ۱۱۰ سرویس بازنویسی‌شده برآورد مدل‌محور هستند، نه خروجی سند حسابرسی‌شده. برچسب منشأ آن‌ها در داشبورد، صفحه جزئیات و CSV حفظ می‌شود.

منبع: `data/masterbook.json` + `data/legacy_services.json` · نسخه انگلیسی: `index.html` · جزئیات سرویس: `service_fa.html?id=N`
"""


# ---------------------------------------------------------------- CSV


def write_csvs():
    headers_en = [
        "id", "origin", "sector", "service", "tier", "verdict", "buyer", "segment", "engine",
        "active_accounts", "monthly_churn_pct", "gross_mrr_toman", "net_collected_mrr_toman",
        "gross_margin_pct", "standalone_ebitda_toman", "standalone_margin_pct",
        "portfolio_ebitda_toman", "portfolio_margin_pct", "cac_toman", "cac_payback_months",
        "ltv_cac", "break_even_customers", "arpu_toman", "usd_rate_toman",
    ]
    with (DATA / "iran-ai-saas-masterbook-310.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers_en)
        for s in SERVICES:
            w.writerow([
                s["id"], s.get("origin", "audited"), s["sector"], s["title"], s["tier"], s["verdict"], s["buyer"], s["segment"], s["engine"],
                s["active"]["accounts"] if s["active"] else 0, s["churn"], round(s["_mrr"]), round(s["_net"]),
                round(s["_gm"], 2), round(s["_ebitda"]), round(s["standalone_margin"], 2),
                round(s["portfolio_ebitda"]), round(s["portfolio_margin"], 2), round(s["cac"]), s["payback"],
                s["ltv_cac"], s["be_customers"], round(s["_arpu"]), USD_TOMAN,
            ])

    headers_fa = [
        "شماره", "منشأ", "بخش", "سرویس", "سطح", "حکم", "خریدار", "بخش مشتری", "موتور",
        "حساب فعال", "ریزش ماهانه ٪", "MRR ناخالص (تومان)", "MRR خالص (تومان)",
        "حاشیه ناخالص ٪", "EBITDA مستقل (تومان)", "حاشیه مستقل ٪",
        "EBITDA سبد (تومان)", "حاشیه سبد ٪", "CAC (تومان)", "بازگشت CAC (ماه)",
        "LTV:CAC", "مشتری سربه‌سر", "ARPU (تومان)", "نرخ دلار (تومان)",
    ]
    with (DATA / "iran-ai-saas-masterbook-310-fa.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(headers_fa)
        for s in SERVICES:
            fa = FA_SERVICES[str(s["id"])]
            w.writerow([
                s["id"], "بازنویسی‌شده" if s.get("origin") == "legacy" else "حسابرسی‌شده", SECTORS_FA.get(s["sector"], s["sector"]), fa["title"], TIERS_FA.get(s["tier"], s["tier"]),
                VERDICTS_FA.get(s["verdict"], s["verdict"]), fa["buyer"], SEGMENTS_FA.get(s["segment"], s["segment"]),
                ENGINES_FA.get(s["engine"], s["engine"]), s["active"]["accounts"] if s["active"] else 0, s["churn"],
                round(s["_mrr"]), round(s["_net"]), round(s["_gm"], 2), round(s["_ebitda"]),
                round(s["standalone_margin"], 2), round(s["portfolio_ebitda"]), round(s["portfolio_margin"], 2),
                round(s["cac"]), s["payback"], s["ltv_cac"], s["be_customers"], round(s["_arpu"]), USD_TOMAN,
            ])


def main():
    (ROOT / "index.html").write_text(dashboard_html(False), encoding="utf-8")
    (ROOT / "fa.html").write_text(dashboard_html(True), encoding="utf-8")
    (ROOT / "service.html").write_text(service_page_html(False), encoding="utf-8")
    (ROOT / "service_fa.html").write_text(service_page_html(True), encoding="utf-8")
    (ROOT / "iran-ai-saas-report-v3.1.md").write_text(report_en(), encoding="utf-8")
    (ROOT / "iran-ai-saas-report-v3.1-fa.md").write_text(report_fa(), encoding="utf-8")
    write_csvs()
    for name in ["index.html", "fa.html", "service.html", "service_fa.html", "iran-ai-saas-report-v3.1.md", "iran-ai-saas-report-v3.1-fa.md"]:
        print(f"wrote {name} ({(ROOT / name).stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
