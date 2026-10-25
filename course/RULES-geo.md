# Rules for restyling the Moodle course "Application of geoinformatics to natural hazards mapping and monitoring" (AGeoHazard, test course id=15)

Working copy: `C:\Users\marek.urbaniak\Documents\geo-natural-hazard\course\mcontent\` (one file per Moodle text field).
Untouched originals for reference: `...\course\mcontent-orig\`. File naming: `s<section>-<modtype>-<cmid>[-p<lessonpageid>].html`,
`*.intro.html` = activity description, `s<N>-summary.html` = section summary. `names.tsv` lists activity names, lesson page titles and
lesson buttons (jumps) — DO NOT edit it. Edit only the files of YOUR section(s). Do not touch any other directory.

## Goal (what the lecturer asked for)
Rebuild the course pages in the visual style of the IoT course (clean cards, numbered steps, callouts), **blue palette**, with a
clear roadmap: the student must be able to follow the next instruction intuitively, and milestones (topics and key moments)
must stand out. Course content language: **English**. Keep the facts; improve structure, wording and currency.

## Context you must respect
- Lecture decks (reveal.js) already exist as resources "Lecture N – …" (cm 405–412). Each lecture ends with slides
  "In the lab" and "Before next class"; the lab pages you restyle must match those steps. Lecture sources (markdown) are in
  `C:\Users\marek.urbaniak\Documents\geo-natural-hazard\presentation\obsidian\cycle\L0N_*.md` — read the one for your section
  (slides "In the lab …" and "Before next class") and make the lesson pages the step-by-step counterpart of those slides.
- **No calendar dates in any text** (pages, summaries, assignment descriptions, module names, slides): the course is restored
  every year for a new group with a new timetable. Write "at the start of lab N", "before the first lab", "a few days before the lab"
  – never "30.11", "Monday", "winter 2026/27". The real dates live only in `course/schedule.json` (applied to the assignment
  due dates and the course start date by `course/assignments.php`) and Moodle shows them itself (activity dates, calendar).
  Late submissions stay open (no cut-off date); they are only marked late.
- Schedule of the 2026/27 run (reference only – do not copy these dates into content): lecture of week N introduces the lab of week N+1.
  L1 9.11 → Lab 1 16.11 (Copernicus Browser, CDSE account, GEE registration, first script);
  L2 16.11 → Lab 2 23.11 (GEE JS: collections, filters, NDVI, classes, areas; homework "index areas");
  L3 23.11 → Lab 3 30.11 (RF + k-means, accuracy, report);
  L4 30.11 → Lab 4 7.12 (MNDWI + Sentinel-1 flood, UN-SPIDER script);
  L5 7.12 → Lab 5 14.12 (landslide density heatmap, Handwerger 2022);
  L6 14.12 → Lab 6 21.12 (NBR/dNBR burn severity);
  L7 21.12 → Lab 7 11.01 (4 h: Colab + geemap, QA bitmasks, rgee, capstone notebook); L8 11.01 wrap-up.
- Milestones (one per module, highlighted): M1 accounts ready + first script (16.11); M2 "index areas" script link (23.11);
  M3 classification report (30.11); M4 flood extent map + sensitivity table (7.12); M5 landslide heatmap note (14.12);
  M6 burn severity map + report (21.12); M7 capstone notebook (11.01).
- Facts verified on 21.10.2026: EO Browser was retired in March 2026 → replace every mention/instruction with **Copernicus Browser**
  (https://browser.dataspace.copernicus.eu/, free CDSE account). GEE requires a registered Google Cloud project
  (https://developers.google.com/earth-engine/guides/access, noncommercial use). Sentinel-2 = 2A/2B/2C; Landsat 7 retired 2025.
  Sentinel-2 collection to use: `COPERNICUS/S2_SR_HARMONIZED`. Dead links to fix: `r-earthengine.com` → https://r-spatial.github.io/rgee/ ;
  `developers.google.com/earth-engine/guides/earth-engine/guides/...` (doubled path) → single path.
- Keep every `@@PLUGINFILE@@/...` image reference (they are files attached to that field). Keep existing external links unless dead.
- Keep lesson navigation semantics: lesson buttons/jumps live in `names.tsv` and are NOT edited by you; the page content may refer
  to "Next" as the button below.

## Form (HTML conventions — identical to the IoT course; the CSS is added automatically later by `inline-iot-css.py`)
Wrap every field in `<div class="iot-material iot-material--page" data-iot-material="v1"> … </div>` (labels: `iot-material--label`).
Inside, use ONLY these building blocks (no inline `style=`, no coloured `<span>` pills, no `<br>` spacing, no `font-size`):
- `<p class="iot-material-lead">…</p>` — one framed lead paragraph at the top: what this page is for and what the student will have at the end.
- `<h3 class="iot-material-divider">Section heading</h3>`, `<h4 class="iot-material-divider iot-material-divider--sub">Sub heading</h4>`.
- `<ol class="iot-material-steps"><li><strong>Step title.</strong> text …</li>…</ol>` — numbered procedure; each step one action.
- `<ul class="iot-material-list">` / `<ol class="iot-material-list">` — plain lists.
- Callouts: `<div class="iot-material-callout"><p class="iot-material-callout-title">Title</p><p>…</p></div>`; variants
  `iot-material-callout--task` (what to submit / deliverable = milestone), `--check` (self-check, "you are done when…"),
  `--warn` (common mistake), `--danger` (data loss / account problems).
- `<table class="iot-material-table">` with `<thead>` for comparisons; `<pre><code class="language-javascript">` (or `language-python`,
  `language-r`) for code, with `&lt; &gt; &amp;` escaped; inline `<code>`.
- Formulas: plain text in `<code>` or a `<p>` (e.g. `NDWI = (Green − NIR) / (Green + NIR)`), no MathJax needed.
- Links: `<a href="…" target="_blank" rel="noopener">`. Images: keep the original `<img src="@@PLUGINFILE@@/…">`, inside
  `<figure class="iot-material-figure"><img …><figcaption>…</figcaption></figure>`; drop `width/height` attributes larger than 900.
- Page structure for an exercise page: lead → "Before you start" (accounts, links) → numbered steps → deliverable callout (`--task`)
  → self-check callout (`--check`) → "Common problems" (`--warn`). Quiz pages (titles "…quiz…", "NDVI", "image collections S2 levels"):
  keep the question text only, wrapped in the container, one short `<p>`.
- Remove junk markup from the old editor (`<span jsslot…>`, `data-once`, empty `<p></p>`, `<br>` runs, `&nbsp;` chains,
  `font-size: 0.9375rem` spans). Fix English (e.g. "Regarding to" → "Regarding", "repped" → "repeated", "advices" → "advice").
- Do not create new Moodle activities. Do not rename activities (report proposals instead). Keep each file a valid HTML fragment
  (balanced tags). UTF-8, LF.

## Final report (English, ≤ 300 words)
Files changed (one line each), rename proposals (`cm <id>: "old" → "new"`, `lessonpage <id>: …`), anything you removed and why,
links you replaced, and open questions for the lecturer.
