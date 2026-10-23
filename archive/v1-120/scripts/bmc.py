import math

USD_TOMAN = 270_000
MONTHS = 12
AVG_SALARY_TOMAN = 120_000_000

CATEGORY_BMC = {
    "Sales & Marketing": {
        "segments": ["کسب‌وکارهای کوچک و متوسط با تیم بازاریابی ۱ تا ۵ نفره", "آژانس‌های دیجیتال مارکتینگ و فروشندگان اینستاگرام"],
        "channels": ["فروش مستقیم و معرفی مشتری", "اینستاگرام و لینکدین", "وبینار و آموزش رایگان", "همکاری با آژانس‌ها و مشاوران"],
        "relationships": ["آنبوردینگ خودکار و ویدیوی آموزشی", "پشتیبانی واتساپ و پیامک", "تماس موفقیت مشتری ماهانه", "باشگاه مشتریان و وبینار فصلی"],
        "resources": ["مدل زبانی فارسی و قالب‌های تبلیغاتی", "کتابخانه ترند و لحن برند", "داده تعامل و عملکرد کمپین", "تیم محتوا و فروش"],
        "activities": ["تولید و بهبود قالب‌های فارسی", "آموزش مدل روی لحن برند", "فروش و آنبوردینگ", "پایش کیفیت خروجی و بازخورد"],
        "partners": ["اینستاگرام و پلتفرم‌های تبلیغاتی", "درگاه پرداخت زرین‌پال", "ارسال پیامک کاوه‌نگار", "آژانس‌ها و فریلنسرها"],
        "outcome": "کاهش زمان تولید محتوا و افزایش نرخ تبدیل کمپین‌ها",
    },
    "E-commerce & Retail": {
        "segments": ["فروشندگان دیجی‌کالا، باسلام و فروشگاه‌های اینستاگرامی", "خرده‌فروشان چندکاناله و تیم‌های عملیات فروش"],
        "channels": ["فروش مستقیم به فروشندگان بزرگ", "گروه‌های تلگرامی و انجمن فروشندگان", "همکاری با انبارها و شرکت‌های ارسال", "محتوای آموزشی سئو"],
        "relationships": ["راه‌اندازی با داده فروشگاه", "پشتیبانی اختصاصی فروشندگان بزرگ", "گزارش عملکرد ماهانه", "قرارداد سالانه با تخفیف پیش‌پرداخت"],
        "resources": ["اتصال به API مارکت‌پلیس‌ها", "مدل تشخیص تصویر و دسته‌بندی", "داده قیمت و تقاضای محلی", "تیم عملیات فروشنده"],
        "activities": ["همگام‌سازی کاتالوگ و موجودی", "بهینه‌سازی فید و قیمت", "پایش رقبا", "پشتیبانی عملیات فروش"],
        "partners": ["دیجی‌کالا و باسلام", "شاپرک و PSPها", "شرکت‌های لجستیک", "ترب و ایمالز"],
        "outcome": "افزایش فروش و کاهش کار دستی در عملیات فروشگاه",
    },
    "Accounting, Tax & Finance": {
        "segments": ["کسب‌وکارهای کوچک و متوسط با مالیات بر ارزش افزوده", "مؤسسات حسابداری و مشاوران مالیاتی"],
        "channels": ["همکاری با مؤسسات حسابداری", "فروش مستقیم به مدیران مالی", "وبینار قوانین مالیاتی", "معرفی از سوی حسابداران"],
        "relationships": ["آنبوردینگ با داده مالی واقعی", "پشتیبانی تخصصی مالیاتی", "بازبینی فصلی و به‌روزرسانی قوانین", "قرارداد سالانه و محرمانگی"],
        "resources": ["اتصال مودیان و فرمت بانک‌ها", "موتور قواعد مالیاتی ایران", "مدل OCR اسناد فارسی", "تیم حسابداری و انطباق"],
        "activities": ["به‌روزرسانی قواعد مالیاتی", "تطبیق و اعتبارسنجی اسناد", "پشتیبانی اظهارنامه", "توسعه یکپارچگی بانکی"],
        "partners": ["سازمان امور مالیاتی و مودیان", "بانک‌ها و PSPها", "مؤسسات حسابداری", "شرکت‌های نرم‌افزار مالی"],
        "outcome": "کاهش جریمه مالیاتی و صرفه‌جویی در ساعت کار حسابدار",
    },
    "Legal, Compliance & Documents": {
        "segments": ["دفاتر حقوقی و وکلای مستقل", "واحدهای حقوقی شرکت‌ها و تیم‌های انطباق"],
        "channels": ["فروش مستقیم و معرفی وکیل", "همایش‌های حقوقی", "محتوای تخصصی و وبینار", "همکاری با دفاتر بزرگ"],
        "relationships": ["پایلوت روی پرونده واقعی", "پشتیبانی حقوقی و آموزش", "قرارداد محرمانگی و استقرار خصوصی", "بازبینی دوره‌ای کیفیت"],
        "resources": ["پایگاه قوانین و رویه ایران", "مدل بازیابی و استخراج اسناد", "پیکره قراردادهای فارسی", "تیم حقوقی ناظر"],
        "activities": ["به‌روزرسانی قوانین و آرای", "آموزش مدل روی اسناد مشتری", "بازبینی خروجی توسط وکیل", "توسعه استقرار خصوصی"],
        "partners": ["کانون وکلا و دفاتر حقوقی", "پایگاه‌های قوانین", "ارائه‌دهندگان ابر خصوصی", "دانشگاه‌های حقوق"],
        "outcome": "کاهش ریسک حقوقی و سرعت بالاتر بررسی اسناد",
    },
    "Healthcare & Clinic Operations": {
        "segments": ["کلینیک‌های خصوصی، مطب دندان‌پزشکی و آزمایشگاه‌ها", "بیمارستان‌های کوچک و زنجیره‌های درمانی"],
        "channels": ["فروش میدانی به کلینیک‌ها", "نمایشگاه‌های سلامت", "همکاری با شرکت‌های HIS", "معرفی پزشکان"],
        "relationships": ["پایلوت رایگان محدود و آموزش پرسنل", "پشتیبانی تلفنی و حضوری", "بازبینی ماهانه فرایند", "قرارداد محرمانگی داده بیمار"],
        "resources": ["مدل گفتار و OCR پزشکی فارسی", "اتصال به HIS و تقویم", "پروتکل‌های بالینی محلی", "تیم پشتیبانی درمان"],
        "activities": ["آموزش مدل روی اصطلاحات پزشکی", "یکپارچه‌سازی با HIS", "آموزش پرسنل", "پایش کیفیت و حریم خصوصی"],
        "partners": ["کلینیک‌ها و بیمارستان‌ها", "شرکت‌های HIS", "بیمه‌های درمانی", "ارائه‌دهندگان پیامک"],
        "outcome": "کاهش زمان پذیرش و بهبود پیگیری بیمار",
    },
    "Education & Workforce Training": {
        "segments": ["دانش‌آموزان و داوطلبان کنکور", "مدارس، آموزشگاه‌ها و تیم‌های آموزش سازمانی"],
        "channels": ["فروش مستقیم به آموزشگاه‌ها", "اینستاگرام و تلگرام آموزشی", "همکاری با معلمان و مشاوران", "فروش سازمانی به شرکت‌ها"],
        "relationships": ["ثبت‌نام خودکار و مسیر یادگیری", "پشتیبانی آموزشی", "گزارش پیشرفت برای والدین و مدیر", "قرارداد سالانه مدرسه"],
        "resources": ["بانک سؤال و محتوای فارسی", "مدل تطبیقی و ارزیابی", "داده عملکرد یادگیرنده", "تیم محتوا و معلم"],
        "activities": ["تولید و بازبینی محتوا", "شخصی‌سازی مسیر یادگیری", "فروش به آموزشگاه", "پشتیبانی و گزارش‌دهی"],
        "partners": ["مدارس و آموزشگاه‌ها", "معلمان و مشاوران", "وزارت آموزش و پرورش", "پلتفرم‌های پرداخت"],
        "outcome": "یادگیری شخصی‌سازی‌شده و صرفه‌جویی در زمان معلم",
    },
    "Real Estate, Construction & Facilities": {
        "segments": ["مشاوران املاک و آژانس‌های مسکن", "پیمانکاران، سازندگان و مدیران ساختمان"],
        "channels": ["فروش مستقیم به آژانس‌ها", "دیوار و اینستاگرام", "همکاری با انجمن‌های صنفی", "نمایشگاه ساختمان"],
        "relationships": ["آنبوردینگ با آگهی واقعی", "پشتیبانی واتساپ", "گزارش عملکرد سرنخ", "قرارداد سالانه آژانس"],
        "resources": ["داده محله و معاملات", "مدل ارزش‌گذاری و بینایی", "اتصال به دیوار و CRM", "تیم مشاور املاک"],
        "activities": ["به‌روزرسانی داده بازار", "آموزش مدل ارزش‌گذاری", "یکپارچه‌سازی با CRM", "پشتیبانی آژانس‌ها"],
        "partners": ["دیوار و آژانس‌های املاک", "شهرداری و نظام مهندسی", "شرکت‌های ساختمانی", "بانک‌ها"],
        "outcome": "سرنخ باکیفیت‌تر و برآورد سریع‌تر ارزش ملک",
    },
    "Logistics, Fleet & Last-Mile": {
        "segments": ["شرکت‌های حمل و پیک شهری", "ناوگان‌های توزیع و انبارها"],
        "channels": ["فروش مستقیم به ناوگان‌ها", "همکاری با شرکت‌های لجستیک", "نمایشگاه حمل‌ونقل", "معرفی رانندگان"],
        "relationships": ["پایلوت روی مسیر واقعی", "پشتیبانی عملیات ۲۴/۷", "گزارش صرفه‌جویی ماهانه", "قرارداد سالانه ناوگان"],
        "resources": ["نقشه و داده ترافیک ایران", "مدل مسیریابی و پیش‌بینی", "اتصال GPS و کارت سوخت", "تیم عملیات لجستیک"],
        "activities": ["بهینه‌سازی مسیر و ظرفیت", "پایش زنجیره سرد", "یکپارچه‌سازی GPS", "پشتیبانی راننده"],
        "partners": ["شرکت‌های حمل و پیک", "ارائه‌دهندگان GPS", "بیمه‌ها", "گمرک و انبارها"],
        "outcome": "کاهش هزینه سوخت و افزایش به‌موقع‌رسیدن تحویل",
    },
    "Manufacturing, Energy & Agriculture": {
        "segments": ["کارخانه‌ها و واحدهای تولیدی متوسط", "مزارع، دامداری‌ها و نیروگاه‌های تجدیدپذیر"],
        "channels": ["فروش میدانی و پروژه‌ای", "همکاری با پارک‌های فناوری", "نمایشگاه صنعت و کشاورزی", "معرفی شرکت‌های مهندسی"],
        "relationships": ["پایلوت در خط تولید", "پشتیبانی فنی و آموزش اپراتور", "گزارش صرفه‌جویی و انطباق", "قرارداد نگهداری سالانه"],
        "resources": ["داده سنسور و تصویر صنعتی", "مدل پیش‌بینی و بینایی", "اتصال PLC و IoT", "تیم مهندسی صنایع"],
        "activities": ["نصب سنسور و جمع‌آوری داده", "آموزش مدل روی عیوب", "پایش و هشدار", "نگهداری و کالیبراسیون"],
        "partners": ["کارخانه‌ها و پارک‌های فناوری", "تأمین‌کنندگان سنسور", "شرکت‌های مهندسی", "وزارت جهاد و انرژی"],
        "outcome": "کاهش توقف خط و مصرف انرژی",
    },
    "HR, Recruiting & Internal Ops": {
        "segments": ["تیم‌های منابع انسانی شرکت‌های متوسط", "شرکت‌های فناوری و سازمان‌های خدماتی"],
        "channels": ["فروش مستقیم به HR", "لینکدین و رویدادهای HR", "همکاری با مشاوران استخدام", "محتوای تخصصی منابع انسانی"],
        "relationships": ["آنبوردینگ با آیین‌نامه شرکت", "پشتیبانی HR و آموزش", "گزارش تعهد کارکنان", "قرارداد سالانه سازمانی"],
        "resources": ["مدل تحلیل رزومه و گفتار فارسی", "قالب‌های شرح شغل", "داده نظرسنجی و سازمان", "تیم مشاور HR"],
        "activities": ["تحلیل رزومه و مصاحبه", "تولید محتوای HR", "پایش تعهد کارکنان", "پشتیبانی انطباق"],
        "partners": ["شرکت‌های متوسط و بزرگ", "مشاوران استخدام", "پلتفرم‌های آگهی شغلی", "ارائه‌دهندگان ابر"],
        "outcome": "استخدام سریع‌تر و کاهش ترک خدمت",
    },
    "Media, Content & Creator Economy": {
        "segments": ["تولیدکنندگان محتوا و یوتیوبرها", "آژانس‌های رسانه‌ای و پلتفرم‌های ویدیو"],
        "channels": ["اینستاگرام و یوتیوب", "فروش مستقیم به آژانس‌ها", "همکاری با پادکسترها", "پلن رایگان و ارتقای اشتراک"],
        "relationships": ["خودخدمت و اشتراک ماهانه", "پشتیبانی چت", "جامعه تولیدکنندگان", "تخفیف سالانه"],
        "resources": ["مدل گفتار، ترجمه و تولید ویدیو", "کتابخانه موسیقی و قالب", "داده ترند فارسی", "تیم محتوا و پشتیبانی"],
        "activities": ["پردازش ویدیو و صدا", "به‌روزرسانی قالب‌ها", "مدیریت مصرف GPU", "پشتیبانی خالق"],
        "partners": ["پلتفرم‌های ویدیو", "آژانس‌ها", "ارائه‌دهندگان GPU", "شبکه‌های اجتماعی"],
        "outcome": "تولید سریع‌تر محتوای حرفه‌ای با هزینه کمتر",
    },
    "Developer, Data & IT Ops": {
        "segments": ["تیم‌های محصول و استارتاپ‌های فناوری", "تیم‌های داده، امنیت و زیرساخت سازمان‌ها"],
        "channels": ["فروش مستقیم و POC فنی", "جامعه توسعه‌دهندگان و گیت‌هاب", "همکاری با شرکت‌های ابری", "محتوای فنی و وبینار"],
        "relationships": ["دسترسی آزمایشی و مستندات", "پشتیبانی فنی اختصاصی", "SLA و قرارداد سازمانی", "بازخورد محصول و نقشه راه"],
        "resources": ["زیرساخت GPU و مدل", "API و مستندات", "داده و پیکره فارسی", "تیم مهندسی و SRE"],
        "activities": ["توسعه API و زیرساخت", "بهینه‌سازی هزینه استنتاج", "پشتیبانی فنی", "امنیت و انطباق"],
        "partners": ["ارائه‌دهندگان ابر داخلی", "تیم‌های توسعه", "دانشگاه‌ها و پژوهشگاه‌ها", "شرکت‌های امنیت"],
        "outcome": "کاهش زمان توسعه و هزینه زیرساخت هوش مصنوعی",
    },
}

MODEL_UNITS = {
    "min": (300, "دقیقه مصرف ماهانه"),
    "case": (40, "پرونده در ماه"),
    "user": (3, "کاربر به ازای هر مشتری"),
    "dev": (3, "توسعه‌دهنده به ازای هر مشتری"),
    "employee": (20, "کارمند به ازای هر مشتری"),
    "vehicle": (5, "خودرو به ازای هر مشتری"),
    "driver": (5, "راننده به ازای هر مشتری"),
}


def _parse_usd(price):
    if "%" in price:
        return None
    body = price.lstrip("$")
    amount = body.split("/")[0]
    values = []
    for token in amount.split("-"):
        try:
            multiplier = 1000 if token.endswith("k") else 1
            values.append(float(token[:-1] if multiplier == 1000 else token) * multiplier)
        except ValueError:
            return None
    if len(values) == 1:
        values.append(values[0])
    return values[0], values[1], body


def _arpu_toman(service):
    price = service["price"]
    if price == "10-30% of GMV":
        return 100_000_000, "۲۰٪ از ۵۰۰ میلیون تومان GMV ماهانه"
    if price == "3-8% of freight":
        return 16_500_000, "۵٫۵٪ از ۳۰۰ میلیون تومان کرایه ماهانه"
    parsed = _parse_usd(price)
    if not parsed:
        return 15_000_000, "برآورد تحلیل‌گر"
    low, high, body = parsed
    mid = (low + high) / 2
    units = 1
    note = "یک اشتراک ماهانه"
    parts = body.split("/")
    for part in parts[1:]:
        if part in MODEL_UNITS:
            units, note = MODEL_UNITS[part]
            break
    arpu = mid * units * USD_TOMAN
    arpu = round(arpu / 100_000) * 100_000
    return arpu, f"{mid:g} دلار × {units} {note} × ۲۷۰٬۰۰۰ تومان"


def _customer_count(service, arpu):
    model = service["model"]
    if "Consumer" in model:
        base = 280
    elif "Enterprise" in model:
        base = 14
    elif "Commission" in model:
        base = 70
    elif any(token in model for token in ("Per-case", "Per-document", "Per-assessment")):
        base = 35
    elif any(token in model for token in ("Per-seat", "Per-user", "Per-employee", "Per-driver", "Per-vehicle")):
        base = 45
    else:
        base = 50
    price_factor = max(0.45, min(1.6, math.sqrt(8_000_000 / max(arpu, 1))))
    customers = round(base * (0.55 + service["demand"] / 9) * price_factor)
    return max(8, customers)


def _toman_short(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} میلیارد تومان"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} میلیون تومان"
    if value >= 1_000:
        return f"{value / 1_000:.0f} هزار تومان"
    return f"{value:.0f} تومان"


def build_bmc(service):
    arpu, arpu_note = _arpu_toman(service)
    customers = _customer_count(service, arpu)
    collection = 0.90
    revenue_y1 = customers * arpu * MONTHS * collection

    ai = service["ai"].lower()
    if any(token in ai for token in ("voice", "tts", "asr")):
        ai_rate = 0.16
    elif any(token in ai for token in ("ocr", "vision", "diffusion", "imaging")):
        ai_rate = 0.13
    elif any(token in ai for token in ("llm", "rag", "embedding", "generation")):
        ai_rate = 0.09
    elif any(token in ai for token in ("ml", "anomaly", "credit", "time-series")):
        ai_rate = 0.06
    else:
        ai_rate = 0.05

    model = service["model"]
    if "Consumer" in model:
        support_rate, churn, marketing_rate = 0.12, 0.06, 0.25
    elif "Enterprise" in model:
        support_rate, churn, marketing_rate = 0.07, 0.015, 0.12
    else:
        support_rate, churn, marketing_rate = 0.09, 0.03, 0.18

    cogs_rate = ai_rate + 0.07 + support_rate + 0.025
    team_size = {"Low": 3, "Medium": 4, "High": 6, "Very high": 8}[service["difficulty"]]
    team_cost = team_size * AVG_SALARY_TOMAN
    office_cost = 45_000_000 + team_size * 5_000_000
    tools_cost = 25_000_000
    legal_cost = 10_000_000
    fixed_monthly = team_cost + office_cost + tools_cost + legal_cost
    marketing_y1 = max(50_000_000, revenue_y1 * marketing_rate)

    cogs_y1 = revenue_y1 * cogs_rate
    costs_y1 = cogs_y1 + fixed_monthly * MONTHS + marketing_y1
    net_y1 = revenue_y1 - costs_y1

    contribution = arpu * (1 - cogs_rate)
    break_even = max(1, math.ceil((fixed_monthly + 50_000_000) / max(contribution, 1)))
    cac = marketing_y1 / max(customers, 1)
    payback = cac / max(contribution, 1)
    ltv = contribution / churn
    gross_margin = (1 - cogs_rate) * 100

    growth = 2.0 + (service["score"] - 65) / 40
    customers_y3 = round(customers * growth)
    revenue_y3 = customers_y3 * arpu * MONTHS * 0.92
    cogs_y3 = revenue_y3 * cogs_rate
    fixed_y3 = fixed_monthly * MONTHS * 2.2
    marketing_y3 = revenue_y3 * marketing_rate * 0.8
    costs_y3 = cogs_y3 + fixed_y3 + marketing_y3
    net_y3 = revenue_y3 - costs_y3

    capital_need = max(0, -net_y1) + fixed_monthly * 6
    capital_need = round(capital_need / 100_000_000) * 100_000_000

    if "Subscription" in model and any(token in model for token in ("usage", "credits", "per-doc")):
        shares = [("اشتراک پایه", 0.70), ("مصرف و اعتبار", 0.18), ("راه‌اندازی و آموزش", 0.12)]
    elif "Commission" in model:
        shares = [("کمیسیون معامله", 0.85), ("اشتراک فروشنده", 0.10), ("خدمات مدیریت‌شده", 0.05)]
    elif "Enterprise" in model:
        shares = [("قرارداد سازمانی", 0.75), ("راه‌اندازی و یکپارچه‌سازی", 0.15), ("پشتیبانی و SLA", 0.10)]
    elif "Consumer" in model:
        shares = [("اشتراک مصرفی", 0.90), ("اعتبار مصرف", 0.07), ("افزونه و قالب", 0.03)]
    else:
        shares = [("اشتراک ماهانه/سالانه", 0.82), ("راه‌اندازی و آموزش", 0.10), ("مصرف و افزونه", 0.08)]

    revenue_monthly = revenue_y1 / MONTHS
    revenue_streams = [
        {
            "name": name,
            "share": share,
            "monthly": revenue_monthly * share,
            "annual": revenue_y1 * share,
        }
        for name, share in shares
    ]

    cost_items = [
        {"name": "استنتاج هوش مصنوعی و API مدل", "type": "متغیر", "rate": ai_rate, "monthly": revenue_monthly * ai_rate, "annual": revenue_y1 * ai_rate},
        {"name": "زیرساخت ابری، ذخیره‌سازی و پهنای باند", "type": "متغیر", "rate": 0.07, "monthly": revenue_monthly * 0.07, "annual": revenue_y1 * 0.07},
        {"name": "پشتیبانی مشتری", "type": "متغیر", "rate": support_rate, "monthly": revenue_monthly * support_rate, "annual": revenue_y1 * support_rate},
        {"name": "کارمزد پرداخت و درگاه", "type": "متغیر", "rate": 0.025, "monthly": revenue_monthly * 0.025, "annual": revenue_y1 * 0.025},
        {"name": f"حقوق تیم {team_size} نفره", "type": "ثابت", "rate": None, "monthly": team_cost, "annual": team_cost * MONTHS},
        {"name": "بازاریابی و جذب مشتری", "type": "ثابت", "rate": marketing_rate, "monthly": marketing_y1 / MONTHS, "annual": marketing_y1},
        {"name": "دفتر، تجهیزات و ابزارها", "type": "ثابت", "rate": None, "monthly": office_cost + tools_cost, "annual": (office_cost + tools_cost) * MONTHS},
        {"name": "حقوقی، حسابداری و انطباق", "type": "ثابت", "rate": None, "monthly": legal_cost, "annual": legal_cost * MONTHS},
    ]

    category = service["category_en"]
    profile = CATEGORY_BMC[category]
    model_relationship = []
    if "Enterprise" in model:
        model_relationship = ["مدیر موفقیت مشتری اختصاصی", "بازبینی فصلی قرارداد و SLA"]
    elif "Consumer" in model:
        model_relationship = ["ثبت‌نام و پرداخت خودکار", "پشتیبانی چت و انجمن کاربران"]
    else:
        model_relationship = ["آنبوردینگ هدایت‌شده", "پشتیبانی واتساپ و پیامک"]

    value_props = [
        service["what_fa"],
        service["wedge_fa"],
        f"{profile['outcome']} با هزینه قابل پیش‌بینی به تومان.",
    ]

    bmc = {
        "id": service["id"],
        "name": service["name_fa"],
        "category": service["category"],
        "score": service["score"],
        "difficulty": service["difficulty_fa"],
        "market": service.get("market", ""),
        "price_fa": service["price_fa"],
        "blocks": {
            "customer_segments": [service["buyer_fa"]] + profile["segments"],
            "value_propositions": value_props,
            "channels": profile["channels"],
            "customer_relationships": profile["relationships"] + model_relationship,
            "revenue_streams": [f"{item['name']} — {_toman_short(item['monthly'])} در ماه" for item in revenue_streams],
            "key_resources": profile["resources"] + [f"مدل/فناوری: {service['ai']}"],
            "key_activities": profile["activities"],
            "key_partners": profile["partners"] + ["درگاه پرداخت و پیامک محلی"],
            "cost_structure": [f"{item['name']} — {_toman_short(item['monthly'])} در ماه" for item in cost_items],
        },
        "financials": {
            "exchange_rate": USD_TOMAN,
            "arpu": arpu,
            "arpu_note": arpu_note,
            "customers_y1": customers,
            "customers_y3": customers_y3,
            "revenue_y1": revenue_y1,
            "revenue_y3": revenue_y3,
            "cogs_y1": cogs_y1,
            "costs_y1": costs_y1,
            "net_y1": net_y1,
            "costs_y3": costs_y3,
            "net_y3": net_y3,
            "net_margin_y1": net_y1 / max(revenue_y1, 1) * 100,
            "net_margin_y3": net_y3 / max(revenue_y3, 1) * 100,
            "gross_margin": gross_margin,
            "break_even": break_even,
            "cac": cac,
            "payback": payback,
            "ltv": ltv,
            "ltv_cac": ltv / max(cac, 1),
            "capital_need": capital_need,
            "team_size": team_size,
            "churn": churn,
            "marketing_rate": marketing_rate,
            "cogs_rate": cogs_rate,
            "collection": collection,
        },
        "revenue_streams": revenue_streams,
        "cost_items": cost_items,
    }
    return bmc
