# Star Electric Services, Inc — demo website

**Prospect:** Star Electric Services, Inc · Electrician (Clearwater, FL — Tampa Bay overflow) · (727) 492-6248 · jerry@starelectricservices.com
**Status:** LOCAL DRAFT — not deployed, not pitched. Awaiting Emmanuel's preview approval.

## Concept: "THE BLUEPRINT"
The site reads like an electrical permit drawing set. Warm-paper ground with a
faint blueprint grid, ink-blue linework, dashed conduit-run dividers, sheet
numbers (E-101…E-401), and a drawing title block (PROJECT: YOUR HOME / DRAWN:
10 OCT 2026) anchoring the hero. Photos are annotated like a tech marked them
up on site: white dashed dimension lines, marker circles, mono callouts.

- **Art-direction triple:** drafted / exact / steady.
- **Deliberately broken convention:** no centered hero. The hero is a drawing
  sheet — title-block margin, spec metadata, pain headline set as the drawing
  title, dominant photo right with blueprint dimension callouts.
- **Signature interactive element:** LOAD CHECK — a home load calculator.
  Tap the appliances your home runs + your panel size; a meter bar fills
  against the 80% sizing line and the verdict tells you whether your panel
  is the bottleneck ("OVER THE LINE … A 200A service change ends it.").
  The CTA pre-selects "Panel upgrade" in the 4-step estimate stepper.
- **Motif (count: one):** the junction-box node (square + center dot) —
  eyebrow markers, list bullets, dashed-conduit section dividers, FAQ marks,
  footer divider. Nothing else competes.
- **Accent:** copper, ONLY on primary CTAs (never as decoration).
- **Type:** Bebas Neue (voiced display) + JetBrains Mono (utility + body) —
  two families, self-hosted woff2, zero CDN.

## Distinct from the sibling electrician demos
- maynard-electric ("FIND THE FAULT"): forensic case-file, manila/ink/amber,
  Oswald, case-file board, no stepper.
- mjm-electric ("The Schedule Board"): circuit-trace motif, annotated panel
  HUD chips, cost-estimator slider, 4-step stepper, dark stat band.
- cjs-electric ("The Panel Schedule"): interactive flip-breaker panel.
- all-in-one-electric: dark industrial/amber. gaylord-miller: navy/brass
  heritage timeline.
- This demo: light "whiteprint" blueprint register (paper + ink blue, not
  dark), drawing-sheet hero, load calculator instead of cost estimator,
  own ritual ("Load-calculated, code-drawn, labeled to the last breaker."),
  own enemy line (unlicensed handyman + the inspector red-tag).

## Page order (objection stack, decision-ladder titles)
Two-front-doors strip → title-block header (live Tampa-time clock + OPEN NOW
chip) → hero sheet E-101 (pain H1, offer line, two doors, trust line) →
ticker → named-enemy strip → 1 · symptoms ("5 signs…", annotated old-panel
photo) → 2 · LOAD CHECK (signature) → 3 · services bento (5 cells, from-prices
+ durations, emergency as the large cell) → panel sales letter (100A
bottleneck, before/after pair, $1,800–$2,400 + $95/mo financing) → ritual +
dark stat band (4 outlined cards, grain) → 4 · estimate (meet-your-tech card
+ 4-step stepper with progress bar → mailto handoff; Current Club tiers) →
two-tier service areas (Same-day Clearwater/Dunedin/Safety Harbor · Next-day
Largo/Palm Harbor/Tampa) → FAQ (6, honest ranges + inaction anchor, FAQPage
schema) → final CTA → footer. Sticky mobile bar: CALL (727) 492-6248 + GET MY
PRICE, slides up after hero, hides at final CTA. Kill list honored: no
autoplay, no popups, no chat widget, no modal before dial (every number is a
bare tel: link).

## Placeholder-data caveats
- starelectricservices.com is unreachable (empty reply on http/https, www and
  apex — verified 2026-10-10). Real facts used: business name, phone, email,
  Clearwater FL. Everything else is illustrative.
- ★ 4.7, "600+ jobs", "~1 hr response", review-style lines, and "Jerry,
  Owner" (inferred from jerry@) are demo placeholders — the stat band carries
  an explicit "*Illustrative demo figures" note. No fake license number used
  ("Licensed & insured in Florida" only). No street address invented.

## Trade research baked in
100A→200A service changes; NEC 80% continuous-load sizing (the load-check
white line); AFCI/GFCI; Federal Pacific Stab-Lok / Zinsco vs Florida
insurers; dedicated 40–60A 240V Level 2 EV circuits; whole-house surge
protection (Florida lightning); aluminum/cloth rewiring; permits with City
of Clearwater / Pinellas County; 4–8 hr outage, power back same evening;
torque-checked terminals; labeled-to-the-last-breaker panels.

## Photo trade-literacy audit
- hero-panel-working.webp: PASS (US Siemens-style plug-on breakers, toggles
  ON, correct wire colours, insulated screwdriver on a terminal).
- panel-200a-detail.webp: PASS. ev-charger-install.webp: PASS (conduit,
  level, drill, tool belt all correct). old-panel-warning.webp: PASS
  (rust, cobwebs, scorch — the "warning signs" visual). tech-portrait.webp:
  PASS (background panel softly blurred).
- REGENERATED once: first hero attempt rendered European DIN-rail breakers
  (wrong for US residential) — rebuilt via edit on the verified US panel
  photo instead. Deleted the failed file.

## QA results (qa.py, EXIT 0 — desktop 1440 + mobile 390)
- Contrast tokens ≥4.5:1 (white on copper 4.6, copper-dk on paper 5.1,
  ink on paper 15+). Accessibility six-check: lang, alt text, no empty
  links/buttons, all inputs labeled, keyboard-operable chips/FAQ/stepper.
- No horizontal overflow either width; all 6 images load; all anchors
  resolve; Bebas Neue + JetBrains Mono confirmed via document.fonts.
- Load check verdict toggles; stepper validates each step and completes to a
  working mailto; FAQ accordions; burger opens/closes; sticky bar appears
  after hero, hides at final CTA, call link is bare tel:.
- No-interaction test: hero readable 3s after load, untouched. Zero
  console/page errors. Key facts present in server HTML with JS off.
- og-image.jpg 1200×630 cropped from hero; favicon.svg (copper bolt on
  blueprint ground); full OG/Twitter meta with absolute URLs.

### Failures found and fixed
1. **First hero photo was European DIN-rail hardware** — regenerated (see
   audit above).
2. **clip-path wipe on the figure itself broke IO forever** (the 2026-10-05
   lesson): figures stayed invisible AND their lazy images never loaded.
   Fixed by observing the unclipped parent; wipe still plays, images load.
3. **Lazy images never loaded during QA scroll** — html{scroll-behavior:smooth}
   made the test's window.scrollTo animate; scroll-through now uses
   behavior:'instant'.
4. **`[hidden]` lost to `.btn{display:inline-flex}`** — Back button and the
   pre-selection load-check CTA were visibly rendered. Added
   `[hidden]{display:none!important}`.
5. **Mobile header overflow (scrollWidth 415)** — burger pushed 25px out;
   hcontact hidden on ≤640px (sticky bar carries the phone, per playbook).
6. **Tap targets <44px** — brand link 43px, header phone 42px → min-height
   48px + flex:none on brand/burger.
7. **Bento orphan** — 6 cells in 3 cols left surge alone on row 3; removed
   the surge cell (still in ticker + Care Club) → perfect 2-row grid.
8. **Sticky figures duplicated in stitched screenshots** — .sym-fig/.techcard
   now position:static during capture.

## Substitute QA (claude.ai critique parked — parent runs it)
Screenshots staged at
`~/workspace/goals/tampa-demo-first-cold-pitch/hidden_files/critique-2026-10-10/star-electric-{desktop,mobile}.png`.

**Five-question friend test**
1. "What am I buying?" — PASS: offer line names panel upgrades, EV
   chargers, troubleshooting + from-price in the first viewport.
2. "Where is the price?" — PASS: $1,800 hero anchor, from-prices on every
   bento cell, $1,800–$2,400 range in letter + FAQ.
3. "Too long?" — BORDERLINE: 9 sections is long, but this is a considered
   high-ticket purchase (objection stack, not an emergency page); every
   section answers one objection. Kept; the Current Club strip is the
   leanest it can be.
4. "Why trust this?" — PASS: license line, 4.7, permit promise, tech card,
   before/after pair, named enemy (placeholders flagged above).
5. "Almost closed the tab here?" — sales-letter section is the heaviest
   read; mitigated with the before/after pair beside it and the price box.
   No cut made — watching for the critique pass.

**Blur test (hero):** first fixation = the Bebas headline mass, second = the
copper CTA. The blueprint grid stays quiet. PASS — nothing subtracted.

**Read-aloud test:** all 10 headlines read aloud; all pass, no brochure
phrasing. Ritual line ("Load-calculated, code-drawn, labeled to the last
breaker.") is staccato by design.

**Redesign subtraction audit** (phone / form / services path / trust line):
all present. One deliberate subtraction: the surge bento cell (orphan-grid
fix) — surge still reachable via ticker + Care Club. Asks before first
click: the doors strip + hero doors repeat the SAME two choices (playbook-
sanctioned two-front-doors pattern), not four different asks. First CTA at
~0vh scroll depth.

## Files
- `index.html` — content, OG/Twitter meta (canonical
  https://star-electric-services-demo-iodine-53s-projects.vercel.app/),
  Electrician + FAQPage JSON-LD
- `styles.css`, `app.js`, `qa.py`
- `fonts/` — bebasneue-400.woff2, jetbrainsmono-400.woff2 (variable 100–800)
- `images/` — 5 original AI photos, trade-literacy audited
- `favicon.svg`, `og-image.jpg`

## Still owed
- Design-critique step: claude.ai live-browser critique could not be run
  from this subagent (no live-browser access). Screenshots are staged at the
  paths above; the parent agent should run the critique and fold fixes in.
