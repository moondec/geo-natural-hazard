---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - wildfire
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 6
summary: "Wykład 6 (2 h, 14.12.2026) – pożary: intensywność vs dotkliwość, detekcja aktywnych pożarów (MODIS/VIIRS FIRMS), odpowiedź spektralna spalonej roślinności, NBR, dNBR, RdNBR, progi USGS, dobór obrazów pre/post, EFFIS; wstęp do ćwiczeń 6 (mapa dotkliwości w GEE)"
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

### Lecture 6<!-- element style="letter-spacing: 1.5rem;"-->
## Wildfire detection and burn severity
#### active fires, burned area, dNBR

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
1. Vocabulary: fire intensity, burn severity, soil burn severity
2. Three satellite products: **active fire**, **burned area**, **burn severity**
3. Active fire detection: thermal bands, MODIS / VIIRS, FIRMS
4. Spectral response of burned vegetation → NBR
5. dNBR, RdNBR and the USGS severity classes
6. Choosing pre- and post-fire images (the step where most reports go wrong)
7. Validation: CBI field plots, EFFIS, EMS
8. **In the lab**: the UN-SPIDER burn severity script
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Vocabulary first
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:44px" align="left" drag="95 78" drop="0 15"-->
- **Fire intensity** – energy released per unit time and length of fire front (Byram 1959); physics of the flames, measured *during* the fire (kW/m); from satellites: **Fire Radiative Power** (FRP, MW)
- **Burn (fire) severity** – the effect of the fire on the ecosystem: degree of vegetation mortality, consumption of organic matter; measured *after* the fire – **this is what dNBR maps**
- **Soil burn severity** – fire-induced change in soil physical, chemical and biological properties; drives erosion and post-fire floods / debris flows (link to lecture 5!)
- **Burned area** – the perimeter / pixels that burned, regardless of severity
:::

::: source
source: Keeley, J.E. (2009). Fire intensity, fire severity and burn severity: a brief review and suggested usage. *Int. J. Wildland Fire* 18, 116–126; Moodle lesson page 1
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Three products, three sensors
:::

::: block <!-- element style="font-size:32px" align="left" drag="95 78" drop="0 15"-->
| Product | When | Physical basis | Sensors | Resolution | GEE / source |
|---|---|---|---|---|---|
| **Active fire** (hotspots) | during the fire, several times a day | thermal emission at 4 µm (MWIR) and 11 µm | MODIS, **VIIRS**, Sentinel-3 SLSTR, GOES | 1 km / 375 m | `FIRMS` (NASA), `NASA/VIIRS/002/VNP14A1` |
| **Burned area** | after, monthly | reflectance change + hotspots | MODIS, Sentinel-2/3 | 500 m / 20 m | `MODIS/061/MCD64A1`, EFFIS |
| **Burn severity** | after, per event | NIR drop + SWIR rise → dNBR | Sentinel-2, Landsat | 10–30 m | **your lab** script; MTBS (USA) |

Active fire tells *where it burns now*; burned area tells *how much*; severity tells *how badly* – and only the last one needs the before/after pair.
:::

::: source
source: [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/); [EFFIS](https://forest-fire.emergency.copernicus.eu/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Active fire detection: hot pixels
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:32px" align="left" drag="50 78" drop="0 15"-->
- A fire at 600–1000 K radiates most in the **mid-wave infrared (4 µm)**; the background at 300 K radiates most at 11 µm (Wien's law)
- Algorithm: a pixel is a fire if its 4 µm brightness temperature is far above its neighbours (contextual test) and above 11 µm – day and night, through smoke, **not through clouds**
- **VIIRS** (NOAA-20/21; Suomi-NPP delivery to FIRMS ends 2 Nov 2026): 375 m, twice a day each; **MODIS** (Terra/Aqua): 1 km, archive since 2000 (Terra science ends Feb 2027)
- **FIRMS** delivers hotspots within 3 h; CSV / KML / WMS; in GEE as `FIRMS` collection (daily, 1 km) and VIIRS products
- Use in the lab: hotspot dates = **when** the fire burned → choose the post-fire window
:::

::: block <!-- element style="font-size:27px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
var firms = ee.ImageCollection('FIRMS')
  .filterDate('2025-07-01', '2025-08-31')
  .filterBounds(roi)
  .select('T21');                       // brightness temperature, K
var hot = firms.max().gt(300);          // any detection in the window
Map.addLayer(hot.selfMask(), {palette: ['red']}, 'FIRMS hotspots');
// a chart of detections per day gives the fire timeline
print(ui.Chart.image.series(firms.map(function(i){return i.gt(0);}),
      roi, ee.Reducer.sum(), 1000));
```
<!-- TODO image: Planck curves at 300 K and 800 K with MWIR/TIR bands marked (public-domain figure, e.g. from NASA ARSET or draw in Excalidraw). -->
:::

::: source
source: Giglio, L. et al. (2016). The collection 6 MODIS active fire detection algorithm. *RSE* 178, 31–41; Schroeder, W. et al. (2014). The new VIIRS 375 m active fire product. *RSE* 143, 85–96
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Spectral response of burned vegetation
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="50 78" drop="0 15"-->
Healthy vegetation: high **NIR** (leaf structure), low **SWIR** (water in leaves).
After a fire: leaves gone, char and ash, dry soil → **NIR drops**, **SWIR rises**.

$$ NBR = \frac{NIR - SWIR_2}{NIR + SWIR_2} = \frac{B8 - B12}{B8 + B12} $$ (Sentinel-2) $$ = \frac{SR\_B5 - SR\_B7}{SR\_B5 + SR\_B7} $$ (Landsat 8/9)

NBR is high for green forest (0.3–0.7), near zero for bare soil, strongly negative for freshly burned (−0.2 … −0.5).
:::

<!-- TODO image: reflectance curves healthy vs burned vegetation with S2 bands B8 and B12 marked – exists in Moodle lesson page 2 ("Healthy and burned areas", source USGS/UN-SPIDER) – paste into pliki/. -->

::: block <!-- element style="font-size:32px" align="left" drag="45 80" drop="53 15" bg="#e8f4f8" pad="15px"-->
Why NBR and not NDVI?
- NDVI saturates in dense forest and recovers fast with grass; the **SWIR₂** band (2.2 µm) reacts to char and soil moisture – it stays changed for months
- NBR was designed for severity (Key & Benson 2006) and correlates with field CBI (Composite Burn Index)
- Still: both are used; NDVI difference is a useful second opinion in grassland

Important: SWIR₂ is a **20 m** band on Sentinel-2 – the result is effectively 20 m, not 10 m.
:::

::: source
source: Key, C.H., Benson, N.C. (2006). Landscape Assessment (LA): sampling and analysis methods. USDA FS RMRS-GTR-164-CD; Moodle lesson pages 2–3
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## dNBR and the USGS severity classes
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:25px" align="left" drag="48 78" drop="0 15"-->
$$ dNBR = NBR_{pre} - NBR_{post} $$

Convention: often scaled × 1000. Positive = loss of vegetation; negative = regrowth.

| dNBR (scaled) | dNBR | Burn severity |
|---|---|---|
| < −250 | < −0.25 | enhanced regrowth, high |
| −250 … −100 | −0.25 … −0.10 | enhanced regrowth, low |
| −100 … +100 | −0.10 … 0.10 | **unburned** |
| 100 … 270 | 0.10 … 0.27 | **low severity** |
| 270 … 440 | 0.27 … 0.44 | **moderate–low** |
| 440 … 660 | 0.44 … 0.66 | **moderate–high** |
| > 660 | > 0.66 | **high severity** |
:::

::: block <!-- element style="font-size:22px" align="left" drag="48 78" drop="52 15" bg="#e8f4f8" pad="15px"-->
```javascript
var nbrPre  = pre.normalizedDifference(['B8','B12']);
var nbrPost = post.normalizedDifference(['B8','B12']);
var dNBR = nbrPre.subtract(nbrPost).multiply(1000).rename('dNBR');

var thresholds = ee.Image([-250, -100, 100, 270, 440, 660]);
var severity = dNBR.gt(thresholds).reduce('sum').toInt();   // 0..6
var sevVis = {min: 0, max: 6, palette:
  ['7a8737','acbe4d','0ae042','fff70b','ffaf38','ff641b','a41fd6']};
Map.addLayer(severity.clip(roi), sevVis, 'burn severity');
```
Caveats:
- thresholds were derived for US forests; in Mediterranean shrub or Polish pine they shift – **calibrate** with field data or at least report them as "USGS proposed"
- **RdNBR** = dNBR / √|NBR_pre| normalises for pre-fire vegetation amount – fairer when comparing forest with grassland (Miller & Thode 2007)
:::

::: source
source: [UN-SPIDER burn severity – In detail](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail); [USGS Landsat NBR](https://www.usgs.gov/landsat-missions/landsat-normalized-burn-ratio); thresholds: Key & Benson 2006 (FIREMON)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Choosing the pre- and post-fire images
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:36px" align="left" drag="50 78" drop="0 15"-->
The most common source of a wrong severity map is not the formula – it is the **dates**:
- **pre**: as close as possible before ignition, same season, cloud-free; a median of 2–4 weeks works
- **post** (*initial assessment*): 1–4 weeks after containment – smoke gone, ash still there
- **extended assessment**: next growing season, same phenology as pre – measures mortality, not char
- same sensor, same processing level (L2A), same band set; never mix Landsat pre with Sentinel post without harmonisation
- mask clouds **per pixel** (`SCL` / `QA60`) – a cloud in *pre* looks like high severity
:::

::: block <!-- element style="font-size:34px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Checklist before you trust the map:
1. FIRMS timeline: when did it start, when did it end?
2. Pre and post composites: look at them in true colour – clouds? snow? harvested fields?
3. dNBR histogram over the perimeter: bimodal? where is the unburned peak (should be ~0)?
4. Compare the "unburned" class outside the perimeter: if it shows "low severity" everywhere, your dates differ in phenology
5. Area per class in hectares (lecture 2 code) – the number for the report
:::

::: source
source: [UN-SPIDER burn severity recommended practice (GEE)](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/burn-severity-earth-engine)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Results: recovery after the fire
:::

![[Pasted image 20230107004533.png]]<!-- element drag="100 100" drop="0 -10"-->
::: source
source: Petropoulos, G.P., Griffiths, H.M., Kalivas, D.P. (2014). [Quantifying spatial and temporal vegetation recovery dynamics following a wildfire event in a Mediterranean landscape using EO data and GIS](https://www.researchgate.net/publication/261183988_Quantifying_Spatial_and_Temporal_Vegetation_Recovery_Dynamics_Following_a_Wildfire_Event_in_a_Mediterranean_Landscape_using_EO_Data_and_GIS). *Applied Geography* 50, 120–131
:::

note:
A time series of NBR or NDVI over the burned perimeter for several years after the fire shows the recovery – with `ui.Chart.image.series` this is five lines of code and a very good figure for the report.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Validation and reference data
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
- **Field**: Composite Burn Index (CBI) plots – the standard against which dNBR thresholds were calibrated; you will not have them, say so
- **EFFIS** (Copernicus) – burned-area perimeters for Europe since 2003 (MODIS, ≥ 30 ha; Sentinel-2 since 2018), fire danger forecast, [forest-fire.emergency.copernicus.eu](https://forest-fire.emergency.copernicus.eu/) – your perimeter reference in Europe
- **Copernicus EMS** grading maps after activations (Greece 2023, Portugal 2025…)
- **MTBS** (USA) – Monitoring Trends in Burn Severity, dNBR maps for all large US fires since 1984 – a benchmark to test your script on a known fire
- **Global Fire Atlas / GFED** – fire size, spread, emissions, from MODIS burned area
- In Poland: Lasy Państwowe fire database (Instytut Badawczy Leśnictwa), the April 2020 Biebrza fire (~5 300 ha) is a good Sentinel-2 case
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## From maps to decisions
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:44px" align="left" drag="95 78" drop="0 15"-->
- **Burned Area Emergency Response**: soil burn severity → where erosion and debris flows will hit after the first rain (lecture 5 again)
- **Salvage logging and regeneration planning**: high severity = planting; low = natural regeneration
- **Carbon and emissions**: burned area × fuel load × combustion completeness
- **Insurance and legal**: a reproducible map with stated dates, thresholds and accuracy is evidence; a pretty picture is not
- **Fire danger**: EFFIS Fire Weather Index forecasts – prevention, not mapping

That is why every lab report in this course has: data, dates, method, thresholds, validation, limitations.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (21.12, 3 h)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. Your fire (from last week's homework): FIRMS hotspots → start/end dates; Copernicus Browser → cloud-free pre and post Sentinel-2 dates
2. Open the GEE script (Moodle *Fire detection…* lesson, page 4): set `geometry`, `prefire_start/end`, `postfire_start/end`; run
3. Inspect: NBR pre, NBR post, dNBR – Inspector over unburned forest, a field, the fire core
4. Severity classes with the USGS thresholds; area per class in hectares; a legend
5. Compare the perimeter with EFFIS (or EMS); where do they disagree and why (clouds? phenology? agricultural fields?)
6. Optional: NDVI time series chart over the perimeter for 2 years after the fire
7. Export the severity GeoTIFF; a short report with the checklist from slide 8
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before next class (after the break)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Submit the burn severity report
- [ ] Next lecture: Earth Engine from **Python and R**. Install nothing yet – we start in Google Colab (only a browser)
- [ ] Read the Moodle lesson *Application Programming Interfaces (API) for GEE*, page 1 (Colab basics) – 10 min
- [ ] If you use R: install R ≥ 4.3 and RStudio / Positron on your laptop; `install.packages("rgee")` is quick, but `ee_install()` downloads ~200 MB – do it at home, not on the university Wi-Fi during the lab
- [ ] Literature (optional): [How to generate wildfire boundary maps with Earth Engine](https://medium.com/google-earth/how-to-generate-wildfire-boundary-maps-with-earth-engine-b38eadc97a38); Al-hasn & Almuhammad (2022), [J. For. Sci. 68(3), 96–106](https://jfs.agriculturejournals.cz/pdfs/jfs/2022/03/02.pdf) – dNBR/BAIS2 burned area
:::

---
::: block 
# Thank you :smile:
:::
