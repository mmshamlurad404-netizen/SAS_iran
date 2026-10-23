"""Persian localization layer for the audited 200-service masterbook v3."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FA_SERVICES = json.loads((ROOT / "data" / "fa_services.json").read_text(encoding="utf-8"))
MASTERBOOK = json.loads((ROOT / "data" / "masterbook.json").read_text(encoding="utf-8"))

SECTORS_FA = {
    "A: Sales, Marketing & E-Commerce": "فروش، بازاریابی و تجارت الکترونیک",
    "B: Customer Support & Communication": "پشتیبانی مشتری و ارتباطات",
    "C: Finance, Accounting & Tax": "مالی، حسابداری و مالیات",
    "D: Legal & Government Paperwork": "حقوق و امور اداری دولتی",
    "E: Healthcare": "سلامت",
    "F: Education": "آموزش",
    "G: HR & Recruitment": "منابع انسانی و استخدام",
    "H: Industry, Engineering, Energy & Agriculture": "صنعت، مهندسی، انرژی و کشاورزی",
    "I: Real Estate, Auto, Logistics, Hospitality, Insurance & Trade": "املاک، خودرو، لجستیک، مهمان‌نوازی، بیمه و تجارت",
    "J: Media, Content & Developer Infrastructure": "رسانه، محتوا و زیرساخت توسعه‌دهندگان",
    "K: Iranian E-Commerce, Marketplaces & Social Commerce": "تجارت الکترونیک، مارکت‌پلیس و تجارت اجتماعی ایران",
    "L: Mandatory Compliance, Tax (Moadian), Customs & Portals": "انطباق اجباری، مالیات (مودیان)، گمرک و پورتال‌ها",
    "M: Inflation Survival, Bazaar Trading, FX & Treasury": "بقای تورم، تجارت بازار، ارز و خزانه",
    "N: Factory, Manufacturing, Energy & Grid Resilience": "کارخانه، تولید، انرژی و تاب‌آوری شبکه",
    "O: Construction, Civil Engineering & Real Estate": "ساخت‌وساز، مهندسی عمران و املاک",
    "P: Agriculture, Water Scarcity, Pistachio, Saffron & Greenhouses": "کشاورزی، کم‌آبی، پسته، زعفران و گلخانه",
    "Q: Healthcare, Clinics, Aesthetic Medicine & Pharmacies": "سلامت، کلینیک، پزشکی زیبایی و داروخانه",
    "R: Education, Skill Migration, Konkur & Professional Licensing": "آموزش، مهاجرت مهارتی، کنکور و پروانه‌های حرفه‌ای",
    "S: Logistics, Cross-Border Trade, Transit & Fleet Management": "لجستیک، تجارت فرامرزی، ترانزیت و مدیریت ناوگان",
    "T: Local IT Infrastructure, ERP Plugins & Developer Tools": "زیرساخت فناوری اطلاعات محلی، افزونه‌های ERP و ابزار توسعه",
}

SEGMENTS_FA = {
    "Core Iranian SME, Bazaar, Clinic & Agency B2B": "کسب‌وکار کوچک و متوسط ایرانی، بازار، کلینیک و آژانس B2B",
    "Enterprise, Industrial & Institutional B2B": "سازمانی، صنعتی و نهادی B2B",
    "Prosumer, Micro-Seller & B2B2C (School/Platform Packs)": "حرفه‌ای/خرد، خرده‌فروش و B2B2C (بسته‌های مدرسه/پلتفرم)",
}

TIERS_FA = {"P1": "اولویت ۱", "P2": "اولویت ۲", "P3": "اولویت ۳"}

VERDICTS_FA = {
    "STRONG STANDALONE WEDGE (High B2B Margin)": "گوه مستقل قوی (حاشیه بالای B2B)",
    "VIABLE STANDALONE / STRONG PORTFOLIO ADD-ON": "مستقل قابل‌دوام / مکمل قوی پورتفولیو",
    "SHARED-ENGINE ADD-ON ONLY (High Standalone Overhead)": "فقط مکمل موتور مشترک (سرباز مستقل بالا)",
}

ENGINES_FA = {
    "Engine #1: Persian Conversation & Hybrid Retrieval (RAG)": "موتور ۱: گفتگوی فارسی و بازیابی ترکیبی (RAG)",
    "Engine #2: Persian Document Extraction, Vision & OCR": "موتور ۲: استخراج اسناد، بینایی و OCR فارسی",
    "Engine #3: Persian Speech Recognition (ASR), Voice & TTS": "موتور ۳: تشخیص گفتار، صدا و TTS فارسی",
    "Engine #4: Inflation Indexing, Pricing & Demand Forecasting": "موتور ۴: شاخص‌بندی تورم، قیمت‌گذاری و پیش‌بینی تقاضا",
    "Engine #5A: Persian Generative Content & Academic/Marketing Copy": "موتور ۵A: تولید محتوای فارسی و نگارش بازاریابی/آکادمیک",
    "Engine #5B: Generative Studio Vision, Restyling & Persian Typography": "موتور ۵B: بینایی استودیویی مولد، بازطراحی و تایپوگرافی فارسی",
    "Engine #6: Cross-Platform Workflow Agents & Compliance Automators": "موتور ۶: عامل‌های گردش‌کار چندپلتفرمی و خودکارساز انطباق",
}

STACKS_FA = {
    "LightGBM / Prophet Jalali Seasonality + OR-Tools Constraint Solver + Qwen3-8B Explainer on CPU/Shared GPU": "LightGBM / Prophet با فصلیت جلالی + حل‌کننده قید OR-Tools + توضیح‌دهنده Qwen3-8B روی CPU/GPU مشترک",
    "Quantized Qwen3-14B/32B (AWQ, Apache 2.0) via vLLM + BGE-M3 Persian Embeddings + Qdrant CPU Vector DB": "Qwen3-14B/32B کوانتیزه (AWQ، مجوز Apache 2.0) با vLLM + امبدینگ فارسی BGE-M3 + پایگاه برداری Qdrant روی CPU",
    "Quantized Qwen3-14B / DeepSeek-V3 Distill with Persian Brand-Voice LoRA Adapters": "Qwen3-14B / DeepSeek-V3 Distill کوانتیزه با آداپتورهای LoRA لحن برند فارسی",
    "Qwen3-14B Function-Calling Agent + Temporal/Celery Queue + Domestic Webhook Relay (Bale/Eitaa/Moadian/ERP)": "عامل فراخوانی تابع Qwen3-14B + صف Temporal/Celery + رله وبهوک داخلی (بله/ایتا/مودیان/ERP)",
    "Fine-tuned Qwen2.5-VL-7B/32B + PaddleOCR Persian + Custom Jalali/Digit Post-Processor on Domestic GPU": "Qwen2.5-VL-7B/32B تنظیم‌شده + PaddleOCR فارسی + پردازشگر پسین سفارشی جلالی/ارقام روی GPU داخلی",
    "Fine-tuned Whisper-large-v3-turbo (Colloquial Persian) + Pyannote Diarization + Piper/XTTS Persian Voice": "Whisper-large-v3-turbo (فارسی محاوره‌ای) تنظیم‌شده + تفکیک گویندگان Pyannote + صدای فارسی Piper/XTTS",
    "Flux.1-Schnell / SDXL Quantized + ControlNet + RMBG-2.0 + Programmatic RTL Vazirmatn/IranSans Renderer": "Flux.1-Schnell / SDXL کوانتیزه + ControlNet + RMBG-2.0 + رندر برنامه‌نویسی‌شده تایپوگرافی راست‌به‌چپ وزیرمتن/ایران‌سنس",
}

BILLING_FA = {
    "Monthly": "ماهانه",
    "Per user": "به‌ازای هر کاربر",
    "Monthly credits": "اعتبار ماهانه",
    "Per seat": "به‌ازای هر صندلی",
    "Per document": "به‌ازای هر سند",
    "Per query": "به‌ازای هر پرس‌وجو",
    "Per employee": "به‌ازای هر کارمند",
    "Per project": "به‌ازای هر پروژه",
    "Credits": "اعتبار مصرفی",
    "Monthly + per conversation": "ماهانه + به‌ازای هر گفتگو",
    "Monthly by SKU count": "ماهانه بر اساس تعداد کالا",
    "Per minute": "به‌ازای هر دقیقه",
    "Project": "پروژه‌ای",
    "Per report": "به‌ازای هر گزارش",
    "Per course": "به‌ازای هر دوره",
    "Commission": "کمیسیونی",
    "Monthly + savings share": "ماهانه + سهم از صرفه‌جویی",
    "Per shipment": "به‌ازای هر محموله",
    "Monthly per branch": "ماهانه به‌ازای هر شعبه",
    "Monthly per seat": "ماهانه به‌ازای هر صندلی",
    "Per image pack": "به‌ازای هر بسته تصویر",
    "Monthly + per message": "ماهانه + به‌ازای هر پیام",
    "Monthly + conversations": "ماهانه + گفتگوها",
    "Project + usage": "پروژه + مصرف",
    "Per audio hour": "به‌ازای هر ساعت صدا",
    "Per character": "به‌ازای هر کاراکتر",
    "Per transaction": "به‌ازای هر تراکنش",
    "Per agreement": "به‌ازای هر قرارداد",
    "Per case": "به‌ازای هر پرونده",
    "Per tender": "به‌ازای هر مناقصه",
    "Per application": "به‌ازای هر درخواست",
    "Per scan": "به‌ازای هر اسکن",
    "Per claim": "به‌ازای هر مطالبه",
    "Per student": "به‌ازای هر دانشجو",
    "Per job post": "به‌ازای هر آگهی شغل",
    "Per candidate": "به‌ازای هر داوطلب",
    "Per site": "به‌ازای هر سایت",
    "Per survey": "به‌ازای هر نظرسنجی",
    "Per machine": "به‌ازای هر ماشین",
    "Per line": "به‌ازای هر خط",
    "Per hectare": "به‌ازای هر هکتار",
    "Per RFQ": "به‌ازای هر استعلام",
    "Per 1,000 ads": "به‌ازای هر ۱۰۰۰ آگهی",
    "Per vehicle": "به‌ازای هر خودرو",
    "Per quote": "به‌ازای هر پیش‌فاکتور",
    "Per page": "به‌ازای هر صفحه",
    "Per token": "به‌ازای هر توکن",
    "License + support": "لایسنس + پشتیبانی",
    "Monthly + % of ad spend saved": "ماهانه + درصدی از صرفه‌جویی تبلیغات",
    "Monthly + per listing pack": "ماهانه + بسته آگهی",
    "Low monthly fee + credits": "آبونمان کم + اعتبار",
    "Monthly by transaction volume": "ماهانه بر اساس حجم تراکنش",
    "Per shipment / Monthly": "به‌ازای هر محموله / ماهانه",
    "Per 1,000 items + monthly": "به‌ازای هر ۱۰۰۰ قلم + ماهانه",
    "Per contract / Monthly": "به‌ازای هر قرارداد / ماهانه",
    "Monthly + per bid": "ماهانه + به‌ازای هر پیشنهاد",
    "Monthly per active dossier": "ماهانه به‌ازای هر پرونده فعال",
    "Per user / Monthly": "به‌ازای هر کاربر / ماهانه",
    "Annual retainer + success fee": "حق مشاوره سالانه + کارمزد موفقیت",
    "Per filing": "به‌ازای هر اظهارنامه",
    "Monthly + per cheque check": "ماهانه + به‌ازای هر استعلام چک",
    "Project + audit license": "پروژه + لایسنس حسابرسی",
    "Monthly by volume": "ماهانه بر اساس حجم",
    "Monthly + per search": "ماهانه + به‌ازای هر جست‌وجو",
    "Per site monthly": "ماهانه به‌ازای هر سایت",
    "Monthly per depot": "ماهانه به‌ازای هر انبار",
    "Project setup + monthly license": "راه‌اندازی پروژه + لایسنس ماهانه",
    "Monthly per plant": "ماهانه به‌ازای هر کارخانه",
    "Per project / Monthly": "به‌ازای هر پروژه / ماهانه",
    "Per query / Monthly": "به‌ازای هر پرس‌وجو / ماهانه",
    "Monthly per site": "ماهانه به‌ازای هر سایت",
    "Monthly per agency": "ماهانه به‌ازای هر آژانس",
    "Monthly per unit": "ماهانه به‌ازای هر واحد",
    "Per batch / Monthly": "به‌ازای هر بچ / ماهانه",
    "Monthly per hectare": "ماهانه به‌ازای هر هکتار",
    "Per consultation / Seasonal": "به‌ازای هر مشاوره / فصلی",
    "Seasonal subscription": "اشتراک فصلی",
    "Monthly per 100 head": "ماهانه به‌ازای هر ۱۰۰ رأس",
    "Seasonal": "فصلی",
    "Monthly + per booked lead": "ماهانه + به‌ازای هر سرنخ رزروشده",
    "Per patient dossier": "به‌ازای هر پرونده بیمار",
    "Per active patient": "به‌ازای هر بیمار فعال",
    "Monthly / Exam-season pass": "ماهانه / بلیت فصل آزمون",
    "Per exam cycle": "به‌ازای هر دوره آزمون",
    "Per application package": "به‌ازای هر بسته درخواست",
    "Per seat monthly": "ماهانه به‌ازای هر صندلی",
    "Per trainee": "به‌ازای هر کارآموز",
    "Per manuscript": "به‌ازای هر دست‌نوشته",
    "Monthly per truck": "ماهانه به‌ازای هر کامیون",
    "Per container / Monthly": "به‌ازای هر کانتینر / ماهانه",
    "Per visitor seat": "به‌ازای هر صندلی بازدیدکننده",
    "Monthly per vehicle": "ماهانه به‌ازای هر خودرو",
    "Commission / Monthly": "کمیسیون / ماهانه",
    "Monthly plugin subscription": "اشتراک ماهانه افزونه",
    "Monthly by bandwidth/requests": "ماهانه بر اساس پهنای باند/درخواست",
    "Monthly API subscription": "اشتراک ماهانه API",
    "On-prem license": "لایسنس نصب داخلی",
    "Monthly per agent seat": "ماهانه به‌ازای هر صندلی اپراتور",
    "Annual/Monthly plugin": "افزونه سالانه/ماهانه",
    "Per document API": "به‌ازای هر سند API",
    "Annual enterprise license": "لایسنس سالانه سازمانی",
}

PL_LABELS_FA = {
    "Revenue — Tier 1 (Starter)": "درآمد — سطح ۱ (استارتر)",
    "Revenue — Tier 2 (Growth)": "درآمد — سطح ۲ (گروث)",
    "Revenue — Tier 3 (Pro / Ent / B2B2C Pack)": "درآمد — سطح ۳ (پرو/سازمانی/پک B2B2C)",
    "Revenue — Metered Usage & Overage": "درآمد — مصرف اندازه‌گیری‌شده و مازاد",
    "GROSS BILLED REVENUE (MRR)": "درآمد ناخالص صورت‌سابقه‌شده (MRR)",
    "Less: Bad Debt & DSO Inflation Lag": "کسر: بدهی بد و تأخیر تورمی DSO",
    "COGS — Domestic GPU (+25% Buffer)": "بهای تمام‌شده — GPU داخلی (+۲۵٪ بافر)",
    "COGS — NIN CPU, DB & BGP Relay": "بهای تمام‌شده — CPU/DB و رله BGP داخلی",
    "COGS — SMS & Shaparak Gateway": "بهای تمام‌شده — پیامک و درگاه شپارک",
    "COGS — Partner / Channel Commissions": "بهای تمام‌شده — کمیسیون شرکا/کانال",
    "AUDITED GROSS PROFIT & MARGIN": "سود ناخالص و حاشیه حسابرسی‌شده",
    "OPEX — Tech Payroll (incl. Tamin/Eidi/Sanavat)": "هزینه عملیاتی — حقوق فنی (تأمین/عیدی/سنوات)",
    "OPEX — B2B Sales Closers & Support Payroll": "هزینه عملیاتی — حقوق فروش B2B و پشتیبانی",
    "OPEX — Marketing, Tehran Office & Tax/Legal": "هزینه عملیاتی — بازاریابی، دفتر تهران و مالی/حقوقی",
    "EBITDA (STANDALONE vs. SHARED-ENGINE)": "EBITDA (مستقل در برابر موتور مشترک)",
}

FLOW_LABELS_FA = {
    "revenue": "درآمد",
    "bad_debt": "بدهی بد/DSO",
    "gpu": "GPU داخلی",
    "nin": "زیرساخت NIN",
    "sms": "پیامک/شپارک",
    "partner": "کمیسیون شرکا",
    "tech": "حقوق فنی",
    "sales": "فروش/پشتیبانی",
    "marketing": "بازاریابی/دفتر",
}

_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa_digits(value) -> str:
    return str(value).translate(_DIGITS)


def fa_int(value: float) -> str:
    return fa_digits(f"{int(round(value)):,}").replace(",", "٬")


def fa_dec(value: float, digits: int = 1) -> str:
    s = f"{value:,.{digits}f}"
    return fa_digits(s).replace(",", "٬").replace(".", "٫")


def fa_pct(value: float, digits: int = 1) -> str:
    return f"{fa_dec(value, digits)}٪"


def money_m(value: float) -> str:
    return f"{fa_dec(value / 1_000_000, 1)} میلیون تومان"


def billing_fa(value: str) -> str:
    return BILLING_FA.get(value, value)


def mix_fa(mix: str) -> str:
    def repl(m):
        return f"{fa_digits(m.group(1))} {m.group(2)}"
    out = re.sub(r"(\d+)\s+(Starter|Growth|Pro/Enterprise/Pack)", repl, mix)
    out = out.replace("Starter", "استارتر").replace("Growth", "گروث").replace("Pro/Enterprise/Pack", "پرو/سازمانی/پک")
    return out


def _tier_numbers(s):
    tiers = [p for p in s["pl"] if p["label"].startswith("Revenue — Tier")]
    return tiers


def bmc_fa(s) -> list[dict]:
    fa = FA_SERVICES[str(s["id"])]
    seg = SEGMENTS_FA.get(s["segment"], s["segment"])
    active = s["active"] or {"accounts": 0, "mix": ""}
    stack = STACKS_FA.get(s["stack"], s["stack"])
    gtm = fa["gtm"]
    driver = fa["driver"]
    replaces = fa["replaces"]
    blocks = [
        {
            "key": "segments",
            "num": "۱",
            "title": "بخش‌های مشتری",
            "text": (
                f"خریدار هدف: {fa['buyer']} ({seg}). "
                f"جایگزین یا کاهش‌دهنده: {replaces}. "
                f"پایه فعال حسابرسی‌شده در ماه ۱۲: {fa_int(active['accounts'])} حساب پرداخت‌کننده "
                f"({mix_fa(active['mix'])})" + "، کالیبره‌شده با مقیاس بخش SaaS ایران (لاتکا) و ریزش ماهانه "
                f"{fa_pct(s['churn'] or 0)}."
            ),
        },
        {
            "key": "value",
            "num": "۲",
            "title": "ارزش پیشنهادی",
            "text": (
                f"جایگزین «{replaces}» با کمتر از {fa_digits(s['eliminated_cost_ratio'].replace('<', '').replace('%', '').strip() or '۱۵')}٪ هزینه دستی/جریمه می‌شود. "
                f"موتور داده: {driver}؛ با میزبانی ۱۰۰٪ داخل ایران روی دیتاسنترهای NIN، تا وبهوک‌های داخلی "
                f"(بله/ایتا/وب محلی) در قطعی‌های اینترنت بین‌المللی فعال بمانند."
            ),
        },
        {
            "key": "channels",
            "num": "۳",
            "title": "کانال‌ها و کمیسیون‌ها",
            "text": (
                f"ورود به بازار (GTM) عمدتاً از طریق {gtm} به‌همراه {fa_dec(s['sales_fte'] or 0, 2)} FTE کارشناس فروش سازمانی. "
                f"مدل: کمیسیون {fa_digits(s['partner_pct'])}٪ شرکا/مارکت‌پلیس بر {fa_digits(s['partner_share'])}٪ از درآمد "
                f"({fa_int(s['partner_cogs'])} تومان در ماه در COGS) برای انگیزه‌دهی به نمایندگان ERP، آژانس‌ها و اپ‌استورها."
            ),
        },
        {
            "key": "relationships",
            "num": "۴",
            "title": "روابط با مشتری",
            "text": (
                "آنبوردینگ ترکیبی سلف‌سرویس + تلفنی/رباتی. لینک‌های تمدید خودکار پیامکی کاوه‌نگار؛ "
                f"{fa_dec(s['support_fte'] or 0, 2)} FTE متخصص پشتیبانی برای موارد نیازمند انسان در حلقه و پیگیری "
                "صورت‌حساب SAYAD/شپارک."
            ),
        },
        {
            "key": "revenue",
            "num": "۵",
            "title": "جریان‌های درآمد (حسابرسی‌شده)",
            "text": (
                f"صورتحساب ماهانه به تومان ({billing_fa(s['billing_model'])}): استارتر {fa_int(s['prices'].get('starter', 0))} تومان/ماه | "
                f"گروث {fa_int(s['prices'].get('growth', 0))} | پرو/سازمانی {fa_int(s['prices'].get('pro', 0))} + بسته‌های مصرف "
                f"({fa_int(s['usage_price'] or 0)} تومان/ماه میانگین). "
                f"MRR ناخالص صورت‌سابقه‌شده: {fa_int(s['gross_mrr'])} تومان/ماه؛ MRR خالص وصول‌شده پس از "
                f"{fa_pct(s['dso_pct'])} ذخیره بدهی بد/تأخیر چک: {fa_int(s['net_mrr'])} تومان/ماه."
            ),
        },
        {
            "key": "resources",
            "num": "۶",
            "title": "منابع کلیدی",
            "text": (
                f"GPU داخلی: {fa_dec(s['gpu_nodes'], 2)} گره RTX 6000 Ada 48GB شامل ۲۵٪ بافر پیک "
                f"({fa_int(s['gpu_cost'])} تومان/ماه) + سرورهای CPU/DB داخلی NIN ({fa_int(s['nin_cost'])} تومان/ماه). "
                f"پشته فنی: {stack}. مجموعه داده: {driver}."
            ),
        },
        {
            "key": "activities",
            "num": "۷",
            "title": "فعالیت‌های کلیدی",
            "text": (
                f"حفظ دقت LoRA روی {driver}؛ زنده نگه‌داشتن اتصال‌های {gtm} در برابر تغییرات مسیریابی NIN/BGP؛ "
                "اجرای سخت‌گیرانه صورت‌حساب ماهانه و شاخص‌بندی فصلی CPI/ارز برای جلوگیری از فرسایش حاشیه ریالی توسط تورم."
            ),
        },
        {
            "key": "partners",
            "num": "۸",
            "title": "شرکای کلیدی",
            "text": (
                f"شرکای توزیع و API: {gtm}. زیرساخت: Sindad/Afranet (GPU/NIN)، زرین‌پال/پی‌پینگ (درگاه شپارک) "
                "و معاونت علمی و فناوری (معافیت مالیاتی دانش‌بنیان نوع ۱/۲)."
            ),
        },
        {
            "key": "costs",
            "num": "۹",
            "title": "ساختار هزینه (حسابرسی‌شده)",
            "text": (
                f"هزینه کامل مستقل: {fa_int(s['standalone_cost'])} تومان/ماه؛ EBITDA مستقل: "
                f"{fa_int(s['standalone_ebitda'])} تومان/ماه ({fa_pct(s['standalone_margin'])}). "
                f"هزینه پورتفولیوی موتور مشترک (تقسیم توسعه/دفتر بین ۳ ابزار خواهر): {fa_int(s['portfolio_cost'])} تومان/ماه؛ "
                f"EBITDA پورتفولیو: {fa_int(s['portfolio_ebitda'])} تومان/ماه ({fa_pct(s['portfolio_margin'])})."
            ),
        },
    ]
    return blocks


def bmc_en(s) -> list[dict]:
    titles = {
        "1": ("segments", "Customer Segments"),
        "2": ("value", "Value Propositions"),
        "3": ("channels", "Channels & Commissions"),
        "4": ("relationships", "Customer Relationships"),
        "5": ("revenue", "Revenue Streams (Audited)"),
        "6": ("resources", "Key Resources"),
        "7": ("activities", "Key Activities"),
        "8": ("partners", "Key Partners"),
        "9": ("costs", "Audited Cost Structure"),
    }
    out = []
    for k in "123456789":
        key, title = titles[k]
        out.append({"key": key, "num": k, "title": title, "text": s["bmc"].get(k, "")})
    return out


def pl_fa(s) -> list[dict]:
    """Build the Persian audited P&L with reconstructed basis text."""
    basis_map = {p["label"]: p["basis"] for p in s["pl"]}
    toman = {p["label"]: p["toman"] for p in s["pl"]}
    tiers = _tier_numbers(s)
    rows = []
    labels = [p["label"] for p in s["pl"]]
    for label in labels:
        basis = basis_map.get(label, "")
        val = toman.get(label, 0)
        fa_basis = basis
        try:
            if label.startswith("Revenue — Tier 1"):
                m = re.search(r"(\d+) paying accounts × ([\d,]+) T/mo", basis)
                if m:
                    fa_basis = f"{fa_int(m.group(1))} حساب × {fa_int(float(m.group(2).replace(',', '')))} تومان/ماه"
            elif label.startswith("Revenue — Tier 2"):
                m = re.search(r"(\d+) paying accounts × ([\d,]+) T/mo", basis)
                if m:
                    fa_basis = f"{fa_int(m.group(1))} حساب × {fa_int(float(m.group(2).replace(',', '')))} تومان/ماه"
            elif label.startswith("Revenue — Tier 3"):
                m = re.search(r"(\d+) paying accounts × ([\d,]+) T/mo", basis)
                if m:
                    fa_basis = f"{fa_int(m.group(1))} حساب × {fa_int(float(m.group(2).replace(',', '')))} تومان/ماه"
            elif label.startswith("Revenue — Metered"):
                m = re.search(r"(\d+) accounts × avg ([\d,]+) T/mo", basis)
                if m:
                    fa_basis = f"{fa_int(m.group(1))} حساب × میانگین {fa_int(float(m.group(2).replace(',', '')))} تومان/ماه مصرف"
            elif label.startswith("GROSS BILLED"):
                m = re.search(r"(\d+) Active Accounts \| Blended Billed ARPU: ([\d,]+) T/mo", basis)
                if m:
                    fa_basis = f"{fa_int(m.group(1))} حساب فعال | ARPU ترکیبی صورت‌سابقه: {fa_int(float(m.group(2).replace(',', '')))} تومان/ماه"
            elif label.startswith("Less:"):
                fa_basis = f"{fa_pct(s['dso_pct'])} ذخیره برای تأخیر/نکول چک ← خالص وصولی: {fa_int(s['net_mrr'])} تومان"
            elif label.startswith("COGS — Domestic GPU"):
                fa_basis = f"{fa_dec(s['gpu_nodes'], 2)} گره RTX 6000 Ada 48GB با ۲۵٪ بافر @ ۱۵۰ میلیون تومان/ماه (سینداد)"
            elif label.startswith("COGS — NIN"):
                m = re.search(r"Domestic servers \(([\d,]+) T\) \+ BGP/API tunnel \(([\d,]+) T\)", basis)
                if m:
                    fa_basis = f"سرور داخلی ({fa_int(float(m.group(1).replace(',', '')))} تومان) + رله BGP/API ({fa_int(float(m.group(2).replace(',', '')))} تومان)"
            elif label.startswith("COGS — SMS"):
                m = re.search(r"([\d,]+) SMS @ 38T \+ ([\d,]+) Zarinpal tx", basis)
                if m:
                    fa_basis = f"{fa_int(float(m.group(1).replace(',', '')))} پیامک @ ۳۸ تومان + {fa_int(float(m.group(2).replace(',', '')))} تراکنش زرین‌پال"
            elif label.startswith("COGS — Partner"):
                fa_basis = f"{fa_digits(s['partner_pct'])}٪ سهم شریک بر {fa_digits(s['partner_share'])}٪ درآمد شریکان (ERP/بازار/نمایندگان)"
            elif label.startswith("AUDITED GROSS"):
                gm = s.get("_gm", 0)
                cogs = s.get("_cogs", 0)
                fa_basis = f"MRR خالص منهای COGS مستقیم ({fa_int(cogs)} تومان) ← حاشیه ناخالص {fa_pct(gm)}"
            elif label.startswith("OPEX — Tech"):
                m = re.search(r"([\d.]+) AI Eng \(([\d,]+)T\) \+ ([\d.]+) FullStack \(([\d,]+)T\)", basis)
                if m:
                    fa_basis = f"{fa_dec(float(m.group(1)), 2)} مهندس AI ({fa_int(float(m.group(2).replace(',', '')))} تومان) + {fa_dec(float(m.group(3)), 2)} فول‌استک ({fa_int(float(m.group(4).replace(',', '')))} تومان)"
            elif label.startswith("OPEX — B2B"):
                m = re.search(r"([\d.]+) Sales AE \(([\d,]+)T\) \+ ([\d.]+) Support \(([\d,]+)T\)", basis)
                if m:
                    fa_basis = f"{fa_dec(float(m.group(1)), 2)} فروش ({fa_int(float(m.group(2).replace(',', '')))} تومان) + {fa_dec(float(m.group(3)), 2)} پشتیبانی ({fa_int(float(m.group(4).replace(',', '')))} تومان)"
            elif label.startswith("OPEX — Marketing"):
                m = re.search(r"B2B Ads/Events \(([\d,]+) T\) \+ Office, Moadian & Legal \(([\d,]+) T\)", basis)
                if m:
                    fa_basis = f"تبلیغات B2B/رویدادها ({fa_int(float(m.group(1).replace(',', '')))} تومان) + دفتر تهران، مودیان و حقوقی ({fa_int(float(m.group(2).replace(',', '')))} تومان)"
            elif label.startswith("EBITDA"):
                fa_basis = (
                    f"مستقل: {fa_pct(s['standalone_margin'])} (سربه‌سر: {fa_int(s['be_customers'])} مشتری) | "
                    f"موتور مشترک: {fa_int(s['portfolio_ebitda'])} تومان ({fa_pct(s['portfolio_margin'])}) | "
                    f"CAC: {fa_int(s['cac'])} تومان ({fa_dec(s['payback'])} ماه) | LTV:CAC: {fa_dec(s['ltv_cac'])}x"
                )
        except Exception:
            fa_basis = basis
        rows.append({
            "label": PL_LABELS_FA.get(label, label),
            "basis": fa_basis,
            "toman": val,
            "flow": flow_kind(label),
        })
    return rows


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
