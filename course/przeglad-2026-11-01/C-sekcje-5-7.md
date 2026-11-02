# Reviewer C (Claude Opus, high) – sections 5–7, lectures L05–L08, question bank L5–L7, examples/

No edits. Content compared against the live GEO2 scripts (`05_landslides`, `06_wildfires`) and Handwerger et al. (2022), NHESS.
Lesson page order, jump buttons and quiz slots read from the test Moodle database (read-only PHP). pyflakes run on `examples/`
(installed into the base miniconda environment: `pip uninstall pyflakes` to remove).

## Blockers

1. **`examples/notebooks/07_capstone_template.ipynb` (official M7 starting point) does not run.** Undefined names left by the renaming
   sweep: flood cell `difference = sar_after_smooth.subtract(sar_before_smooth)` but variables are `before_f`/`after_f`;
   `print(... % floodAreaHa)` but variable is `area_ha`; flood map cell `sar_before_smooth`/`sar_after_smooth`; fire map cell
   `m.addLayer(pre, …)`/`post` but variables are `median_pre`/`median_post`. Criterion "a colleague runs all cells top to bottom" fails on
   the template itself. Fix: rename consistently, run end to end in Colab. `python/04_dnbr_burn_severity.py` has the same `pre`/`post` slip
   in its commented-out map block.
2. **`L08_Wrapup.md` slide "Assessment" vs gradebook and `s0-summary`.** Lists "Lab deliverables M1–M6" (M1 not graded), "Lesson quizzes
   (GEE, API)" as assessed (weight 0, s0 says they "do not count"), omits the final test (40 %), refers to "**Course regulations and
   syllabus** – the resource at the top of the Moodle course" (does not exist), gives no M7 deadline although s7-summary, p126 and
   assignment 434 say "confirmed in lecture 8"; "Today" slide promises "Assessment and deadlines". Fix: replace with the gradebook model
   (M2–M7 10 % each + final test 40 % = part B; A 40 % / B 60 %, each passed at 60 %; letters 5.0/4.5/4.0/3.5/3.0 from 92/84/76/68/60 %;
   test format 30 random of 83, 40 min, 2 attempts, best counts, when it opens; M7 deadline). Drop lesson quizzes from the slide.

## Major

3. **p118 steps 2 and 4, s5-assign-432 ("one Sentinel-1 orbit"), L05 "In the lab" vs GEO2 `03_full_workflow_hokkaido_2018`.** Lesson says
   "orbit (ascending or descending – do not mix)"; the script builds both and uses `iRatioUsed = iRatioAvg` (mean of asc/desc I_ratio),
   which matches the paper ("combined ascending and descending performed best, AUC 0.83"). Fix: "use both directions averaged, as in the
   paper; switch `iRatioUsed` to one direction only if the other has no post-event scene"; ask for scene counts per direction in M5.
   Quiz L5-05 ("same orbit") can stay (each stack is single-direction).
4. **Same page and M5: "try the 90th and 80th" percentile.** Script computes `percentile([90, 95, 99])` then `pct.get('VH_p' + PERCENTILE)`;
   `PERCENTILE = 80` fails ("Dictionary does not contain key VH_p80"). Fix: add 80 in GEO2 or say "99th, 95th, 90th".
5. **p122 step 1, "Your own area" bullet, listing; L06 "In the lab" step 2.** Instructions name `var geometry = …`, `SET TIME FRAME`,
   `prefire_start` … (original UN-SPIDER script, sample dates 2016/2017); the linked GEO2 `02_dnbr_burn_severity_sentinel2` uses `var aoi`,
   `PRE_START/PRE_END/POST_START/POST_END`, `NIR_BAND`, `EXPORT_CRS`. Fix: replace listing with the PARAMETERS block of the course script;
   "geometry" → "aoi" on page and slide.
6. **Client vs server: L07 slide, p125 box, quiz L7-06 feedback (and L7-05).** Slide says `if s2.size() > 10:` is "always True"; it raises
   `TypeError: '>' not supported between instances of 'ComputedObject' and 'int'` (earthengine-api 1.7.49). Only bare `if s2.size():` is
   always truthy. `print(n)` prints `ee.Number({...JSON...})`, not `<ee.Number object>`. Fix in slide, page and `build_questions.py`, regenerate XML.
7. **p132 ("an effectively unlimited free quota"), examples/README and `05_cdse_openeo_ndvi.py` ("unlimited free compute/quota").** Wrong for
   2026: noncommercial quota tiers since 27 April 2026 (Community 150 EECU-h/month default, Contributor 1000 with billing account;
   developers.google.com/earth-engine/guides/noncommercial_tiers). L08 itself mentions "noncommercial tiers". Fix: "a free noncommercial quota
   (Community tier, 150 EECU-h/month per project – ample for the labs)"; in lab 1 say where the quota is shown.
8. **Capstone landslide route has no support.** Template, README and QGIS scripts cover flood and fire only; no Python heatmap workflow;
   `js_snippet_to_py` on the landslide script breaks (`'VH_p' + PERCENTILE`, `reduceResolution`/`convolve`). Fix: add a 4c landslide section
   or restrict the capstone to labs 4 and 6 and say so.
9. **M5, M6, M7 intros and p126: no rubric.** "Marked out of 100 against the template" but no points per chapter; M7 has three routes with
   different deliverables and no criteria; M5 "2–4 pages" vs template "3–6 pages". Fix: point table in the shared template (e.g. data 15,
   method 20, map quality 20, numbers 15, validation/sensitivity 15, limitations 10, reproducibility 5); fix M5 page count.
10. **Final test (cm 435) and lessons 3–6.** (1) Quiz intro: "the same kind as the self-check quizzes in the lessons", but lessons 3–6 have
    0 question pages and lesson 7 has one item with all answers correct; ~55 of 83 bank questions have no practice counterpart. Fix: 2–3
    self-check pages in lessons 5 and 6 (reuse L5-06, L6-06, L6-10) or an ungraded practice quiz. (2) `timeopen = timeclose = 0`, no
    password, `visible = 0`; students told only "opened by the lecturer at the end"; not stated when, how long, lab or home, open-book;
    L08 silent; s7 summary links to the hidden quiz (error until shown). Fix: open/close window in `schedule.json`/`assignments.php`;
    mode and rules in s7 summary and L08.
11. **Gradebook: `aggregateonlygraded = 1` on both categories.** A non-submitted homework (no grade) is dropped from the weighted mean
    instead of counting 0, so "10 % each" is not what Moodle computes; same for the course total while part A is empty. Fix: "Exclude
    empty grades" off for part B and the course, or enter 0 after each deadline; say which in s0/L08.
12. **Lesson buttons (live `lesson_answers`).** Lessons 5 and 6: pages say "Press Next" but buttons are "GEE example", "Remote Sensing and
    Electromagnetic Energy" etc.; every page has a jump-0 button named after itself; last pages p118 and p122 ("GEE js example") jump to
    themselves – lesson can never be finished. Lesson 7: leftover jump-0 "python" (p123), "Colab" (p125), "Cloud masking" (p127, a QGIS page);
    p128 has five buttons ("RGEE" reload, "Quiz" next, "Python" previous, "Colab" to page 1, "Next"); p123 (first page) has "Previous".
    Fix: only Previous/Next and "End of lesson" (jump −9) on the last page of each lesson.

## Minor

13. **Mean vs median.** Paper and GEO2 use the temporal median, VH only, `I_ratio = 10·log10(I_pre/I_post)`, combined orbits; p118 and
    L5-05/L5-06 are correct. Wrong: L05 "Reading the heatmap script" ("the course copy may use mean"), L08 "One workflow" table
    ("log-ratio of mean backscatter" vs "log-ratio of medians" two rows below); L05 "In the lab" step 3 "log-ratio layers (VV, VH)" but the
    script has VH only. Fix: "median" everywhere; "VH (ascending, descending, averaged)".
14. **Stale lesson names in cross-references**: p118 and L05 "Before next class" ("lesson *Fire detection and severity estimation*");
    p122 and L06 ("lesson *Application Programming Interfaces (API) for GEE*"); assign 433/434 link texts; L05 "Moodle *Landslides* lesson,
    page 2" and "section *Landslides mapping approaches*"; L06 "*Fire detection…* lesson, page 4"; hidden grade items carry old names.
15. **L06 "Before next class" vs p122 and s6 summary**: lesson and summary ask to install QGIS ≥ 3.44 + Earth Engine plugin and sign in; slide
    mentions only R/rgee; lab 7 depends on the plugin. Add the QGIS line.
16. **L07 "In the lab (4 h)" vs lesson pages**: Colab 45 min vs p125 60; QGIS 1–2 45 vs 35; QGIS 3 45 vs 25; step 4 "QGIS (60 min)" (page says
    30) and repeats "NDVI in the Python Console" from step 2. Fix: align; step 4 "QGIS 4 (30 min): the finished map" leaves ~75 min for the capstone.
17. **Dated statements that will age**: p119 and L06 "Suomi-NPP delivery to FIRMS ends 2 Nov 2026" (NASA Earthdata: 1 Nov; past by lab 6),
    "Terra science operations end Feb 2027"; L06 lists `NASA/VIIRS/002/VNP14A1` (Suomi-NPP based, will stop); p128 "Contains modified
    Copernicus Sentinel data **[2024]**" while examples use 2025; L07 "0.3.3, Aug 2026", "CRAN 1.1.8 (2025)" correct today (plugins.qgis.org:
    0.3.3, min QGIS 3.44; CRAN rgee 1.1.8, 2025-10-15) but carry dates. Fix: "Suomi-NPP ended in late 2026 – use NOAA-20/21 (VJ1/VJ2) in FIRMS",
    "data [year]", drop version dates or keep them in RULES-geo.md.
18. **p127 "QGIS 4" ambiguous** (QGIS version vs lesson page 4): "QGIS 4 works too … use the export path of QGIS 4 today". On QGIS < 3.44 the
    Plugin Manager installs 0.1.7 (min 3.22) rather than "refusing". Fix: "QGIS step 1–4" or "QGIS page 4"; "older QGIS gets plugin 0.1.x with
    fewer tools – use Door A".
19. **Project id vs name**: p123 and README say "copy the **id**, not the project name"; p127, p128 traps and README QGIS section say "name".
    Use "project ID" everywhere.
20. **Code listings**: p123 cell 3 (R) `ggplot(...)` without `library(ggplot2)`; p125 cell 1 ends with a truncated comment "# The automatic
    conversion of code is done by calling the"; p125 JS example computes `composite` but displays `withNdvi.select('ndvi')` (mosaic, not
    median); p128 rgee listing headed "Export, cell 2" → "rgee, cell 1"; L07 slide `img = ee.Algorithms.If(...)` should be wrapped in `ee.Image(...)`.
21. **L05 slide "Terrain" code**: `ee.ImageCollection('COPERNICUS/DEM/GLO30_2024_1')…mosaic()` then `ee.Terrain.products` – a mosaic has no
    native projection, slope depends on zoom; catalog example uses `.mosaic().setDefaultProjection(nativeProj)`. ID valid (GLO30 deprecated →
    GLO30_2024_1). Laplacian is a total-curvature proxy, not "profile curvature proxy".
22. **p119 table "VIIRS 375 m … NASA FIRMS; GEE FIRMS"**: GEE `FIRMS` is MODIS-based 1 km daily; 375 m VIIRS detections only on the FIRMS website.
23. **M7 wording inconsistent**: p126 "notebook link as online text **and** file(s) as upload" vs assignment 434 ".ipynb upload **or** link";
    template requires "comparison with a reference" and "one parameter varied", p126 and s7 summary omit both; s7 summary lists "the API
    quiz" as part of M7 (weight 0); README capstone offers only "Python or R" (no QGIS) and points to "the lesson page *rgee*" (gone).
    Fix: one canonical deliverable list copied to all four places.
24. **`examples/qgis/02_qgis_flood_mask.py` vs `python/03` and the lab 4 script**: different AOI (`[17.20, 50.40, 17.80, 50.90]` vs
    `[17.05, 50.38, 17.75, 50.62]`), `median()` + `focal_median` vs `mosaic()` + `focal_mean`, after-window 09-28 vs 09-25, yet header says
    "same method as GEO2/04_floods/03" and p129 asks to compare hectares. Sensitivity loop in `python/03` omits the connected-pixel filter.
25. **L05 InSAR slide**: limit "> ~ half a wavelength between passes"; usual phase-gradient limit ≈ λ/4 (~1.4 cm C-band) between neighbouring pixels per revisit.
26. **Housekeeping**: `names.tsv` stale (lecture names with dates); L05–L08 frontmatter summaries contain Polish text and dates; L08 cites the
    two quality-assessment PDFs "in Moodle (section *Flood mapping*)" – update if cm 399/400 are removed.

**Checked and correct**: NBR = (B8 − B12)/(B8 + B12) and B8 vs B8A note; Landsat C2 SR_B5/SR_B7 scale/offset; dNBR breaks
−250/−100/100/270/440/660 and labels; RdNBR; 20 m export; `MODIS/061/MCD64A1`; openEO listing; QGIS plugin 0.3.3 / QGIS ≥ 3.44 (last 3.x LTR);
rgee `ee_Initialize(project=)`; quiz 4/4/4/5/4/4/5 slots = 30, 40 min, 2 attempts, highest grade; letters and weights match s0;
question bank L5–L7 correct apart from items 6 and 13.

## Summary
1. Fix runnable artefacts: capstone notebook variables; lab 6 page naming the UN-SPIDER variables instead of the course script's; lab 5
   "80th percentile" step that crashes the GEO2 script.
2. Landslide method consistent with paper and script: both orbits averaged, median, VH only (p118, M5, L05, L08).
3. Rewrite L08 "Assessment" to match gradebook and s0 incl. the M7 deadline; publish the final test window and mode; "exclude empty grades" off.
4. Per-chapter rubric for M5–M7; self-check questions in lessons 5–6.
5. Clean lesson navigation (Previous/Next/End only); correct the "always True" client/server teaching and the "unlimited free quota" claim.

Sources: Handwerger et al. 2022 NHESS (nhess.copernicus.org/articles/22/753/2022/); plugins.qgis.org/plugins/ee_plugin/; CRAN rgee;
developers.google.com/earth-engine/guides/noncommercial_tiers; Copernicus DEM GLO30 catalog page; QGIS 3.44 LTR plans (blog.qgis.org 2025-10-07);
NASA Earthdata Suomi-NPP notice.
