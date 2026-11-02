# Code review B: lessons 4–6 (GEO2 scripts, lesson listings, lecture code)

Scope: GEO2 `04_floods/*`, `05_landslides/*`, `06_wildfires/*`; lesson pages p112, p114, p116, p118, p121, p122;
lecture code in `L04_Floods.md`, `L05_Landslides.md`, `L06_Wildfires.md`. All runs use the harness
(`node run.js <file>` in `Nauka/gee-scripts/.harness`, project ee-geo-hazards). Scratch files are in
`…/scratchpad/codeB/` (`before/`, `after/`, `listings/`, `debug/`, original copies in `orig/`).
GEO2 changes are **not committed** (the uncommitted 02_/03_ changes in the same working tree belong to the other agent).

## 1. Run results

### GEO2 scripts (summary line `== <script> (time, errors)`)

| Script | Before | After | Key printed numbers after |
|---|---|---|---|
| 04/01 water indices | 27 s, 0 errors | 7 s, 0 errors | S2 scenes 12 / 4; optical flood MNDWI 8957 ha, NDWI 5030, AWEI_nsh 6385, AWEI_sh 7140; water before 2686 ha |
| 04/02 orbit check | 6 s, 0 | 6 s, 0 | after: ASC {175:1, 73:2}, DESC {124:2, 22:2} |
| 04/03 flood change detection | 52 s, **1 error** ("Earth Engine capacity exceeded", parallel run); alone 7 s, 0 errors: **2414 ha**, population 1213, cropland 1888, built-up 96 | 46 s, 0 | before 2024-08-25, 09-06; after 2024-09-18; **7019 ha**, population 452, cropland 5519 ha, built-up 30 ha |
| 04/04 threshold sensitivity | 19 s, **2 errors** (capacity exceeded; also alone); passed later in 130 s with spread 10.96 | 106 s, 0 | dB × radius 30/50/100 m: −2 dB 12715/9181/7553; −3 dB 8403/**7019**/6502; −4 dB 6479/5949/5603 ha; spread 2.27 |
| 05/01 stacks and log ratio | 44 s, 0 | 6 s, 0 | 29 pre / 4 post scenes; p80/p90/p95/p99 = 1.62/2.37/3.37/5.62 dB |
| 05/02 masks and heatmap | 62 s, 0 | 7 s, 0 | terrain mask keeps 39.7 % of the AOI; threshold p99 5.87 dB; candidates 270.6 ha; heatmap max 2.57 % |
| 05/03 Hokkaido full workflow | 65 s, 0 | 11 s, 0 | S2 6 / 4 scenes (now Cloud Score+); S1 pre asc/desc 16/30, post 2/4; p90/p95/p99 = 2.19/2.94/4.81 dB; candidates 282.7 ha; all layers render |
| 06/01 FIRMS | 3 s, 0 | 4 s, 0 | 24 daily images; 442 fire pixels, T21 max 500 K; active days 12–19 July (+ 31 July) |
| 06/02 dNBR | 12 s, 0 | 8 s, 0 | classes 0–6 = 359 / 387 / 50825 / 11163 / 3568 / 4719 / 5309 ha (sum 76330 ≈ AOI 76169 ha); burned low..high 24759 ha; moderate-low and above 13596 ha |
| 06/03 EFFIS comparison | 12 s, 0 | 11 s, 0 | placeholder 18736 ha; dNBR burned inside 13805, outside 10954, unburned inside 4968 ha; agreement 74 % (before: 4560 inside, 25144 outside, agreement 22 %) |

The two capacity errors (04/03, 04/04) were transient quota/concurrency errors (10 scripts started at once, other agents
using the same project); with no code change 04/04 passed in a later sequential run.

### Lesson listings and lecture code (cells combined per script)

| Listing | Before | After |
|---|---|---|
| p112 cells (old cells needed `aoi` and lesson 2 `maskSCL`, supplied as context) | 10 s, 0 errors; 8942 ha | 2 s, 0 errors; self-contained; 12 / 4 scenes; MNDWI flood **8957 ha** (= script 04/01) |
| p114 + p116 cells (old: `aoi` supplied) | 31 s, 0 errors; flooded **58 ha** (GSW mask bug) | 41 s, 0 errors; self-contained; **7019 ha** (= script 04/03) |
| p122 cell (parameter block) | nothing to evaluate; names not in the script | listing pasted over the parameter block of 06/02: 7 s, 0 errors; same numbers as 06/02 |
| L04 code (Sentinel-1 + threshold slides, `aoi` supplied) | 33 s, 0 errors; **135 ha** | 1 s, 0 errors; **7019 ha** |
| L05 terrain slide | 1 s, 0 errors (nothing printed) | 3 s, 0 errors; mean slope 10.0°, land fraction 0.999 (Hokkaido AOI check appended) |
| L06 FIRMS + dNBR slides (`aoi`, composites supplied from 06/02) | 2 s, 0 errors (chart only) | 3 s, 0 errors; active days 12–19 July; classes 359 / 387 / 50825 / 11163 / 3568 / 4719 / 5309 ha (= 06/02) |

Identity check (each code line of a listing must also be in the GEO2 script): p112 and p114/p116 have one line that differs
(a `Map.addLayer` without the script's `false`, i.e. the layer is shown). The slides keep the same names and values but put
the parameters on one line, `var A = …, B = …;`, to fit the slide.

## 2. Defects found and fixed

### GEO2
1. **04/03 and 04/04: the default compared two different orbits** (`RELATIVE_ORBIT = null`, DESCENDING). The before mosaic
   was orbit 22 (8 Sept, 71 % of the AOI) on top, the after mosaic orbit 124 (27 Sept). The script itself says this must not be
   done. It inflated exposed population (1213 vs 152–681 for single orbits) and made the sensitivity spread 10.96. New default:
   `PASS = 'ASCENDING'`, `RELATIVE_ORBIT = 175` (6 Sept → 18 Sept). This is the only orbit that covers 100 % of the AOI and has
   a scene within 3 days of the peak; I chose it with the rule in script 02. Other single orbits: DESC 124 (3 → 27 Sept) 2350 ha;
   DESC 22 (8 → 20 Sept, 71 % of the AOI) 3899 ha. README of 04 explains the choice.
2. 04/03: comments added on why `unmask(0)` and `selfMask()` are needed (the same lines are now in the listing). 04/02: `roiArea`
   / `roi_coverage_pct` → `aoiArea` / `aoi_coverage_pct` (`aoi` convention). 04/01: comment typo "thresholds medianAfter looking"
   (left over from the renaming).
3. **06/01–03: the AOI cut off the western part of the Landiras scar.** The scar spans −0.656…−0.445° E and the AOI started at
   −0.62. **The 06/03 placeholder perimeter lay mostly east of the scar**: agreement was 22 %, with 25144 ha "burned outside".
   New AOI `[-0.72, 44.40, -0.36, 44.64]` in all three scripts. The new placeholder is traced along the dNBR scar and labelled
   as not a reference. Main scar: 14168 ha at low severity and above, which matches the about 13 800 ha in the README.
4. 06/02: area property `floodAreaHa` (renaming artefact) → `area_ha` (table and chart). 06/03: asset properties `medianPre` /
   `medianPost` → `pre_period` / `post_period`.
5. 05/03: QA60 replaced by Cloud Score+ (`csPlus`, `linkCollection`, `cs_cdf >= 0.6`) for the Sentinel-2 check. Students copy
   the script to their own event, and QA60 is empty for 2022–Feb 2024. README of 05 updated.
6. 05/02, 05/03: `PERCENTILE` comment "90, 95 or 99" (other values crash). 05/02: the commented GLO-30 alternative now has
   `setDefaultProjection` (otherwise slope depends on zoom).

### Lesson pages
- **p112**: cells rewritten to match 04/01: `aoi` and dates as parameters, `MAX_CLOUD_PCT = 40`, `maskAndScale`, `s2Before/s2After`,
  printed scene counts (the empty-collection trap), `addWaterIndices`, `medianBefore/medianAfter`, a new histogram cell in step 3,
  and `THRESH_MNDWI` + `floodFromIndex` (`unmask(0)`) + `areaHa` at 10 m. Step 2 links GEO2 04/01; step 4 says to set `THRESH_MNDWI`.
- **p114**: cells = steps 1–4 of 04/03 (parameters, `resolution_meters`, `RELATIVE_ORBIT`, `s1Before/s1After`, after window
  16–28 Sept instead of 15–25, `clip(aoi)`, `focal_median` with `SPECKLE_RADIUS_M` instead of `focal_mean`). Text: "focal median",
  "one orbit direction and relative orbit", links to 04/03 and 04/02.
- **p116**: cell 1 = STEP 5 (dB difference by default, `USE_RATIO`/`RATIO_THRESHOLD` as the explained alternative); cell 2 = masks
  with `.unmask(0)`, `selfMask()`, Copernicus GLO-30 slope (HydroSHEDS removed); cell 3 = area as in STEP 7. Text: script 3 (orbit
  check) and script 4 (sensitivity) added under "Before you start"; step 2 "replace the `aoi` rectangle"; step 3 `PASS`,
  `RELATIVE_ORBIT`, `THRESHOLD_DB = -3`, and "for the ratio values of the M4 table set `USE_RATIO = true`"; step 4 explanation; step 7
  names the parameters and script 4.
- **p118** (no code): averaged ascending/descending log-ratios (`iRatioUsed`, fall back to `iRatioAsc`/`iRatioDesc`), EVENT
  block names (`aoi`, `PRE_START` … `POST_END`), "try 95 and 90" instead of "90th and 80th", and the empty-collection hint.
- **p121**: "SCL or QA60" → SCL / Cloud Score+, not QA60.
- **p122**: the UN-SPIDER `SET TIME FRAME` block (2016/2017, `prefire_start`, `geometry`) replaced by the parameter block of 06/02.
  Text uses `aoi`, `PRE_*`/`POST_*`, `EXPORT_CRS`, `MAX_CLOUD_PCT`, `THRESHOLDS`, and "class areas = AOI minus cloud-masked pixels".

### Lectures (code blocks and the line that describes them; the font size of three code boxes was reduced to 20–22 px so the longer code fits)
- L04 Sentinel-1 slide and "Choosing the threshold" slide: same code as p114/p116 (GSW bug fixed, GLO-30, `focal_median`, orbit
  175, `THRESHOLD_DB`/`USE_RATIO`). The ratio bullet now says that −3 dB is the lab script's default.
- L05 terrain slide: NASADEM elevation, `swb`, slope and Gaussian-smoothed curvature as in 05/02, with the GLO-30 alternative
  using `setDefaultProjection`. This replaces the zoom-dependent `mosaic()` + `Terrain.products` + "profile curvature" Laplacian.
  Lines "Reading the heatmap script" and "In the lab" 2–3 now use `aoi`, `PRE_START … POST_END`, `PERCENTILE`, averaged
  directions, VH only (removed `eventDate`, "may use mean", "VV, VH").
- L06 FIRMS slide: excerpt of 06/01 (`confidenceFilter`, `t21Max`, `perDay`, `activeDays`, Landiras dates). dNBR slide:
  `medianPre/medianPost`, `NIR_BAND`, `THRESHOLDS`, `PALETTE` as in 06/02. QA60 line fixed; "In the lab" step 2 uses the script names.

No anonymous `code.earthengine.google.co.in` or hash links were found in the scope. All 56 URLs in the touched files return
HTTP 200, except documented bot blocks (403: medium.com, mdpi.com, researchgate.net, usgs.gov NBR page). `scriptPath` links
return 200 for any path; the four new ones point to files that exist in GEO2.

## 3. Checked and not changed
- Dataset ids are current: `JRC/GSW1_4` (latest), `COPERNICUS/DEM/GLO30_2024_1`, `FIRMS`, `ESA/WorldCover/v200`, GHSL P2023A.
  `NASA/NASADEM_HGT/001` and `WWF/HydroSHEDS/03VFDEM` are **not deprecated** in the EE STAC catalog.
- The landslide scripts keep NASADEM on purpose: it is the paper's DEM, and its `swb` band is the water mask. Only
  `COPERNICUS/DEM/GLO30` (without the year) is deprecated, and it is not used.
- dNBR formula, USGS breaks and palette, SCL classes, Landsat C2 hint (QA_PIXEL bits 3/4, scale/offset) are correct.
- Reading of the flood numbers: 7019 ha (18 Sept, SAR, with masks) vs 8957 ha (MNDWI, 18/21 Sept, no slope or permanent-water
  mask) are consistent. 2414 ha (27 Sept) reflects the receding flood and the orbit mix.

## 4. Mismatches left for the owner (not edited, outside my mandate)
1. **M4 ratio vs dB** (your decision): `s4-assign-431` (threshold 1.25, "difference threshold (1.25)", 1.15/1.25/1.40 table),
   `s4-lesson-401.intro` (three ratio thresholds), the p116 M4 callout, and L04 "In the lab" step 4 still speak in ratios. The listing
   and the text now say how to get the ratio table (`USE_RATIO = true`). Ratio table for the default event (radius 30/50/100 m):
   1.15 → 10662/7790/6549; 1.25 → 5973/5143/4731; 1.40 → 3358/2976/2468 ha.
2. **"Area changes by less than a factor of two between 1.15 and 1.40"** (p116 check box, s4-assign-431, script 04 label "lesson
   target: below 2"). This fails even for the default event: 7790 / 2976 = 2.6 at 50 m; spread over the full table 4.3 (ratio) and
   2.27 (dB). Recommend turning it into "report and explain the factor".
3. `s5-assign-432`: "event date", "one Sentinel-1 orbit", "percentile (99th, 90th, 80th)". These conflict with 05/03 (both directions
   averaged; percentiles 90/95/99; the EVENT block has no event-date parameter). L05 method slide step 1 "same orbit" is still true
   per stack.
4. p112 "buildings also reflect little NIR" and the same wording in quiz L4-03 (reviewer B, item 16). p114 polarisation-mixed dB
   values (−22/−12 dB). p115 says HydroSHEDS is "used by the UN-SPIDER script" (true for the original, not for the course script).
5. Outside my scope but affected by changes here: `examples/qgis/03_qgis_dnbr_classes.py` still uses the old Landiras AOI
   `[-0.62, 44.36, -0.20, 44.64]`. The flood examples (`examples/python/03…`, `examples/qgis/02…`) use other AOIs/methods and no
   orbit pinning (reviewer C, item 24). They should take `ASCENDING`/175 and the new AOI if they must reproduce the GEO2 numbers.
6. GEO2 changes must be pushed by the owner. Until then the Code Editor scripts (opened via `scriptPath`) still have the old
   defaults: DESC/null, the old Landiras AOI, and `floodAreaHa`.
