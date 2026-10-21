---
date_create: 2026-10-22
tags:
  - Geo
  - GEE
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 0
summary: "Propozycja (22.10.2026): krótka prezentacja „About the course” zastępująca intro, które dublowało wykład 1 – organizacja, harmonogram, kamienie milowe, zaliczenie, narzędzia, literatura (8 slajdów)"
timeForPresentation: 900
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

### About the course<!-- element style="letter-spacing: 1.5rem;"-->
## Application of geoinformatics to natural hazards mapping and monitoring
#### Geoinformation and Spatial Management · winter 2026/27

#### Marek Urbaniak

</grid>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## What this course is about
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>

::: block <!-- element style="font-size:44px" align="left" drag="95 78" drop="0 15"-->
- Satellites see what nobody measured on the ground: the state **before** a flood, a landslide or a fire, and the state **after** it
+ One recipe, three hazards: before → after → difference → threshold → map with hectares and an honest uncertainty
+ Tools: **Copernicus Browser**, **Google Earth Engine** (JavaScript, Python, R), machine learning, Python notebooks
+ Outcome: you can produce a reproducible hazard map of a real event and defend its numbers
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Schedule – Mondays, room 15
:::

::: block <!-- element style="font-size:34px" align="left" drag="95 80" drop="0 15"-->
| Date | Lecture (10:45–12:15) | Lab (8:30–10:45) – introduced by the previous lecture |
|---|---|---|
| 9.11 | L1 Kick-off: hazards, Earth observation, your accounts (11:30–12:15) | – |
| 16.11 | L2 Google Earth Engine: the Code Editor | Lab 1 Copernicus Browser, GEE account, first script |
| 23.11 | L3 Machine learning for land cover classification | Lab 2 GEE: indices, classes, areas |
| 30.11 | L4 Flood mapping: optical indices and SAR | Lab 3 Random Forest + k-means, accuracy |
| 7.12 | L5 Landslide mapping with satellite radar | Lab 4 Flood extent from Sentinel-1 |
| 14.12 | L6 Wildfire detection and burn severity | Lab 5 Landslide density heatmap |
| 21.12 | L7 GEE from Python and R | Lab 6 Burn severity (dNBR) |
| 11.01 | L8 Wrap-up: uncertainty, services, assessment (11:30–12:15) | Lab 7 (4 h) Colab, geemap, rgee, capstone |
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Seven milestones = seven deliverables
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:38px" align="left" drag="95 80" drop="0 15"-->
| | Due | You hand in |
|---|---|---|
| **M1** | 16.11 (lab 1) | CDSE account, registered GEE Cloud project, one event found in Copernicus Browser, first script |
| **M2** | 30.11 | Script link: index → classes → area per class in hectares (your ROI) |
| **M3** | 7.12 | Classification report: RF and k-means maps, two confusion matrices, kappa, conclusions |
| **M4** | 14.12 | Flood extent map (Sentinel-1), hectares, threshold-sensitivity table, comparison with GFM/EMS |
| **M5** | 21.12 | Landslide density heatmap of a documented event + note on where it fails |
| **M6** | 11.01 | Burn severity map (dNBR, USGS classes), hectares per class, EFFIS comparison |
| **M7** | 25.01 (tbc) | Capstone notebook: one hazard workflow reproduced in Python or R with text, figures, limitations |
:::

::: block <!-- element style="font-size:32px" drag="95 10" drop="0 90" bg="#fff3cd" pad="8px 20px"-->
A milestone is due at the start of the next lab. Submit in Moodle (assignment or lesson), always with the script link.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Assessment
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
<!-- TODO: fill in the real rules (same placeholders as in L08) -->
- Lab deliverables M1–M6: __ % (each graded pass / revise / fail; two revisions allowed)
- Capstone notebook M7: __ %
- Lesson quizzes (GEE, API): __ %
- Attendance at labs: required (one absence allowed)
- Final deadline for all submissions: __.01.2027
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before the first lab (16.11): two accounts
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 78" drop="0 15"-->
- [ ] Free account at [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) → log in once to [Copernicus Browser](https://browser.dataspace.copernicus.eu/)
- [ ] Google account → [register a Google Cloud project for Earth Engine](https://developers.google.com/earth-engine/guides/access), **noncommercial (education)** – approval can take a day
- [ ] Optional: install R ≥ 4.3 + RStudio/Positron (only if you want the R path in lab 7)
- [ ] Problems → the Announcements forum in Moodle, before Friday
:::

---
::: block
## Literature
:::

Must read:<!-- element style="font-size: 54px; color:brown" align="left" -->

1. Handwerger et al. (2022). Generating landslide density heatmaps for rapid detection using open-access satellite radar data in Google Earth Engine. [NHESS 22, 753–773](https://nhess.copernicus.org/articles/22/753/2022/)
2. Notti et al. (2018). Potential and limitations of open satellite data for flood mapping. [Remote Sensing 10, 1673](https://www.mdpi.com/2072-4292/10/11/1673)
3. [UN-SPIDER recommended practices](https://un-spider.org/advisory-support/recommended-practices) – floods, burn severity, landslides

Books (free online):<!-- element style="font-size: 54px; color:blue" align="left" -->

- Cardille et al. (eds.) 2024, [Cloud-Based Remote Sensing with Google Earth Engine](https://www.eefabook.org/)
- Lovelace, Nowosad, Muenchow, [Geocomputation with R](https://r.geocompx.org/); Pebesma & Bivand, [Spatial Data Science](https://r-spatial.org/book/)
- Wickham & Grolemund, [R for Data Science](https://r4ds.hadley.nz/); [rgee documentation](https://r-spatial.github.io/rgee/)

---
::: block
# See you on 9 November :smile:
:::
