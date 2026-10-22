---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 8
summary: "Wykład 8 (1 h, 11.01.2027) – podsumowanie: wspólny schemat metod, skąd biorą się błędy (jakość danych, progi, walidacja), serwisy operacyjne, co dalej (literatura, kursy), zaliczenie"
timeForPresentation: 2700
theme: beige
width: 1920
height: 1200
margin: 0
maxScale: 4
transition: zoom
course: Application of geoinformatics to natural hazards mapping and monitoring
---

<!-- slide data-background-image=![[sateliteGEEbanner.png|1920]] -->
<grid drag="60 34" drop="left" bg="#EEB73F" align="left" pad="250px 0  250px 300px">

### Lecture 8<!-- element style="letter-spacing: 1.5rem;"-->
## From pixels to hazard maps
#### wrap-up, uncertainty, what next

#### Marek Urbaniak

</grid>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Today (45 min)
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>

::: block <!-- element style="font-size: 44px" align="left" drag="80 80" drop="0 15"-->
1. One workflow, three hazards – what you actually learned
2. Where the errors come from: data quality, dates, thresholds, validation
3. How to write the limitations section (and why reviewers read it first)
4. Operational services: the same methods, every day, by someone else
5. Assessment and deadlines
6. Where to go next: courses, books, data
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## One workflow, three hazards
:::

::: block <!-- element style="font-size:24px" align="left" drag="95 80" drop="0 15"-->
| Step | Flood (lab 4) | Landslide (lab 5) | Wildfire (lab 6) |
|---|---|---|---|
| sensor | Sentinel-1 VH (+ S2 MNDWI) | Sentinel-1 VH (+ S2 NDVI) | Sentinel-2 B8/B12 (+ FIRMS) |
| before | 2–4 weeks, same orbit | months, same orbit | 2–4 weeks, same season |
| after | days after peak | weeks after event | 1–4 weeks after containment |
| quantity | backscatter dB | log-ratio of mean backscatter | NBR |
| difference | after − before | pre − post (log-ratio of medians) | pre − post (dNBR) |
| threshold | −3 dB / ratio 1.25 / Otsu | change > t, then density grid | USGS classes (100, 270, 440, 660) |
| masks | permanent water, slope < 5°, specks | slope 5–10°, curvature, water | clouds (SCL), perimeter |
| output | extent, ha, exposed people | density heatmap | severity classes, ha per class |
| reference | GFM, EMS, gauges | EMS grading, inventories | EFFIS, MTBS, CBI |

Plus lab 2 (indices, areas), lab 3 (classification, accuracy) and lab 7 (the same in Python/R). You can now build a before/after change product for **any** hazard with an event date.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Where the errors come from
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:22px" align="left" drag="50 78" drop="0 15"-->
**1. Input data quality**
- clouds, shadows, haze not masked; cirrus in "clear" scenes
- geometric misregistration between dates (a 1-pixel shift creates a fake change along every edge)
- radiometric: different processing baselines, TOA vs BOA mixed
- SAR: speckle, different orbits/incidence angles, wind on water
- QA flags and quality bands exist for a reason – read them (lab 7)
:::

::: block <!-- element style="font-size:22px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
**2. Method choices**
- dates (phenology, snow, harvest) – the number one source of false change
- thresholds transferred from another biome
- spatial resolution vs object size (20 m SWIR, small landslides)
- composite method (median vs. single scene)

**3. Validation**
- no reference data = no accuracy, only a picture
- reference from the same sensor is not independent
- accuracy varies by class and by region – report per class

Two papers on quality assessment in Moodle (section *Flood mapping*): Crespi & De Vendictis 2009, Sensors 9, 3289–3313 (high-resolution imagery QA); Tecuapetla-Gómez et al. 2021, ISPRS IJGI 10, 267 (TATSSI – quality flags of EO products).
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Uncertainty you can quantify in one afternoon
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
1. **Threshold sensitivity**: run the map with the threshold ± 20 % → range of area (ha). Report *"flooded area 4 210 ha (3 650–4 820 for ratio 1.15–1.40)"*, not a single number
2. **Date sensitivity**: a second pre-event composite (different weeks) → how much of the "change" moves
3. **Confusion matrix** against any independent reference (EMS, EFFIS, field, VHR image): overall accuracy, per-class, kappa (lecture 3)
4. **Area-adjusted accuracy** (Olofsson et al. 2014) – if you go on to a thesis: stratified sampling, confidence intervals on the area
5. **Visual check** of 20 random pixels per class in Copernicus Browser – cheap, honest, always possible

The report sentence that makes you credible: *"The method detects X with Y % accuracy against Z; it fails in … because …"*
:::

::: source
source: Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## The same methods, every day, by someone else
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:25px" align="left" drag="95 78" drop="0 15"-->
| Service | Hazard | Method inside | You used it as |
|---|---|---|---|
| [Copernicus EMS Rapid Mapping](https://mapping.emergency.copernicus.eu/activations/) | all | VHR optical + SAR, analysts | reference maps |
| [Global Flood Monitoring](https://global-flood.emergency.copernicus.eu/) | floods | Sentinel-1, Otsu + ensemble | lab 4 reference |
| [GloFAS / EFAS](https://global-flood.emergency.copernicus.eu/glofas-forecasting/) | floods | hydrological forecast | context |
| [EFFIS](https://forest-fire.emergency.copernicus.eu/) | fires | MODIS/S2 burned area, FWI | lab 6 reference |
| [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) | fires | VIIRS/MODIS active fire | lab 6 timeline |
| [NASA LHASA](https://gpm.nasa.gov/landslides/) | landslides | rainfall + susceptibility nowcast | context |
| [EGMS](https://egms.land.copernicus.eu/) | slow motion | InSAR time series | context |
| [Copernicus Browser Highlights](https://browser.dataspace.copernicus.eu/) | all | curated events | lab 1 |

Know them, cite them, compare against them – and know that the method you ran in the lab is what runs inside.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## What is coming (2026–2030)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
- **Sentinel-1C/1D** have restored the 6-day repeat (June 2026; 1A retired); **NISAR** (NASA/ISRO, L-band, 2025, data public since July 2026) – free L-band SAR every 12 days, better under vegetation
- **Sentinel-2C** (+ 2D in 2028) and the expansion missions: LSTM thermal 2028, ROSE-L L-band SAR 2028/29, CHIME hyperspectral 2029
- **Landsat 10** (ex-Landsat Next: one satellite, 26 bands, 10–20 m, launch 2031)
- **Earth Engine**: noncommercial tiers, Cloud Score+, more AI-ready embeddings (`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`) – a 64-band "fingerprint" per pixel you can classify with RF directly
- **Foundation models** (Prithvi, Clay, SatMAE) – pretrained on millions of scenes, fine-tuned for floods/fires with a few hundred labels
- **Copernicus Data Space**: openEO and STAC APIs – the open alternative to GEE for reproducible science
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Assessment
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:44px" align="left" drag="95 78" drop="0 15"-->
- Lab deliverables M1–M6: submitted in Moodle (assignments and lessons), always with the script link
- Capstone notebook M7 (lab 7): one hazard reproduced in Python or R, with text, figures, parameters, limitations
- Lesson quizzes (GEE, API)
- Grading weights, deadlines and attendance rules: **Course regulations and syllabus** – the resource at the top of the Moodle course
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Where to go next
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:32px" align="left" drag="48 80" drop="0 15"-->
**Courses (free)**
- [End-to-End Google Earth Engine](https://courses.spatialthoughts.com/end-to-end-gee.html) – Spatial Thoughts; now you can follow it
- [NASA ARSET trainings](https://www.earthdata.nasa.gov/learn/trainings) – fundamentals, SAR, floods, fires (recorded webinars)
- [Earth Engine tutorials](https://developers.google.com/earth-engine/tutorials/ttt), [geemap tutorials](https://geemap.org/tutorials/)
- [UN-SPIDER recommended practices](https://un-spider.org/advisory-support/recommended-practices) – all hazards, step by step
- [Copernicus Data Space videos](https://www.youtube.com/@copernicusdataspaceecosystem)
:::

::: block <!-- element style="font-size:29px" align="left" drag="48 80" drop="52 15" bg="#e8f4f8" pad="15px"-->
**Books**
- Cardille, Crowley, Saah, Clinton (eds.) 2024, *[Cloud-Based Remote Sensing with Google Earth Engine](https://www.eefabook.org/)* – free, every chapter is a GEE script
- Lovelace, Nowosad, Muenchow, *[Geocomputation with R](https://r.geocompx.org/)*; Pebesma & Bivand, *[Spatial Data Science](https://r-spatial.org/book/)*
- Wickham & Grolemund, *[R for Data Science](https://r4ds.hadley.nz/)*; Wickham, *[Advanced R](https://adv-r.hadley.nz/)*
- Wimberly, *[Geographic Data Science with R](https://bookdown.org/mcwimberly/gdswr-book/)*
- Hengl & MacMillan, *[Predictive Soil Mapping with R](https://soilmapper.org/)*
- *[rgee documentation](https://r-spatial.github.io/rgee/)*

**Papers you read in this course**
- Handwerger et al. 2022, NHESS (landslides, SAR)
- Notti et al. 2018, Remote Sensing (floods, open data)
- Key & Benson 2006 (NBR); Olofsson et al. 2014 (accuracy)
:::

---
::: block 
# Thank you :smile:
:::

### … and good luck with the capstone notebooks
