---
summary: Proponowane nowe slajdy do ApplicationHazards_GEO.md (21.10.2026). Każdy blok między "---" to jeden slajd w stylu tpl-con-default-slide; wklej wybrane w odpowiednie miejsce prezentacji.
---

<!-- PROPOZYCJA 1: wstawić po slajdzie "Copernicus Browser" (14) -->
<!-- slide template="[[tpl-con-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F" rotate="-15"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: title 
## Where to get satellite data in 2026?
:::

::: block <!-- element style="font-size: 44px;" align="left" -->
| Tool | What is it | Cost | We use it in |
|---|---|---|---|
| [Copernicus Browser](https://browser.dataspace.copernicus.eu/) | GUI: browse, compare, timelapse, export Sentinel data | free (account) | lecture, homework |
| [CDSE APIs](https://documentation.dataspace.copernicus.eu/APIs.html) | [openEO](https://documentation.dataspace.copernicus.eu/APIs/openEO/openEO.html), [STAC](https://documentation.dataspace.copernicus.eu/APIs/STAC.html), S3, Sentinel Hub API | free quota | Jupyter |
| [Google Earth Engine](https://earthengine.google.com/) | cloud computing on a petabyte catalogue (JS, Python, R) | free for noncommercial use (Cloud project) | GEE editor, ML, rgee |
| [Planet Insights Platform](https://www.planet.com/products/planet-insights-platform/) | commercial successor of EO Browser / Sentinel Hub, PlanetScope 3 m | commercial (trial) | – |
:::

---
<!-- PROPOZYCJA 2: wstawić po slajdzie "Idea of remote sensing" (10) lub po "Compare Landsat and Sentinel bands" (12) -->
<!-- slide template="[[tpl-con-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 90" bg="#F06400" rotate="25"/>

::: title 
## Active sensors: Sentinel-1 SAR for floods and landslides
:::

::: block <!-- element style="font-size: 48px;" -->
- C-band **Synthetic Aperture Radar** – works through clouds and at night (floods usually come with clouds!)
+ Constellation: [Sentinel-1C](https://sentiwiki.copernicus.eu/web/s1-mission) (2024) and 1D (2025); 1A ends operations in June 2026; 6-day revisit in Europe
+ Water = smooth surface = low backscatter (dark) → simple thresholding of VV/VH gives a flood mask ([UN-SPIDER recommended practice](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping))
+ Ready product: [Global Flood Monitoring](https://global-flood.emergency.copernicus.eu/) (CEMS) – automatic flood maps from every Sentinel-1 scene
+ Landslides: change of backscatter / coherence (InSAR) before and after the event
:::

---
<!-- PROPOZYCJA 3: wstawić po slajdzie "Landslides, wildfires, and other hazards..." (3) lub przed "Home work" -->
<!-- slide template="[[tpl-con-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: title 
## Operational services – when somebody has already done the mapping
:::

::: block <!-- element style="font-size: 48px;" -->
- [Copernicus Emergency Management Service](https://emergency.copernicus.eu/) – [Rapid Mapping](https://rapidmapping.emergency.copernicus.eu/) activations: ready delineation and grading maps for recent disasters
+ [EFFIS](https://forest-fire.emergency.copernicus.eu/) – European Forest Fire Information System: fire danger forecast, burnt area, active fires
+ [GloFAS / EFAS](https://global-flood.emergency.copernicus.eu/) – flood forecasts and Global Flood Monitoring (Sentinel-1)
+ Copernicus Browser **Highlights** – curated examples of events (fires, floods, eruptions) ready to open and compare
+ Use them to **find a study case** and to **validate** your own classification
:::

---
<!-- PROPOZYCJA 4: dopisać na slajdzie 5 "How to choose data..." jako kolejny fragment (data-fragment-index="5") obok mapy -->
::: block <!-- element drag="55 30" drop="45 65" class="fragment fade-up" data-fragment-index="5" align="left" bg="coral" pad="10px" style="font-size: 40px;" -->
$$ dNBR = NBR_{prefire} - NBR_{postfire} $$
Burn severity (USGS, Key & Benson 2006): < 0.1 unburned · 0.1–0.27 low · 0.27–0.44 moderate-low · 0.44–0.66 moderate-high · > 0.66 high
[UN-SPIDER: NBR in detail](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail/normalized-burn-ratio)
:::
