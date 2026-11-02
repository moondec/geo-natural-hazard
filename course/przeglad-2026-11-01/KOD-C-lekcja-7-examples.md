# KOD-C – lesson 7 code: examples/, lesson 7 listings, L07 slides (validation and fixes)

Agent C (Claude Opus 5.5), 2026-11-02. Scope: `examples/{python,qgis,R,notebooks}`, `examples/README.md`,
`course/mcontent/s7-lesson-404-p123/p125/p126/p127/p128/p129/p130/p132.html`, `presentation/obsidian/cycle/L07_APIs.md`.
Nothing committed, nothing pushed, no Moodle access, GEO2 not touched (only read and run). All scratch files are in
`C:/Users/marek.urbaniak/AppData/Local/Temp/claude/C--Users-marek-urbaniak-Documents-Dydaktyka/bab5f36d-a316-4c1e-9c6b-2367d77bbb51/scratchpad/codeC/`
(below: `codeC/`). The full unified diff of every change against the pre-edit state (the GitHub `main` copy, which was
identical to the local files for every untouched file, plus a backup of the notebook) is `codeC/all_changes.diff`.

## 1. Environments and test method

| What | How |
|---|---|
| EE scripts (`python/01,03,04`) | `C:/Users/marek.urbaniak/Documents/Nauka/gee-scripts/.venv/Scripts/python.exe` (Python 3.14, earthengine-api 1.7.49, openeo 0.53.0) via `codeC/run_ee.py <script>`: redirects `ee.Initialize` to project `ee-geo-hazards`, stubs `Task.start()`/`Task.status()` (no Drive export was started). Repo files keep `PROJECT = 'ee-your-project'`. |
| geemap / notebook (`python/02`, notebook, p125, L07) | new venv `C:/Users/marek.urbaniak/AppData/Local/Temp/ghC` (Python 3.13.5, earthengine-api 1.7.50, geemap 0.38.9, pandas 3.1.0, nbclient 0.11, ipykernel 7.4). It could not live in `codeC/`: pip failed with `WinError 3` (Windows long-path limit, `@jupyter-widgets` schema path), so it sits at a short path under `Temp`. Notebook executed headless with `codeC/run_nb.py` (copy with the project substituted, `allow_errors=True` so that every failing cell is reported). |
| QGIS scripts | (a) `"C:/Program Files/QGIS 3.44.4/bin/python-qgis.bat" codeC/qgis_check.py examples/qgis` (compile + import list, QGIS 3.44.4, Python 3.12.11); (b) EE logic with plain `ee` + stub `ee_plugin.Map` (`codeC/stub/ee_plugin.py`, `addLayer` calls `getMapId(vis)` so objects and vis params are validated on the server) via `codeC/run_qgis.py`. The plugin was not installed. |
| Reference numbers | `node run.js` (harness) on the current GEO2 working tree `04_floods/03_sentinel1_flood_change_detection` and `06_wildfires/02_dnbr_burn_severity_sentinel2`. |
| openEO | dry run without login (`codeC/openeo_dry.py`, `codeC/openeo_cell_dry.py`): connection, `describe_collection('SENTINEL2_L2A')`, graph built and `validate()`d on the backend, `download()` stubbed. |
| R | `Rscript` 4.5.1 `parse()` only; rgee, terra, sf, ggplot2 are not installed. |
| Static | `pyflakes` 4.1.0 on `python/`, `qgis/` and on the concatenated notebook code cells. |
| URLs | `curl -L` with a browser UA, 44 URLs (list and codes in `codeC/urlcheck.tsv`). |

## 2. Results per file (command → result, before and after)

### examples/python
| File | Before | After |
|---|---|---|
| `01_hello_earth_engine.py` (`run_ee.py`) | `scenes: 17`, `mean NDVI in the AOI: {'NDVI': 0.5024}`, 13 s | unchanged file, same output |
| `02_geemap_ndvi_map.py` (ghC venv, `run_ee.py`) | runs; `ndvi_poznan_2025.tif` written (3.5 MB); `gdalinfo`: EPSG:2180, 10 m, NDVI min −0.23 / max 0.93 / mean 0.505; Drive export stubbed. `geemap.Map` and `split_map` do not crash headless | unchanged file |
| `03_flood_s1_change_detection.py` | `before scenes: 8`, `after scenes: 2`, **flooded 1415.4 ha**; sensitivity −2/−3/−4 dB → 2505 / **1433** / 1091 ha (the −3 dB row ≠ main result: loop had no speck filter). Parameters differed from GEO2 04/03 (AOI, after window, `focal_mean`, NASADEM, speck filter on the raw mask, no `resolution_meters`, both descending tracks) | `before scenes: 2 ['2024-08-25','2024-09-06']`, `after scenes: 1 ['2024-09-18']`, **flooded 7019.3 ha** (GEO2 harness: **7019 ha**); sensitivity −2/−3/−4 dB → 9181 / **7019** / 5949 ha (−3 row = main result) |
| `04_dnbr_burn_severity.py` | pre 11 / post 7 scenes; classes 0–6 = 540 / 571 / 66 493 / 14 019 / 3063 / 3036 / 2850 ha; burned (3–6) 22 968 ha. Old AOI, SCL keep-list [4,5,6,11] (drops class 7) | pre 11 / post 7; classes 0–6 = 356 / 324 / 50 875 / 11 177 / 3569 / 4719 / 5309 ha; **moderate-low and above 13 597 ha** (coordinator: GEO2 ≈ 13 600); burned (3–6) **24 774 ha** (GEO2 harness: 24 759 ha); total 76 330 ha vs AOI 76 169 ha. Cloud Score+ branch (flag True, scratch copy, old AOI): runs, burned 28 607 vs SCL 29 724 ha |
| `05_cdse_openeo_ndvi.py` (dry) | backend API 1.2.0; `SENTINEL2_L2A` has B04/B08/SCL, `eo:cloud_cover` filter emitted as `lte 30`; graph `load_collection, mask, ndvi, reduce_dimension`; backend `validate()` → `[]`; `resample_spatial(projection=2180, resolution=10)` builds; no deprecation warnings with `-W always` (openeo 0.53.0; PyPI current 0.54.0) | same (comment change only) |

### examples/qgis (stub Map, plain ee)
| File | Before | After |
|---|---|---|
| all three, `python-qgis.bat qgis_check.py` | compile OK; imports `ee`, `ee_plugin`; neither importable in the bare QGIS Python (expected: the plugin ships `ee`) | compile OK |
| `01_qgis_console_ndvi.py` | `Scenes used: 17`, both layers accepted by `getMapId`, `centerObject` OK | unchanged |
| `02_qgis_flood_mask.py` | scenes 8 / 4, **3542 ha** (median instead of mosaic, other mask order, both tracks) – header claimed "same method as GEO2/04_floods/03" | scenes 2 / 1, **7018 ha** (GEO2 7019; the 1 ha comes from clipping after instead of before the focal filter) |
| `03_qgis_dnbr_classes.py` | moderate-low+ 12 425 ha, burned 29 704 ha (= old GEO2 AOI, matched GEO2 at that time) | moderate-low+ **13 596 ha**, burned **24 759 ha** (= GEO2 24 759) |

Plugin API: names checked against the plugin user guide (gee-community.github.io/qgis-earthengine-plugin/usage/):
`from ee_plugin import Map`; `addLayer(eeObject, visParams, name, shown, opacity)`, `centerObject`, `getBounds`,
`getCenter`, `setCenter`, `getScale`, `getZoom`, `setZoom` – the scripts and the p130 table use only these. plugins.qgis.org:
0.3.3 needs QGIS ≥ 3.44 (max 4.99); for QGIS 3.40 the repository offers **0.1.7** (min 3.22) – so "0.3.x refuses older
QGIS" was wrong. Authors listed: Gennadii Donchyts, Xavier C. Llano, Fedor Baart, Zac Deziel, Anthony Lukach.

### examples/notebooks/07_capstone_template.ipynb (`run_nb.py`, ghC venv)
- Before: pyflakes on the code cells: 7 undefined names (`sar_after_smooth`, `sar_before_smooth` ×2, `floodAreaHa`, `pre`, `post`).
  Run: cell 1 OK; **cell 7 NameError `sar_after_smooth`**, cell 8 NameError `sar_before_smooth`, cell 9 NameError
  `permanent_water` (cascade), cell 11 OK (old AOI, 90 572 ha total), **cell 12 NameError `pre`**; 4 errors. The "after dates"
  line printed `system:index` strings, not dates.
- After the renaming fix one more defect appeared in cell 12: `m.add_legend(..., labels=CLASS_NAMES, colors=...)` →
  `ValueError: The legend keys and colors must be the same length.` In geemap 0.38.9 (`map_widgets.Legend`) `labels` is
  overwritten by the default keys when `keys` is None; fixed with the documented `keys=`.
- Final run (`run_nb.py ... codeC/nb_final.ipynb`, 415 s): **0 errors**. Cell 1 "Hello from Earth Engine"; cell 7
  before 2 scenes `['2024-08-25', '2024-09-06']`, after 1 scene `['2024-09-18']`, **flooded 7019 ha** (GEO2 7019);
  cell 8 `geemap.Map` widget created; cell 9 sensitivity (ha, threshold × focal_median radius 30/50/100 m):
  −4 dB 6479 / 5949 / 5603, **−3 dB 8403 / 7019 / 6502**, −2 dB 12 715 / 9181 / 7553 (the −3 dB / 50 m cell equals the main
  result); cell 11 pre 11 / post 7, classes 356 / 324 / 50 875 / 11 177 / 3569 / 4719 / 5309 ha, burned (3–6) **24 774 ha**;
  cell 12 map with legend; cell 13 histogram figure. pyflakes on the final code cells: clean; `nbformat.validate`: OK.
  (Two markdown-only edits – "orbit direction and relative orbit" – were made after this run started.)

### Lesson listings and slides
| Listing | Command | Result |
|---|---|---|
| p123 cell 1 + p125 cells 1–3 + "run the printed code" (`codeC/run_p125_nb.py`, nbclient) | after | cell 1 prints "Hello from Earth Engine"; translator prints 43 lines; translated code runs, layer "NDVI Composite", composite 13 bands |
| p125 JS example (harness `run.js`) | before / after | before: 0 errors, layer OK (QA60 mask, displayed the unreduced `withNdvi`); after: 0 errors, layer OK |
| p125 `geemap.js_snippet_to_py` (`codeC/js2py_test.py`) | before | **translation breaks**: `"system:time_start"` → `""system":time_start"` (SyntaxError); with single quotes it becomes `'"system":time_start'` (runs, silently wrong). The translator does quote dict keys, `.and()`→`.And()`, adds `.getInfo()` to `print()` (tested), contrary to step 4 of the page |
| p125 after | | translation compiles and runs (example no longer uses `copyProperties`) |
| p128 Export cell 1 appended to current GEO2 06/02 (harness) | after | 0 errors; image export band `severity`, table export `M6_area_ha` registered |
| p128 rgee cell, p123 R cell | – | static only (no rgee/ggplot2/rpy2 locally) |
| p130 cells 1+2 (stub Map) | after (unchanged) | `Scenes: 17`, both layers OK |
| p132 openEO cell (dry) | after (unchanged code) | graph validated, `[]` |
| L07 Python blocks (`codeC/test_l07.py`, ghC venv) | after | Colab slide: `scenes: 17`; client/server slide: `print(n)` prints `ee.Number({ "functionInvocationValue": ... })`, `print(n.getInfo())` → 17, `if s2.size() > 10` → **TypeError '>' not supported between instances of 'Number' and 'int'**, `if s2.size():` → True (also `bool(ee.Number(0))` → True), `ee.Image(ee.Algorithms.If(...))` → 26 bands (without `ee.Image` the result is a `ComputedObject` with no `.select`); "Getting data out": **`geemap.ee_to_df` fails with pandas 3.1.0** (`ValueError: Cannot specify both 'axis' and 'index'/'columns'`, geemap `common.py` line 8888), works with pandas 2.3.3 (17 rows, columns date/ndvi); export and `ee_export_image` OK; QGIS slide (stub) OK; openEO slide (dry, gee venv) validated |

Client/server claims checked with `codeC/client_server.py` (earthengine-api 1.7.49): reviewer C item 6 confirmed.

### R
`Rscript -e "invisible(parse('...'))"` → parse OK for `01_rgee_hello.R` and `02_rgee_dnbr.R`, before and after.
rgee CRAN 1.1.8 (2025-10-15); rgee README still states "requires gcloud CLI to authenticate new users" and uses
`ee_Initialize(project = ...)`. rgee is presented as optional everywhere in scope (README "R and rgee (volunteers)",
p126 "in R (rgee) for volunteers", p128 "For volunteers: rgee", L07 "rgee for R volunteers").

### URLs (44 checked, `codeC/urlcheck.tsv`)
All 200, including `raw.githubusercontent.com/moondec/geo-natural-hazard/main/examples/README.md`,
`.../examples/notebooks/07_capstone_template.ipynb`, the GitHub blob/tree links of p129/p130/p132/p128/p123, the Colab
GitHub link of the notebook and of the Spatial Thoughts notebook (raw file exists), plugins.qgis.org, plugin docs
(installation, troubleshooting, usage), rgee pages, CDSE, openEO, epsg.io, `noncommercial_tiers`, `cloud.google.com/earth-engine/pricing`.
Caveat: `colab.research.google.com/...` always answers 200 (single-page app); the targets exist, but the in-browser
behaviour of `#create=true&language=r` was not checked. `http://localhost:8088/mod/assign/view.php?id=434` (p126) skipped (Moodle-internal).

## 3. What was changed (file – change – why)

**examples/python/03_flood_s1_change_detection.py** – aligned with the current GEO2 04/03 (coordinator sync): AOI
`[17.20, 50.40, 17.80, 50.90]`, after window to 09-28, `ORBIT_PASS='ASCENDING'` + `RELATIVE_ORBIT=175` filter,
`resolution_meters == 10`, `mosaic` + `focal_median`, JRC `.unmask(0)`, Copernicus GLO-30 slope with
`setDefaultProjection`, new `mask_flood()` (`selfMask`, water, slope, then `connectedPixelCount(25, True)`); the
sensitivity loop now uses `mask_flood()` (reviewer C 24 / D 1); scene dates printed; `floodAreaHa` → `flood_area`
(Python naming); docstring says it is the Python version of GEO2 04/03.

**examples/python/04_dnbr_burn_severity.py** – AOI `[-0.72, 44.40, -0.36, 44.64]`, PRE_END 07-11, SCL mask = GEO2
(drop 3, 8, 9, 10, 11) instead of the keep-list [4,5,6,11], EXPORT_CRS `EPSG:32630` (convention: UTM outside Poland,
was Lambert-93 2154), local `s2` → `s2_filtered`, renaming artefacts in the docstring ("median_pre-fire"), commented
map block `pre/post` → `median_pre/median_post`, `add_legend(keys=...)`, printed "burned (classes 3-6)". Why the mask:
`codeC/scl_dark_check.py` shows that in the cloud-free post-fire scenes 44–55 % of the dNBR > 440 pixels are SCL class 7
(unclassified) and 0 % class 2; with the same AOI the old keep-list gave 25 335 ha burned (dNBR > 100) vs 29 724 ha.

**examples/python/05_cdse_openeo_ndvi.py** – last comment: "unlimited quota" → both sides have limits (openEO credits,
EE monthly noncommercial quota).

**examples/qgis/02_qgis_flood_mask.py** – same method and track as GEO2 04/03 (mosaic, `resolution_meters`, ascending
track 175, GLO-30 slope, mask order, 8-connected speck filter). Header claim "same method" is now true.

**examples/qgis/03_qgis_dnbr_classes.py** – AOI to the new GEO2 AOI.

**examples/R/02_rgee_dnbr.R** – same AOI, PRE_END and SCL mask as GEO2/Python 04 (`$Or`, `$Not`); pixel-count comment.

**examples/notebooks/07_capstone_template.ipynb** – undefined names fixed; flood cell = python/03 (incl. orbit 175 and
`mask_flood`), sensitivity table uses the same masks and `focal_median`; fire cell = python/04 (AOI, mask,
`s2_filtered`, burned total printed); `add_legend(keys=...)`; separate `FLOOD_EXPORT_CRS` (2180) / `FIRE_EXPORT_CRS`
(32630) – the single `EXPORT_CRS = 'EPSG:2180'` would have exported the Gironde result in the Polish grid; data table and
limitations NASADEM → Copernicus DEM; setup comments (geemap preinstalled in Colab; `ee.Authenticate()` is a no-op
with valid credentials – verified in `ee/oauth.py`); markdown "orbit direction" → "orbit direction and relative orbit".
Source cells kept as single strings (original JSON style, `indent=1`).

**examples/README.md** – table rows for 03/04 (GEO2 parameters, Copernicus DEM); local setup: Python 3.12+ (PyPI:
earthengine-api requires ≥ 3.11, geemap 0.38.9 requires ≥ 3.12), `"pandas<3"` with the reason; gcloud paragraph
replaced (the Python API uses the browser flow when gcloud is absent – `ee/oauth.py`: `localhost` if a browser is viable
and gcloud not installed, `notebook` in Jupyter, `colab` in Colab; `--auth_mode=notebook` for headless servers);
CDSE paragraph: "unlimited free compute" → both sides limited, link to noncommercial tiers; QGIS: "0.3.3 or newer"
(date dropped), "project ID", old QGIS gets plugin 0.1.x; rgee: gcloud is an rgee requirement, dead reference to
"the lesson page *rgee*" → lesson 7 QGIS page 4; data table NASADEM → `COPERNICUS/DEM/GLO30_2024_1`.

**p123** – R cell: `library(ggplot2)` added (reviewer C 20).
**p125** – cell 1: truncated comment replaced; cell 2 JS: `geometry` → `aoi`, QA60 → SCL mask (`maskS2scl`), no
`copyProperties` (translator bug), `filtered` → `s2Filtered`, `withNdvi` → `s2ndvi`, map shows `composite.select('ndvi')`
(median, not the collection); step 4 rewritten (what the translator does and the verified colon-string bug); step 5
mentions the SCL mask; client/server box corrected (`ee.Number({…})`, TypeError, bare `if` always true, `getInfo()` /
`ee.Algorithms.If`).
**p127** – old QGIS gets plugin 0.1.x (not "refuses"); "export path of QGIS 4" → "Door A on QGIS page 4"; author line;
"project name" → "project ID" (steps 6–7, alt texts, caption).
**p128** – rgee listing header "Export, cell 2" → "rgee, cell 1"; source line `[2024]` → `[year of your scenes]`;
QGIS-version trap (0.1.x); "project name" → "project ID"; "(CRAN 1.1.8, 2025)" → "(CRAN 1.1.8)".
**p132** – "effectively unlimited free quota" → free noncommercial quota, Community tier 150 EECU-hours a month per
Cloud project, link to the noncommercial tiers page (numbers verified on that page: Community 150, Contributor 1000 with
billing account, Partner 100 000 EECU-h/month); "free compute" → "free noncommercial compute". No calendar date added.
**L07_APIs.md** – client/server slide code and comments (17 instead of 37 = actual result of the slide code; TypeError;
bare `if`; `ee.Image(ee.Algorithms.If(...))`); Door A `region: AOI` → `aoi`; plugin "0.3.3 or newer", "project ID";
trap "QGIS < 3.44 → only plugin 0.1.x"; rgee version date dropped; CDSE table "free quota" → "free noncommercial quota
(monthly limit)"; QGIS slide code = p130 cell 2 (cloud filter, `rename('NDVI')`); "In the lab" timings aligned with the
pages (Colab 60, QGIS 1–2 35, QGIS 3 25, QGIS 4 30 min) and step 4 no longer repeats the console NDVI.

Not changed although checked: `python/01`, `python/02`, `qgis/01`, `R/01`, p126, p129, p130 (code correct, numbers plausible).

Other code that may be affected: GEO2 04/03 and 06/02 are now the reference for these examples – any further change of
their CHANGE HERE values must be repeated in `python/03`, `python/04`, `qgis/02`, `qgis/03`, `R/02` and notebook cells
5/7/11. The lab 4/6 lesson listings and slides (other agents) were not compared with the examples.

## 4. Could not be validated, and why
- **QGIS plugin itself**: not installed (brief); only the EE logic with a stub `Map` and a compile check under the QGIS
  Python. Tile rendering inside QGIS, the Processing algorithms, the Data Catalog and the sign-in dialogs of p127–p129 are unverified.
- **rgee / R**: rgee, terra, sf, ggplot2 not installed; parse only. `R/02` logic is the same expression chain as Python 04
  (validated), but `ee_as_rast(via = "getDownloadURL")`, `ee_extract` column names (`substr(..., 2, 9)` date parsing in R/01)
  and the `Map$addLayer(...) + Map$addLayer(...)` composition were not run. p123 `%%R` cell (rpy2) not run.
- **CDSE openEO with login**: needs the owner's CDSE account; download/batch job not executed (graph validated by the backend).
- **Colab**: notebook run locally with nbclient (Python 3.13, geemap 0.38.9), not in Colab; Colab's preinstalled versions
  (pandas, geemap) not checked. The `geemap.Map` widgets were created but not displayed.
- **Drive exports**: stubbed on purpose; export parameters (crs/scale/region) only checked as code.

## 5. Open questions / findings for the owner
1. **Capstone landslide route** (reviewer C 8, D 10): the template and examples still cover flood and fire only; not
   decided here.
2. **Sensitivity "factor < 2"** (lesson 4/M4, decision not mine): with the new defaults the Python table is
   9181 / 7019 / 5949 ha (−2/−3/−4 dB, factor 1.5); in the notebook 3×3 table the filter radius matters as much
   (−3 dB: 8403 / 7019 / 6502 ha for 30 / 50 / 100 m; extremes 12 715 vs 5603 ha, factor 2.3).
   Sync note: GEO2 04/03 and 06/02 changed in the working tree during this session (another agent; uncommitted):
   flood DESCENDING/all tracks → ASCENDING track 175, fire AOI → [-0.72, 44.40, -0.36, 44.64]. The examples follow the
   working tree as read after those edits (coordinator request); reference runs: flood 7019 ha, fire burned 24 759 ha,
   moderate-low+ ≈ 13 600 ha.
3. **`s2` after filters**: convention says `s2Filtered`, but GEO2 06/02 itself uses `var s2 = ...filterBounds().filter()`,
   and so do `python/01`, `02`, `qgis/01`, p130 and L07. Left as is to stay identical to GEO2; rename everywhere or nowhere.
4. **p124 (API quiz, outside my scope)**: "Julia" is one of four "correct" answers while EarthEngine.jl is unmaintained;
   all four answers must be ticked without "(select all that apply)" (reviewer D 2).
5. **`pandas<3` pin** in the README is a workaround for a geemap bug (`ee_to_df`), to be removed when geemap is fixed.
6. **L07 frontmatter** still has a Polish summary with a calendar date (housekeeping, not changed).
7. **Python 01/02, L07 Colab slide, qgis/01, p130**: scene-level cloud filter only, no per-pixel mask (consistent with
   each other; lesson 2 teaches "clouds first"). Not changed.
8. The burned total (classes 3–6, 24 774 ha) is well above the ~14 000 ha of the July fire because "low severity"
   (11 177 ha) includes unburned forest and fields that changed between June and August; worth one sentence in the
   lesson 6 interpretation (moderate-low and above: 13 597 ha).
9. Housekeeping done without asking first: I deleted `examples/python/__pycache__/` and `examples/qgis/__pycache__/`
   (only `.pyc` bytecode caches, e.g. `03_flood_s1_change_detection.cpython-314.pyc` from an earlier pyflakes/run of the
   old code; regenerated automatically, not content). They should not be committed anyway.
10. The test venv at `C:/Users/marek.urbaniak/AppData/Local/Temp/ghC` (+ `ghC_pd2` with pandas 2.3.3) lies outside the
   scratchpad because of the long-path limit; it can be deleted (`rm -rf` of both folders) – contains only pip packages.
