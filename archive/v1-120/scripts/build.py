import csv
import json
from pathlib import Path

from data import SERVICES, CATEGORIES
from fa import (
    CATEGORY_FA, MODEL_FA, DIFFICULTY_FA, COMPETITION_FA, TTR_FA, SERVICE_FA,
)
from bmc import USD_TOMAN, build_bmc

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

CSV_FIELDS = [
    "id", "category", "name", "what", "buyer", "ai", "wedge", "model", "price",
    "market", "competition", "difficulty", "capital", "ttr",
    "demand", "wtp", "feasibility", "defensibility", "capital_efficiency", "score",
]

CSV_FIELDS_FA = [
    "id", "category_fa", "name_fa", "what_fa", "buyer_fa", "wedge_fa", "ai",
    "model_fa", "price_fa", "difficulty_fa", "competition_fa", "capital_fa",
    "ttr_fa", "demand", "wtp", "feasibility", "defensibility",
    "capital_efficiency", "score", "arpu_toman", "revenue_y1", "costs_y1",
    "net_y1", "gross_margin", "break_even", "capital_need",
]

FA_DIGITS = str.maketrans("0123456789.", "۰۱۲۳۴۵۶۷۸۹٫")


def fa_num(value):
    return str(value).translate(FA_DIGITS)


def _fa_number(value, digits=1):
    if abs(value - round(value)) < 0.05:
        text = f"{round(value):,}"
    else:
        text = f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    return text.translate(FA_DIGITS)


def _toman_parts(amount):
    amount = abs(amount)
    if amount >= 1_000_000_000:
        return amount / 1_000_000_000, "میلیارد تومان"
    if amount >= 1_000_000:
        return amount / 1_000_000, "میلیون تومان"
    return amount / 1_000, "هزار تومان"


def _toman_range(low, high):
    unit_value = max(low, high)
    low_value, unit = _toman_parts(unit_value)
    low_scaled = low / (unit_value / low_value) if unit_value else 0
    high_scaled = high / (unit_value / low_value) if unit_value else 0
    return f"{_fa_number(low_scaled)} تا {_fa_number(high_scaled)} {unit}"


def fa_price(price):
    if price == "10-30% of GMV":
        return "۱۰ تا ۳۰٪ از ارزش ناخالص معامله"
    if price == "3-8% of freight":
        return "۳ تا ۸٪ از کرایه حمل"
    body = price.lstrip("$")
    parts = body.split("/")
    amount = parts[0]
    units = parts[1:]
    values = []
    for token in amount.split("-"):
        try:
            multiplier = 1000 if token.endswith("k") else 1
            values.append(float(token[:-1] if multiplier == 1000 else token) * multiplier * USD_TOMAN)
        except ValueError:
            values.append(0.0)
    if len(values) == 1:
        values.append(values[0])
    low, high = values[0], values[1]
    unit_fa = {
        "min": "دقیقه", "dev": "توسعه‌دهنده", "user": "کاربر", "case": "پرونده",
        "employee": "کارمند", "vehicle": "خودرو", "driver": "راننده", "mo": "ماه",
    }
    if units and units[-1] == "mo":
        tail = "در ماه"
        if len(units) > 1:
            tail = f"برای هر {unit_fa.get(units[0], units[0])} در ماه"
    elif units:
        tail = f"برای هر {unit_fa.get(units[0], units[0])}"
    else:
        tail = "در ماه"
    return f"{_toman_range(low, high)} {tail}"


def write_csv():
    path = DATA_DIR / "iran-ai-saas-services.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for item in SERVICES:
            writer.writerow({key: item[key] for key in CSV_FIELDS})
    return path


def write_json():
    path = DATA_DIR / "iran-ai-saas-services.json"
    path.write_text(json.dumps(SERVICES, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_catalogue():
    parts = []
    for category in CATEGORIES:
        items = [item for item in SERVICES if item["category"] == category]
        avg = round(sum(item["score"] for item in items) / len(items), 1)
        parts.append(f"### {category}")
        parts.append("")
        parts.append(f"*{len(items)} services, average opportunity score {avg}/100.*")
        parts.append("")
        parts.append("| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |")
        parts.append("|---:|---|---|---|---|---|---:|")
        for item in items:
            parts.append(
                f"| {item['id']} | **{item['name']}** | {item['buyer']} | {item['wedge']} | "
                f"{item['price']} | {item['model']} | {item['score']} |"
            )
        parts.append("")
    return "\n".join(parts)


def build_top_table(limit=25):
    ranked = sorted(SERVICES, key=lambda item: (-item["score"], -item["demand"], item["id"]))[:limit]
    lines = [
        "| Rank | Service | Category | Score | Why it ranks |",
        "|---:|---|---|---:|---|",
    ]
    for rank, item in enumerate(ranked, start=1):
        lines.append(
            f"| {rank} | **{item['name']}** | {item['category']} | {item['score']} | {item['what']} |"
        )
    return "\n".join(lines)


def build_category_summary():
    rows = []
    for category in CATEGORIES:
        items = [item for item in SERVICES if item["category"] == category]
        avg = round(sum(item["score"] for item in items) / len(items), 1)
        best = max(items, key=lambda item: item["score"])
        rows.append((category, len(items), avg, best["name"], best["score"]))
    rows.sort(key=lambda row: -row[2])
    lines = [
        "| Category | Services | Avg. score | Highest-scoring service | Score |",
        "|---|---:|---:|---|---:|",
    ]
    for category, count, avg, best, best_score in rows:
        lines.append(f"| {category} | {count} | {avg} | {best} | {best_score} |")
    return "\n".join(lines)


def build_report():
    template = (TEMPLATE_DIR / "report_template.md").read_text(encoding="utf-8")
    output = (
        template
        .replace("{{CATALOGUE}}", build_catalogue())
        .replace("{{TOP25}}", build_top_table(25))
        .replace("{{CATEGORY_SUMMARY}}", build_category_summary())
        .replace("{{TOTAL}}", str(len(SERVICES)))
        .replace("{{CATEGORY_COUNT}}", str(len(CATEGORIES)))
    )
    path = ROOT / "iran-ai-saas-report.md"
    path.write_text(output, encoding="utf-8")
    return path


def build_dashboard():
    template = (TEMPLATE_DIR / "dashboard.html").read_text(encoding="utf-8")
    output = (
        template
        .replace("__SERVICES_JSON__", json.dumps(SERVICES, ensure_ascii=False))
        .replace("__CATEGORIES_JSON__", json.dumps(CATEGORIES, ensure_ascii=False))
        .replace("__TOTAL__", str(len(SERVICES)))
        .replace("__CATEGORY_COUNT__", str(len(CATEGORIES)))
    )
    path = ROOT / "index.html"
    path.write_text(output, encoding="utf-8")
    return path


def localized_services():
    items = []
    for item in SERVICES:
        name_fa, what_fa, buyer_fa, wedge_fa = SERVICE_FA[item["name"]]
        localized = dict(item)
        localized.update({
            "category_en": item["category"],
            "category": CATEGORY_FA[item["category"]],
            "category_fa": CATEGORY_FA[item["category"]],
            "name_fa": name_fa,
            "what_fa": what_fa,
            "buyer_fa": buyer_fa,
            "wedge_fa": wedge_fa,
            "model_fa": MODEL_FA.get(item["model"], item["model"]),
            "price_fa": fa_price(item["price"]),
            "difficulty_fa": DIFFICULTY_FA.get(item["difficulty"], item["difficulty"]),
            "competition_fa": COMPETITION_FA.get(item["competition"], item["competition"]),
            "capital_fa": item["capital"],
            "ttr_fa": TTR_FA.get(item["ttr"], item["ttr"]),
        })
        items.append(localized)
    return items


def write_csv_fa():
    path = DATA_DIR / "iran-ai-saas-services-fa.csv"
    items = localized_services()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS_FA)
        writer.writeheader()
        for item in items:
            bmc = build_bmc(item)
            financials = bmc["financials"]
            row = {key: item[key] for key in CSV_FIELDS_FA if key in item}
            row.update({
                "arpu_toman": financials["arpu"],
                "revenue_y1": round(financials["revenue_y1"]),
                "costs_y1": round(financials["costs_y1"]),
                "net_y1": round(financials["net_y1"]),
                "gross_margin": round(financials["gross_margin"], 1),
                "break_even": financials["break_even"],
                "capital_need": financials["capital_need"],
            })
            writer.writerow({key: row.get(key, "") for key in CSV_FIELDS_FA})
    return path


def build_catalogue_fa():
    parts = []
    items_all = localized_services()
    for category in CATEGORIES:
        items = [item for item in items_all if item["category_en"] == category]
        avg = round(sum(item["score"] for item in items) / len(items), 1)
        parts.append(f"### {CATEGORY_FA[category]}")
        parts.append("")
        parts.append(f"*{fa_num(len(items))} سرویس، میانگین امتیاز فرصت {fa_num(f'{avg:g}')} از ۱۰۰.*")
        parts.append("")
        parts.append("| # | سرویس | خریدار اصلی | مزیت ایران | بازه قیمت | مدل درآمد | امتیاز |")
        parts.append("|---:|---|---|---|---|---|---:|")
        for item in items:
            parts.append(
                f"| {fa_num(item['id'])} | **[{item['name_fa']}](service.html?id={item['id']})** | {item['buyer_fa']} | "
                f"{item['wedge_fa']} | {item['price_fa']} | {item['model_fa']} | {fa_num('%g' % item['score'])} |"
            )
        parts.append("")
    return "\n".join(parts)


def build_top_table_fa(limit=25):
    ranked = sorted(localized_services(), key=lambda item: (-item["score"], -item["demand"], item["id"]))[:limit]
    lines = [
        "| رتبه | سرویس | دسته‌بندی | امتیاز | دلیل رتبه |",
        "|---:|---|---|---:|---|",
    ]
    for rank, item in enumerate(ranked, start=1):
        lines.append(
            f"| {fa_num(rank)} | **[{item['name_fa']}](service.html?id={item['id']})** | {item['category']} | "
            f"{fa_num('%g' % item['score'])} | {item['what_fa']} |"
        )
    return "\n".join(lines)


def build_category_summary_fa():
    items_all = localized_services()
    rows = []
    for category in CATEGORIES:
        items = [item for item in items_all if item["category_en"] == category]
        avg = round(sum(item["score"] for item in items) / len(items), 1)
        best = max(items, key=lambda item: item["score"])
        rows.append((CATEGORY_FA[category], len(items), avg, best["name_fa"], best["score"]))
    rows.sort(key=lambda row: -row[2])
    lines = [
        "| دسته‌بندی | تعداد سرویس | میانگین امتیاز | بهترین سرویس | امتیاز |",
        "|---|---:|---:|---|---:|",
    ]
    for category, count, avg, best, best_score in rows:
        lines.append(
            f"| {category} | {fa_num(count)} | {fa_num(f'{avg:g}')} | {best} | {fa_num(f'{best_score:g}')} |"
        )
    return "\n".join(lines)


def build_report_fa():
    template = (TEMPLATE_DIR / "report_fa_template.md").read_text(encoding="utf-8")
    output = (
        template
        .replace("{{CATALOGUE_FA}}", build_catalogue_fa())
        .replace("{{TOP25_FA}}", build_top_table_fa(25))
        .replace("{{TOP25}}", build_top_table_fa(25))
        .replace("{{CATEGORY_SUMMARY_FA}}", build_category_summary_fa())
        .replace("{{TOTAL}}", fa_num(len(SERVICES)))
        .replace("{{CATEGORY_COUNT}}", fa_num(len(CATEGORIES)))
    )
    path = ROOT / "iran-ai-saas-report-fa.md"
    path.write_text(output, encoding="utf-8")
    return path


def build_dashboard_fa():
    template = (TEMPLATE_DIR / "dashboard_fa.html").read_text(encoding="utf-8")
    items = localized_services()
    categories = [CATEGORY_FA[category] for category in CATEGORIES]
    output = (
        template
        .replace("__SERVICES_JSON__", json.dumps(items, ensure_ascii=False))
        .replace("__CATEGORIES_JSON__", json.dumps(categories, ensure_ascii=False))
        .replace("__TOTAL__", fa_num(len(items)))
        .replace("__CATEGORY_COUNT__", fa_num(len(categories)))
    )
    path = ROOT / "fa.html"
    path.write_text(output, encoding="utf-8")
    return path


def build_service_page():
    template = (TEMPLATE_DIR / "service_fa.html").read_text(encoding="utf-8")
    items = localized_services()
    bmc_items = [build_bmc(item) for item in items]
    output = (
        template
        .replace("__BMC_JSON__", json.dumps(bmc_items, ensure_ascii=False))
        .replace("{{TITLE}}", "بوم مدل کسب‌وکار ۱۲۰ سرویس")
        .replace("{{TOTAL}}", fa_num(len(items)))
    )
    path = ROOT / "service.html"
    path.write_text(output, encoding="utf-8")
    return path


def write_bmc_json():
    path = DATA_DIR / "business-model-canvas.json"
    payload = [build_bmc(item) for item in localized_services()]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    csv_path = write_csv()
    json_path = write_json()
    csv_fa_path = write_csv_fa()
    bmc_json_path = write_bmc_json()
    report_path = build_report()
    report_fa_path = build_report_fa()
    dashboard_path = build_dashboard()
    dashboard_fa_path = build_dashboard_fa()
    service_page_path = build_service_page()
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_fa_path}")
    print(f"Wrote {bmc_json_path}")
    print(f"Wrote {report_path}")
    print(f"Wrote {report_fa_path}")
    print(f"Wrote {dashboard_path}")
    print(f"Wrote {dashboard_fa_path}")
    print(f"Wrote {service_page_path}")
    print(f"Services: {len(SERVICES)} | Categories: {len(CATEGORIES)}")
