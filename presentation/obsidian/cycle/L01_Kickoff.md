---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - Copernicus
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 1
summary: "Wykład 1 (1 h, 9.11.2026) – zagrożenia naturalne wg UN, schemat before/after, jak działają satelity EO, skąd brać dane w 2026, Copernicus Browser; wstęp do ćwiczeń 1 (konto CDSE, rejestracja GEE)"
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
<grid drag="64 58" drop="0 27" bg="#EEB73F" align="left" pad="60px 60px 60px 300px">

### Lecture 1<!-- element style="letter-spacing: 1.5rem;"-->
## Natural hazards and Earth observation
#### course kick-off

#### Marek Urbaniak

</grid>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Today (45 min) and the road ahead
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="92 95" bg="#F06400" />

::: block <!-- element style="font-size: 44px" align="left" drag="80 80" drop="0 15"-->
1. Which natural hazards and why satellites?
2. One method for all of them: **before / after**
3. How EO satellites see the ground (passive, active, resolution, bands)
4. Where to get data in 2026 (and what disappeared)
5. **In the lab next week**: Copernicus Browser + your Google Earth Engine account
:::

::: block <!-- element style="font-size: 36px" drag="80 20" drop="0 85" bg="#fff3cd" pad="10px 20px"-->
Lecture plan: L1 kick-off → L2 GEE Code Editor → L3 machine learning → L4 floods → L5 landslides → L6 wildfires → L7 Python/R APIs → L8 wrap-up. Each lecture prepares the following lab.
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
# Natural Hazards following UN
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="92 95" bg="#F06400" />
::: block <!-- element class="fragment fade-out" data-fragment-index="1" drag="100 100" drop="0 0" align="left"-->
### Biological
![[Pasted image 20230109111013.png]]
:::
::: block <!-- element class="fragment fade-in-then-out" data-fragment-index="1" drag="100 100" drop="0 0" align="left"-->
### Climatological
![[Pasted image 20230109111126.png]]
:::
::: block<!-- element class="fragment fade-in-then-out" data-fragment-index="2" drag="100 100" drop="0 0" align="left"-->
### Extraterrestrial
![[Pasted image 20230109111154.png]]
:::
::: block<!-- element class="fragment fade-in-then-out" data-fragment-index="3" drag="100 100" drop="0 0" align="left"-->
### Geophysical
![[Pasted image 20230109111224.png]]
:::
::: block<!-- element class="fragment fade-in-then-out" data-fragment-index="4" drag="100 100" drop="0 0" align="left"-->
### Hydrological
![[Pasted image 20230109111301.png]]
:::
::: block<!-- element class="fragment fade-in-then-out" data-fragment-index="5" drag="100 100" drop="0 0" align="left"-->
### Meteorological
![[Pasted image 20230109111336.png]]
:::
::: source
source: [https://www.un-spider.org](https://www.un-spider.org/risks-and-disasters/natural-hazards#no-back)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## We will focus on three of them
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: block <!-- element style="font-size:46px" align="left" drag="60 60" drop="0 15"-->
- **Floods** (hydrological) – lecture 4, lab 4
+ **Landslides** / mass movement (geophysical, hydrological trigger) – lecture 5, lab 5
+ **Wildfires** (climatological) – lecture 6, lab 6
+ and tools that work for all of them: Copernicus Browser, Google Earth Engine, machine learning, Python and R
:::

::: block <!-- element style="font-size:40px" align="left" drag="35 72" drop="63 15" bg="#e8f4f8" pad="15px"-->
**Why satellites?**
- the event area is large or inaccessible
- we need the state **before** the event, and nobody measured it on the ground
- repeat observations every few days, for free
- consistent method for the whole region
:::

::: source
source: [UN-SPIDER recommended practices](https://un-spider.org/advisory-support/recommended-practices)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## One method for all hazards: before / after
:::

::: block <!-- element style="font-size:34px" align="left" drag="49 70" drop="0 15"-->
+ Step 1 – select satellite images for the period<br>**before** the event
+ Step 2 – select images for the period **after** the event
+ Step 3 – compute the same quantity for both (an index, backscatter, a class)
+ Step 4 – **difference** = change caused by the event
+ Step 5 – threshold / classify the difference, compute the area, make a map
:::

![[S2L2A-1348973218860829-timelapse.gif]]<!-- element  drag="50 80" drop="50 10" class="fragment fade-out" data-fragment-index="1"-->
![[S2L2A-1015625487634027-timelapse.gif]]<!-- element  drag="50 80" drop="50 10" class="fragment fade-in-then-out" data-fragment-index="1"-->

::: block <!-- element style="font-size:36px" drag="100 12" drop="0 88" bg="#fff3cd" pad="10px 20px"-->
Labs 4, 5 and 6 are three variants of exactly this recipe. Learn it once.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Example: burn severity from pre- and post-fire images
:::

### An example - Indicating burn severity
![[Pasted image 20230106230924.png|900]]<!-- element  class="fragment fade-in-then-out" data-fragment-index="2"-->

::: block <!-- element  drag="55 25" drop="45 0" class="fragment fade-in-then-out" data-fragment-index="3" align="left" bg="coral" pad="10px"  -->
Bands and satellite products for indicating burned area:
$$ NBR = \frac{NIR - SWIR}{NIR + SWIR} $$
:::

![[Pasted image 20230106232307.png]]<!-- element drag="100 100" drop="0 10" class="fragment fade-in-then-out" data-fragment-index="4"-->
::: source
source: Dimitris Karakostis, [Remote Sensing in support of impact evaluation by wildfires](https://www.geo.fu-berlin.de/en/v/geo-it/webinar/webinar-1)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## How EO satellites work: passive and active
:::

::: block <!-- element style="font-size: 44px;" -->
EO satellites can be divided into two types based on how they capture imagery: **passive** and **active**.
:::

<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" rotate="35"/>
::: block <!-- element bg="#bc8f8f" pad="3px 20px 3px 20px" -->
![[ezmaker.png]]
:::
::: source
source: satellites4everyone.co.uk (site offline – [archived copy](https://web.archive.org/web/2023/http://satellites4everyone.co.uk/?page_id=4402))
:::

note:
PASSIVE: detect sunlight reflected (visible, NIR, SWIR) or heat emitted (TIR) by the surface. Cannot see through clouds. Examples: Sentinel-2, Landsat 8/9, MODIS, VIIRS.
ACTIVE: transmit microwaves and measure the echo (SAR). Work day and night and through clouds. Examples: Sentinel-1, ICEYE, TerraSAR-X.
Floods and landslides happen in bad weather – that is why lab 4 and 5 use SAR.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Four resolutions you must always check
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:30px" align="left" drag="55 78" drop="0 15"-->
| Resolution | Question | Sentinel-2 | Landsat 8/9 | Sentinel-1 | MODIS |
|---|---|---|---|---|---|
| **spatial** | how big is a pixel? | 10 / 20 / 60 m | 30 m (15 m pan) | 10 m (GRD) | 250–1000 m |
| **temporal** | how often does it come back? | 5 days (2B+2C in opposite phase; 2A on an extended campaign to end 2026) | 8 days (8+9) | 6–12 days | daily |
| **spectral** | which bands? | 13 | 11 | C-band radar | 36 |
| **radiometric** | how fine are the values? | 12 bit | 12 / 14 bit | 16 bit | 12 bit |
:::

::: block <!-- element style="font-size:32px" align="left" drag="40 75" drop="60 15" bg="#e8f4f8" pad="15px"-->
Rule of thumb for hazards:
- small event (a landslide, 1 ha) → spatial resolution first
- fast event (a flood peak, 2 days) → temporal resolution first
- what you want to *see* (water, burned vegetation) → spectral resolution first
- a cloudy season → radar
:::


---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Compare Landsat and Sentinel bands
:::

![[Pasted image 20230106213729.png|1050]]

::: block <!-- element style="font-size: 28px;" class="fragment fade-up" -->
Landsat 8 and **Landsat 9** (2021) carry the same bands (OLI-2 / TIRS-2); Landsat 7 was decommissioned in June 2025. Sentinel-2 now flies as a triplet: **2A, 2B and 2C** (2C operational since January 2025; 2A on an extended campaign until the end of 2026). Band names in Earth Engine: Sentinel-2 `B4` = red, `B8` = NIR, `B11/B12` = SWIR; Landsat 8/9 `SR_B4` = red, `SR_B5` = NIR, `SR_B6/SR_B7` = SWIR. Write them down – every index in this course uses them.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Where to get satellite data in 2026?
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:26px" align="left" drag="95 70" drop="0 15"-->
| Tool | What it is | Cost | Data | Used in this course |
|---|---|---|---|---|
| [Copernicus Browser](https://browser.dataspace.copernicus.eu/) | web viewer of the Copernicus Data Space Ecosystem (CDSE) | free account | Sentinel-1/2/3/5P, DEM, mosaics | lab 1 – find the event, pick dates |
| [CDSE APIs](https://dataspace.copernicus.eu/analyse/apis) + [JupyterLab](https://dataspace.copernicus.eu/analyse/jupyterlab) | openEO, STAC, Sentinel Hub API, S3 download; free hosted notebooks (on request) | free quota | the same | optional (lesson 7, for the curious) |
| [Google Earth Engine](https://earthengine.google.com/) | cloud computing on a petabyte catalogue | free for [noncommercial use](https://earthengine.google.com/noncommercial/), needs a Google Cloud project | Sentinel, Landsat, MODIS, DEMs, climate… | labs 2–7 |
| [Planet Insights Platform](https://www.planet.com/products/planet-insights-platform/) | commercial successor of EO Browser / Sentinel Hub | paid (trial) | Sentinel + PlanetScope 3 m | no |
| [USGS EarthExplorer](https://earthexplorer.usgs.gov/) | Landsat archive download | free account | Landsat 1–9 | no |
:::

::: block <!-- element style="font-size:23px" drag="95 14" drop="0 86" bg="#fff3cd" pad="10px 20px"-->
**EO Browser** (used in the previous editions of this course) was retired in March 2026. Everything you find in older tutorials about EO Browser works almost identically in Copernicus Browser.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F" rotate="-15"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />
![[Pasted image 20251102204319.png]]
::: title 
## Copernicus Browser
:::

::: block <!-- element style="font-size: 44px;"  -->
- Part of the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (EU / ESA); a free account is required
+ Browse and compare full-resolution images (Sentinel-1, Sentinel-2 + mosaics, Sentinel-3, Sentinel-5P, DEM)
+ Tools: compare, timelapse, time series and histograms, import AOI (KML/GeoJSON), export GeoTIFF, 3D view, custom scripts e.g. [NDVI](https://custom-scripts.sentinel-hub.com/sentinel-2/ndvi/), [NBR](https://custom-scripts.sentinel-hub.com/sentinel-2/nbr/)
+ **Highlights** – ready-made examples of real events (fires, floods, eruptions) – a good place to find your study case
+ Import layers into QGIS / ArcGIS via WMS/WMTS
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
# How to find a study example?
:::
<grid drag="13 26" drop="0 -80" bg="#ffB73F" rotate="-15"/>
<grid drag="10 36" drop="-95 -55" bg="#00ced1"/>
<grid drag="4 66" drop="3 -5" bg="#F06400" />
<grid drag="30 70" drop="right" bg="#0EB73F"/>

![[Pasted image 20251102204241.png]]<!-- element drag="80 100" drop= "center"-->

note:
Show live: Copernicus Browser → Highlights → pick a wildfire → note the date and the AOI; then Visualize → compare mode → split before/after.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Custom scripts: indices without programming
:::
<grid drag="60 6" drop="0 0" border="medium dashed red" pad="3px"/>
<grid drag="30 70" drop="right" bg="#0EB73F"/>

::: block <!-- element  drag="70 100" drop="center" align="left" -->
https://custom-scripts.sentinel-hub.com/
![[Pasted image 20230109181444.png|700]]
:::

note:
A custom script is a few lines of JavaScript that tells the browser how to combine bands into colours. The same idea (band maths) returns in Earth Engine next week – there you will write it yourself.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## In the lab next week (3 h)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
1. **Copernicus Browser** – log in, find one wildfire and one flood in Highlights, open compare mode, read the acquisition dates and cloud cover
2. Apply a custom script (NDVI, NBR, false colour) and export a GeoTIFF of your AOI
3. Make a timelapse of your event (will be useful for your reports)
4. **Google Earth Engine** – open the [Code Editor](https://code.earthengine.google.com/), check that your Cloud project is registered, run the first script: load Sentinel-2, centre the map on Poznań
5. Add the [End-to-End GEE](https://courses.spatialthoughts.com/end-to-end-gee.html) repository to your Scripts panel (we will use it as a cookbook, not as homework)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Before next class – do it now, it takes time
:::

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Create a free account at [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) and log in to [Copernicus Browser](https://browser.dataspace.copernicus.eu/)
- [ ] Register for Google Earth Engine with your Google account: [how to get access](https://developers.google.com/earth-engine/guides/access) → create a Cloud project → register it for **noncommercial (education)** use. Access is enabled immediately, but the Cloud project, the Earth Engine API and the eligibility questionnaire take 20–30 min and sometimes fail – **do it a few days before the lab**
- [ ] Watch: [A short guide to Copernicus Browser](https://www.youtube.com/watch?v=F0lIn5r6ZWk) (10 min) and, optionally, [Introduction to CDSE](https://www.youtube.com/watch?v=GecNCdilbig)
- [ ] Bring to the lab: one hazard event you are curious about (place + approximate date)
- [ ] Optional, for the curious: while logged in at CDSE, request access to the free [JupyterLab](https://dataspace.copernicus.eu/analyse/jupyterlab) (approved in ~2 working days) – used only on an optional page of lesson 7
:::

::: block <!-- element style="font-size:34px" drag="95 12" drop="0 88" bg="#fff3cd" pad="10px 20px"-->
Problems with registration? Write on the course forum a few days before the lab – not on the morning of the lab.
:::

---
::: block 
# Thank you :smile:
:::
