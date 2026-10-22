---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - SAR
  - flood
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 4
summary: "Wykład 4 (2 h, 30.11.2026) – mapowanie powodzi: wskaźniki wodne (NDWI, MNDWI, AWEI), podstawy SAR (Sentinel-1, polaryzacja, backscatter, odbicie lustrzane), progowanie i detekcja zmian, InSAR, serwisy operacyjne; wstęp do ćwiczeń 4 (skrypt UN-SPIDER)"
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

### Lecture 4<!-- element style="letter-spacing: 1.5rem;"-->
## Flood mapping
#### optical water indices and Sentinel-1 radar

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
1. Why floods are the hardest case for optical satellites
2. Water in the optical bands: NDWI, MNDWI, AWEI – and their limits
3. SAR in 15 minutes: wavelength, polarisation, backscatter, why water is dark
4. Sentinel-1: the constellation, products, what `COPERNICUS/S1_GRD` contains
5. Flood extent from SAR: thresholding, Otsu, change detection, masks (slope, permanent water)
6. InSAR and DEMs (one slide), ICEYE and commercial constellations
7. Operational services: Copernicus EMS, GloFAS, Global Flood Monitoring
8. **In the lab**: the UN-SPIDER flood script, step by step
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Floods: the observation problem
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:44px" align="left" drag="52 75" drop="0 15"-->
- Hydrological hazard: river (fluvial), flash / surface (pluvial), coastal, dam failure
- The flood peak lasts hours to days – it falls **between** two Sentinel-2 passes (5 days) and **under the clouds** that caused it
- What managers need within 24 h: **extent** (where is water), later **depth**, **duration**, **damage**
- Poland 2024 (September, Odra / Nysa Kłodzka): Copernicus EMS activation [EMSR756 "Flood in South West Poland"](https://mapping.emergency.copernicus.eu/activations/EMSR756) – mostly Sentinel-1 and commercial SAR
:::

::: block <!-- element style="font-size:40px" align="left" drag="45 75" drop="55 15" bg="#e8f4f8" pad="15px"-->
Two sensor families, two labs in one:
1. **optical** (Sentinel-2, Landsat) – water indices; works when the sky is clear, good for *after* the event and for permanent water
2. **radar** (Sentinel-1) – backscatter; works through clouds, day and night → the standard for the flood peak

Same recipe as always: before / after / difference / threshold / area.
:::

::: source
source: [Notti et al. (2018), Potential and limitations of open satellite data for flood mapping, Remote Sensing 10, 1673](https://www.mdpi.com/2072-4292/10/11/1673)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Water in the optical bands
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:25px" align="left" drag="50 78" drop="0 15"-->
Water **absorbs** NIR and SWIR almost completely and reflects a little green/blue. Vegetation and soil reflect NIR and SWIR strongly. Hence:

$$ NDWI = \frac{Green - NIR}{Green + NIR} = \frac{B3 - B8}{B3 + B8} $$ (McFeeters 1996)

$$ MNDWI = \frac{Green - SWIR}{Green + SWIR} = \frac{B3 - B11}{B3 + B11} $$ (Xu 2006)

- water → positive values; land → negative
- NDWI confuses water with **built-up** areas (both low NIR); MNDWI separates them because buildings reflect SWIR, water does not
- typical threshold: MNDWI > 0 (adjust with the Inspector and a histogram)
:::

::: block <!-- element style="font-size:22px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
| Index | Bands (S2) | Good at | Weak at |
|---|---|---|---|
| NDWI | B3, B8 | open water, 10 m | built-up, shadows |
| MNDWI | B3, B11 | water vs. urban | 20 m (SWIR) |
| AWEI_nsh / AWEI_sh | B3, B8, B11, B12 (+ B2 for AWEI_sh) | shadow, dark surfaces | needs scaling 0–1 |
| NDVI < 0 | B4, B8 | quick check | turbid water |
| Scene classification `SCL` = 6 | – | ready water mask | coarse, clouds |

Turbid flood water (sediment!) reflects more red/NIR than a clear lake – thresholds move. Always look at the histogram of the index over your AOI.
:::

::: source
source: Moodle lesson *Learning objectives of this topic* (Flood mapping), pages 3–4; [Awesome spectral indices – water](https://github.com/awesome-spectral-indices/awesome-spectral-indices)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Radar in 15 minutes: active sensing
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:22px" align="left" drag="50 78" drop="0 15"-->
- **SAR** = Synthetic Aperture Radar: the satellite emits microwave pulses sideways and records the echo (*backscatter*, σ⁰, in dB)
- **Wavelength**: X-band ~3 cm (TerraSAR-X, ICEYE), **C-band ~5.6 cm (Sentinel-1)**, L-band ~24 cm (ALOS-2, NISAR). Longer wave → penetrates deeper into vegetation/soil, insensitive to rain
- **Polarisation**: transmit/receive vertical or horizontal. Sentinel-1 over land: **VV** and **VH**. VH is sensitive to volume scattering (vegetation), VV to surface roughness
- Clouds, smoke, night: **no effect** on C-band
- Side-looking geometry → shadow and layover in mountains; speckle (salt-and-pepper noise) → always filter
:::

::: block <!-- element style="font-size:22px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
What the echo tells us:

| Surface | Mechanism | Backscatter |
|---|---|---|
| calm water | **specular** – pulse bounces away from the antenna | very low (dark, < −18 dB) |
| bare soil, grass | surface scattering, roughness | medium |
| forest, crops | volume scattering | medium–high (esp. VH) |
| buildings | double-bounce (wall + ground) | very high (bright) |
| **flooded forest / city** | double-bounce water + trunk/wall | **brighter** than before! |
| wind-roughened water | surface scattering | brighter – false "land" |

<!-- TODO image: sketch of specular reflection on water vs diffuse on rough surface vs double bounce (Excalidraw, 3 panels). -->
:::

::: source
source: [NASA EarthData – What is SAR?](https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Sentinel-1: the workhorse for floods
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:34px" align="left" drag="50 78" drop="0 15"-->
- Copernicus C-band SAR mission; **1A** (2014, end of operations June 2026), 1B lost in 2021, **1C** (launched Dec 2024), **1D** (launched Nov 2025) → 6-day repeat over Europe again
- Main mode over land: **IW** (Interferometric Wide), 250 km swath, 10 m **GRD** pixel spacing (≈ 20 m resolution, amplitude only); the GEE collection is calibrated and terrain-corrected (σ⁰ in dB), the raw ESA GRD is not
- Ascending (evening) and descending (morning) orbits – do not mix them in change detection
- Free, open, in Copernicus Browser and in Earth Engine: `COPERNICUS/S1_GRD`, bands `VV`, `VH`, `angle`, values already in dB
:::

::: block <!-- element style="font-size:34px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filterBounds(roi)
  .select('VH');

var before = s1.filterDate('2024-08-20', '2024-09-10').mosaic();
var after  = s1.filterDate('2024-09-15', '2024-09-25').mosaic();

// speckle filter: 50 m focal mean (circle)
var smooth = 50;
var beforeF = before.focal_mean(smooth, 'circle', 'meters');
var afterF  = after.focal_mean(smooth, 'circle', 'meters');
Map.addLayer(beforeF, {min: -25, max: 0}, 'before VH');
Map.addLayer(afterF,  {min: -25, max: 0}, 'after VH');
```
Choose VH for floods in open land (bigger contrast land/water); VV for flooded vegetation (double bounce).
:::

::: source
source: [Sentinel-1 GRD in Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD); [ESA Sentinel-1 mission](https://sentiwiki.copernicus.eu/web/s1-mission)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## From backscatter to flood extent
:::

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
![[diagram_L04_sar_flood.svg]]
:::

::: block <!-- element style="font-size:36px" align="left" drag="95 14" drop="0 86" bg="#fff3cd" pad="10px 20px"-->
Two strategies: (a) **single image** – everything darker than a threshold is water (needs a good threshold, fails for permanent water and shadows); (b) **change detection** – only pixels that *became* dark are flood (the UN-SPIDER script). (b) is more robust and is the one you will run.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Choosing the threshold
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:30px" align="left" drag="50 78" drop="0 15"-->
- Backscatter histogram over a flooded area is **bimodal**: a water peak around −22 dB and a land peak around −12 dB
- **Manual**: read values with the Inspector over known water and land, pick the valley (e.g. −18 dB)
- **Ratio / difference**: the UN-SPIDER script divides the **dB images**, `after.divide(before)`, and flags ratio > **1.25** – the after value is ≥ 25 % more negative (≈ 3 dB darker around −12 dB); a ratio of dB values is not a physical ratio, so the cleaner equivalent is the difference in dB: `after.subtract(before).lt(-3)`
- **Otsu**: automatic threshold that maximises the separation of two classes in the histogram – objective, reproducible, used by the Global Flood Monitoring service
- Report which one you used and why – it is the main uncertainty of the map
:::

::: block <!-- element style="font-size:26px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
// difference in dB and the UN-SPIDER style ratio
var diff = afterF.subtract(beforeF);          // dB
var flooded = diff.lt(-3);                    // became ≥ 3 dB darker
// UN-SPIDER style (ratio of dB images):
// var ratio = afterF.divide(beforeF); var flooded = ratio.gt(1.25);

// masks
var jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality');
var permanent = jrc.gte(10);                   // water ≥ 10 months/yr
var dem = ee.Image('WWF/HydroSHEDS/03VFDEM');
var slope = ee.Terrain.slope(dem);
flooded = flooded.updateMask(permanent.not())
                 .updateMask(slope.lt(5))
                 .updateMask(flooded.connectedPixelCount(25).gte(8)); // specks, as UN-SPIDER

var area_ha = flooded.multiply(ee.Image.pixelArea()).divide(1e4)
  .reduceRegion({reducer: ee.Reducer.sum(), geometry: roi, scale: 10, maxPixels: 1e10});
print('flooded area [ha]', area_ha);
```
:::

::: source
source: [UN-SPIDER – Recommended practice: flood mapping with Sentinel-1 in GEE](https://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping); Otsu (1979) IEEE Trans. SMC 9, 62–66
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Where SAR flood maps go wrong
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
| Looks like water but is not | Is water but looks like land |
|---|---|
| radar **shadow** behind mountains → slope mask | **wind** roughens the surface → compare with a calm date |
| smooth surfaces: airport runways, motorways, dry sand, salt flats | **flooded vegetation / forest** – double bounce makes it *brighter* → look for an increase in VV |
| wet snow, very wet soil | **urban flooding** – layover and double bounce dominate → optical or very high-resolution SAR |
| permanent lakes and rivers → JRC mask | shallow water with emergent plants |

Validation: Copernicus Browser true-colour of the first clear day after the event, EMS Rapid Mapping products, news photos with coordinates, gauge data (IMGW). Your report must say **what you compared against**.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## InSAR and DEMs (the other half of radar)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:34px" align="left" drag="52 75" drop="0 15"-->
- Amplitude (what we used) tells *how much* echo; **phase** tells *how far*
- **InSAR** = interferometry of two SAR images → ground elevation (SRTM 2000, TanDEM-X / Copernicus DEM 30 m) or millimetre **displacement** between dates (subsidence, landslides – lecture 5, earthquakes, dams)
- For floods a DEM gives: slope masks, flow accumulation, **flood depth** (water surface minus terrain), HAND (height above nearest drainage) for exposure
- In GEE: `COPERNICUS/DEM/GLO30_2024_1` (an ImageCollection – `.select('DEM').mosaic()`), `NASA/NASADEM_HGT/001`, `MERIT/Hydro/v1_0_1` (HAND)
:::

::: block <!-- element style="font-size:32px" align="left" drag="43 78" drop="55 15" bg="#e8f4f8" pad="15px"-->
**Commercial high-resolution SAR**
- **ICEYE** (Finland, large office in Warsaw): more than 70 small X-band satellites launched by 2026, 25 cm–1 m, revisit of hours; sells flood depth and extent products to insurers and governments; used in Polish 2024 flood response
- Capella, Umbra (USA), TerraSAR-X / PAZ (DE/ES), COSMO-SkyMed (IT)
- Free for research under proposals; in emergencies through the **International Charter Space and Major Disasters**
:::

::: source
source: [ICEYE flood insights](https://www.iceye.com/solutions/government/flood-insights)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Operational services: who does this every day
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:22px" align="left" drag="95 78" drop="0 15"-->
| Service | What | Latency | Link |
|---|---|---|---|
| **Copernicus EMS Rapid Mapping** | flood/fire/landslide delineation and grading maps on activation by a national authority | hours–days | [mapping.emergency.copernicus.eu/activations](https://mapping.emergency.copernicus.eu/activations) |
| **Global Flood Monitoring (GFM)** | automatic Sentinel-1 flood extent for the whole world, every S1 scene, three independent classifiers (DLR, LIST, TU Wien) combined by majority vote | ~8 h | [global-flood.emergency.copernicus.eu](https://global-flood.emergency.copernicus.eu/) |
| **GloFAS / EFAS** | hydrological *forecasts* of river floods (30 days / 10 days) | daily | [global-flood.emergency.copernicus.eu/glofas-forecasting](https://global-flood.emergency.copernicus.eu/glofas-forecasting/) |
| **International Charter** | free satellite tasking (all agencies) for major disasters | hours | [disasterscharter.org](https://disasterscharter.org/) |
| **JRC Global Surface Water** | 1984–2021 Landsat water occurrence, seasonality | archive | `JRC/GSW1_4/GlobalSurfaceWater` |

Use them as **reference data** for your own map in the report – and know that the lab script (before/after ratio) is a simplified cousin of the change-detection methods inside GFM, not the same method.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (7.12, 3 h)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. Copernicus Browser: find a flood in *Highlights* (or Poland, Sept 2024); compare Sentinel-2 and Sentinel-1 of the same days – see what clouds do
2. Optical: MNDWI before/after on Sentinel-2, histogram, threshold, water area (20 min; reuse lecture 2 code)
3. SAR: open the **updated UN-SPIDER script** (Moodle, lesson page 7, link 2): set AOI, before/after dates, orbit; run; read the flooded area and the exposed population / cropland
4. Change the threshold (1.25 → 1.15 → 1.4) and the speckle filter – write down how the area changes: this is your uncertainty
5. Compare with the GFM product or an EMS map for the same event; one paragraph of agreement/disagreement
6. Reference: S2 (no SAR) example script (Moodle, link 1)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before next class
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Finish the flood exercise (script link + flooded area + threshold sensitivity table)
- [ ] Read the **must-read** paper for next week: Handwerger et al. (2022), [NHESS 22, 753](https://nhess.copernicus.org/articles/22/753/2022/nhess-22-753-2022.pdf) – sections 1, 2 and 3.1 (what the SAR change method does); skip the equations on first read
- [ ] Look at the landslide types figure in Moodle (*Landslides* lesson, page 1)
- [ ] Optional: [ARSET – Introduction to SAR](https://appliedsciences.nasa.gov/get-involved/training/english/arset-introduction-synthetic-aperture-radar) (NASA, free, recorded)
:::

---
::: block 
# Thank you :smile:
:::
