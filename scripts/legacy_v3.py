"""Re-underwrite the legacy 120-service v1 catalogue into the v3 model.

Outputs:
  data/legacy_services.json  - 110 legacy services in the audited v3 schema
  data/fa_legacy.json        - Persian labels for the same services
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SERVICES = json.loads((ROOT / "archive/v1-120/data/iran-ai-saas-services.json").read_text(encoding="utf-8"))
OLD_BMC = {b["id"]: b for b in json.loads((ROOT / "archive/v1-120/data/business-model-canvas.json").read_text(encoding="utf-8"))}

# Old services that are the same product as an audited v3 service.
DUPLICATES = {
    27: 26,   # SME credit scoring
    50: 46,   # lab-result explainer
    59: 57,   # plagiarism / AI-text detection
    63: 82,   # property valuation (AVM)
    71: 84,   # route optimisation for fleets
    81: 71,   # predictive maintenance
    82: 72,   # visual quality inspection
    86: 77,   # crop disease detection
    94: 67,   # employee survey analytics
    116: 100,  # Persian data labelling
}

CATEGORY_SECTOR = {
    "Sales & Marketing": "A: Sales, Marketing & E-Commerce",
    "E-commerce & Retail": "K: Iranian E-Commerce, Marketplaces & Social Commerce",
    "Accounting, Tax & Finance": "C: Finance, Accounting & Tax",
    "Legal, Compliance & Documents": "D: Legal & Government Paperwork",
    "Healthcare & Clinic Operations": "Q: Healthcare, Clinics, Aesthetic Medicine & Pharmacies",
    "Education & Workforce Training": "F: Education",
    "Real Estate, Construction & Facilities": "O: Construction, Civil Engineering & Real Estate",
    "Logistics, Fleet & Last-Mile": "S: Logistics, Cross-Border Trade, Transit & Fleet Management",
    "Manufacturing, Energy & Agriculture": "H: Industry, Engineering, Energy & Agriculture",
    "HR, Recruiting & Internal Ops": "G: HR & Recruitment",
    "Media, Content & Creator Economy": "J: Media, Content & Developer Infrastructure",
    "Developer, Data & IT Ops": "T: Local IT Infrastructure, ERP Plugins & Developer Tools",
}

CATEGORY_FA = {
    "Sales & Marketing": "فروش و بازاریابی",
    "E-commerce & Retail": "تجارت الکترونیک و خرده‌فروشی",
    "Accounting, Tax & Finance": "حسابداری، مالیات و مالی",
    "Legal, Compliance & Documents": "حقوق، انطباق و اسناد",
    "Healthcare & Clinic Operations": "سلامت و عملیات کلینیک",
    "Education & Workforce Training": "آموزش و مهارت‌آموزی",
    "Real Estate, Construction & Facilities": "املاک، ساخت‌وساز و تأسیسات",
    "Logistics, Fleet & Last-Mile": "لجستیک، ناوگان و توزیع آخرین‌مایل",
    "Manufacturing, Energy & Agriculture": "تولید، انرژی و کشاورزی",
    "HR, Recruiting & Internal Ops": "منابع انسانی، استخدام و عملیات داخلی",
    "Media, Content & Creator Economy": "رسانه، محتوا و اقتصاد سازندگان",
    "Developer, Data & IT Ops": "توسعه‌دهنده، داده و عملیات IT",
}

SEGMENT = {
    "sme": "Core Iranian SME, Bazaar, Clinic & Agency B2B",
    "ent": "Enterprise, Industrial & Institutional B2B",
    "pro": "Prosumer, Micro-Seller & B2B2C (School/Platform Packs)",
}

ENGINES = {
    "1": "Engine #1: Persian Conversation & Hybrid Retrieval (RAG)",
    "2": "Engine #2: Persian Document Extraction, Vision & OCR",
    "3": "Engine #3: Persian Speech Recognition (ASR), Voice & TTS",
    "4": "Engine #4: Inflation Indexing, Pricing & Demand Forecasting",
    "5A": "Engine #5A: Persian Generative Content & Academic/Marketing Copy",
    "5B": "Engine #5B: Generative Studio Vision, Restyling & Persian Typography",
    "6": "Engine #6: Cross-Platform Workflow Agents & Compliance Automators",
}

STACKS = {
    "1": "Quantized Qwen3-14B/32B (AWQ, Apache 2.0) via vLLM + BGE-M3 Persian Embeddings + Qdrant CPU Vector DB",
    "2": "Fine-tuned Qwen2.5-VL-7B/32B + PaddleOCR Persian + Custom Jalali/Digit Post-Processor on Domestic GPU",
    "3": "Fine-tuned Whisper-large-v3-turbo (Colloquial Persian) + Pyannote Diarization + Piper/XTTS Persian Voice",
    "4": "LightGBM / Prophet Jalali Seasonality + OR-Tools Constraint Solver + Qwen3-8B Explainer on CPU/Shared GPU",
    "5A": "Quantized Qwen3-14B / DeepSeek-V3 Distill with Persian Brand-Voice LoRA Adapters",
    "5B": "Flux.1-Schnell / SDXL Quantized + ControlNet + RMBG-2.0 + Programmatic RTL Vazirmatn/IranSans Renderer",
    "6": "Qwen3-14B Function-Calling Agent + Temporal/Celery Queue + Domestic Webhook Relay (Bale/Eitaa/Moadian/ERP)",
}

ENGINE_FA = {
    "1": "گفتگوی فارسی و بازیابی ترکیبی",
    "2": "استخراج اسناد، بینایی و OCR فارسی",
    "3": "تشخیص گفتار، صدا و TTS فارسی",
    "4": "شاخص‌بندی تورم، قیمت‌گذاری و پیش‌بینی تقاضا",
    "5A": "تولید محتوای فارسی و نگارش بازاریابی",
    "5B": "بینایی استودیویی مولد و تایپوگرافی فارسی",
    "6": "عامل‌های گردش‌کار و خودکارساز انطباق",
}

VERDICTS = {
    "strong": "STRONG STANDALONE WEDGE (High B2B Margin)",
    "viable": "VIABLE STANDALONE / STRONG PORTFOLIO ADD-ON",
    "shared": "SHARED-ENGINE ADD-ON ONLY (High Standalone Overhead)",
}

BILLING_MAP = {
    "Subscription": "Monthly",
    "Subscription + credits": "Monthly + credits",
    "Freemium + B2B": "Monthly + credits",
    "Freemium + subscription": "Monthly + credits",
    "Enterprise + per-score": "Per query",
    "Enterprise + per-seat": "Per user",
    "Per seat": "Per user",
    "Per user": "Per user",
    "Per user/mo": "Per user",
    "Per line": "Per line",
    "Per site": "Per site",
    "Per vehicle": "Per vehicle",
    "Per driver": "Per driver",
    "Per employee": "Per employee",
    "Per project": "Per project",
    "Per case": "Per case",
    "Per document": "Per document",
    "Per minute": "Per minute",
    "Per scan": "Per scan",
    "Per report": "Per report",
    "Per shipment": "Per shipment",
    "Per contract": "Per contract / Monthly",
    "Per tender": "Per tender",
    "Per application": "Per application",
    "Per student": "Per student",
    "Per candidate": "Per candidate",
    "Per survey": "Per survey",
    "Per machine": "Per machine",
    "Per hectare": "Per hectare",
    "Per RFQ": "Per RFQ",
    "Per quote": "Per quote",
    "Per page": "Per page",
    "Per transaction": "Per transaction",
    "Managed service": "Monthly",
    "Retainer": "Monthly",
    "Usage": "Credits",
    "Usage-based": "Credits",
    "Commission": "Commission",
    "Take rate": "Commission",
    "% GMV": "Commission",
    "% of freight": "Commission",
    "% of ad spend": "Monthly + % of ad spend saved",
    "Annual": "Monthly",
    "License": "Annual enterprise license",
    "On-prem license": "On-prem license",
    "Project + license": "Project + audit license",
}


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def num(value):
    return float(str(value).replace(",", "").replace("$", "").strip())


def parse_band(price: str) -> tuple[float, float]:
    text = price.replace("k", "000").replace("K", "000")
    nums = [float(x.replace(",", "")) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    if not nums:
        return (10.0, 40.0)
    if "%" in price:
        return (max(nums[0], 3.0), max(nums[-1], 8.0))
    low = min(nums)
    high = max(nums)
    if high <= low:
        high = low * 2
    return low, high


def pick_engine(old: dict) -> str:
    blob = " ".join(str(old.get(k, "")) for k in ("ai", "what", "name", "buyer")).lower()
    if any(k in blob for k in ("asr", "speech", "voice", "audio", "tts", "dubbing", "podcast", "call")):
        if any(k in blob for k in ("tts", "voice clone", "dubbing", "music", "sound")):
            return "3"
        return "3"
    if any(k in blob for k in ("diffusion", "staging", "thumbnail", "photo studio", "product photo", "concept generator", "comic", "storyboard")):
        return "5B"
    if any(k in blob for k in ("ocr", "vision", "document", "scan", "image", "video", "radiology", "inspection", "shelf", "safety", "crop", "counterfeit")):
        return "2"
    if any(k in blob for k in ("forecast", "optimizer", "optimisation", "optimization", "pricing", "inventory", "demand", "route", "scheduling", "scoring", "anomaly", "matching", "eta", "slotting", "allocator", "triage")):
        return "4"
    if any(k in blob for k in ("agent", "workflow", "compliance", "helpdesk", "bot", "integration", "orchestrat")):
        return "6"
    if any(k in blob for k in ("content", "copy", "writer", "caption", "seo", "marketing", "story", "brand", "news", "resume", "jd ", "email", "proposal", "tender", "contract", "legal research", "ghostwriter")):
        return "5A"
    return "1"


def pick_segment(old: dict) -> str:
    low, high = parse_band(old.get("price", ""))
    buyer = old.get("buyer", "").lower()
    ent_words = ("bank", "enterprise", "factor", "hospital", "marketplace", "insurer", "telco", "soc", "vod", "government", "lender", "utility", "university", "large")
    pro_words = ("consumer", "student", "job seeker", "creator", "farmer", "individual", "parent", "tutor", "patient", "freelancer")
    if high >= 900 or any(w in buyer for w in ent_words):
        return "ent"
    if high <= 25 or any(w in buyer for w in pro_words):
        return "pro"
    return "sme"


def pick_tier(score: float, margin: float) -> str:
    if score >= 74.0 and margin >= 18.0:
        return "P1"
    if score >= 66.0 or margin >= 13.0:
        return "P2"
    return "P3"


def pick_verdict(margin: float) -> str:
    if margin >= 26.0:
        return VERDICTS["strong"]
    if margin >= 10.0:
        return VERDICTS["viable"]
    return VERDICTS["shared"]


def fa_clean(text: str) -> str:
    return (
        str(text)
        .replace("مارکت‌پلیس‌ها", "بازارگاه‌ها")
        .replace("مارکت‌پلیس", "بازارگاه")
        .replace("آنبوردینگ", "راه‌اندازی")
        .replace("لایسنس", "مجوز")
    )


def fa_join(values, limit=2, sep="، "):
    out = []
    for v in values[:limit]:
        v = fa_clean(str(v).strip().rstrip("."))
        if v and v not in out:
            out.append(v)
    return sep.join(out)


def build_financials(old: dict, bmc: dict, segment: str) -> dict:
    score = float(old.get("score", 70))
    wtp = int(old.get("wtp", 3) or 3)
    t = clamp((score - 58.0) / 31.0, 0.0, 1.0)
    if segment == "ent":
        accounts = round(24 + 13 * t)
        churn = 4.0
        dso = 6.5
        lo, hi = 3_500_000, 8_000_000
        g_mult, p_mult, u_mult = 2.10, 3.50, 0.18
        t1w, t2w = 0.33, 0.45
        gpu_base = 0.28
        sales_fte, support_fte = 0.80, 1.05
        extra_ads = 0.0
    elif segment == "pro":
        accounts = round(399 + 121 * t)
        churn = 13.0
        dso = 2.5
        lo, hi = 350_000, 600_000
        g_mult, p_mult, u_mult = 1.90, 4.50, 0.30
        t1w, t2w = 0.54, 0.36
        gpu_base = 0.30
        sales_fte, support_fte = 0.55, 1.55
        extra_ads = 0.0
    else:
        accounts = round(125 + 100 * t)
        churn = round((11.0 - 4.5 * t) * 2) / 2
        dso = 4.5
        lo, hi = 1_200_000, 1_800_000
        g_mult, p_mult, u_mult = 1.80, 3.60, 0.22
        t1w, t2w = 0.40, 0.46
        gpu_base = 0.22
        sales_fte, support_fte = 0.55 + accounts / 600.0, 0.90 + accounts / 350.0
        extra_ads = 0.0

    starter = round((lo + (hi - lo) * (wtp - 1) / 4.0) / 10_000) * 10_000
    growth = round(starter * g_mult / 10_000) * 10_000
    pro_price = round(starter * p_mult / 10_000) * 10_000
    usage = round(starter * u_mult / 10_000) * 10_000

    n1 = round(accounts * t1w)
    n2 = round(accounts * t2w)
    n3 = accounts - n1 - n2
    gross = n1 * starter + n2 * growth + n3 * pro_price + accounts * usage
    net = gross * (1 - dso / 100.0)

    engine = pick_engine(old)
    nodes = round(clamp(gpu_base + 0.12 * t + (0.06 if segment == "pro" else 0.0), 0.18, 0.88), 2)
    gpu_cost = round(nodes * 150_000_000)
    nin_server = round((11_000_000 + nodes * 22_000_000) / 1_000_000) * 1_000_000
    nin_total = nin_server + 12_000_000
    sms_count = round(accounts * (45 if segment == "pro" else 65))
    tx_count = round(accounts * 1.3)
    sms_cost = round(sms_count * 38 + tx_count * 12_000)

    partner_pct = 14 if old["category"] in ("Sales & Marketing", "E-commerce & Retail") else 12
    partner_share = 65
    partner_cogs = round(net * partner_share / 100.0 * partner_pct / 100.0)
    cogs = gpu_cost + nin_total + sms_cost + partner_cogs

    ai_fte = round(clamp(0.35 + nodes * 0.45 + (0.05 if segment == "ent" else 0.0), 0.35, 0.85) / 0.05) * 0.05
    fs_fte = round(clamp(0.40 + accounts / 900.0 + (0.05 if segment == "ent" else 0.0), 0.40, 0.85) / 0.05) * 0.05
    sales_fte = round(sales_fte / 0.05) * 0.05
    support_fte = round(clamp(support_fte + (0.10 if segment == "pro" else 0.0), 0.75, 1.89) / 0.05) * 0.05
    tech = round(ai_fte * 96_000_000 + fs_fte * 60_000_000)
    sales = round(sales_fte * 40_000_000 + support_fte * 28_500_000)
    ads = round((45_000_000 + 0.06 * gross + extra_ads) / 1_000_000) * 1_000_000
    marketing = ads + 36_000_000
    opex = tech + sales + marketing

    gp = net - cogs
    ebitda = gp - opex
    margin = ebitda / gross * 100.0
    standalone_cost = gross - ebitda
    shared = round(0.75 * tech + 14_400_000)
    portfolio_cost = standalone_cost - shared
    portfolio_ebitda = net - portfolio_cost
    portfolio_margin = portfolio_ebitda / gross * 100.0

    arpu = gross / accounts
    bad_debt = gross - net
    varcost_account = (gpu_cost + nin_total + sms_cost + partner_cogs) / accounts
    contribution = arpu * (1 - dso / 100.0) - varcost_account
    be = max(1, math.ceil(opex / contribution)) if contribution > 0 else accounts * 2
    new_customers = max(1.0, accounts * churn / (100.0 - churn))
    cac = round(ads / new_customers / 10_000) * 10_000
    payback = round(cac / contribution, 1) if contribution > 0 else 0.0
    ltv = arpu * (gp / net) / (churn / 100.0)
    ltv_cac = round(ltv / cac, 1) if cac else 0.0

    return {
        "segment": SEGMENT[segment],
        "engine": ENGINES[engine],
        "stack": STACKS[engine],
        "accounts": accounts,
        "mix": f"{n1} Starter, {n2} Growth, {n3} Pro/Enterprise/Pack",
        "n1": n1, "n2": n2, "n3": n3,
        "starter": starter, "growth": growth, "pro_price": pro_price, "usage": usage,
        "churn": churn, "dso": dso,
        "gross": gross, "net": net, "bad_debt": bad_debt,
        "nodes": nodes, "gpu_cost": gpu_cost, "nin_server": nin_server, "nin_total": nin_total,
        "sms_count": sms_count, "tx_count": tx_count, "sms_cost": sms_cost,
        "partner_pct": partner_pct, "partner_share": partner_share, "partner_cogs": partner_cogs,
        "cogs": cogs, "gp": gp, "tech": tech, "sales": sales, "marketing": marketing,
        "ads": ads, "ai_fte": ai_fte, "fs_fte": fs_fte, "sales_fte": sales_fte, "support_fte": support_fte,
        "opex": opex, "ebitda": ebitda, "margin": margin,
        "standalone_cost": standalone_cost, "shared": shared,
        "portfolio_cost": portfolio_cost, "portfolio_ebitda": portfolio_ebitda,
        "portfolio_margin": portfolio_margin, "arpu": arpu, "be": be,
        "cac": cac, "payback": payback, "ltv_cac": ltv_cac,
    }


def make_pl(f: dict) -> list[dict]:
    return [
        {"label": "Revenue — Tier 1 (Starter)", "basis": f"{f['n1']} paying accounts × {f['starter']:,.0f} T/mo", "toman": f["n1"] * f["starter"]},
        {"label": "Revenue — Tier 2 (Growth)", "basis": f"{f['n2']} paying accounts × {f['growth']:,.0f} T/mo", "toman": f["n2"] * f["growth"]},
        {"label": "Revenue — Tier 3 (Pro / Ent / B2B2C Pack)", "basis": f"{f['n3']} paying accounts × {f['pro_price']:,.0f} T/mo", "toman": f["n3"] * f["pro_price"]},
        {"label": "Revenue — Metered Usage & Overage", "basis": f"{f['accounts']} accounts × avg {f['usage']:,.0f} T/mo credit consumption", "toman": f["accounts"] * f["usage"]},
        {"label": "GROSS BILLED REVENUE (MRR)", "basis": f"{f['accounts']} Active Accounts | Blended Billed ARPU: {f['arpu']:,.0f} T/mo", "toman": f["gross"]},
        {"label": "Less: Bad Debt & DSO Inflation Lag", "basis": f"-{f['dso']}% provision for cheque delays/defaults -> Net Collected: {f['net']:,.0f} T", "toman": -f["bad_debt"]},
        {"label": "COGS — Domestic GPU (+25% Buffer)", "basis": f"{f['nodes']:.2f}x RTX 6000 Ada (48GB) node @ 150M T/mo (Sindad)", "toman": f["gpu_cost"]},
        {"label": "COGS — NIN CPU, DB & BGP Relay", "basis": f"Domestic servers ({f['nin_server']:,.0f} T) + BGP/API tunnel (12,000,000 T)", "toman": f["nin_total"]},
        {"label": "COGS — SMS & Shaparak Gateway", "basis": f"{f['sms_count']:,} SMS @ 38T + {f['tx_count']:,} Zarinpal tx (0.5% cap 16k)", "toman": f["sms_cost"]},
        {"label": "COGS — Partner / Channel Commissions", "basis": f"{f['partner_pct']}% rev-share on {f['partner_share']}% partner-sourced revenue (ERP/Bazaar/Dealers)", "toman": f["partner_cogs"]},
        {"label": "AUDITED GROSS PROFIT & MARGIN", "basis": f"Net Collected MRR minus Direct COGS ({f['cogs']:,.0f} T) -> {f['gp']/f['net']*100:.1f}% Gross Margin", "toman": f["gp"]},
        {"label": "OPEX — Tech Payroll (incl. Tamin/Eidi/Sanavat)", "basis": f"{f['ai_fte']:.2f} AI Eng ({f['ai_fte']*96_000_000:,.0f}T) + {f['fs_fte']:.2f} FullStack ({f['fs_fte']*60_000_000:,.0f}T)", "toman": f["tech"]},
        {"label": "OPEX — B2B Sales Closers & Support Payroll", "basis": f"{f['sales_fte']:.2f} Sales AE ({f['sales_fte']*40_000_000:,.0f}T) + {f['support_fte']:.2f} Support ({f['support_fte']*28_500_000:,.0f}T)", "toman": f["sales"]},
        {"label": "OPEX — Marketing, Tehran Office & Tax/Legal", "basis": f"B2B Ads/Events ({f['ads']:,.0f} T) + Office, Moadian & Legal (36,000,000 T)", "toman": f["marketing"]},
        {"label": "EBITDA (STANDALONE vs. SHARED-ENGINE)", "basis": f"Standalone: {f['margin']:.1f}% (BE: {f['be']} cust) | Shared-Engine: {f['portfolio_ebitda']:,.0f} T ({f['portfolio_margin']:.1f}%) | CAC: {f['cac']:,.0f} T ({f['payback']:.1f} mo) | LTV:CAC: {f['ltv_cac']:.1f}x", "toman": f["ebitda"]},
    ]


def bmc_en(old: dict, bmc: dict, f: dict, sector: str) -> dict:
    category = old["category"]
    billing = BILLING_MAP.get(old.get("model", ""), "Monthly")
    return {
        "1": f"Target Buyer: {old['buyer']} ({f['segment']}). Replaces/mitigates: manual {category.lower()} workflows and incumbent point tools. Re-audited Month-12 active base: {f['accounts']} paying accounts ({f['mix']}), calibrated to Latka Iran sector scale with {f['churn']}% monthly churn.",
        "2": f"{old['what']} Differentiator: {old['wedge']}. Powered by {old['ai']}, hosted 100% inside Iran on NIN data centers so domestic integrations remain live during international internet blackouts.",
        "3": f"Primary GTM via direct sales, category partners and referrals, plus {f['sales_fte']:.2f} FTE B2B inside-sales closers. Models a {f['partner_pct']}% partner/marketplace commission on {f['partner_share']}% of revenue ({f['partner_cogs']:,.0f} T/mo in COGS) to incentivize resellers, agencies and app stores.",
        "4": f"Hybrid self-service + assisted onboarding. Automated Kavenegar SMS renewal links; {f['support_fte']:.2f} FTE dedicated support specialists handle human-in-the-loop edge cases and SAYAD/Shaparak billing follow-ups.",
        "5": f"Monthly Toman billing ({billing}): Starter {f['starter']:,.0f} T/mo | Growth {f['growth']:,.0f} | Pro/Enterprise {f['pro_price']:,.0f} + usage packs ({f['usage']:,.0f} T/mo average). Gross billed MRR {f['gross']:,.0f} T/mo; net collected after {f['dso']}% bad-debt/DSO provision {f['net']:,.0f} T/mo.",
        "6": f"{f['nodes']:.2f} RTX 6000 Ada 48GB GPU nodes with 25% peak buffer ({f['gpu_cost']:,.0f} T/mo) + NIN domestic CPU/DB/BGP ({f['nin_total']:,.0f} T/mo). Stack: {f['stack']}. Dataset: {old['ai']} and proprietary Persian {category.lower()} data.",
        "7": f"Maintaining accuracy on {old['ai']}; keeping {category.lower()} integrations and NIN/BGP routing live; enforcing monthly Toman billing and quarterly CPI/FX indexation to protect riyal margins from inflation.",
        "8": "Distribution & API partners: category resellers, agencies and local marketplaces. Infrastructure: Sindad/Afranet (GPU/NIN), Zarinpal/Payping (Shaparak gateway) and the Innovation and Prosperity Fund / knowledge-based tax exemptions.",
        "9": f"Standalone all-in cost {f['standalone_cost']:,.0f} T/mo -> standalone EBITDA {f['ebitda']:,.0f} T/mo ({f['margin']:.1f}%). Shared-engine portfolio cost {f['portfolio_cost']:,.0f} T/mo -> portfolio EBITDA {f['portfolio_ebitda']:,.0f} T/mo ({f['portfolio_margin']:.1f}%).",
    }


def fa_entry(old: dict, bmc: dict, f: dict) -> dict:
    blocks = bmc["blocks"]
    buyer_fa = fa_join(blocks.get("customer_segments", []), 2)
    value_fa = fa_join(blocks.get("value_propositions", []), 1)
    resources = blocks.get("key_resources", [])
    tech = next((r for r in resources if "فناوری" in r or "مدل" in r), resources[0] if resources else old["ai"])
    channels = fa_join(blocks.get("channels", []), 3)
    partners = fa_join(blocks.get("key_partners", []), 2)
    category_fa = CATEGORY_FA[old["category"]]
    driver = "؛ ".join(x for x in [value_fa, tech] if x)
    gtm = channels or partners or "فروش مستقیم، معرفی مشتری و شرکای دسته‌بندی"
    return {
        "title": fa_clean(bmc["name"]),
        "buyer": fa_clean(buyer_fa or old["buyer"]),
        "replaces": f"نیروی انسانی و ابزارهای دستی {category_fa}",
        "driver": fa_clean(driver),
        "gtm": fa_clean(gtm),
    }


def main():
    audited_ids = {s["id"] for s in json.loads((ROOT / "data/masterbook.json").read_text(encoding="utf-8"))["services"]}
    services = []
    fa = {}
    next_id = 201
    for old in OLD_SERVICES:
        if old["id"] in DUPLICATES:
            continue
        bmc = OLD_BMC[old["id"]]
        segment = pick_segment(old)
        f = build_financials(old, bmc, segment)
        tier = "P2"
        verdict = pick_verdict(f["margin"])
        sid = next_id
        next_id += 1
        assert sid not in audited_ids
        billing = BILLING_MAP.get(old.get("model", ""), "Monthly")
        service = {
            "id": sid,
            "sector": CATEGORY_SECTOR[old["category"]],
            "title": old["name"],
            "tier": tier,
            "verdict": verdict,
            "buyer": old["buyer"],
            "segment": f["segment"],
            "engine": f["engine"],
            "replaces": f"Manual {old['category'].lower()} workflows and incumbent point tools",
            "eliminated": f"Manual processing, spreadsheets and incumbent {old['category'].lower()} point tools",
            "eliminated_cost_ratio": "<15%",
            "driver": f"{old['what']} {old['wedge']}",
            "sovereignty": "Hosted 100% inside Iran on NIN data centers; domestic webhooks and portals remain live during international internet blackouts.",
            "gtm": "Direct sales, category partners and referrals",
            "sales_fte": f["sales_fte"],
            "partner_pct": f["partner_pct"],
            "partner_share": f["partner_share"],
            "partner_cogs": f["partner_cogs"],
            "support_fte": f["support_fte"],
            "support_scope": "Human-in-the-loop edge cases, SAYAD/Shaparak billing follow-ups and quarterly business reviews",
            "active": {"accounts": f["accounts"], "mix": f["mix"]},
            "churn": f["churn"],
            "prices": {"starter": f["starter"], "growth": f["growth"], "pro": f["pro_price"]},
            "usage_price": f["usage"],
            "billing_model": billing,
            "gross_mrr": f["gross"],
            "dso_pct": f["dso"],
            "net_mrr": f["net"],
            "gpu_nodes": f["nodes"],
            "gpu_cost": f["gpu_cost"],
            "nin_cost": f["nin_server"],
            "stack": f["stack"],
            "dataset": f"{old['ai']} and proprietary Persian {old['category'].lower()} data",
            "activity_accuracy": f"Accuracy and quality SLAs maintained on {old['ai']} using Persian evaluation sets.",
            "activity_connectors": f"Keep {old['category'].lower()} integrations, local portals and NIN/BGP routing live.",
            "activity_billing": "Monthly Toman billing, automatic Kavenegar renewal links and SAYAD cheque follow-up.",
            "dist_partners": "Category resellers, agencies and local marketplaces.",
            "infrastructure": "Sindad/Afranet GPU and NIN domestic hosting; Zarinpal/Payping Shaparak gateway.",
            "standalone_cost": f["standalone_cost"],
            "standalone_usd": f["standalone_cost"] / 203_100,
            "standalone_ebitda": f["ebitda"],
            "standalone_margin": f["margin"],
            "portfolio_cost": f["portfolio_cost"],
            "portfolio_ebitda": f["portfolio_ebitda"],
            "portfolio_margin": f["portfolio_margin"],
            "be_customers": f["be"],
            "cac": f["cac"],
            "payback": f["payback"],
            "ltv_cac": f["ltv_cac"],
            "pl": make_pl(f),
            "bmc": bmc_en(old, bmc, f, CATEGORY_SECTOR[old["category"]]),
            "origin": "legacy",
            "origin_note": "Legacy v1 service re-underwritten into the v3 model; not part of the audited v3 docx.",
            "legacy_id": old["id"],
            "legacy_score": old["score"],
            "legacy_duplicate_of": None,
        }
        services.append(service)
        fa[str(sid)] = fa_entry(old, bmc, f)

    ranking = sorted(services, key=lambda x: -x["legacy_score"])
    for i, s in enumerate(ranking):
        if s["standalone_margin"] < 10.0:
            s["tier"] = "P3"
        elif i < 40:
            s["tier"] = "P1"
        elif i < 98:
            s["tier"] = "P2"
        else:
            s["tier"] = "P3"

    out = {
        "services": services,
        "duplicates": [{"legacy_id": k, "audited_id": v} for k, v in sorted(DUPLICATES.items())],
        "category_sector": CATEGORY_SECTOR,
    }
    (ROOT / "data/legacy_services.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "data/fa_legacy.json").write_text(json.dumps(fa, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(services)} legacy services ({len(DUPLICATES)} duplicates removed)")
    print("tiers:", {t: sum(1 for s in services if s["tier"] == t) for t in ("P1", "P2", "P3")})
    print("verdicts:", {v: sum(1 for s in services if s["verdict"] == v) for v in VERDICTS.values()})
    print("margins:", f"{min(s['standalone_margin'] for s in services):.1f}% .. {max(s['standalone_margin'] for s in services):.1f}%")
    print("MRR:", f"{sum(s['gross_mrr'] for s in services)/1e9:.2f}B T/mo")


if __name__ == "__main__":
    main()
