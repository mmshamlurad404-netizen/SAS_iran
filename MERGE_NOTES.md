# Merge notes: sourced canvases for services 1-100

What was merged (1 Nov 2026): 100 business model canvases built from sourced inputs
(each number tagged [S] sourced, [D] derived and recomputed by code, [A] assumption) were merged into
the 310-service masterbook. All 100 matched audited services #1-#100 by id and title, so no service was
added and nothing is duplicated. The v3.1 figures are unchanged; the sourced model sits beside them.

## Where things are
- `data/sourced-canvases-100.md`: the 100 canvases, single source of truth (edit this file, then rebuild).
- `data/sourced_canvases.json`, `data/iran-ai-saas-sourced-100.csv`: generated from the file above.
- `scripts/sourced_v4.py`: parser; `scripts/build_v3.py` imports it (the only edits there: load data,
  `sourced_payload`, a "Sourced model (v4)" block on `service.html` / `service_fa.html`, section 10 in both reports).
- `scripts/docx_export.js`: the Word dossier now appends the sourced model for services 1-100.
- `templates/masterbook.css`: styles for the new block.
- Generated files rebuilt: `service*.html`, `index/fa/public/pro/corporate*.html`, `iran-ai-saas-report-v3.1*.md`,
  `data/export-en.json`, `data/export-fa.json`, CSVs.

## Rebuild
`PYTHONPATH=scripts python3 scripts/build_v3.py`

## Known differences between the two models (read before using either)
- v3.1 is a month-12 run rate at 270,000 T/USD with Latka-calibrated account counts; the sourced model is a
  month-by-month ramp at 265,295 T/USD (open market, 17 Oct 2026) with assumed customer counts.
- v3.1 shows all 100 of these services with positive standalone EBITDA at month 12; the sourced base case has
  12 that never break even within 24 months. Section 10 of the report lists both side by side.
- The sourced text is English only; Persian pages show it with a note.
- Many Iranian sites block automated reading, so local competitor prices and market sizes are often unverified;
  each canvas lists what could not be verified.
