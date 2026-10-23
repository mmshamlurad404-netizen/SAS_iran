# AI-Enabled SaaS Opportunities in Iran

> Persian edition: [فرصت‌های SaaS هوش مصنوعی در ایران](iran-ai-saas-report-fa.md)  
> The Persian edition and dashboard use Toman at IRR 270,000 per USD; this English edition keeps the original USD price bands.

## Phase 1 market report and 120-service opportunity catalogue

**Prepared:** 22 October 2026  
**Scope:** AI-first software-as-a-service businesses that can be built and sold primarily inside Iran, with an optional export layer.  
**Interpretation note:** The request used "SAS"; this report treats it as **SaaS** (software as a service) with AI as a core part of the product, not as a side feature.

> **Confidence statement.** This is phase-1 desk research. Macro figures come from the World Bank, WIPO, StartupBlink (via Tehran Times), and public Iranian platform pages. Market sizes, buyer counts, price bands, and scores are analyst estimates, not audited data. They are designed to help choose what to validate next, not to replace customer interviews or paid pilots.

---

## 1. Executive summary

1. **Iran is a large digital market with an unusual cost and payment structure.** Population is about **92.4 million**, internet penetration is **85.3%**, mobile subscriptions are **174 per 100 people**, and **77.4%** of people live in cities. This is enough scale for vertical SaaS, but not enough for lazy consumer subscriptions.
2. **The startup base is small relative to the population but growing quickly.** StartupBlink 2026 ranks Iran **103rd globally** and **10th in West Asia**, with **118 tracked startups**, growth of **54.4%** year on year. Iran also claims **6,000+ startups** and **4,500+ registered knowledge-based companies** outside the tracked index.
3. **Tehran dominates.** The capital hosts **96 tracked startups (81% of the country)** and ranks **348th** among global startup cities. The next wave of software companies will still be sold from Tehran, even when customers are national.
4. **Consumer ARPU is low; B2B ROI selling is where profit lives.** GDP per capita was about **USD 5,190 in 2024** and **USD 3,924 in 2025** on World Bank current-dollar data, with inflation of **32-44%** in recent years. A USD 5 consumer subscription is a real purchase decision. A USD 150 business subscription that saves a clinic, accountant, or contractor several hours per week is much easier to justify.
5. **The winning product is not a translated global SaaS.** It is a **Persian-first workflow** wired into local rails: Moadian e-invoicing, Shaparak payments, Shahkar identity, Kavenegar-style SMS/OTP, Digikala/Basalam seller panels, Divar listings, Torob/Emalls feeds, and Iranian accounting and labor rules.
6. **AI makes previously unprofitable niches viable.** Persian OCR, speech recognition, document extraction, and retrieval over local regulations can now be delivered at low marginal cost. The constraint is trust and distribution, not model capability.
7. **The best near-term profit pools are boring back-office and revenue workflows.** Tax reconciliation, bookkeeping, contract review, clinic reception, real-estate lead qualification, resume screening, review management, marketplace seller operations, tender writing, and document AI rank highest in this catalogue.
8. **Avoid generic horizontal chatbots and ad-supported consumer apps.** They face global alternatives, high support costs, weak willingness to pay, and constant feature catch-up. Vertical depth and local integrations are the defensible moat.
9. **Gross margin is controllable but not automatic.** Target **70-85%** gross margin. Cap inference, use small models, cache aggressively, batch OCR, and offer on-premise deployment for data-sensitive enterprises. Uncapped AI usage can turn a 75% margin product into a 35% margin product overnight.
10. **Phase 2 should be narrow.** Pick **two** plays, run **20 customer interviews**, sign **5 paid pilots**, and require a **payback period under 6 months** before adding a third product line.

---

## 2. Market snapshot

| Indicator | Value | Year | Why it matters |
|---|---:|---|---|
| Population | 92.4 million | 2025 | Scale for vertical SaaS and consumer tools |
| Internet users | 85.3% of population | 2024 | Roughly 78 million addressable online users |
| Mobile subscriptions | 174 per 100 people | 2024 | Mobile-first product design is mandatory |
| Urban population | 77.4% | 2025 | Density makes field sales and service possible |
| GDP per capita | USD 5,190 / USD 3,924 | 2024 / 2025 | Low USD ARPU; current-dollar figures distorted by exchange rates |
| Inflation | 32.5% / 42.2% | 2024 / 2025 | Price annually, preferably quarterly, and prepay |
| Tertiary enrollment | 58.7% gross | 2022 | Large talent pool and education demand |
| Secure internet servers | 7,226 per million | 2024 | Digital infrastructure is improving from a low base |
| Startup ecosystem rank | 103 global, 10 West Asia | 2026 | Small but growing; local competition is still beatable |
| Tracked startups | 118 | 2026 | StartupBlink count; Iran claims 6,000+ total |
| Startup ecosystem growth | +54.4% | 2025-2026 | Fast relative growth from a small base |
| Knowledge-based companies | 4,500+ | 2026 | Tax incentives, grants, and procurement access |
| Science and technology parks | 45+ | 2026 | Distribution and credibility channels |
| University students | 3 million+ | 2026 | Education, hiring, and campus GTM |
| Tehran share of tracked startups | 81% | 2026 | Talent and sales concentration |
| Fintech startups | 23 (19% of tracked) | 2026 | Payments and lending are the most mature vertical |

**Reading the numbers correctly.** Iran's GDP per capita in current USD is not a reliable guide to purchasing power because of exchange-rate distortion and inflation. The practical conclusion is simpler: price in IRR for local customers, keep a USD-linked tier for exporters and diaspora, and sell business outcomes rather than seats.

---

## 3. The Iran-specific operating reality

Any AI SaaS plan that ignores these eight constraints will look good in a slide deck and fail in production.

### 3.1 Payments are local, and recurring billing is weak

- Card payments run through the domestic **Shaparak** network and licensed PSPs. International cards, Stripe, and PayPal are not normal options for local customers.
- Online gateways such as **Zarinpal** (which claims more than one million businesses) work well for one-off payments. True recurring card mandates are limited, so most SaaS companies rely on wallets, manual renewal, annual prepayment, reseller codes, or SMS reminders.
- **Design implication:** build a billing wallet from day one. Offer annual prepay with a 15-20% discount. Treat "subscription" as "prepaid balance plus renewal reminder", not as a Stripe-style auto-charge.

### 3.2 Compute and model access require a local-first architecture

- Sanctions and vendor policies make foreign GPU clouds and AI APIs unreliable, expensive, or unavailable for Iranian entities.
- Local cloud and hosting providers exist, but GPU capacity is scarce and priced at a premium. Many teams self-host open-weight models or use a hybrid of local inference and carefully managed foreign APIs.
- **Design implication:** assume constrained compute. Use small language models for classification and extraction, larger models only for high-value generation, cache aggressively, and offer an on-premise or private-cloud option for banks, hospitals, and law firms.

### 3.3 Connectivity is not always stable

- Access to global platforms fluctuates, and periodic disruptions affect both consumers and businesses. SMS, USSD, and local mirrors remain important fallbacks.
- **Design implication:** make the core workflow work on low bandwidth. Queue actions offline. Send critical notifications by SMS as well as push. Do not make a foreign messaging app the only channel.

### 3.4 Currency and inflation change pricing every quarter

- Inflation has run at **32-44%** in recent years. A price set in IRR in January is a discount by December.
- **Design implication:** publish prices in IRR with a clear revision clause. Keep an internal USD-denominated cost model. Offer prepaid credit packs so customers can lock in value and you get cash upfront.

### 3.5 Regulation is a product requirement, not a legal afterthought

- **Moadian** e-invoicing, VAT rules, labor and social-insurance rules, and municipal permits are all digitized enough to integrate, but complex enough to be a moat.
- Identity verification uses **Shahkar** and related services. Website trust marks such as **Enamad** and **Samandehi** matter for conversion.
- Health, insurance, lending, and education are licensed domains. Partnering with a licensed incumbent is often faster than applying for a license.
- **Design implication:** budget for a part-time legal/regulatory advisor. Build audit logs, consent records, data-retention controls, and a local data-residency option.

### 3.6 Trust is earned through proof, not branding

- Buyers prefer a known vendor, a physical address, a reference customer, and a pilot contract. A polished English website does not substitute for a local case study.
- **Design implication:** sell a 30-day paid pilot with a written success metric. Publish Persian case studies with real numbers. Offer on-premise deployment for sensitive data. Use Enamad and Samandehi where relevant.

### 3.7 Sales is relationship-led and channel-heavy

- Accountants, clinic software vendors, real-estate agencies, ad agencies, ERP integrators, and industry associations control access to SMBs.
- **Design implication:** build a partner program before building a large direct sales team. A partner who already handles a customer's books or clinic software can sell, onboard, and support your product for a 20-30% revenue share.

### 3.8 Talent is strong but retention is hard

- Iran has a deep engineering and data-science talent pool, but emigration and inflation put pressure on salaries. Remote work for foreign companies is a constant competitor for senior engineers.
- **Design implication:** hire for product ownership, not just coding. Use meaningful equity, remote-friendly terms, and export revenue to pay senior staff competitively.

---

## 4. Where profit actually comes from

### 4.1 Unit economics targets

| Metric | Target | Comment |
|---|---:|---|
| Gross margin | 70-85% | Below 60% means inference, support, or hosting is out of control |
| Monthly SMB churn | < 3% | Above 5% means the product is a nice-to-have |
| Monthly enterprise churn | < 1% | Annual contracts and integrations create stickiness |
| CAC payback | < 6 months | Partner-led sales should be closer to 3 months |
| Annual prepay share | > 40% of revenue | Critical for cashflow in a high-inflation market |
| Revenue concentration | No customer > 15% | Protect against a single enterprise loss |

### 4.2 The three profitable models in this market

**A. Vertical SMB SaaS.** A narrow workflow such as clinic reception, seller listing management, or bookkeeping. Low price (USD 20-100/month), high volume, partner-led distribution, and strong retention because the product becomes part of daily operations.

**B. Compliance and document infrastructure.** Moadian reconciliation, contract review, document AI, and tax dispute dossiers. Higher price (USD 100-1,000/month), annual contracts, and defensibility from integrations and local regulatory knowledge.

**C. Enterprise AI with on-premise deployment.** Banks, insurers, hospitals, and large manufacturers pay USD 1,000-10,000/month for private deployment, audit logs, and support. Longer sales cycles, but high contract value and low churn.

### 4.3 The AI cost trap

AI features have three cost layers: model inference, document/audio preprocessing, and human review. The last one is the most underestimated. A "fully automated" product that needs a human to fix 20% of outputs has a support cost that behaves like a services business.

Control the trap with:

- Small models for classification, extraction, and routing.
- Larger models only for customer-facing generation.
- Caching and deduplication of repeated documents and questions.
- Batch processing for non-urgent OCR and transcription.
- Human-in-the-loop only where the value justifies it, with a clear review UI.
- On-premise pricing that includes an annual support and update fee.

### 4.4 Illustrative financial archetypes

| Archetype | Customers | ARPU | MRR | Gross margin | CAC | Payback | Key assumption |
|---|---:|---:|---:|---:|---:|---:|---|
| SMB vertical SaaS | 500 | USD 25 | USD 12,500 | 77% | USD 80 | 3.2 months | 500 paying SMBs after 12-18 months |
| Clinic voice reception | 150 | USD 120 | USD 18,000 | 70% | USD 250 | 2.1 months | 10 new clinics per month via partners |
| Enterprise document AI | 20 | USD 1,500 | USD 30,000 | 60% | USD 3,000 | 2.0 months | 2 new enterprise clients per quarter |

These are planning assumptions, not forecasts. They show the shape of a viable business: modest ARPU, controlled CAC, and annual prepayment.

---

## 5. Demand map by sector

| Sector | Primary buyer | Pain | Willingness to pay | Best AI wedge |
|---|---|---|---|---|
| Accounting and tax | SMBs, accounting firms | Moadian mismatches, VAT deadlines, manual data entry | High | Reconciliation, bookkeeping, dispute dossiers |
| Healthcare | Private clinics, dentists, labs | Reception overload, no-shows, documentation | High | Voice reception, scribe, follow-up |
| Real estate | Agencies, landlords | Lead response time, listing quality, valuation | Medium-high | Lead qualification, listing writer, AVM |
| E-commerce | Sellers, marketplaces | Listing quality, returns, pricing, support | Medium | Seller copilot, catalog enrichment, returns triage |
| Legal | Law firms, notaries, in-house | Contract review, research, document volume | High | Contract review, legal research, PII redaction |
| Recruitment | HR teams, recruiters | CV volume, interview quality, time-to-hire | Medium-high | Screening, interview assistant, sourcing |
| Logistics | Fleets, couriers, distributors | Routing, fuel loss, delivery visibility | Medium-high | Dispatch, fuel anomaly, ETA notifications |
| Manufacturing | Factories | Downtime, quality defects, energy cost | High (enterprise) | Predictive maintenance, visual inspection |
| Education | Schools, teachers, students | Exam prep, teacher workload, admin | Low-medium | Lesson generator, adaptive practice, admin |
| Media and creators | Creators, studios, VOD | Editing time, localization, moderation | Medium | Video editing, subtitling, dubbing |
| Marketing | Agencies, SMBs | Content volume, ad performance, reviews | Medium | Ad copy, product photos, review management |
| Professional services | Consultants, contractors | Tender writing, proposals, compliance | High | Tender/RFP writer, compliance copilot |

---

## 6. How the 120 services were scored

Each service was scored 1-5 on five criteria, then weighted into a 0-100 opportunity score:

| Criterion | Weight | What it measures |
|---|---:|---|
| Demand | 25% | How painful and frequent the problem is |
| Willingness to pay | 20% | Whether the buyer already spends money on this problem |
| Feasibility | 20% | Whether a small team can ship a credible product in 3-6 months |
| Defensibility | 20% | Local integrations, data, workflow lock-in, regulatory knowledge |
| Capital efficiency | 15% | How little capital is needed to reach first revenue |

The score is deliberately biased toward **execution fit in Iran**, not total addressable market. A large market with a 12-month sales cycle and a foreign API dependency scores lower than a boring workflow with 500 ready buyers and a local integration moat.

### Category summary

| Category | Services | Avg. score | Highest-scoring service | Score |
|---|---:|---:|---|---:|
| Sales & Marketing | 10 | 79.8 | Review & Reputation Manager | 84.0 |
| Accounting, Tax & Finance | 10 | 79.2 | Moadian Reconciliation & VAT Assistant | 89.0 |
| E-commerce & Retail | 10 | 76.3 | Catalog Enrichment | 84.0 |
| HR, Recruiting & Internal Ops | 10 | 76.0 | Resume Screening | 81.0 |
| Legal, Compliance & Documents | 10 | 75.6 | Persian Contract Review | 89.0 |
| Healthcare & Clinic Operations | 10 | 74.2 | AI Clinic Receptionist | 85.0 |
| Real Estate, Construction & Facilities | 10 | 74.1 | Real Estate Lead Qualifier | 85.0 |
| Logistics, Fleet & Last-Mile | 10 | 73.3 | Fuel Theft & Anomaly Detection | 80.0 |
| Developer, Data & IT Ops | 10 | 72.8 | Document AI API | 82.0 |
| Media, Content & Creator Economy | 10 | 72.0 | Podcast & Video Repurposing | 80.0 |
| Education & Workforce Training | 10 | 71.9 | Teacher Lesson & Exam Generator | 77.0 |
| Manufacturing, Energy & Agriculture | 10 | 66.9 | Predictive Maintenance | 74.0 |

### The top 25

| Rank | Service | Category | Score | Why it ranks |
|---:|---|---|---:|---|
| 1 | **Moadian Reconciliation & VAT Assistant** | Accounting, Tax & Finance | 89.0 | Matches e-invoices, flags mismatches, and prepares VAT filings. |
| 2 | **Persian Contract Review** | Legal, Compliance & Documents | 89.0 | Flags risky clauses, missing terms, and inconsistencies in Persian contracts. |
| 3 | **AI Bookkeeper** | Accounting, Tax & Finance | 85.0 | Extracts invoices and receipts, categorizes entries, and reconciles bank statements. |
| 4 | **AI Clinic Receptionist** | Healthcare & Clinic Operations | 85.0 | Books appointments by voice and messaging, answers FAQs, sends reminders. |
| 5 | **Real Estate Lead Qualifier** | Real Estate, Construction & Facilities | 85.0 | Replies to inquiries, qualifies budget and timeline, and books visits. |
| 6 | **Review & Reputation Manager** | Sales & Marketing | 84.0 | Monitors Google Maps, Digikala, Snapp, and Torob reviews and drafts replies. |
| 7 | **Catalog Enrichment** | E-commerce & Retail | 84.0 | Fills Persian attributes, size charts, translations, and SEO fields. |
| 8 | **Tender & RFP Writer** | Sales & Marketing | 84.0 | Finds public and private tenders, checks eligibility, drafts proposals. |
| 9 | **Persian Medical Scribe** | Healthcare & Clinic Operations | 82.0 | Listens to the visit and drafts a Persian SOAP note for review. |
| 10 | **Document AI API** | Developer, Data & IT Ops | 82.0 | OCR and extraction for IDs, checks, invoices, and contracts. |
| 11 | **AI Product Photo Studio** | Sales & Marketing | 81.0 | Turns phone photos into catalog and model shots with background cleanup. |
| 12 | **Marketplace Seller Copilot** | E-commerce & Retail | 81.0 | Advises on listings, pricing, inventory, and ads for local marketplaces. |
| 13 | **Resume Screening** | HR, Recruiting & Internal Ops | 81.0 | Ranks Persian CVs against a role and explains the shortlist. |
| 14 | **Persian LLM Gateway** | Developer, Data & IT Ops | 81.0 | One API with local billing, caching, fallback, and data residency. |
| 15 | **Persian Sales Call Analyzer** | Sales & Marketing | 81.0 | Transcribes sales calls, mines objections, and coaches reps. |
| 16 | **Local Ad Optimizer** | Sales & Marketing | 81.0 | Allocates budget and tests creatives across Yektanet, Tapsell, and Adro. |
| 17 | **Returns & Fraud Triage** | E-commerce & Retail | 81.0 | Classifies return reasons and flags serial returners and policy abuse. |
| 18 | **Demand Forecasting for Retail** | E-commerce & Retail | 81.0 | SKU-level forecasts for chains and distributors under volatile demand. |
| 19 | **Tax Dispute Dossier Builder** | Accounting, Tax & Finance | 81.0 | Assembles evidence, forms, and Persian arguments for tax appeals. |
| 20 | **Notary & Registry Doc Prep** | Legal, Compliance & Documents | 81.0 | Drafts deeds, powers of attorney, and registry forms with checks. |
| 21 | **Instagram Ad Copy & Hook Studio** | Sales & Marketing | 80.0 | Generates Persian captions, hooks, CTAs, and A/B variants for shop posts. |
| 22 | **Telegram/WhatsApp Order Bot** | E-commerce & Retail | 80.0 | Takes orders, answers stock and price questions, and routes to fulfillment. |
| 23 | **Listing Writer & Photo Enhancer** | Real Estate, Construction & Facilities | 80.0 | Writes Persian listings and improves photos with optional virtual staging. |
| 24 | **Podcast & Video Repurposing** | Media, Content & Creator Economy | 80.0 | Turns long-form content into clips, posts, and newsletters. |
| 25 | **Market & Competitor Monitor** | Sales & Marketing | 80.0 | Tracks prices, assortment, ads, and social buzz for a category. |

---

## 7. Ten plays worth building first

These are the ten services with the best combination of demand, willingness to pay, feasibility, and defensibility. Each can be launched by a team of 2-4 people within one quarter.

### 7.1 Moadian Reconciliation & VAT Assistant

**Problem:** SMBs and accounting firms struggle to match issued and received e-invoices, reconcile them with bank deposits, and prepare VAT filings. Errors create penalties and consume hours.

**Product:** Connect to Moadian and bank statements, automatically match invoices to payments, flag mismatches, classify VAT, and generate a filing-ready report with a Persian audit trail.

**Buyer and pricing:** SMBs at USD 30-80/month; accounting firms at USD 100-300/month for multi-client dashboards.

**Why it wins:** The integration is hard, the rules change, and the cost of an error is high. Once an accountant runs 50 clients through the product, switching costs are enormous.

**GTM:** Partner with accounting firms and tax consultants. Offer a free reconciliation audit for the first month. Expand from reconciliation to bookkeeping and tax disputes.

**Main risk:** Regulatory changes and API access. Build a manual fallback and a regulatory update process.

### 7.2 AI Bookkeeper

**Problem:** Small businesses keep books in spreadsheets or legacy desktop software. Receipts are paper or photos. Accountants spend hours on data entry and cleanup.

**Product:** Mobile receipt capture, Persian OCR, bank-statement import, automatic categorization, and a review queue that exports to local accounting software.

**Buyer and pricing:** SMBs at USD 20-60/month; accounting firms at USD 100-300/month.

**Why it wins:** It saves measurable hours from the first week, and the accountant becomes a distribution channel. The more historical data it processes, the more valuable the categorization becomes.

**GTM:** Start with 20 accounting firms, not 2,000 SMBs. Let them resell to their clients.

**Main risk:** OCR accuracy on low-quality receipts. Use a human review queue and charge for volume, not "unlimited".

### 7.3 Persian Contract Review

**Problem:** Law firms and SMBs review Persian contracts manually. Risky clauses, missing terms, and inconsistent obligations are easy to miss.

**Product:** Upload a contract, get a clause-by-clause risk report, suggested edits, and a checklist of missing protections. Offer an on-premise or private-cloud option.

**Buyer and pricing:** Law firms at USD 100-300/month; SMBs at USD 50-100/month or per-document.

**Why it wins:** High willingness to pay, a clear professional use case, and a defensible local legal corpus. Confidentiality makes local/on-prem deployment a real advantage over global tools.

**GTM:** Co-sell with law firms. Publish red-flag checklists. Do not position it as a lawyer replacement; position it as a first-pass reviewer.

**Main risk:** Liability and accuracy. Require human review, add disclaimers, and keep a citation trail.

### 7.4 AI Clinic Receptionist

**Problem:** Private clinics miss calls, double-book appointments, and spend staff time on reminders and repetitive questions.

**Product:** A Persian voice and messaging receptionist that books, reschedules, answers FAQs, sends SMS reminders, and escalates urgent cases to a human.

**Buyer and pricing:** Clinics at USD 50-200/month depending on call volume and locations.

**Why it wins:** Immediate ROI in missed appointments and staff time. Persian voice quality is a real barrier for global competitors. Clinics are concentrated and reachable through software vendors and associations.

**GTM:** Sell through clinic management software vendors and dental supply channels. Offer a 30-day pilot with call-answer rate and no-show rate as success metrics.

**Main risk:** Medical advice and emergencies. Hard-code escalation rules and never provide diagnosis.

### 7.5 Real Estate Lead Qualifier

**Problem:** Agencies receive many low-quality inquiries from Divar and Instagram. Response time is slow, and agents waste time on unqualified leads.

**Product:** A Persian chat assistant that responds instantly, asks budget/location/timeline questions, scores leads, books visits, and syncs to the agency's CRM.

**Buyer and pricing:** Agencies at USD 50-200/month; multi-office brokerages at USD 300-800/month.

**Why it wins:** Direct revenue impact: faster response and better lead quality. The product can be sold on a "more qualified visits" promise, not on AI.

**GTM:** Partner with agency associations and CRM vendors. Provide a free lead-response audit.

**Main risk:** Lead data access and platform terms. Use official APIs or customer-provided exports.

### 7.6 Resume Screening

**Problem:** Recruiters receive hundreds of Persian CVs per role, often in inconsistent formats. Screening is slow and biased toward keywords.

**Product:** Upload CVs, rank against a structured role profile, explain the ranking, flag missing must-haves, and generate interview questions.

**Buyer and pricing:** HR teams at USD 50-300/month; recruitment agencies at USD 200-600/month.

**Why it wins:** Clear time savings, easy to trial, and a natural expansion path into interview assistance and sourcing. Persian CV parsing is still weak in global tools.

**GTM:** Sell to recruitment agencies first; they have high volume and can resell to employers.

**Main risk:** Bias and legal exposure. Keep humans in the decision, log criteria, and avoid protected attributes.

### 7.7 Review & Reputation Manager

**Problem:** Local businesses live on Google Maps, Digikala, Snapp, and Torob reviews but do not monitor or respond consistently.

**Product:** Aggregates reviews, detects urgent issues, drafts Persian replies in the brand voice, and reports trends across locations.

**Buyer and pricing:** Clinics, restaurants, retail chains at USD 20-100/month per location.

**Why it wins:** Low price, immediate value, and a strong wedge into broader customer-support and marketing tools. Local platform coverage is a real gap.

**GTM:** Sell through marketing agencies and franchise associations. Offer a free reputation audit.

**Main risk:** Scraping and platform terms. Use official APIs where possible and cache responsibly.

### 7.8 Marketplace Seller Copilot

**Problem:** Sellers on Digikala and Basalam struggle with listing quality, pricing, inventory, and advertising. Small errors cost sales.

**Product:** A copilot that audits listings, suggests titles and attributes, flags stock risks, recommends prices, and drafts ad campaigns.

**Buyer and pricing:** Sellers at USD 15-80/month; large sellers at USD 100-300/month.

**Why it wins:** The seller base is large, digital, and already pays for tools and ads. A 5% sales lift pays for the subscription many times over.

**GTM:** Seller communities, Telegram groups, and marketplace-approved partner programs. Use before/after sales data in case studies.

**Main risk:** Platform dependency. Diversify across marketplaces and direct-to-consumer stores.

### 7.9 Tender & RFP Writer

**Problem:** Contractors and suppliers miss tenders or submit weak proposals because the documents are long, eligibility rules are complex, and deadlines are short.

**Product:** Monitors tender portals, matches opportunities to a company profile, extracts requirements, drafts a Persian proposal, and checks submission completeness.

**Buyer and pricing:** Contractors and IT firms at USD 100-600/month, plus a success fee for large bids.

**Why it wins:** High contract value per customer and a clear link to revenue. Once the company profile and past proposals are loaded, switching is painful.

**GTM:** Industry associations, chambers of commerce, and bid consultants. Start with one sector such as construction or IT services.

**Main risk:** Data access and accuracy of eligibility checks. Keep a human review step before submission.

### 7.10 Document AI API

**Problem:** Banks, insurers, fintechs, and logistics companies process Persian IDs, checks, invoices, and contracts manually.

**Product:** An API that extracts structured data from Persian documents with confidence scores, human-review queues, and on-premise deployment.

**Buyer and pricing:** Enterprises at USD 300-2,000/month plus usage.

**Why it wins:** Horizontal infrastructure with many use cases, high switching costs, and a defensible Persian document corpus. It can be sold directly or embedded in other SaaS products.

**GTM:** Start with one document type in one industry, such as checks for a lender or waybills for a freight forwarder. Expand by document type, not by industry.

**Main risk:** Accuracy and data security. Invest in evaluation sets, audit logs, and private deployment.

---

## 8. Full catalogue of 120 services

The catalogue is grouped into **12 categories** of ten services each. Scores are on a 0-100 scale using the method in section 6. The same data is available in `data/iran-ai-saas-services.csv` for sorting and filtering.

### Sales & Marketing

*10 services, average opportunity score 79.8/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 1 | **Instagram Ad Copy & Hook Studio** | Instagram sellers, small agencies | Persian slang, catalog awareness, Nowruz/Yalda occasion packs. | $10-40/mo | Subscription | 80.0 |
| 2 | **AI Product Photo Studio** | E-commerce sellers, fashion retailers | Modest-wear presets, local size charts, low-cost batch processing. | $15-80/mo | Subscription + credits | 81.0 |
| 3 | **B2B Lead Finder & Outreach** | Agencies, B2B SaaS, wholesalers | Local directories, Persian email etiquette, Instagram DM workflows. | $30-150/mo | Subscription | 76.0 |
| 4 | **Persian SEO Content Engine** | Publishers, e-commerce, agencies | Persian morphology, local search intent, Google plus local engines. | $50-300/mo | Subscription | 76.0 |
| 5 | **Review & Reputation Manager** | Clinics, restaurants, retailers | Local platforms global tools ignore, Persian tone, escalation rules. | $20-100/mo | Subscription | 84.0 |
| 6 | **Persian Sales Call Analyzer** | Call centers, insurers, real estate | Persian dialect ASR, local CRM integration, IRR scripts. | $100-500/mo | Per-seat + usage | 81.0 |
| 7 | **Tender & RFP Writer** | Contractors, IT firms, suppliers | Iranian tender portals, Persian forms, local qualification rules. | $100-600/mo | Subscription + success fee | 84.0 |
| 8 | **UGC & Storyboard Generator** | Brands, agencies, creators | Persian cultural cues, local trends, low-budget production plans. | $20-100/mo | Subscription | 75.0 |
| 9 | **Local Ad Optimizer** | Performance agencies, e-commerce | Local ad APIs, Persian creatives, IRR bidding and reporting. | $100-500/mo | Subscription + spend % | 81.0 |
| 10 | **Market & Competitor Monitor** | FMCG, retailers, investors | Local marketplaces and Instagram, Persian sentiment, IRR normalization. | $100-800/mo | Subscription | 80.0 |

### E-commerce & Retail

*10 services, average opportunity score 76.3/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 11 | **Marketplace Seller Copilot** | Basalam and Digikala sellers | Seller panels, Persian attributes, local fees and logistics rules. | $15-80/mo | Subscription | 81.0 |
| 12 | **Product Feed Optimizer** | E-commerce managers | Persian taxonomy, local comparison engines, RTL attributes. | $50-300/mo | Subscription | 79.0 |
| 13 | **Returns & Fraud Triage** | E-commerce, marketplaces | Local order data, Persian chat, COD dispute patterns. | $100-500/mo | Subscription | 81.0 |
| 14 | **Visual Search & Similar Products** | Marketplaces, fashion retailers | Persian fashion and home catalog, modest-wear coverage. | $200-1k/mo | Usage-based | 61.0 |
| 15 | **Demand Forecasting for Retail** | Retail chains, distributors | Iranian holidays, inflation shocks, local seasonality and stockouts. | $200-1k/mo | Subscription | 81.0 |
| 16 | **Shelf Audit from Phone Photos** | FMCG distributors | Local brands, low-cost Android, offline-first field sync. | $150-800/mo | Per-store + subscription | 74.0 |
| 17 | **Telegram/WhatsApp Order Bot** | Small shops, bakeries, grocers | Telegram-first commerce, Persian voice notes, simple settlement. | $10-50/mo | Subscription | 80.0 |
| 18 | **Personalization & Coupon Engine** | E-commerce managers | Sparse data, COD behavior, local category structure. | $200-1k/mo | Subscription | 73.0 |
| 19 | **Catalog Enrichment** | Marketplaces, large sellers | Persian taxonomy, RTL normalization, local sizing conventions. | $30-200/mo | Usage-based | 84.0 |
| 20 | **Counterfeit & Listing Quality Detector** | Marketplaces, brand owners | Local brand registry, Persian text patterns, image reuse detection. | $300-1.5k/mo | Enterprise | 69.0 |

### Accounting, Tax & Finance

*10 services, average opportunity score 79.2/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 21 | **AI Bookkeeper** | SMBs, accounting firms | Persian OCR, Iranian bank formats, Moadian-ready exports. | $20-100/mo | Subscription | 85.0 |
| 22 | **Moadian Reconciliation & VAT Assistant** | SMBs, accountants | Direct Moadian integration, Iranian tax code, Persian explanations. | $30-150/mo | Subscription | 89.0 |
| 23 | **Expense & Receipt Capture** | SMBs, field teams | Persian receipts, RTL UI, SMS and Telegram approvals. | $10-50/user/mo | Per-seat | 79.0 |
| 24 | **SMB CFO Copilot** | Founders, finance managers | IRR inflation, local tax rules, Persian management reports. | $50-300/mo | Subscription | 76.0 |
| 25 | **Payroll & Labor Law Calculator** | SMBs, HR teams | Current labor and social-insurance rules, Persian payslips. | $30-150/mo | Subscription | 77.0 |
| 26 | **Audit Sampling & Anomaly Detection** | Audit firms | Iranian charts of accounts, Persian explanations, local audit standards. | $200-1k/mo | Enterprise | 72.0 |
| 27 | **SME Credit Scoring** | Banks, fintechs, lenders | Alternative data, local defaults, thin-file borrowers. | $1k-5k/mo | Enterprise + per-score | 74.0 |
| 28 | **Collections Assistant** | SMBs, lenders | Persian tone, local payment links, installment norms. | $30-150/mo | Subscription | 79.0 |
| 29 | **FX & Import Cost Tracker** | Importers, trading companies | Local FX rates, customs costs, inflation-adjusted margins. | $50-300/mo | Subscription | 80.0 |
| 30 | **Tax Dispute Dossier Builder** | Accountants, lawyers, SMBs | Iranian tax procedures, hearing formats, Persian legal letters. | $100-500/mo | Per-case + subscription | 81.0 |

### Legal, Compliance & Documents

*10 services, average opportunity score 75.6/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 31 | **Persian Contract Review** | Law firms, SMBs, in-house counsel | Iranian civil law, Persian drafting style, on-prem option. | $50-300/mo | Subscription + per-doc | 89.0 |
| 32 | **Legal Research Assistant** | Lawyers, in-house counsel | Persian legal corpus, local citations, court hierarchy. | $50-300/mo | Subscription | 77.0 |
| 33 | **Notary & Registry Doc Prep** | Notaries, lawyers | Official Persian forms, registry rules, local property clauses. | $50-250/mo | Subscription + per-doc | 81.0 |
| 34 | **Compliance Copilot** | SMBs, operations managers | Iranian regulations, update tracking, Persian guidance. | $30-150/mo | Subscription | 76.0 |
| 35 | **E-discovery & Document Review** | Law firms, corporates | Persian OCR, on-prem deployment, privilege controls. | $300-1.5k/mo | Enterprise | 69.0 |
| 36 | **Trademark & Patent Search** | Brands, IP firms | Local registry data, Persian marks, class recommendations. | $50-300/mo | Per-search + subscription | 72.0 |
| 37 | **Corporate Docs Generator** | Companies, lawyers | Iranian corporate law, Persian formal register. | $30-150/mo | Subscription | 79.0 |
| 38 | **Visa & Immigration Doc Assistant** | Individuals, immigration agencies | Persian applicants, embassy-specific quirks, translation checks. | $10-50/case | Per-case | 68.0 |
| 39 | **Litigation Strategy Assistant** | Litigators | Iranian courts, Persian procedure, local precedent. | $100-500/mo | Subscription | 69.0 |
| 40 | **PII Redaction** | Law firms, hospitals, BPOs | Persian NER, national ID and card formats, on-prem option. | $50-300/mo | Usage-based | 76.0 |

### Healthcare & Clinic Operations

*10 services, average opportunity score 74.2/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 41 | **Persian Medical Scribe** | Physicians, clinics | Persian medical vocabulary, local EHR exports, consent workflow. | $50-200/mo | Per-physician | 82.0 |
| 42 | **AI Clinic Receptionist** | Clinics, dentists, labs | Persian voice, local calendars, SMS and WhatsApp reminders. | $50-200/mo | Subscription | 85.0 |
| 43 | **Patient Follow-up & Adherence** | Clinics, hospitals | Persian messaging, local care pathways, family contact norms. | $50-250/mo | Per-patient | 76.0 |
| 44 | **Non-diagnostic Triage Chatbot** | Clinics, insurers | Persian symptom language, local care pathways, hard safety rails. | $100-500/mo | Subscription | 64.0 |
| 45 | **Medical Coding & Claims** | Clinics, insurers | Iranian insurance rules, Persian documentation, local code sets. | $100-500/mo | Subscription | 74.0 |
| 46 | **Radiology Workflow Triage** | Imaging centers, hospitals | Local PACS integration, Persian reports, regulatory review. | $500-3k/mo | Enterprise | 62.0 |
| 47 | **Dental Practice Copilot** | Dentists | Persian dental terminology, local insurance, installment plans. | $50-200/mo | Subscription | 80.0 |
| 48 | **Pharmacy Inventory & Rx OCR** | Pharmacies | Persian handwriting, local drug database, insurance codes. | $40-150/mo | Subscription | 77.0 |
| 49 | **Mental Health Journal & Coach** | Consumers | Persian emotional language, privacy-first design, local crisis resources. | $3-10/mo | Consumer subscription | 71.0 |
| 50 | **Lab Report Explainer** | Patients, clinics | Persian lab formats, reference ranges, strong disclaimers. | $2-8/mo | Freemium + B2B | 71.0 |

### Education & Workforce Training

*10 services, average opportunity score 71.9/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 51 | **Konkur Adaptive Practice** | Students, parents | Iranian curriculum, Konkur format, Persian explanations. | $5-20/mo | Consumer subscription | 74.0 |
| 52 | **Medical & Engineering Exam Prep** | University entrance candidates | Local syllabi, Persian terminology, past-exam patterns. | $8-25/mo | Consumer subscription | 69.0 |
| 53 | **AI Language Tutor** | Consumers, schools | Persian-L1 error patterns, RTL UI, low-bandwidth audio. | $5-20/mo | Consumer subscription | 70.0 |
| 54 | **School Admin Assistant** | Private schools | Iranian school software, Persian SMS, parent communication norms. | $50-300/mo | Per-school | 73.0 |
| 55 | **Teacher Lesson & Exam Generator** | Teachers, schools | Iranian textbooks, Persian assessment style, curriculum alignment. | $5-30/mo | Freemium + subscription | 77.0 |
| 56 | **Corporate Training Simulator** | Banks, telcos, retailers | Persian scripts, local scenarios, manager dashboards. | $200-1k/mo | Enterprise | 74.0 |
| 57 | **CV & Interview Coach** | Job seekers, universities | Iranian job market, Persian interview norms, salary context. | $3-15/mo | Freemium + subscription | 76.0 |
| 58 | **Skills Assessment & Learning Path** | Companies, training centers | Local labor market, Persian certifications, employer input. | $20-100/mo | Per-assessment | 71.0 |
| 59 | **Persian Plagiarism & AI Detector** | Universities, schools | Persian corpora, local academic norms, appeal workflow. | $100-500/mo | Per-seat | 70.0 |
| 60 | **Tutoring Marketplace with AI Matching** | Parents, tutors | Local tutors, trust and verification, installment payments. | 10-30% of GMV | Commission | 65.0 |

### Real Estate, Construction & Facilities

*10 services, average opportunity score 74.1/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 61 | **Listing Writer & Photo Enhancer** | Agencies, property owners | Divar norms, local property types, neighborhood vocabulary. | $15-60/mo | Subscription | 80.0 |
| 62 | **Real Estate Lead Qualifier** | Agencies | Persian chat, Divar and Instagram leads, visit scheduling. | $50-200/mo | Subscription | 85.0 |
| 63 | **Property Valuation (AVM)** | Agencies, banks, investors | Local listing data, inflation-adjusted comparables, neighborhood effects. | $100-500/mo | API + subscription | 77.0 |
| 64 | **Virtual Staging & Renovation Visualizer** | Agencies, contractors, homeowners | Local interior styles, Persian homes, budget material options. | $20-100/mo | Credits + subscription | 72.0 |
| 65 | **Construction Takeoff & BOQ** | Contractors, consultants | Iranian price lists, metric units, Persian specifications. | $200-1k/mo | Per-project | 77.0 |
| 66 | **Permit & Document Checker** | Developers, architects | Local municipal rules, Persian forms, change tracking. | $50-300/mo | Subscription | 71.0 |
| 67 | **Facilities Ticketing & Predictive Maintenance** | Property managers, malls | Persian requests, local vendors, SMS notifications. | $100-500/mo | Subscription | 68.0 |
| 68 | **Lease Abstraction** | Landlords, REITs, law firms | Persian leases, local clauses, escalation schedules. | $100-500/mo | Per-document + subscription | 72.0 |
| 69 | **Architectural Concept Generator** | Architects, developers | Local codes, cultural styles, Persian brief interpretation. | $30-150/mo | Subscription | 67.0 |
| 70 | **Rental Market Analytics** | Investors, agencies | Local listing data, inflation adjustment, neighborhood granularity. | $100-500/mo | Subscription | 72.0 |

### Logistics, Fleet & Last-Mile

*10 services, average opportunity score 73.3/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 71 | **Dispatch & Route Optimization** | Distributors, couriers | Tehran traffic, informal addresses, COD and return flows. | $100-500/mo | Subscription | 77.0 |
| 72 | **Delivery ETA & Notifications** | E-commerce, couriers | Local traffic patterns, Persian messaging, low-cost SMS fallback. | $50-300/mo | Usage-based | 76.0 |
| 73 | **Warehouse Slotting & Inventory** | Warehouses, distributors | Local SKU profiles, space constraints, manual processes. | $200-1k/mo | Subscription | 72.0 |
| 74 | **Freight Document OCR** | Freight forwarders | Persian documents, local formats, customs fields. | $50-300/mo | Usage-based | 76.0 |
| 75 | **Driver Safety Coaching** | Fleets, insurers | Local roads, Persian coaching, insurance incentives. | $5-15/driver/mo | Per-driver | 69.0 |
| 76 | **Fuel Theft & Anomaly Detection** | Fleets | Local fuel cards, GPS data, manual logs. | $3-10/vehicle/mo | Per-vehicle | 80.0 |
| 77 | **Cold-Chain Monitoring** | Pharma and food distributors | Local cold-chain gaps, SMS alerts, calibration workflows. | $100-500/mo | Subscription + hardware | 72.0 |
| 78 | **Courier Chatbot & Proof of Delivery** | Couriers, e-commerce | Persian, WhatsApp and Telegram, local address quirks. | $30-150/mo | Subscription | 76.0 |
| 79 | **Customs Tariff Classifier** | Importers, customs brokers | Iranian customs rules, Persian descriptions, update tracking. | $100-500/mo | Per-declaration + subscription | 77.0 |
| 80 | **Load Matching Marketplace** | Truckers, shippers | Local lanes, trust and verification, COD settlement. | 3-8% of freight | Commission | 58.0 |

### Manufacturing, Energy & Agriculture

*10 services, average opportunity score 66.9/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 81 | **Predictive Maintenance** | Factories | Old equipment, local technicians, Persian alerts. | $300-2k/mo | Subscription + sensors | 74.0 |
| 82 | **Visual Quality Inspection** | Factories | Local products, low-cost edge devices, Persian dashboards. | $500-3k/mo | Per-line | 69.0 |
| 83 | **Energy Consumption Optimizer** | Factories, large buildings | Subsidized energy makes ROI complex; focus on quality and outages. | $200-1k/mo | Subscription | 61.0 |
| 84 | **Production Planning & Scheduling** | Factories | Local supply volatility, Persian shop-floor workflows. | $300-1.5k/mo | Subscription | 69.0 |
| 85 | **Safety & PPE Monitoring** | Industrial sites | Local HSE rules, Persian reports, edge deployment. | $300-1.5k/mo | Per-camera | 65.0 |
| 86 | **Crop Disease Detection** | Farmers, agricultural co-ops | Local crops, Persian guidance, offline mode. | $2-10/mo | Freemium + B2B | 61.0 |
| 87 | **Irrigation Optimizer** | Farms, greenhouses | Water scarcity, local crops, low-connectivity sensors. | $50-300/mo | Subscription + hardware | 70.0 |
| 88 | **Livestock Health & Yield** | Dairy and poultry farms | Local breeds, Persian alerts, vet integration. | $100-500/mo | Subscription + hardware | 69.0 |
| 89 | **Solar & Wind Forecasting** | Renewables, industrials | Local irradiance and wind data, grid constraints. | $300-1.5k/mo | Subscription | 60.0 |
| 90 | **Supplier Risk Monitor** | Manufacturers, importers | Local supplier networks, Persian sources, FX exposure. | $100-500/mo | Subscription | 71.0 |

### HR, Recruiting & Internal Ops

*10 services, average opportunity score 76.0/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 91 | **Resume Screening** | HR teams, recruiters | Persian CVs, local universities, Iranian job titles. | $50-300/mo | Subscription | 81.0 |
| 92 | **Interview Assistant** | HR teams, hiring managers | Persian interviews, local role competencies, structured scorecards. | $50-300/mo | Subscription | 73.0 |
| 93 | **JD & Sourcing Copilot** | Recruiters | Persian job market, local boards, salary context. | $30-150/mo | Subscription | 75.0 |
| 94 | **Engagement Survey Analytics** | HR teams | Persian sentiment, local culture, anonymity safeguards. | $100-500/mo | Subscription | 71.0 |
| 95 | **HR Policy Q&A Bot** | Employees, HR | Iranian labor law, Persian policy documents, escalation. | $20-100/mo | Per-seat | 76.0 |
| 96 | **Payroll Explainer Bot** | Employees, HR | Iranian payroll rules, Persian payslip formats. | $10-50/mo | Per-seat | 75.0 |
| 97 | **Persian Meeting Notes** | Teams, consultancies | Persian ASR, mixed English technical terms, RTL summaries. | $10-40/user/mo | Per-seat | 77.0 |
| 98 | **Company Knowledge Base Builder** | Mid-market companies | Persian docs, on-prem option, access controls. | $200-1k/mo | Subscription | 80.0 |
| 99 | **Internal IT Helpdesk** | IT teams | Persian, local software, asset and access workflows. | $100-500/mo | Subscription | 76.0 |
| 100 | **Shift Scheduling** | Operations managers | Iranian labor rules, Persian UI, last-minute absence handling. | $2-5/employee/mo | Per-employee | 76.0 |

### Media, Content & Creator Economy

*10 services, average opportunity score 72.0/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 101 | **Persian Video Editor** | Creators, agencies | Persian ASR, RTL subtitles, local platform aspect ratios. | $10-50/mo | Subscription | 77.0 |
| 102 | **Podcast & Video Repurposing** | Creators, brands | Persian content, local platforms, Persian copywriting. | $15-60/mo | Subscription | 80.0 |
| 103 | **AI Dubbing & Localization** | Studios, VOD, brands | Persian voices, local licensing, cultural adaptation. | $50-300/mo | Per-minute + subscription | 73.0 |
| 104 | **Thumbnail & Title Lab** | Creators, media | Persian YouTube and Aparat trends, local taboos. | $10-50/mo | Subscription | 75.0 |
| 105 | **AI Music & Sound Design** | Creators, agencies | Iranian musical styles, licensing clarity, brand safety. | $10-50/mo | Subscription + credits | 63.0 |
| 106 | **Newsroom Assistant** | Newsrooms | Persian news, local sources, editorial guardrails. | $200-1k/mo | Enterprise | 69.0 |
| 107 | **Persian Subtitling for VOD** | VOD, e-learning | Persian ASR accuracy, RTL rendering, local slang. | $0.1-0.5/min | Per-minute | 76.0 |
| 108 | **Comic & Storyboard Generator** | Creators, animation studios | Persian stories, cultural styles, character consistency. | $20-80/mo | Subscription | 63.0 |
| 109 | **Personal Brand Ghostwriter** | Founders, professionals | Persian professional tone, local topics, voice cloning from samples. | $20-100/mo | Subscription | 75.0 |
| 110 | **Persian UGC Moderation** | Platforms, marketplaces | Persian slang, local context, fast review queue. | $200-1k/mo | Usage-based | 69.0 |

### Developer, Data & IT Ops

*10 services, average opportunity score 72.8/100.*

| # | Service | Primary buyer | Iran-specific wedge | Price band | Model | Score |
|---:|---|---|---|---|---|---:|
| 111 | **Persian LLM Gateway** | Startups, enterprises | IRR billing, local hosting, Persian benchmarks, compliance. | $50-1k/mo | Usage-based | 81.0 |
| 112 | **AI Code Assistant for Persian Teams** | Development teams | Persian comments, RTL frontends, local frameworks and APIs. | $10-30/dev/mo | Per-seat | 68.0 |
| 113 | **Test Generation & QA** | Enterprises, dev shops | Persian business logic, local stacks, regression safety. | $100-500/mo | Subscription | 68.0 |
| 114 | **Log & Incident Copilot** | IT ops, banks | Local infrastructure, Persian summaries, on-prem. | $200-1k/mo | Subscription | 65.0 |
| 115 | **Persian BI & SQL Copilot** | Analysts, SMBs | Persian, local databases, RTL charts, access control. | $50-300/mo | Per-seat | 73.0 |
| 116 | **Persian Data Labeling Platform** | AI teams, research labs | Persian annotators, local compliance, fast throughput. | $500-3k/mo | Managed service | 68.0 |
| 117 | **Document AI API** | Fintechs, insurers, banks | Persian documents, national ID and card formats, on-prem. | $100-1k/mo | Usage-based | 82.0 |
| 118 | **Persian TTS & Voice Clone API** | Enterprises, media | Persian accents, local licensing, emotional control. | $50-500/mo | Usage-based | 77.0 |
| 119 | **RAG Chatbot Builder** | SMBs, enterprises | Persian, local integrations, data residency, easy handoff. | $50-300/mo | Subscription | 77.0 |
| 120 | **Security Copilot for SOC** | Banks, enterprises, SOCs | Persian logs, local threat intel, on-prem deployment. | $500-2k/mo | Enterprise | 69.0 |


---

## 9. Go-to-market playbook

### 9.1 Pick one beachhead, not a platform

The fastest path to revenue is one workflow, one buyer type, one city, and one channel. "AI platform for Iranian businesses" is not a beachhead. "Moadian reconciliation for 50 accounting firms in Tehran" is.

A good beachhead has four properties:

- The buyer already spends money on the problem.
- The workflow is frequent, not annual.
- The output can be measured in hours saved, errors avoided, or revenue gained.
- A channel partner already has access to the buyer.

### 9.2 Channel partners by category

| Category | Best channel | Why |
|---|---|---|
| Accounting and tax | Accounting firms, tax consultants | They already manage many SMBs and can resell |
| Healthcare | Clinic software vendors, dental suppliers, medical associations | Trust and workflow access |
| Real estate | Agency associations, CRM vendors, Divar-focused agencies | Concentrated buyer base |
| E-commerce | Seller communities, marketplace partner programs, ad agencies | Digital buyers, fast trials |
| Legal | Bar associations, law firms, notary networks | Credibility and confidentiality requirements |
| Recruitment | Recruitment agencies, HR communities | High volume, measurable ROI |
| Logistics | Fleet-management vendors, fuel-card providers, distributors | Hardware and operations relationships |
| Manufacturing | Industrial parks, engineering firms, equipment vendors | Long sales cycles but high contract value |

### 9.3 Demand generation that works in Iran

- **Persian SEO:** Long-tail queries such as "نرم افزار مغایرت گیری مودیان" or "هوش مصنوعی برای مطب" convert well because competition is low.
- **Instagram and Telegram:** Still the main discovery channels for SMBs. Use short demos, customer stories, and direct-response offers.
- **Webinars and workshops:** "How to reconcile Moadian invoices in 30 minutes" outperforms generic AI webinars.
- **Associations and chambers:** Co-host training sessions and publish a joint checklist.
- **Exhibitions:** ELECOMP, INOTEX, Iran Med, Iran Smart City, and industry-specific trade shows are still effective for B2B trust.
- **Referral program:** Give partners and customers a revenue share or service credit, not a discount.

### 9.4 Sales motion

1. **Diagnostic call (20 minutes):** Quantify the current cost of the workflow. Do not demo first.
2. **Tailored demo (20 minutes):** Show only the workflow the buyer described.
3. **Paid pilot (30 days):** One success metric, one owner, one weekly check-in. Charge a small fee to filter serious buyers.
4. **Convert to annual contract:** Offer a 15-20% discount for annual prepayment. Include onboarding and training.
5. **Expand:** Add a second workflow only after the first is used weekly.

### 9.5 Pricing and packaging

- **Three tiers plus usage.** A low-priced starter tier for trial, a core tier for the main buyer, and an enterprise tier with on-premise, SSO, audit logs, and support.
- **Annual prepay.** Critical for cashflow and inflation protection. Target 40%+ of revenue.
- **Setup fee.** Charge for data migration, integrations, and training. It filters low-intent buyers and funds onboarding.
- **Usage caps.** Define document, minute, or seat limits. Charge overages instead of offering "unlimited AI".
- **Inflation clause.** Publish a quarterly or semi-annual price review. Grandfather annual prepayers.
- **Outcome pricing where possible.** For collections, tenders, and lead generation, a success fee aligns incentives and increases willingness to pay.

### 9.6 Knowledge-based status and incentives

Iran's knowledge-based company status can bring tax benefits, grants, and access to science parks and procurement. It is useful but slow. Do not make it a dependency for the first six months. Apply once the product has revenue and a clear R&D narrative.

### 9.7 Export layer

The same product can be sold to Persian-speaking markets and the diaspora:

- **Diaspora:** Price in USD/EUR, sell remotely, support in Persian and English.
- **Afghanistan and Tajikistan:** Persian-language products with lower price points and local payment partners.
- **Iraq and CIS:** Strong trade links, but require local partners and Arabic/Russian localization.
- **Global niche:** Persian OCR, subtitling, and voice tools can be sold to media companies and researchers worldwide.

Export revenue is valuable because it is denominated in hard currency, but it adds support and compliance complexity. Treat it as a second phase, not the first.

---

## 10. Compliance, risk and resilience

### 10.1 Data and privacy

- Keep sensitive data (health, financial, legal) in local or private infrastructure.
- Build consent records, retention policies, access logs, and deletion workflows.
- Offer a PII-redaction mode for documents sent to any external model.
- Avoid sending raw customer data to foreign APIs without explicit consent and a data-processing agreement.

### 10.2 AI accuracy and liability

- Use human-in-the-loop for medical, legal, financial, and safety decisions.
- Publish clear limitations and require the customer to review outputs.
- Keep citations and confidence scores for every extracted fact or clause.
- Buy professional liability insurance where available.
- Do not position products as substitutes for licensed professionals.

### 10.3 Content and platform rules

- Persian content moderation must handle slang, sarcasm, and local context.
- Platforms and marketplaces have terms of service; use official APIs or customer-provided data.
- Keep an abuse-reporting and takedown process.

### 10.4 Licensing

- Payments, lending, insurance, health, and education are regulated. Partner with licensed entities or obtain advice before launching.
- A "software tool" can still be treated as a regulated service if it makes decisions or handles money.

### 10.5 Sanctions and supply chain

- Do not build the core product on a foreign API that can be cut off without notice.
- Keep a local fallback model and a manual fallback process.
- Screen hardware and software vendors for export-control exposure.
- Maintain a legal entity and banking setup that can receive export payments.

### 10.6 Business continuity

- Host in at least two local availability zones or providers.
- Use SMS and phone fallbacks for critical notifications.
- Keep an offline mode for field and clinic workflows.
- Test incident response quarterly.
- Document a manual process for every automated workflow so customers can continue during an outage.

---

## 11. 90-day validation plan

| Phase | Weeks | Actions | Output |
|---|---|---|---|
| Select | 1-2 | Choose two services from the top 25. Interview 20 buyers. Map the current workflow and cost. | Two validated problem statements and buyer profiles |
| Build | 3-6 | Build the smallest useful workflow with 5 design partners. Integrate one local rail (Moadian, Shahkar, Zarinpal, Kavengar, or a marketplace API). | Working MVP used weekly by 5 design partners |
| Pilot | 7-10 | Convert to paid pilots. Define one success metric. Measure time saved, errors reduced, or revenue gained. | 5 paid pilots with baseline and endline data |
| Decide | 11-13 | Package pricing, publish one case study, sign one channel partner. Decide to scale, pivot, or stop. | Go/no-go memo and a 12-month plan |

**Go criteria:**

- At least 5 of 10 pilot customers pay.
- At least 3 use the product weekly without prompting.
- Measured ROI is at least 3x the price.
- CAC payback is under 6 months.
- Gross margin is above 60% at pilot scale.

**Stop criteria:**

- Fewer than 3 paying pilots after 90 days.
- Customers use the product once and do not return.
- The workflow requires a licensed professional to operate.
- A single foreign API dependency cannot be replaced.
- Support cost per customer exceeds 30% of revenue.

---

## 12. 12-month roadmap

| Quarter | Focus | Key milestones |
|---|---|---|
| Q1 | Validation | 2 products, 20 interviews, 5 paid pilots, 1 channel partner |
| Q2 | Product-market fit | 30-50 paying customers, 70%+ gross margin, first case study |
| Q3 | Distribution | 100-150 customers, 2-3 channel partners, annual prepay > 30% |
| Q4 | Scale and export | 250-400 customers, USD 15k-30k MRR, first diaspora or export revenue |

**Lean team for the first year:**

- 1 founder/CEO owning sales and product.
- 1 senior full-stack engineer.
- 1 ML/LLM engineer (can be part-time at first).
- 1 implementation/support specialist with domain knowledge.
- Contractors for design, legal, and regulatory research.

**Indicative first-year budget:** USD 25,000-60,000 depending on salaries, compute, and whether the team is full-time. The largest controllable cost is inference; the largest uncontrollable cost is currency depreciation.

---

## 13. Risks and kill criteria

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Connectivity disruption | Medium | High | Local hosting, offline mode, SMS fallback |
| Currency and inflation | High | Medium | Quarterly repricing, annual prepay, USD-linked export tier |
| Sanctions and API cut-off | Medium | High | Local/open models, multi-provider, manual fallback |
| Regulatory change | Medium | Medium | Regulatory advisor, modular rules engine, pilot with licensed partner |
| AI accuracy failure | Medium | High | Human review, evaluation sets, disclaimers, insurance |
| Low willingness to pay | High | High | Sell ROI, target businesses not consumers, partner-led distribution |
| Global competitor via VPN | Medium | Medium | Local integrations, Persian support, on-premise, price |
| Talent attrition | High | Medium | Equity, remote flexibility, export revenue for senior pay |
| Payment fraud and chargebacks | Medium | Medium | KYC, prepaid wallet, manual review for high-risk accounts |
| Platform dependency | High | Medium | Multi-platform integrations, direct channels, own data |

**Kill criteria for any product line:**

- Fewer than 10 paying customers after 6 months.
- CAC payback above 12 months.
- Gross margin below 50% at USD 10k MRR.
- Monthly churn above 8% for SMB or 2% for enterprise.
- The product cannot be used without a licensed professional in the loop.
- A single foreign vendor can shut down the core workflow.

---

## 14. Sources and data notes

**Macro and technology indicators**

- World Bank Open Data, Iran (IRN), indicator `SP.POP.TOTL` (population), `IT.NET.USER.ZS` (internet users), `IT.CEL.SETS.P2` (mobile subscriptions), `SP.URB.TOTL.IN.ZS` (urban population), `NY.GDP.PCAP.CD` (GDP per capita), `FP.CPI.TOTL.ZG` (inflation), `SE.TER.ENRR` (tertiary enrollment), `IT.NET.SECR.P6` (secure servers): https://api.worldbank.org/v2/country/IRN/indicator/
- World Bank data last updated 8 October 2026; latest values are 2024-2025 depending on the indicator.

**Ecosystem and innovation**

- Tehran Times, "Tehran moves up in Global Startup Ecosystem Index", 6 June 2026: https://www.tehrantimes.com/news/527056/Tehran-moves-up-in-Global-Startup-Ecosystem-Index
- Tehran Times, "GII 2026 places Tehran 65th among top 100 science and technology clusters", 9 September 2026: https://www.tehrantimes.com/news/529855/GII-2026-places-Tehran-65th-among-top-100-science-and-technology
- Tehran Times, "Iran joins countries with advanced quantum training laboratories", 21 October 2026: https://www.tehrantimes.com/news/531337/Iran-joins-countries-with-advanced-quantum-training-laboratories
- WIPO Global Innovation Index 2026 cluster data, as reported by Tehran Times.

**Local platforms and infrastructure**

- Zarinpal payment gateway: https://zarinpal.com/
- Kavenegar SMS, OTP, and voice API: https://kavenegar.com/
- Cafe Bazaar, Iran's largest Persian-language Android store: https://cafebazaar.ir/
- Divar, Iran's largest classifieds marketplace: https://divar.ir/

**Data caveats**

- There is no reliable public estimate of Iran's AI SaaS market size. Figures in this report are directional and should be replaced with bottom-up customer counts during phase 2.
- StartupBlink tracks a narrow set of startups (118 for Iran in 2026), while Iranian sources claim 6,000+ startups. Both can be true; they measure different populations.
- Buyer counts such as "1M+ Instagram sellers" or "100k+ agents" are order-of-magnitude estimates, not census data.
- The 2026 operating environment includes heightened geopolitical risk and periodic connectivity disruption. Business continuity planning is not optional.

---

## Appendix A: Scoring rubric

| Score | Demand | Willingness to pay | Feasibility | Defensibility | Capital efficiency |
|---:|---|---|---|---|---|
| 5 | Daily, painful, budgeted problem | Buyer already pays for a solution | Small team can ship in 1-3 months | Strong local data or integration moat | Under USD 25k to first revenue |
| 4 | Weekly, important problem | Clear ROI and budget | 3-6 months with a small team | Moderate integration or data advantage | USD 25-75k |
| 3 | Monthly, nice-to-have | Some budget, but discretionary | 6-9 months | Some differentiation | USD 75-200k |
| 2 | Occasional | Low willingness to pay | 9-12 months | Weak differentiation | USD 200-500k |
| 1 | Rare or hypothetical | No budget | 12+ months or specialized team | Commodity | Above USD 500k |

**Opportunity score = (0.25 × demand + 0.20 × willingness to pay + 0.20 × feasibility + 0.20 × defensibility + 0.15 × capital efficiency) ÷ 5 × 100.**

---

## Appendix B: Dataset schema

The file `data/iran-ai-saas-services.csv` contains one row per service with the following columns:

| Column | Description |
|---|---|
| `id` | Stable service ID (1-120) |
| `category` | One of 12 categories |
| `name` | Service name |
| `what` | One-line description |
| `buyer` | Primary buyer |
| `ai` | Core AI capability |
| `wedge` | Iran-specific advantage |
| `model` | Revenue model |
| `price` | Indicative price band in USD |
| `market` | Buyer-count proxy (estimate) |
| `competition` | Low, Medium, High |
| `difficulty` | Low, Medium, High, Very high |
| `capital` | Relative capital need ($ to $$$$) |
| `ttr` | Time to first revenue |
| `demand` | 1-5 score |
| `wtp` | 1-5 score |
| `feasibility` | 1-5 score |
| `defensibility` | 1-5 score |
| `capital_efficiency` | 1-5 score |
| `score` | Weighted opportunity score (0-100) |

**Next step:** choose two services, run 20 interviews, and replace every estimate in this report with a measured number from a paid pilot.
