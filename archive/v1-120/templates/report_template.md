# AI-Enabled SaaS Opportunities in Iran

> Persian edition: [فرصت‌های SaaS هوش مصنوعی در ایران](iran-ai-saas-report-fa.md)  
> The Persian edition and dashboard use Toman at IRR 270,000 per USD; this English edition keeps the original USD price bands.

## Phase 1 market report and {{TOTAL}}-service opportunity catalogue

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

## 6. How the {{TOTAL}} services were scored

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

{{CATEGORY_SUMMARY}}

### The top 25

{{TOP25}}

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

## 8. Full catalogue of {{TOTAL}} services

The catalogue is grouped into **{{CATEGORY_COUNT}} categories** of ten services each. Scores are on a 0-100 scale using the method in section 6. The same data is available in `data/iran-ai-saas-services.csv` for sorting and filtering.

{{CATALOGUE}}

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
| `id` | Stable service ID (1-{{TOTAL}}) |
| `category` | One of {{CATEGORY_COUNT}} categories |
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
