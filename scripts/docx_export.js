(function (global) {
  const CRC_TABLE = (function () {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(u8) {
    let c = 0xFFFFFFFF;
    for (let i = 0; i < u8.length; i++) c = CRC_TABLE[(c ^ u8[i]) & 255] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  function u8cat(parts) {
    let n = 0;
    for (const p of parts) n += p.length;
    const out = new Uint8Array(n);
    let o = 0;
    for (const p of parts) { out.set(p, o); o += p.length; }
    return out;
  }

  function dv(n) { const b = new ArrayBuffer(n); return { b, v: new DataView(b), u: new Uint8Array(b) }; }

  function zipStore(files) {
    const enc = new TextEncoder();
    const locals = [];
    const centrals = [];
    let offset = 0;
    for (const f of files) {
      const name = enc.encode(f.name);
      const data = typeof f.data === "string" ? enc.encode(f.data) : f.data;
      const crc = crc32(data);
      const lh = dv(30);
      lh.v.setUint32(0, 0x04034b50, true);
      lh.v.setUint16(4, 20, true);
      lh.v.setUint16(6, 0x0800, true);
      lh.v.setUint16(8, 0, true);
      lh.v.setUint32(14, crc, true);
      lh.v.setUint32(18, data.length, true);
      lh.v.setUint32(22, data.length, true);
      lh.v.setUint16(26, name.length, true);
      locals.push(lh.u, name, data);
      const ch = dv(46);
      ch.v.setUint32(0, 0x02014b50, true);
      ch.v.setUint16(4, 20, true);
      ch.v.setUint16(6, 20, true);
      ch.v.setUint16(8, 0x0800, true);
      ch.v.setUint32(16, crc, true);
      ch.v.setUint32(20, data.length, true);
      ch.v.setUint32(24, data.length, true);
      ch.v.setUint16(28, name.length, true);
      ch.v.setUint32(42, offset, true);
      centrals.push(ch.u, name);
      offset += 30 + name.length + data.length;
    }
    const central = u8cat(centrals);
    const eocd = dv(22);
    eocd.v.setUint32(0, 0x06054b50, true);
    eocd.v.setUint16(8, files.length, true);
    eocd.v.setUint16(10, files.length, true);
    eocd.v.setUint32(12, central.length, true);
    eocd.v.setUint32(16, offset, true);
    return u8cat([...locals, central, eocd.u]);
  }

  function xml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function run(text, fa, opts) {
    opts = opts || {};
    const size = opts.size ? `<w:sz w:val="${opts.size}"/><w:szCs w:val="${opts.size}"/>` : "";
    const bold = opts.bold ? "<w:b/><w:bCs/>" : "";
    const color = opts.color ? `<w:color w:val="${opts.color}"/>` : "";
    const rtl = fa ? "<w:rtl/>" : "";
    const font = fa
      ? '<w:rFonts w:ascii="Tahoma" w:hAnsi="Tahoma" w:cs="Tahoma" w:eastAsia="Tahoma"/>'
      : '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>';
    return `<w:r><w:rPr>${font}${bold}${size}${color}${rtl}</w:rPr><w:t xml:space="preserve">${xml(text)}</w:t></w:r>`;
  }

  function p(text, fa, opts) {
    opts = opts || {};
    const jc = opts.center ? "center" : (fa ? "right" : "left");
    const sp = opts.spaceAfter == null ? 120 : opts.spaceAfter;
    const bidi = fa ? "<w:bidi/>" : "";
    const keep = opts.keep ? "<w:keepNext/>" : "";
    return `<w:p><w:pPr>${keep}<w:spacing w:after="${sp}"/><w:jc w:val="${jc}"/>${bidi}</w:pPr>${run(text, fa, opts)}</w:p>`;
  }

  function heading(text, fa, level) {
    const size = level === 1 ? 36 : level === 2 ? 28 : 22;
    const color = level === 1 ? "0F5C4C" : "17201C";
    return p(text, fa, { bold: true, size: size, color: color, spaceAfter: 160, keep: true });
  }

  function kv(label, value, fa) {
    const jc = fa ? "right" : "left";
    const bidi = fa ? "<w:bidi/>" : "";
    return `<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="${jc}"/>${bidi}</w:pPr>${run(label + (fa ? " " : ": "), fa, { bold: true, size: 20, color: "64706A"})}${run(value == null || value === "" ? "—" : value, fa, { size: 20 })}</w:p>`;
  }

  function pageBreak() {
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>';
  }

  function tbl(headers, rows, fa) {
    const cols = headers.length;
    const width = Math.floor(9360 / cols);
    const grid = headers.map(() => `<w:gridCol w:w="${width}"/>`).join("");
    function cell(text, header) {
      const fill = header ? '<w:shd w:val="clear" w:fill="F1EDE4"/>' : "";
      const jc = fa ? "right" : "left";
      const bidi = fa ? "<w:bidi/>" : "";
      return `<w:tc><w:tcPr><w:tcW w:w="${width}" w:type="dxa"/>${fill}<w:tcBorders><w:top w:val="single" w:sz="4" w:color="E3DED4"/><w:left w:val="single" w:sz="4" w:color="E3DED4"/><w:bottom w:val="single" w:sz="4" w:color="E3DED4"/><w:right w:val="single" w:sz="4" w:color="E3DED4"/></w:tcBorders></w:tcPr><w:p><w:pPr><w:jc w:val="${jc}"/>${bidi}</w:pPr>${run(text, fa, { bold: !!header, size: header ? 16 : 18 })}</w:p></w:tc>`;
    }
    const head = `<w:tr>${headers.map(h => cell(h, true)).join("")}</w:tr>`;
    const body = rows.map(r => `<w:tr>${r.map(c => cell(c, false)).join("")}</w:tr>`).join("");
    return `<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:bidiVisual w:val="${fa ? "1" : "0"}"/><w:tblBorders><w:insideH w:val="single" w:sz="4" w:color="E3DED4"/><w:insideV w:val="single" w:sz="4" w:color="E3DED4"/></w:tblBorders></w:tblPr><w:tblGrid>${grid}</w:tblGrid>${head}${body}</w:tbl><w:p/>`;
  }

  function fmt(n, fa) {
    if (n == null || n === "") return "—";
    const v = Number(n);
    if (!isFinite(v)) return String(n);
    const s = Math.round(v).toString();
    if (!fa) return s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const faDigits = "۰۱۲۳۴۵۶۷۸۹";
    return s.replace(/\B(?=(\d{3})+(?!\d))/g, "٬").replace(/\d/g, d => faDigits[d]);
  }

  function pct(n, fa) {
    if (n == null) return "—";
    const v = Number(n);
    const s = (Math.round(v * 10) / 10).toString();
    if (!fa) return s + "%";
    const faDigits = "۰۱۲۳۴۵۶۷۸۹";
    return s.replace(".", "٫").replace(/\d/g, d => faDigits[d]) + "٪";
  }

  function money(n, fa) {
    return fmt(n, fa) + (fa ? " تومان" : " Toman");
  }

  function serviceXml(s, fa) {
    const parts = [];
    parts.push(heading((s.id ? "#" + s.id + "  " : "") + (s.title || ""), fa, 1));
    parts.push(p([s.sector, s.tier, s.channel_label, s.hosting_label].filter(Boolean).join(" · "), fa, { size: 18, color: "64706A", spaceAfter: 200 }));
    const origin = s.origin === "legacy"
      ? (fa ? "بازنویسی‌شده v1→v3" : "Legacy v1 → v3")
      : (fa ? "حسابرسی‌شده v3" : "Audited v3");
    const meta = [
      [fa ? "خریدار" : "Buyer", s.buyer],
      [fa ? "بخش مشتری" : "Segment", s.segment],
      [fa ? "حکم" : "Verdict", s.verdict],
      [fa ? "موتور" : "Engine", s.engine],
      [fa ? "کانال فروش" : "Sales channel", s.channel_label],
      [fa ? "میزبانی" : "Hosting", s.hosting_label],
      [fa ? "منشأ" : "Origin", origin],
      [fa ? "مدل صورتحساب" : "Billing", s.billing_model],
      [fa ? "جایگزین" : "Replaces", s.replaces],
      [fa ? "ورود به بازار" : "GTM", s.gtm],
      [fa ? "داده / موتور" : "Dataset / driver", s.driver || s.dataset],
      [fa ? "پشته فنی" : "Stack", s.stack],
      [fa ? "زیرساخت" : "Infrastructure", s.infrastructure],
      [fa ? "شرکای توزیع" : "Distribution partners", typeof s.dist_partners === "string" ? s.dist_partners : (s.dist_partners || []).join(", ")],
    ];
    meta.forEach(([k, v]) => { if (v) parts.push(kv(k, v, fa)); });
    if (s.channel_note) parts.push(p(s.channel_note, fa, { size: 18, spaceAfter: 80 }));
    if (s.hosting_note) parts.push(p(s.hosting_note, fa, { size: 18, spaceAfter: 160 }));
    if (s.origin === "legacy") {
      parts.push(p(fa
        ? "این سرویس از کاتالوگ قدیمی v1 آمده و با موتور مالی، بوم ۹بخشی و فرض‌های ۱۴۰۵ به مدل v3 بازنویسی شده است."
        : "This service comes from the legacy v1 catalogue and has been re-underwritten into the v3 model with the 1405 assumptions.", fa, { size: 18, spaceAfter: 200 }));
    }

    parts.push(heading(fa ? "شاخص‌های ماه ۱۲" : "Month-12 metrics", fa, 2));
    const mix = s.active && s.active.mix ? s.active.mix : "";
    const kpi = [
      [fa ? "MRR ناخالص" : "Gross MRR", money(s.mrr, fa)],
      [fa ? "MRR خالص" : "Net collected MRR", money(s.net, fa)],
      [fa ? "مطالبات مشکوک / DSO" : "Bad debt / DSO", money(s.bad_debt, fa)],
      [fa ? "سود ناخالص" : "Gross profit", money(s.gp, fa)],
      [fa ? "حاشیه ناخالص" : "Gross margin", pct(s.gm, fa)],
      [fa ? "EBITDA مستقل" : "Standalone EBITDA", money(s.ebitda, fa)],
      [fa ? "حاشیه مستقل" : "Standalone margin", pct(s.margin, fa)],
      [fa ? "EBITDA سبد" : "Portfolio EBITDA", money(s.portfolio, fa)],
      [fa ? "حاشیه سبد" : "Portfolio margin", pct(s.portfolio_margin, fa)],
      [fa ? "هزینه مستقل" : "Standalone cost", money(s.standalone_cost, fa)],
      [fa ? "هزینه سبد" : "Portfolio cost", money(s.portfolio_cost, fa)],
      ["CAC", money(s.cac, fa)],
      [fa ? "بازگشت CAC" : "CAC payback", (s.payback == null ? "—" : String(s.payback)) + (fa ? " ماه" : " mo")],
      ["LTV:CAC", s.ltv == null ? "—" : (Math.round(s.ltv * 10) / 10) + "x"],
      [fa ? "مشتری سربه‌سر" : "Break-even customers", fmt(s.be, fa)],
      [fa ? "حساب فعال" : "Active accounts", fmt(s.active && s.active.accounts, fa) + (mix ? " (" + mix + ")" : "")],
      [fa ? "ریزش ماهانه" : "Monthly churn", pct(s.churn, fa)],
      ["ARPU", money(s.arpu, fa)],
      [fa ? "پایه / رشد / حرفه‌ای" : "Starter / Growth / Pro", [s.prices && s.prices.starter, s.prices && s.prices.growth, s.prices && s.prices.pro].map(v => money(v, fa)).join(" · ")],
      [fa ? "بسته مصرف" : "Usage pack", money(s.usage_price, fa)],
      [fa ? "گره GPU" : "GPU nodes", s.gpu_nodes == null ? "—" : String(s.gpu_nodes)],
      [fa ? "هزینه GPU" : "GPU cost", money(s.gpu_cost, fa)],
      [fa ? "هزینه NIN" : "NIN cost", money(s.nin_cost, fa)],
      [fa ? "کمیسیون شریک" : "Partner commission", pct(s.partner_pct, fa) + " / " + pct(s.partner_share, fa)],
      [fa ? "بهای شریک" : "Partner COGS", money(s.partner_cogs, fa)],
      [fa ? "ذخیره DSO" : "DSO provision", pct(s.dso_pct, fa)],
      [fa ? "فروش (نفر)" : "Sales FTE", s.sales_fte == null ? "—" : String(s.sales_fte)],
      [fa ? "پشتیبانی (نفر)" : "Support FTE", s.support_fte == null ? "—" : String(s.support_fte)],
      [fa ? "محدوده پشتیبانی" : "Support scope", s.support_scope],
    ];
    kpi.forEach(([k, v]) => parts.push(kv(k, v, fa)));

    if (s.bmc && s.bmc.length) {
      parts.push(heading(fa ? "بوم مدل کسب‌وکار" : "Business Model Canvas", fa, 2));
      s.bmc.forEach(b => {
        parts.push(heading((b.num ? b.num + ". " : "") + (b.title || ""), fa, 3));
        parts.push(p(b.text || "", fa, { size: 20, spaceAfter: 160 }));
      });
    }

    if (s.pl && s.pl.length) {
      parts.push(heading(fa ? "صورت سود و زیان حسابرسی‌شده" : "Audited P&L", fa, 2));
      const headers = fa
        ? ["ردیف", "مبنای محاسبه", "تومان"]
        : ["Line", "Basis", "Toman", "USD"];
      const rows = s.pl.map(r => {
        const toman = fmt(r.toman, fa);
        if (fa) return [r.label || "", r.basis || "", toman];
        const usd = r.usd == null ? "—" : ("$" + fmt(r.usd, false));
        return [r.label || "", r.basis || "", toman, usd];
      });
      parts.push(tbl(headers, rows, fa));
    }
    return parts.join("");
  }

  function documentXml(services, opts) {
    const fa = opts.lang === "fa";
    const title = opts.title || (fa ? "خروجی مستربوک" : "Masterbook export");
    const now = new Date();
    const date = now.toISOString().slice(0, 10);
    const cover = [
      heading(title, fa, 1),
      p(fa ? "سند کامل سرویس‌های انتخاب‌شده / فیلترشده" : "Full dossier of selected / filtered services", fa, { size: 22, color: "64706A" }),
      kv(fa ? "تعداد سرویس" : "Services", String(services.length), fa),
      kv(fa ? "تاریخ" : "Date", date, fa),
      kv(fa ? "نرخ دلار قرارداد" : "Project USD rate", fa ? "۲۷۰٬۰۰۰ تومان" : "270,000 Toman", fa),
      p(fa
        ? "هر سرویس شامل خریدار، کانال، میزبانی، شاخص‌های ماه ۱۲، بوم ۹بخشی و صورت سود و زیان حسابرسی‌شده است."
        : "Each service includes buyer, channel, hosting, Month-12 metrics, the nine-block canvas and the audited P&L.", fa, { size: 20, spaceAfter: 280 }),
    ].join("");
    const body = services.map((s, i) => (i ? pageBreak() : "") + serviceXml(s, fa)).join("");
    const bidi = fa ? '<w:bidi w:val="1"/>' : "";
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>${cover}${pageBreak()}${body}<w:sectPr>${bidi}<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr></w:body>
</w:document>`;
  }

  function buildDocx(services, opts) {
    const fa = opts.lang === "fa";
    const settings = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">${fa ? "<w:bidi/>" : ""}<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>`;
    const styles = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="${fa ? "Tahoma" : "Calibri"}" w:hAnsi="${fa ? "Tahoma" : "Calibri"}" w:cs="Tahoma"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
</w:styles>`;
    const ctypes = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>`;
    const rels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>`;
    const docRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>`;
    const now = new Date().toISOString();
    const core = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>${xml(opts.title || "Masterbook export")}</dc:title>
  <dc:creator>Iran AI SaaS Masterbook</dc:creator>
  <cp:lastModifiedBy>Iran AI SaaS Masterbook</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">${now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">${now}</dcterms:modified>
</cp:coreProperties>`;
    const app = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Iran AI SaaS Masterbook</Application></Properties>`;
    return zipStore([
      { name: "[Content_Types].xml", data: ctypes },
      { name: "_rels/.rels", data: rels },
      { name: "word/document.xml", data: documentXml(services, opts) },
      { name: "word/_rels/document.xml.rels", data: docRels },
      { name: "word/styles.xml", data: styles },
      { name: "word/settings.xml", data: settings },
      { name: "docProps/core.xml", data: core },
      { name: "docProps/app.xml", data: app },
    ]);
  }

  function download(u8, filename) {
    const blob = new Blob([u8], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }

  global.exportServicesDocx = function (services, opts) {
    opts = opts || {};
    const fa = opts.lang === "fa";
    const bytes = buildDocx(services, opts);
    const stamp = new Date().toISOString().slice(0, 10);
    const name = opts.filename || (fa ? ("mostarbook-" + services.length + "-" + stamp + ".docx") : ("masterbook-" + services.length + "-" + stamp + ".docx"));
    download(bytes, name);
    return bytes.length;
  };
})(window);
