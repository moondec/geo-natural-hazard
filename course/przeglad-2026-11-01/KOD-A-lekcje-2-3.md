# Code review A – lessons 2 and 3 (JavaScript, Code Editor)

Scope: GEO2 `02_code_editor/*`, `03_classification/*`; Moodle listings s2-lesson-391-p100, p101, p131, s2-label-394,
s3-lesson-396-p106, p107, p108; code blocks of lectures L02 and L03. Harness: `node run.js <file>` in
`Nauka/gee-scripts/.harness` (real EE API, project ee-geo-hazards). Scratch files (extracted listings, outputs,
edit scripts): `C:/Users/marek.urbaniak/AppData/Local/Temp/claude/C--Users-marek-urbaniak-Documents-Dydaktyka/bab5f36d-a316-4c1e-9c6b-2367d77bbb51/scratchpad/codeA/`
(`before-*.js/.out`, `after-*.js/.out`, `baseline.txt`, `after-scripts.txt`, `orig/` = copies of the pages and lectures before editing).
GEO2 changes are **not committed** (other agents' changes to 04–06 are in the same working tree).

## 1. Key finding not in the reviewer reports: `randomColumn()` is not deterministic here

On the client-built training tables (FeatureCollections of buffered points, 8 per class) `randomColumn('random', seed)`
returned a different assignment of random numbers for each request (same set of values, assigned to different
features). Shown in `det*.js`: 12 identical prints of `fc.randomColumn('random', 10).filter(gte 0.7).aggregate_histogram('landcover')`
gave 2 different results, also with explicit `rowKeys`, after `sort()`, before/after `toList()`, and for a single 8-feature
collection. Because every `print()` is a separate request, the printed confusion matrix, overall accuracy, producer's/user's
accuracy and kappa came from **different splits** and did not agree with each other. This was already the case in the
original scripts (baseline 03: matrix diagonal 467/493 = 0.947, printed overall accuracy 0.955; Landsat 05 after the first fix:
matrix and producer's accuracy inconsistent).
Fix: the split is now deterministic and by polygon – `markTestPolygons()` numbers the polygons of each class 0, 1, 2, … via
`toList()` and sets `test = 1` for every third polygon (2, 5, 8, …; ≈ 30 %, automatically stratified by class); `sampleRegions`
copies `test` to every pixel. After the change all printed numbers are mutually consistent (e.g. 03: rows 91/90/94/91 =
test histogram; OA 278/366 = 0.7596 = printed). The same issue may affect any other script in the course that uses
`randomColumn` for a split (I did not check 04–06; they are outside my scope).

## 2. Validation runs (exact `run.js` summary lines)

### GEO2 scripts (before = `baseline.txt`, after = `after-scripts.txt`)

| Script | Before | After |
|---|---|---|
| 02_code_editor/01_first_sentinel2_image | `(3 s, 0 error(s))`, 21 scenes | `(3 s, 0 error(s))`, 21 scenes (script unchanged) |
| 02_code_editor/02_ndvi_median_composite | `(3 s, 0 error(s))`, 21 scenes, no cloud mask | `(3 s, 0 error(s))`, 21 scenes, Cloud Score+ masked |
| 02_code_editor/03_ndvi_classes_and_area | `(19 s, 0 error(s))`, water 55 ha, sum 7760 / AOI 7792 ha, no cloud mask | `(27 s, 0 error(s))`, masked: water 78 ha, sum 7760 / AOI 7791 ha |
| 02_code_editor/04_admin_borders_GAUL | `(5 s, 0 error(s))`, Poznan 261.16 km² | `(6 s, 0 error(s))`, Poznan 261.16 km², 42 scenes |
| 02_code_editor/05_cloud_masking_SCL_CloudScorePlus | `(4 s, 0 error(s))`, 36 scenes, 23.8 valid obs/pixel | `(4 s, 0 error(s))`, 36 scenes, 23.8 valid obs/pixel |
| 02_code_editor/06_ndvi_time_series_chart | `(1 s, 0 error(s))`, 124 scenes | `(2 s, 0 error(s))`, 124 scenes |
| 03_classification/01_random_forest_sentinel2 | `(24 s, 0 error(s))`, 25 scenes, 374/367/372/368 px | `(49 s, 0 error(s))`, 25 scenes, 374/367/372/368 px, export crs EPSG:2180 |
| 03_classification/02_kmeans_unsupervised | `(18 s, 0 error(s))` | `(22 s, 0 error(s))` |
| 03_classification/03_accuracy_assessment | `(12 s, 0 error(s))`, RF OA 0.955 (per-pixel split, prints inconsistent), k-means OA 0.550 | `(16 s, 0 error(s))`, split by polygon (1115 train / 366 test px), RF OA 0.760, kappa 0.680 (all prints consistent), k-means OA 0.478 |
| 03_classification/04_rf_vs_kmeans_comparison | `(84 s, 0 error(s))`, RF OA 0.966, k-means OA 0.529 | `(41 s, 0 error(s))`, RF OA 0.650 / kappa 0.534, k-means (z-scored stack, majority vote) OA 0.740 / kappa 0.653 |
| 03_classification/05_landsat9_alternative | `(14 s, 0 error(s))`, RF OA 0.896 | `(5 s, 0 error(s))`, 34 scenes, RF OA 0.621 |

The drop of the RF accuracy (0.95 → 0.76 for S2, 0.90 → 0.62 for Landsat) is the expected effect of the split by polygon
(see 4.1): the earlier figures were inflated by spatial autocorrelation.

### Lesson listings (cells extracted with `extract.py`, HTML-unescaped, one file per chain)

| Listing (file) | Before | After |
|---|---|---|
| p100 alone (`*-p100.js`) | `(1 s, 0 error(s))`, 21 scenes | `(1 s, 0 error(s))`, `"Number of scenes after filtering:": 21` |
| p100 + p131 + p101 = steps 4–6 (`*-steps4to6.js`) | `(4 s, 0 error(s))` – AOI = 100 m buffer: classes 0 / 1.1 / 0.9 / 1.1 ha (≈ 3 ha in total) | `(18 s, 0 error(s))` – AOI = 5 km buffer: water 78 ha, raw sums identical to GEO2 03 (782 280 / 13 102 405 / 15 495 531 / 48 527 728 m²), sum 7760 ha / AOI 7791 ha |
| s2-label-394 (`*-label394.js`) | `(2 s, 0 error(s))`, 35 districts | unchanged (code was already correct) |
| prelude + p108 + p106 + p107 (`*-lesson3.js`) | `(14 s, 0 error(s))`, RF OA 0.940 (per-pixel split), k-means OA 0.214 with the page's example remap | `(17 s, 0 error(s))`, test px 91/90/94/91, RF matrix `[[91,0,0,0],[0,69,21,0],[0,52,42,0],[6,0,9,76]]`, OA 0.7596, kappa 0.680 – identical to GEO2 03; k-means OA 0.437 (example remap, not fitted to the data – by design) |
| p108 with the stratifiedSample option instead of cell 2 (`after-p108-option.js`) | – | `(35 s, 0 error(s))`, test flag 1115/366, OA 0.746 (matrix consistent) |

The lesson-3 prelude (not on the page) defines `aoi` (8 km buffer, GEO2 default) and four "drawn" FeatureCollections
with the default points of GEO2 01 – the harness cannot draw geometries.

### Lecture code blocks (`extract_md.py`; L03 run in lab order: training → RF → accuracy → k-means → improving, composite from p108 cell 1)

| Lecture | Before | After |
|---|---|---|
| L02 (6 blocks in order) | `(20 s, 0 error(s))`, `scenes: 17` (30 % filter), water 65 ha (no mask) | `(20 s, 0 error(s))`, 21 scenes, water 78 ha – same as lesson and GEO2 03 |
| L03 (5 blocks) | `(1 s, 1 error(s))` – `Required argument (...) missing`: `composite.addBands(clusters)` with `clusters` not yet defined | `(18 s, 0 error(s))`, RF matrix and OA 0.7596 identical to p108 / GEO2 03 |

Verified separately: `FAO/GAUL/2025/level0` → `Collection asset 'FAO/GAUL/2025/level0' not found`; level1 has 16 Polish units;
level2 `Poznan` = 261 km², `Poznanski` = 1 892 km². QA60: a 2023-06-07 scene has 21 636 valid QA60 pixels, all 0 (no flags);
a 2025-06-01 scene has 10 005 flagged pixels → QA60 is *zero*, not *masked*, in 2022-01-25…2024-02-28 (`qa60.js`).
Olofsson et al. 2014 checked on Crossref (RSE 148, 42–57, doi 10.1016/j.rse.2014.02.015). URLs added: GEO2 scriptPath links and
`code.earthengine.google.com/?scriptPath=users%2Fujavalgandhi…` → HTTP 200; developers.google.com clustering guide → 200.

## 3. Changes

### GEO2 (`C:/Users/marek.urbaniak/Documents/Nauka/gee-scripts/GEO2`, uncommitted)
Naming everywhere: `s2` = raw collection, `s2Filtered` = after filters, `s2MaskedCS` = Cloud Score+ masked, `maskCS()`
identical to lesson step 5 cell 2; `maskSCL()` identical to step 5 cell 1.
- `02_code_editor/00_README`: step table re-numbered to the lesson (step 5 = script 05, step 6 = 02 + 03); note that 02/03 use
  the masked collection.
- `02_ndvi_median_composite`: header "step 5.1" → "step 6 part 1"; Cloud Score+ mask added (`s2MaskedCS`); fixed the false
  claim that the median-of-NDVI equals the NDVI of the median composite.
- `03_ndvi_classes_and_area` (homework template): header "steps 5.2-5.4" → "step 6 parts 2-4"; **Cloud Score+ mask added**
  (reviewer A 5); area code renamed to `areaGroups`/`areaList`/`areaTable` = lesson/L02; `scale` comment corrected (same area,
  100× computation – not "Too many pixels" as the only outcome); sanity test "≈".
- `04_admin_borders_GAUL`: header states there is no level0 table; `s2Filtered`.
- `05_cloud_masking_SCL_CloudScorePlus`: header "returns in Lecture 7" → "Lesson 2 step 5 / Lecture 2 slide"; QA60 text corrected
  (zeros, not masked; populated again after 2024-02-28); function renamed `maskQA60` = lesson cell 3; SCL mask now drops 0 and 1;
  constants `QA_BAND`/`CLEAR_THRESHOLD` replaced by `maskCS()`.
- `06_ndvi_time_series_chart`: header "Lecture 7-8" (L07 = APIs) → change-detection labs; `s2MaskedCS`, `s2ndvi`.
- `03_classification/00_README`: split by polygon + why not `randomColumn`; stratifiedSample snippet carries the `test` band;
  "re-sample from the stack".
- `01_random_forest_sentinel2`: `maskCS`/`s2MaskedCS`; `maskScl` → `maskSCL` with 0/1; `inputProperties: composite.bandNames()`;
  export `crs: 'EPSG:2180'`; property `floodAreaHa` → `area_ha` (wrong rename from commit 8575cba – a land-cover table had a
  "flood" column).
- `02_kmeans_unsupervised`: same mask/naming; `area_ha`; export crs; note that the remap list needs K entries.
- `03_accuracy_assessment`, `04_rf_vs_kmeans_comparison`, `05_landsat9_alternative`: per-pixel `randomColumn` split →
  `markTestPolygons()` split by polygon with the optimism note (Olofsson 2014); 03 prints test pixels per class; 05: Landsat
  `copyProperties` result cast to `ee.Image`, export crs; `area_ha` in 04/05.

### Lesson pages (`course/mcontent`)
- **p100**: Import button described correctly (Code Editor search results); variant B AOI `Point(16.92, 52.44).buffer(100)`, zoom 16
  → `Point(16.93, 52.41).buffer(5000)`, zoom 12 (= GEO2 01, L02); filter order/form = GEO2 01; labelled `print`.
- **p131**: heading "Three levels…" (4-row table) → "Where Sentinel-2 stores cloud information"; table 30 % → 35 %; SCL row lists 0/1;
  QA60 row and warning callout corrected (band is 0, mask removes nothing, composite stays cloudy – the page claimed it
  masks everything and gives a grey map); cell 1 `maskSCL` drops 0 and 1, wrong `.copyProperties(...) // filterDate needs it`
  removed, layer names = GEO2 05; cell 3 `maskQA60` without `copyProperties`, titled as a bitmask-reading example; count
  instruction now a `Map.addLayer(...)` call; Python sentence no longer "only differences".
- **p101**: "Before you start" points to the 5 km default; cell 1 = GEO2 02 (two-line `addNDVI`, `s2ndvi.select('NDVI').median()`)
  plus the NDVI layer the Inspector check needs; cell 2 `vegetation` → `green`, `.multiply().rename()` order = GEO2 03;
  cells 5–7 = GEO2 03 part B + area table (classNames, classPalette, `.rename('class')`, `print('Classified image:', …)` –
  arguments were reversed), sanity-test print added; `scale` callout rewritten (same area, 100× samples, ≈ 8·10⁷ vs 8·10⁵);
  "sum must equal" → "close to; gap = edge/cloudy pixels".
- **s2-label-394**: verified, unchanged (level1 + dissolve for Poland; level0 really does not exist).
- **p108**: links: `.co.in` mirrors → `code.earthengine.google.com`, GEO2 01 and 03 linked (01 was linked nowhere); cell 1 = GEO2 01
  composite (Cloud Score+, 40 %; was unmasked, 20 %); cell 2 `markTestPolygons` + `properties: ['landcover', 'test']`; cell 3 split by
  polygon + test histogram; text of step 5 explains why; cell 4 `smileRandomForest({numberOfTrees: 50, seed: 42})`; cell 5 labels
  "producer's / user's accuracy"; one sentence that the accuracy is optimistic (Olofsson et al. 2014); export with
  `crs: 'EPSG:2180'` / UTM note; `print(cm)` → `confusionMatrix`; "a few hundred metres across" → "70–200 m (50–500 px)",
  "at least 10 per class"; common-mistake bullet includes per-pixel split; stratifiedSample option keeps the test flag.
- **p106**: anonymous `.co.in/<hash>` links → GEO2 02 and 03 + GEE clustering guide; cell 1 `seed: 42`; cell 2 `.rename('cluster')`;
  cell 3 remap in the GEO2 form (`CLUSTER_TO_CLASS`, position = cluster id); k = 6/8 note that remap lists need k entries; export crs.
- **p107**: SCL classes 0, 1, 3, 8, 9, 10; QA60 "no cloud flags"; normalisation sentence adds k-means (z-score, as GEO2 04);
  cell 1 band names upper-case (= GEO2 04), **re-samples the polygons from `stack`** and trains/classifies `stack`; importance via
  `ee.Dictionary(classifier.explain().get('importance'))`; common-mistake box and self-check reworded accordingly.

### Lectures (`presentation/obsidian/cycle`; docs rebuild not done)
- **L02**: filtering slide = p100/GEO2 01 (`s2` + `s2Filtered`, 35 %, zoom 12, `rgbVis`); clouds slide QA60 function = p131 cell 3,
  description line "no flags (all 0)…", SCL bullet 0/1, "differs mainly by `.And()`"; map() slide starts from `s2MaskedCS`
  (Cloud Score+ lines added, font 34 → 28 px); thresholds slide = p101 cell 2/5 (renames, classNames, classPalette);
  area slide `groupName: 'code'` (was `'class'`), names column, `scale` bullet corrected, "≈ AOI area", chart call fixed
  (font 32 → 28 px); GAUL slide: no level0 table, `'Poznanski'` (1 892 km² ring around the city) → `'Poznan'` (261 km², = GEO2 04 default).
- **L03**: RF slide trains on `trainSet` with seed; k-means slide seed + rename; training-data slide = p108 cells 2–3 (no undefined
  `clusters`, `geometries: true`, split by polygon; font 32 → 24 px); accuracy slide labels; improving slide = p107 band names +
  comment to re-sample; importance call.

## 4. Open questions / not done
1. **Honest accuracy with the default training points is ≈ 0.76 (RF S2) / 0.62 (Landsat)**, below the "above about 0.8" self-check
   in p108 and script 03. Per-point indices (`pointcheck.js`): water points 6–8 (Warta: 16.9423/52.4112, 16.9408/52.4149,
   16.9220/52.3587) have NDVI 0.11–0.39 (not open water at 10 m); urban points 3–8 have NDVI 0.40–0.62 (green housing estates);
   crops 0.36–0.78 (harvest in the season). The points need checking on the map by the owner – I did not move them.
2. **Slide layout**: the L02 map()/area slides and the L03 training-data slide got longer code with smaller fonts; check the
   rendered slides in the central docs rebuild.
3. k-means with k = 4 never produces a "crops" class on the default data (mapping `[1,3,0,1]` in 03) – consistent with reviewer B 9
   (decision on fixed k is the owner's).
4. Lesson-3 default AOI is an 8 km buffer (≈ 201 km²) while p108 asks for a 60–100 km² AOI; left unchanged (lesson 3 uses the
   student's lab-2 AOI); the 5 km lesson-2 default (78.5 km²) would fit 60–100 km².
5. Not in my remit, seen while editing: L03 "Improving the classification" list item 1 says "SCL (classes 3, 8, 9, 10)" and
   "lecture 7 explains the bits" (it is lecture 2 / lesson 2 step 5); L03 RF slide text "bootstrap with replacement" (reviewer B 15);
   p101 deliverable still says "paste the link … in the quiz pages" (reviewer A 3); no EVI/SAVI `expression()` example (reviewer A 6).
6. p108/p106 listings use literal dates and `confusionMatrix` (scripts use `START/END` and `cmRandomForest`/`cmKmeans`); logic and
   numbers are identical, only these names differ by design (single-classifier page vs. two-classifier script).
7. Script 01 (RF) still trains on all labelled pixels (no split) – by design, accuracy is in 03.
