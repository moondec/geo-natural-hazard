# Reviewer B (Claude Opus, high) – sections 3–4, lectures L03/L04, question bank L3/L4

Read every s3-/s4- field, `names.tsv` lines 76–142, L03, L04, the L3/L4 part of `course/questions/build_questions.py`, `RULES-geo.md`,
`schedule.json`, the live structure dump and the GEO2 scripts the lessons link to (`03_classification`, `04_floods`). No edits.

## Blocker

1. **p116 (Flood script, cell 2) and L04 slide "Choosing the threshold": the permanent-water mask removes the whole flood.**
   `var permanentWater = gsw.gte(10); … flooded.updateMask(permanentWater.not())`. In `JRC/GSW1_4/GlobalSurfaceWater` "areas where water
   has never been detected are masked", so `permanentWater.not()` is masked on all land that was never water and `updateMask` deletes every
   flood pixel there; the area comes out near zero. `flooded` is also never self-masked before `connectedPixelCount`. GEO2 script 03 does both
   correctly: `gsw.gte(PERMANENT_WATER_MONTHS).unmask(0)` and `floodRaw.selfMask()`. Fix: copy those lines into the listing and the slide; re-run with `run.js`.

## Major

2. **p116, s4-assign-431, s4-lesson-401.intro, L04 "In the lab": homework asks for a 1.25 ratio, the script defaults to −3 dB.** GEO2 03 has
   `USE_RATIO = false`, `THRESHOLD_DB = -3`; GEO2 04_threshold_sensitivity defaults `[-2, -3, -4]` dB. The p116 listing ("The script computes the
   change like this") differs from script 03: `focal_mean` vs `focal_median`; HydroSHEDS vs Copernicus GLO30 for the slope mask; after window
   15–25 Sept vs 16–28 Sept. Fix: one convention (tell students "set `USE_RATIO = true`" or rewrite M4 in dB −2/−3/−4); make the listing match script 03.
3. **p116 / M4: useful scripts never linked.** GEO2 `04_floods/04_threshold_sensitivity` builds exactly the M4 table (threshold × radius, CSV);
   `02_sentinel1_orbit_check` answers step 3 "check which orbit covers your area". Without them 3×3 sensitivity + GFM comparison + optical part
   is too much for 3 h. Fix: list as scripts 3 and 4 in "Before you start"; name them in steps 3 and 7.
4. **Lesson page 116 title "ICEYE – high temporal and spatial resolution SAR" (button "ICEYE" on p115)** is actually the main lab 4 exercise and
   the M4 deliverable; the homework points to "lesson page *ICEYE / the lab scripts*". The ICEYE paragraph is marketing and unsourced ("large
   office in Warsaw", "more than 70 satellites launched by 2026", "used in the Polish flood response of September 2024") plus a sales link; L04
   cites the same page as slide source. Fix: rename "Lab 4: Sentinel-1 flood script (UN-SPIDER)" and the button; reduce ICEYE to one neutral
   sentence on p114 ("commercial X-band constellations (ICEYE, Capella, Umbra): sub-metre, sub-daily, not free"); drop the sales link in lesson and slide.
5. **s3-lesson-396-p109 "Landslides and wildfire", L03 slide "ML for hazards: two papers you will reproduce".** Lead says "Two applications of
   machine learning", but both examples say "no training data" / "no machine learning". Both promise "the Random Forest classification of damage
   classes is the lab's own extension" (lab 6) – no RF in lab 6 or L06. Wildfire script is an anonymous `code.earthengine.google.co.in/399574…`
   snapshot (a 200 response proves nothing). Slide cites UN-SPIDER, page cites Al-hasn & Almuhammad 2022. Fix: delete the page; move the Dynamic
   World box to p106/p107 and the lab 5/6 links to their lessons; or rewrite as "ML in hazard mapping" with real ML examples. Remove the RF claim from the slide.
6. **p108 cell 3 (and L03 training slide): the 70/30 split is done per pixel.** Neighbouring pixels of the same small polygon land in both sets;
   accuracy inflated (spatial autocorrelation), the "above about 0.8" self-check passes trivially; test pixels only from pure patches, so not
   map accuracy. Fix: split per polygon (`randomColumn` on `trainingSamples` before `sampleRegions`, or separate validation polygons); one sentence
   that this accuracy is optimistic; reference Olofsson et al. 2014, RSE 148, 42–57.
7. **L03 slide "Training data…" code contradicts p108.** Slide uses `composite.addBands(clusters).sampleRegions({…})`, but `clusters` does not exist
   yet in the lab order (RF first) → "clusters is not defined"; omits `geometries: true` which p106 needs. Fix: use p108 cell 2 code on the slide.
8. **p107 "Improving the Classification": two gaps.** (a) After building `stack` the page says "train on `stack.bandNames()`", but `trainSet` was
   sampled from `composite` → missing-property error unless `sampleRegions` is re-run on `stack`; the "Common mistake" box and quiz L3-12 miss
   this. (b) Normalisation "required for SVM or neural networks and harmless for RF" never mentions k-means, which is distance-based: elevation
   (m) and slope added to reflectance (0–10 000) without scaling dominate; GEO2 script 04 z-scores for this reason. Fix: "re-sample the polygons
   from `stack`"; "normalise (z-score) before k-means".
9. **s3-assign-398 vs p106.** Homework: "justify the selected number of classes"; p106: "try k = 6 and k = 8"; template and "Before you upload"
   require 4×4 matrices and a legend "0…3". Fix: four classes fixed, k = 6/8 clusters merged many-to-one with `remap`; or allow n×n matrices.
10. **Resource cm 397 "Short deck: Random Forest and k-means".** Full reveal.js export: ~300 files incl. a 20 MB `GEO_ML_Classifiers.zip` of
    itself, a 10 MB banner, all of MathJax, Font Awesome, all themes and source maps. Same 2023 Excalidraw drawings as Lecture 3, which covers RF
    and k-means in more depth. Appears under three names: "ML in GEE" (p105), "Short deck: the two classifiers" (s3-summary), "GEO_ML_Classifiers
    slides" (L03 "Before next class"). Fix: delete cm 397; remove links from p105 step 1, s3-summary and L03, or point them to Lecture 3 (cm 425).
11. **cm 399 and cm 400 (the two PDFs) and the s4-summary block "Error estimation – reading".** Crespi & De Vendictis 2009 is about geometric and
    radiometric quality of VHR sensors; TATSSI 2021 about QA flags in MODIS-type time series. Neither deals with flood-map or classification
    uncertainty, so "background for the uncertainty part of your reports" is not true. TATSSI is 16 MB; both are open access at MDPI anyway.
    Fix: remove both; if a reading is wanted, Olofsson et al. 2014 (section 3) and Notti et al. 2018 (section 4, already cited).

## Minor

12. **p115 "InSAR detection techniques".** Lead: "what InSAR delivers for flood mapping – elevation models and displacement"; displacement is
    for landslides. The flood-relevant InSAR use, coherence loss in urban floods (e.g. Chini et al. 2019, RS 11, 107 – verify), is missing.
    Fix: retitle "DEMs for flood mapping (InSAR in brief)" or add a coherence paragraph. The DEM table is good.
13. **p114, L04 "Choosing the threshold", quiz L4-05: dB values mixed between polarisations.** "VH water ≈ −22 dB, land ≈ −12 dB": land −12 dB is a
    typical VV value, VH land is about −15 to −20 dB; the −18 dB water limit in the tables fits VV. "Choose VH for open land" is debatable: GFM
    (the reference product) works on VV. Fix: values per polarisation; VV operational default, VH used in the UN-SPIDER script.
14. **Sentinel-1 status in p111, p114, L04.** "1D operational since May 2026", "1A worked … to June 2026" unsourced. Fix: check ESA SentiWiki and
    cite, or soften to "1C (2024) and 1D (2025)".
15. **L04 slides, smaller overstatements.** Charter: "free satellite tasking (all agencies)" – only member agencies, only authorised users trigger
    an activation. "Otsu … used by the Global Flood Monitoring service" – only one of GFM's three algorithms uses split-based thresholding.
    L03 "Random Forest in four steps": bootstrap "with replacement", but GEE's default `bagFraction` 0.5 samples without replacement.
16. **p112 "Water indices".** Thresholds hard-coded `gt(0)` right after step 3 says "pick the threshold in the valley"; no histogram code.
    `CLOUDY_PIXEL_PERCENTAGE < 20` after a flood can leave an empty collection → "No band named 'B3'". Names `s2`, `medianBefore` break the
    GEO2 convention (`s2Filtered`, `s2Before/s2After`). References missing: McFeeters 1996 (IJRS 17, 1425–1432), Xu 2006 (IJRS 27, 3025–3033),
    Huang 2018, Feyisa 2014 (AWEI, RSE 140, 23–35). "Buildings also reflect little NIR" is a poor explanation (Xu: built-up land can have
    green ≥ NIR); same wording in quiz L4-03's correct answer. Fix: `var t = 0;` + `ui.Chart.image.histogram` snippet, print collection sizes, add references, reword.
17. **p110 and p113 tables only as images** ("table Multispectral for flood.png", German-named "Indizes.png") – not accessible, formulas
    uncheckable. Fix: retype as `iot-material-table` with AWEI formulas in text.
18. **p108 small inconsistencies.** Self-check says `print(cm)` but the variable is `confusionMatrix`; output labelled "consumer accuracy" while the
    text says "user's accuracy"; "a few hundred metres across" ≠ "50–500 pixels" (300 m × 300 m = 900 pixels); `Export.image.toDrive` has no `crs`
    (convention EPSG:2180 or UTM); Lecture 3 says "ten bands" and p105 lists "B2…B12, NDVI, MNDWI…" but the composite has 6 bands; links to
    `code.earthengine.google.co.in` mirrors and anonymous hash links (p106) – link GEO2 `01_random_forest_sentinel2` and
    `02_kmeans_unsupervised` instead (script 01 is not linked anywhere).
19. **Self-check "the area changes by less than a factor of two between 1.15 and 1.40"** (p116, M4 box, L4-12 feedback) turns a result into a
    pass/fail rule with an arbitrary factor. Fix: ask students to report and explain the factor.
20. **Question bank (`build_questions.py`).** L4-11 "50 m focal mean" but the script uses `focal_median`; L4-10 feedback names the HydroSHEDS slope
    mask, the course script uses Copernicus DEM; L4-03's correct option contains "Buildings reflect little NIR like water"; L4-05 feedback repeats
    "land around −12 dB" in VH. The rest of L3-01…12 and L4 is correct and unambiguous; L3-05's 88 % matches the matrix.
21. **Stale names and dates.** L04 water-indices slide cites the lesson as "*Learning objectives of this topic* … pages 3–4" (old name); hidden
    gradebook items carry old names ("Learning objectives of this topic", "Classifiers"); `names.tsv` still has "(23.11)", "(30.11)", "(due 7.12)"
    although live names are clean – regenerate; L03/L04 front-matter `summary` fields contain "23.11.2026", "30.11.2026". Page titles:
    "Satellites characteristic" → "Satellite characteristics"; "Other water indices" vs button "Other water indexes".
22. **p111 table.** Proba-V revisit "5 – 1" (should be 1 – 5); claims to be Notti's "Table 1, updated" but adds a Sentinel-1 row while the lead
    talks only about optical satellites; p114 "amplitude only" → "intensity σ⁰, no phase".

## Summary
1. The permanent-water mask in p116/L04 (`gsw.gte(10)` without `.unmask(0)`, no `selfMask`) wipes out the flood – copy the working lines from GEO2 script 03.
2. Make the lab 4 deliverable match the scripts (ratio vs dB); link GEO2 `04_threshold_sensitivity` and `02_sentinel1_orbit_check`; listing identical to script 03.
3. Rename lesson page 116 to "Lab 4: Sentinel-1 flood script"; cut ICEYE to one neutral sentence; delete or rewrite p109.
4. Fix the classification method: per-polygon split, re-sample from `stack`, normalise before k-means, settle "4×4 vs justify k", fix the undefined `clusters` on the slide.
5. Remove the redundant 60 MB "Short deck" (cm 397) and the two off-topic PDFs (cm 399/400); link Olofsson et al. 2014 instead.
