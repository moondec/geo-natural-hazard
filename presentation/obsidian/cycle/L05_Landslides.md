---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - SAR
  - landslide
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 5
summary: "Wykład 5 (2 h, 7.12.2026) – osuwiska: definicja i typy (Varnes/Hungr), czynniki i wyzwalacze, inwentaryzacja vs podatność, metody optyczne (NDVI change), SAR amplitude change (Handwerger et al. 2022), InSAR, DEM; wstęp do ćwiczeń 5 (skrypt heatmap gęstości osuwisk)"
timeForPresentation: 5400
theme: beige
width: 1920
height: 1200
margin: 0
maxScale: 4
transition: zoom
course: Application of geoinformatics to natural hazards mapping and monitoring
---

<!-- slide data-background-image=![[sateliteGEEbanner.png|1920]] -->
<grid drag="64 58" drop="0 27" bg="#EEB73F" align="left" pad="60px 60px 60px 300px">

### Lecture 5<!-- element style="letter-spacing: 1.5rem;"-->
## Landslide mapping with satellite data
#### from a landslide inventory to a density heatmap

#### Marek Urbaniak

</grid>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Today (90 min)
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>

::: block <!-- element style="font-size: 44px" align="left" drag="80 80" drop="0 15"-->
1. What a landslide is, and the types that look different from space
2. Causes and triggers: rain, earthquakes, people
3. Three products: **inventory**, **susceptibility**, **hazard / risk**
4. Optical detection: vegetation loss (NDVI change), bare soil, shadows
5. SAR amplitude change – the Handwerger et al. (2022) heatmap method you will run
6. InSAR: slow-moving landslides, millimetres per year
7. Terrain: DEM derivatives that every landslide model uses
8. **In the lab**: the GEE landslide density script on a real event
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## What is a landslide?
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:40px" align="left" drag="52 75" drop="0 15"-->
**Landslide** – the downslope movement of soil, rock and organic material under the effect of gravity, and the landform that results from it (USGS).

Classified by **material** (rock, debris, earth) and **type of movement**:
- **falls** and **topples** – rock from cliffs
- **slides** – rotational (slump) and translational (planar)
- **flows** – debris flow, mudflow, earthflow (fast, long run-out)
- **spreads** and complex / composite
:::

::: block <!-- element style="font-size:35px" align="left" drag="45 75" drop="55 15" bg="#e8f4f8" pad="15px"-->
From orbit you see the **scar** (bare, bright, steep source area), the **track** and the **deposit** (fan, dammed river). Size: from 10 m (one Sentinel pixel) to km². Most rain-triggered landslides are **small** – resolution matters more than for floods.

In Poland: Carpathian flysch (Beskidy, Pogórze) – ~95 % of Polish landslides; the SOPO inventory by PGI-NRI holds > 70 000 of them (2023) ([geoportal SOPO](https://geoportal.pgi.gov.pl/portal/page/portal/SOPO)).
:::


::: source
source: Hungr, O., Leroueil, S., Picarelli, L. (2014). The Varnes classification of landslide types, an update. *Landslides* 11, 167–194; [USGS Landslide Handbook](https://pubs.usgs.gov/circ/1325/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Causes vs. triggers
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:39px" align="left" drag="50 78" drop="0 15"-->
**Preconditions** (why *here*): slope angle and aspect, lithology (clay, flysch, weathered rock), soil depth, drainage, land cover (forest roots), old landslides, road cuts, deforestation

**Triggers** (why *now*):
- **rainfall** – intense (hours) or prolonged (weeks); the global majority
- **earthquakes** – thousands of co-seismic landslides at once (Nepal 2015, Sulawesi 2018)
- snowmelt, river undercutting, volcanic activity, human loading / excavation
:::

::: block <!-- element style="font-size:37px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Why this matters for the satellite method:
- a rain- or earthquake-triggered **event** gives a sharp *before/after* date → change detection works (lab 5)
- slow creep over years has no event date → InSAR time series instead
- preconditions are the **predictors** of a susceptibility model (Random Forest again – lecture 3)

Data for triggers in GEE: rainfall `NASA/GPM_L3/IMERG_V07` (30 min, 10 km), `UCSB-CHG/CHIRPS/DAILY`; earthquakes: USGS catalogue (CSV → Assets).
:::

::: source
source: [NASA Global Landslide Catalog & LHASA model](https://gpm.nasa.gov/landslides/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Three products, three questions
:::

::: block <!-- element style="font-size:32px" align="left" drag="95 78" drop="0 15"-->
| Product | Question | Input | Method | Example |
|---|---|---|---|---|
| **Inventory** | where did landslides happen (after event X)? | before/after images | change detection, visual mapping, ML | lab 5 heatmap; Copernicus EMS grading maps |
| **Susceptibility** | where *could* they happen? | inventory + preconditions (slope, lithology, land cover…) | statistical / ML model (logistic regression, RF) | SOPO, [NASA LHASA](https://gpm.nasa.gov/landslides/) |
| **Hazard / risk** | how likely, how often, what is exposed? | susceptibility + trigger frequency + elements at risk | probabilistic | insurance, planning |

This course: an **inventory** from satellites (this week) – the input of everything else. Without an inventory there is no model to train.
:::

::: source
source: Guzzetti et al. (2012). Landslide inventory maps: new tools for an old problem. *Earth-Science Reviews* 112, 42–66.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Optical detection: what changes
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="50 78" drop="0 15"-->
A fresh landslide removes vegetation and exposes soil/rock:
- **NDVI drops** sharply (0.7 → 0.2) → `dNDVI = NDVI_before − NDVI_after > 0.2–0.3` on steep slopes
- brightness increases in red and SWIR (bare soil), decreases in NIR
- texture: elongated patches along the slope direction; a river may be dammed (new water in MNDWI)
- the same recipe as lab 2 + 4: median composites before/after → index → difference → threshold → **slope mask** (> 10–15°) → area
:::

::: block <!-- element style="font-size:40px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Limits of optical:
- clouds during the rainy trigger – the first clear image may come weeks later
- vegetation regrows; agriculture, logging and burned areas also lose NDVI → confusion
- shadows on steep north slopes
- 10 m pixels miss the small ones

Use it: as validation of the SAR map on the first clear day, and for earthquake events in dry seasons. Very high resolution (PlanetScope 3 m, Pléiades 0.5 m) is what EMS uses – not free.
:::

::: source
source: Belgeo (2015) [Landslide mapping and monitoring with remote sensing](https://journals.openedition.org/belgeo/15944) – Moodle literature list
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## SAR amplitude change: the method of lab 5
:::

::: block <!-- element style="font-size:30px" align="left" drag="50 78" drop="0 15"-->
Handwerger et al. (2022): **landslide density heatmaps** from Sentinel-1, fully in GEE, no training data.

1. Stacks of S1 GRD **VH** images **before** (months) and **after** (weeks) the event, same orbit; temporal **median** of each stack (pixels ≤ −30 dB removed)
2. Pixel-wise **log-ratio**: $I_{ratio} = 10\log_{10}\frac{I_{pre}}{I_{post}} = I_{pre} - I_{post}$ [dB] – positive where backscatter decreased
3. Landslide candidates = pixels with $I_{ratio}$ above the **99th percentile** of the AOI (vegetation removed → VH drops)
4. Masks: slope < 5–10° (flat areas, floods), curvature, water (NASADEM) – no built-up mask
5. Kernel **density heatmap** of the candidate pixels (100 m cells, 1–3 km radius) → which valleys were hit
:::

::: block <!-- element style="font-size:29px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Why a heatmap and not single landslides?
- speckle and layover make single-pixel detections unreliable
- emergency managers need to know *which valleys* were hit within a day – not polygons
- the heatmap is then validated against mapped inventories (Hokkaido 2018 earthquake, Hiroshima 2018 rain, Haiti 2021 – all in the paper)

Script: [GEO2 › 05_landslides › 03_full_workflow_hokkaido_2018](https://code.earthengine.google.com/?scriptPath=users%2Fmarekurbaniak%2FGEO2%3A05_landslides%2F03_full_workflow_hokkaido_2018) (Moodle, *Landslides* lesson, page 2); the authors' GitHub repository has 30 figure scripts with Code Editor links (start with a Hokkaido figure).
:::

::: source
source: Handwerger, A.L. et al. (2022). Generating landslide density heatmaps for rapid detection using open-access satellite radar data in Google Earth Engine. [NHESS 22, 753–773](https://doi.org/10.5194/nhess-22-753-2022)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Reading the heatmap script
:::

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
![[diagram_L05_heatmap_script.svg]]
:::

::: block <!-- element style="font-size:36px" drag="95 14" drop="0 86" bg="#fff3cd" pad="10px 20px"-->
The parameters you will change: AOI geometry, `eventDate`, length of the pre-event stack (longer = less noise), the change threshold, the grid size. Everything else you have already seen in labs 2 and 4 (filter, median – the course copy may use mean –, ratio, percentile, mask, reduce).
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## InSAR: slow landslides, millimetres per year
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:39px" align="left" drag="52 75" drop="0 15"-->
- The **phase** difference between two SAR acquisitions = ground motion in the line of sight (+ topography + atmosphere + noise)
- Time-series methods (PS-InSAR, SBAS) on dozens of Sentinel-1 scenes → velocity maps, mm/yr precision, over cities, dams, slow-moving slopes
- **European Ground Motion Service** (Copernicus Land): free velocity maps of Europe: baseline 2015–2021 plus annual 5-year updates, latest 2020–2024; EU Login needed ([egms.land.copernicus.eu](https://egms.land.copernicus.eu/))
- Not in GEE (needs the SLC product and phase processing): SNAP (ESA, free), LiCSAR / LiCSBAS (COMET, free, pre-processed interferograms), commercial platforms
:::

::: block <!-- element style="font-size:37px" align="left" drag="43 75" drop="55 15" bg="#e8f4f8" pad="15px"-->
Where it fails:
- fast movement (> ~ half a wavelength between passes, i.e. cm in 6 days) → phase decorrelates – that is exactly a *catastrophic* landslide, hence amplitude methods for events
- dense vegetation, snow → decorrelation
- motion perpendicular to the line of sight (north–south) is invisible

Division of labour: **InSAR = monitoring** before the failure; **amplitude change = detection** after it.
:::

::: source
source: [EGMS product description](https://land.copernicus.eu/en/products/european-ground-motion-service); Moodle lesson *Flood mapping* page 6 (InSAR)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Terrain: the DEM derivatives everybody uses
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:26px" align="left" drag="50 78" drop="0 15"-->
```javascript
var dem = ee.ImageCollection('COPERNICUS/DEM/GLO30_2024_1').select('DEM').mosaic();  // 30 m, TanDEM-X 2010–2015
// or NASA/NASADEM_HGT/001 (SRTM reprocessed), or your LiDAR DTM uploaded as an Asset
var terrain = ee.Terrain.products(dem);   // elevation, slope, aspect, hillshade
var slope = terrain.select('slope');
var aspect = terrain.select('aspect');
var curvature = dem.convolve(ee.Kernel.laplacian8());   // simple profile curvature proxy

Map.addLayer(slope, {min: 0, max: 45, palette: ['white', 'yellow', 'red']}, 'slope');
```
In Poland: the national LiDAR DTM (1 m, ISOK / geoportal.gov.pl) – vastly better than any global DEM for landslide scars (shaded relief shows old slumps under forest).
:::

::: block <!-- element style="font-size:27px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Used as:
- **masks** in detection (slope > 5–10°; floods are flat, landslides are not)
- **predictors** in susceptibility models: slope, aspect, curvature, elevation, distance to rivers and roads, TWI (topographic wetness index), lithology
- **visual mapping**: hillshade at low sun angle reveals old landslide morphology

Combine with lecture 3: inventory points (label 1) + random non-landslide points (label 0) + terrain + land cover bands → `smileRandomForest` with `setOutputMode('PROBABILITY')` → susceptibility map 0–1. Optional extension of lab 5 for the ambitious.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Where to get help and reference data
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- **Copernicus EMS** – grading maps after major landslide events (activations list, free GIS layers): [emergency.copernicus.eu](https://mapping.emergency.copernicus.eu/)
- **International Charter Space and Major Disasters** – [disasterscharter.org](https://disasterscharter.org/) (activations with maps)
- **Sentinel Asia** – Asia-Pacific disaster support: [sentinel-asia.org](https://sentinel-asia.org/)
- **NASA Global Landslide Catalog** (points 2007–~2020, continued as COOLR) and **LHASA 2.0** nowcast: [gpm.nasa.gov/landslides](https://gpm.nasa.gov/landslides/)
- **SOPO** (PGI-NRI) – Polish landslide inventory, the validation layer if you choose a Carpathian case
- **UN-SPIDER** – [landslide knowledge portal](https://www.un-spider.org/disaster-type/landslide)
:::

::: source
source: Moodle section *Landslides mapping approaches* – summary
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (3 h)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. Choose an event with a known date and a reference inventory: the paper's cases (Hokkaido 6.09.2018, Hiroshima July 2018, Haiti 14.08.2021) or one from an EMS activation
2. Open the heatmap script (Moodle *Landslides* lesson, page 2); set AOI, event date, pre/post windows, orbit; run – note the computation time
3. Inspect the log-ratio layers (VV, VH) with the Inspector over a known landslide and an untouched slope
4. Change the threshold and the pre-event stack length; see how the heatmap changes
5. Overlay a reference: EMS grading map (upload as Asset) or Sentinel-2 true colour of the first clear day – visual agreement
6. Export the heatmap GeoTIFF; a short note: event, parameters, where it works, where it fails (shadow? floods? agriculture?)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before next class
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Finish the landslide heatmap note (parameters + one figure + link)
- [ ] Next week: **wildfires**. Read the Moodle lesson *Fire detection and severity estimation*, pages 1–3 (15 min)
- [ ] Read the UN-SPIDER [burn severity recommended practice – "In detail"](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail) and note the dNBR classes table
- [ ] Find one fire in Copernicus Browser *Highlights* (or EFFIS) with pre- and post-fire cloud-free Sentinel-2 dates – you will need them in the lab
:::

---
::: block 
# Thank you :smile:
:::
