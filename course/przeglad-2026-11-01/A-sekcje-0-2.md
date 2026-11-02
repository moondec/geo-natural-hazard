# Reviewer A (Claude Opus, high) – sections 0–2, lectures L01–L02, Lesson 2 quizzes, question bank L1/L2

No files were edited. Claims about settings were checked against the live dumps (`gradebook.txt`, `course_struct.txt`).
`names.tsv` in the repo is stale (23.10, still has dates in names); the live course has no dates and has `ops.tsv` applied
(answer 332 = "Earth Engine Explorer", answer 342 = "Earth Engine Developer Guide").

## Blocker

1. **cm 392 Homework M2 – the report cannot be uploaded.** Live settings: `types={"onlinetext":"1","file":"0"}`, yet
   `s2-assign-392.intro.html` says "Upload the report as .pdf or .docx". Fix: enable file submissions (pdf, docx; 1 file);
   script link goes into the online text field, not "the submission comment".

## Major

2. **The M2 deliverable has three different sizes.** p101/p104 and L02 "In the lab" step 5: "a short note with the area table";
   assignment intro: "a short report … 2–3 pages"; report template in the same intro: "3–6 pages". Fix: one length, same wording in all places.
3. **Students are told to paste the script link somewhere that has no input field.** p101 deliverable callout and L02 "In the lab" step 4:
   "paste the link … in the quiz pages that follow"; p102/p103 are multiple-choice. Fix: remove the instruction (or add an essay/short-answer page).
4. **Lab 1 has no step-by-step page.** L01 slide "In the lab next week" has 5 steps (Copernicus Browser Highlights, compare, custom script,
   GeoTIFF export, timelapse, first GEE script, End-to-End repository). `s1-summary.html` items "Lab 1 – Copernicus Browser" and
   "Lab 1 – first GEE script" have no link; section 1 has only the homework page. GEO2 `02_code_editor/01_first_sentinel2_image` is
   linked nowhere. Lesson 2 steps 1–2 (p93, p99) repeat the sign-up check and the repository, which L01 places in Lab 1.
   Fix: add a short Lab 1 page mirroring the 5 slide steps, link script 01; mark p93/p99 "check / skip if done in Lab 1".
5. **"Clouds first" is contradicted by the code students actually copy.** p131 says every later script starts from a masked collection,
   but the L02 slide "map(): add a band to every image" runs `s2.map(addNDVI)` on the unmasked `s2`, and the homework template
   GEO2 `03_ndvi_classes_and_area` has no mask (`s2.map(addIndex)…median()`), while the report template asks for "the cloud mask you applied".
   Fix: add `linkCollection` + `maskCS` to GEO2 03 and the L02 map() slide. GEO2 headers: 03 says "steps 5.2–5.4" (now step 6);
   05 says "pixel masking returns in Lecture 7".
6. **EVI and SAVI are suggested, but nothing shows how to compute them.** Assignment and p104 say "e.g. EVI, NDWI, SAVI, NDMI – not NDVI";
   EVI/SAVI need reflectance 0–1 (constants +1, L = 0.5, 6·RED, 7.5·BLUE); the lesson teaches only `normalizedDifference`; the
   "/10 000" warning is only on an L02 slide. Fix: short `image.expression()` example with `.divide(10000)` on p101 or in the assignment.
7. **Lecture code and lesson code differ** although the slide says "Build the script from this lecture line by line":
   collection variable `s2` (filtered) vs `s2` + `s2Filtered`; CLOUDY_PIXEL_PERCENTAGE 30 vs 35 (and 30 in the p131 table);
   default AOI `poi.buffer(5000)` at 16.93/52.41 vs polygon or `poi.buffer(100)` at 16.92/52.44; group name `'class'` vs `'code'`.
   p100's 100 m buffer (~3 ha) is useless for classes; p101 then says "use poi.buffer(5000)". Fix: one variable set and one default AOI
   (5 km buffer) in slides, lesson and GEO2.
8. **"Marked out of 100" without a rubric.** `s0-summary`: "Every report is marked out of 100 against the report template"; the template
   has chapters but no points; for M2 it asks for "Validation … comparison with a reference", which M2 does not have.
   Fix: points table per chapter, adjusted per homework; an example report would help.
9. **Lesson 2 quiz pages are of low validity.** p97 ("explore high-resolution satellite imagery"): Earth Engine and Timelapse can also be
   argued correct; feedback contradicts itself (answer 331: GEE "primarily … low and medium resolution", answer 339: "equally capable of
   processing high-resolution imagery"). Answer 332 now "Earth Engine Explorer" with feedback "is a lightweight web app" – verify whether
   Explorer is still online. p98: four true components marked red "Not correct", only "All of them" scores (trick question).
   p103: all 3 options correct, no distractor. p102: "integrated with Google's AI Platform" is true but marked wrong; "Data is downloaded" is
   misleading wording for "already ingested in the cloud". Fix: replace p97, p98, p103 with questions on lesson content (exclusive
   `filterDate` end, scene filter vs pixel mask, `cs_cdf` direction, `scale`). "Javascript" → "JavaScript" (answer 335).
10. **The `scale` explanation is wrong.** L02 "From classes to hectares": "`scale: 1` forces a billion samples and … *Too many pixels* or a
    wrong, over-smoothed answer"; p101: "a hundred times more samples … or gives an over-smoothed answer". A finer scale oversamples
    (nearest neighbour), it does not smooth; for a 5 km buffer 1 m means ~8·10⁷ pixels, not a billion; with `maxPixels: 1e10` it may
    simply run slowly or time out. Bank question L2-09 makes this its correct answer and its feedback repeats "a too large one smooths".
    Fix: "the area is (almost) the same, but 100× more computation; use the native resolution"; reword L2-09.

## Minor

11. **Registration time given four ways**: "up to a day" (s0, s1-summary), "enabled immediately … 20–30 minutes" (s1-page-390, L01),
    "within minutes, sometimes after a day" (p93), "20–30 minutes" (bank L1-02). Unify.
12. **"Required" videos differ**: s1-page-390 requires 3 videos incl. CDSE intro and Spatial Thoughts Module 1; L01 marks CDSE intro
    optional and omits Module 1; L02 lists Module 1 as optional. Align.
13. **Old names**: L02 "In the lab" step 1: "Moodle → *GEE – javascript editor* → lesson" (now "Lesson 2: …"); p104 "module 1 and module 2"
    vs L02 "module 2, section 03".
14. **`s0-summary` grading text**: "30 questions from the seven lessons" (six lessons 2–7); "milestone of module N is due at the start of
    lab N+1" contradicts M1 "Due in lab 1"; "You pass from 60 %, in each piece" – Moodle cannot enforce a per-homework pass; confirm intent.
15. **cm 388 forum named "Ogłoszenia"** (Polish) while pages say "Announcements forum"; forum intro "Enrolment key for this course: GEO"
    is visible only to already enrolled students – remove.
16. **cm 393 label** sits after the homework, repeats the video from homework 1, live name "Source: https://www.sentinel-hub.com/" does not
    match content (shows in completion reports); labels 393–395 have manual completion on. Fix: move to section 1 or delete; completion off on labels.
17. **L02 GAUL slide**: `GAUL2_NAME = 'Poznanski'` is the rural district *around* the city (ring with a hole), labelled "Poznań district",
    ~1 900 km², above the homework limit 50–500 km². Use the city unit or warn. s2-label-394's "no level0 in the 2025 edition" not re-verified.
18. **p131 code and text**: comment on `.copyProperties(... 'system:time_start') // keep the date (filterDate needs it)` is wrong
    (`updateMask` keeps properties; `copyProperties` returns `ee.Element`, chaining `.clip()` fails); "Three levels of cloud information"
    heads a 4-row table; `s2MaskedCS.select('B4').count()` needs `Map.addLayer`; "In Python the only differences are .And() …" overstated
    (same on the L02 slide); the SCL mask does not drop 0 (no data) or 1 (saturated).
19. **p100**: variant A ("the Import button") shows the same code as variant B; the Import button is in the Code Editor search dialog, not on the catalogue page.
20. **p101 / p94**: `print(classified, 'Classified')` arguments reversed; "the sum of all classes must equal the area of aoi" → "approximately;
    gap = masked / edge pixels"; p94: catalogue section is "Explore with Earth Engine".
21. **Lesson 2 buttons and settings**: leftover self-jump buttons "1. signUp GEE", "2. Loading End-to-End…", "3. Add image collection",
    "4. javascript", "5. Area computation" (on page "6."), all [jump 0]; "Area" shortcuts on p93/p94 skip the clouds page; `displayleft=0`,
    `progressbar=0` for a 13-page lesson. Fix: remove self-jumps, turn on the left menu.
22. **p93**: domain `your_id@student.puls.edu.pl` vs IoT tools `@student.up.poznan.pl` – verify; check the university Google account may create
    Cloud projects; 2023 screenshot ("The page has changed") – replace.
23. **s2-assign-392 index list**: ~40 custom-script links, many not indices ("Color correction", "Global mosaic best pixel", "Tonemapped
    Natural Color", "Highlight Optimized Natural Color", "TOA Ratio B09-B8A"). Cut to ~10 indices computable from S2 L2A.
24. **s2-label-395**: COSMO-SkyMed is ASI, not "(ESA)"; missing Copernicus DEM GLO-30 and the course's own reference sources
    (Copernicus EMS Rapid Mapping, EFFIS, GFM) which s0 names as validation references.
25. **Hard-coded `http://localhost:8088/...` links** (8× `section.php` in s0, plus page/lesson/assign/forum links). After restore on
    elearning2 check every one was rewritten; not certain the 4.5 backup encodes `course/section.php?id=`.
26. **Question bank L1/L2**: L1-03/L1-04 test Lesson 2 content and duplicate p95; L1-05 feedback "two satellites" outdated (2B + 2C, 2A extended);
    L1-01 "replace in 2026" – Copernicus Browser dates from 2023, reword "which tool, retired in March 2026, …". Other L2 items fine.
27. **L01/L02 slides**: frontmatter `summary` has "9.11.2026", "16.11.2026" (not rendered, but breaks the rule); L02 "The Code Editor" slide
    still has a TODO screenshot; "Natural Hazards following UN" → "according to the UN"; L02 area code uses `{class: …}` (lesson uses 'code').
28. **Unverified, worth checking**: whether Copernicus Browser still labels the panel "Highlights" (L01, s1-summary); Earth Engine
    noncommercial quota tiers may matter for the registration text.

## Summary
1. Turn on file upload in Homework M2; one deliverable everywhere (link + report of N pages); drop "paste the link in the quiz pages".
2. Make cloud masking real in the code students copy (L02 map() slide, GEO2 `03_ndvi_classes_and_area`); align names, thresholds and
   default AOI between L02, Lesson 2 and GEO2; add `expression()` + /10000 for EVI/SAVI.
3. Add a Lab 1 step-by-step page mirroring L01 "In the lab"; cut duplicated sign-up/repository steps in Lesson 2.
4. Replace weak/trick Lesson 2 quiz pages (p97, p98, p103); fix the wrong "over-smoothed / billion samples" `scale` explanation incl. L2-09.
5. Publish a points rubric per report chapter so "marked out of 100 against the template" can be applied.
