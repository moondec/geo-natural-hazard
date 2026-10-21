---
date_create: 2023-01-05
tags:
  - Geo
  - GEE
  - R
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
summary: "Podstawowe informacje o kursie (część wstępnej analizy w GEE, zastosowanie RGEE, Algorytmy ML -klasyfikacje- analiza statystyczna w R)"
timeForPresentation: 108000
theme: beige
width: 1920
height: 1200
margin: 0
maxScale: 4
transition: zoom
course: Application of geoinformatics to natural hazards mapping and monitoring
---


<!-- slide data-background-image=![[sateliteGEEbanner.png|1920]] -->
<grid drag="60 30" drop="left" bg="#EEB73F" align="left" pad="250px 0  250px 300px">

### Part 2<!-- element style="letter-spacing: 1.5rem;"-->

#### Marek Urbaniak

</grid>
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
<!-- slide template="[[tpl-geo-default-slide]]"-->

::: title 
## Landslides, wildfires, and other hazards...
:::

<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: block <!-- element style= "color:navy"-->
### We will focus on several of them
:::

::: block <!-- element style="font-size:45px"-->
- Wildfires (e.g. [Forest Fires](https://www.un-spider.org/category/disaster-type/forest-fire))
+ [Landslides](https://www.un-spider.org/category/disaster-type/landslide) or Mass Movement
+ [Droughts](https://www.un-spider.org/category/disaster-type/drought)
+ And maybe [air pollution](https://bookdown.org/david_carslaw/openair/)
:::

### General methodology template:<!-- element class="fragment fade-up" data-fragment-index="3" style= "color:darkgreen"-->

+ Step 1 - Select satellite images for the period **before** the event
 + Step 2 - Select satellite images for the period **after** the event [^1]

![[Pasted image 20251102203814.png]]<!-- element class="fragment fade-up" data-fragment-index="4"-->

![[Pasted image 20230109115309.png|800]]<!-- element  drag="100 60" drop="50 0" class="fragment fade-out" data-fragment-index="1"-->

![[S2L2A-1348973218860829-timelapse.gif]]<!-- element  drag="60 100" drop="40 0" class="fragment fade-in-then-out" data-fragment-index="1"-->

![[S2L2A-1015625487634027-timelapse.gif]]<!-- element  drag="60 100" drop="40 0" class="fragment fade-in-then-out" data-fragment-index="2"-->

### For other advice visit e.g.<!-- element style="color:red" class="fragment fade-up" data-fragment-index="6"--> [https://un-spider.org](https://un-spider.org/advisory-support/recommended-practices)<!-- element class="fragment fade-up" data-fragment-index="6"-->

<grid drag= "100 60" drop= "0 0" style="font-size: 20px" align="justify">
[^1]: For this purpose we can use [Copernicus Browser](https://browser.dataspace.copernicus.eu/) **We will come back to it later**<!-- element class="fragment fade-up" data-fragment-index="4"-->
</grid>

::: source
source: [https://un-spider.org/](https://un-spider.org/advisory-support/recommended-practices)
:::

note:

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## How to choose data for particular analysis?
:::

### An example - Indicating burn severity
![[Pasted image 20230106230924.png|900]]<!-- element  class="fragment fade-in-then-out" data-fragment-index="2"-->

<grid drag="60 30" drop="left" background="#1F90FF" align="left" pad="250px 0  250px 300px">
</grid>

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
## Results
:::

![[Pasted image 20230107004533.png]]<!-- element drag="100 100" drop="0 -10"-->
::: source
source: [Petropoulos, G. P., Griffiths, H. M., & Kalivas, D. P. (2014). [Quantifying spatial and temporal vegetation recovery dynamics following a wildfire event in a Mediterranean landscape using EO data and GIS](https://www.researchgate.net/publication/261183988_Quantifying_Spatial_and_Temporal_Vegetation_Recovery_Dynamics_Following_a_Wildfire_Event_in_a_Mediterranean_Landscape_using_EO_Data_and_GIS). _Applied Geography_, _50_, 120–131.]
:::

---
<grid drag="10 100" drop="right" bg="#0EB73F"/>
<grid drag="13 20" drop="10 3" bg="#ffB73F"/>
<grid drag="13 20" drop="17 15" bg="#00ced1"/>
<grid drag="13 20" drop="27 5" bg="#F06400" />

![[Pasted image 20251102203708.png|1000]]

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
# ![[Pasted image 20251102203848.png]]
:::

### How to find a study example?<!-- element style="font-size: 60px" drag="60 20" drop="0 -95"-->



<style>
	.with-border{
		border: 5px solid red;
	}
</style>

<grid drag="20 100" drop="-90" bg="#adff2f"/>

<grid  drag="100 100" drop="0 0">
![[Pasted image 20251102210010.png]]
</grid>

<grid  drag="40 80" drop="0 19" class= "fragment fade-in-then-out" frag="2">
![[Pasted image 20251102210158.png]]
</grid>

<grid style= "border: 7px solid red;" drag="25 15" drop="8 36" class="fragment fade-in-then-out" frag="3" />

<grid  drag="40 100" drop="0 10" class= "fragment fade-in-then-out" frag="4">
![[Pasted image 20251102210305.png]]
</grid>

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

---
<grid drag="60 6" drop="0 0" border="medium dashed red" pad="3px"/>
<grid drag="30 70" drop="right" bg="#0EB73F"/>

<grid drag="13 26" drop="0 -74" bg="#ffB73F"/>
<grid drag="10 36" drop="-95 -55" bg="#00ced1"/>
<grid drag="15 66" drop="3 -5" bg="#F06400" />

::: block <!-- element  drag="70 100" drop="center" align="left" -->
https://custom-scripts.sentinel-hub.com/
![[Pasted image 20230109181444.png]]
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Idea of remote sensing :smile: HOW EO SATELLITES WORK
:::

::: block <!-- element style="font-size: 50px;" -->
EO satellites can be divided into two types based on how they capture imagery; **passive** and **active**.
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
> ### PASSIVE EO SATELLITES

Passive satellites detect radiation reflected off the Earth’s surface, such as visible light and infrared. In general, passive satellites are not able to work through clouds.

Approximate max resolution: 50cm

> ### ACTIVE EO SATELLITES

Active satellites transmit energy towards the Earth and measure the returned signal which provides information about the Earth’s surface. In general, active satellites can see through cloud.

Approximate max resolution: 25cm

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## HOW MUCH CAN SATELLITES SEE?
:::
::: block<!-- element flow="row"-->
![[Pasted image 20230109220407.png|900]]

![[Pasted image 20230109220634.png|800]]
:::

---

<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Compare Landsat and Sentinel bands
:::

![[Pasted image 20230106213729.png|1050]]

::: block <!-- element style="font-size: 30px;" class="fragment fade-up" -->
Landsat 8 and **Landsat 9** (2021) carry the same bands (OLI-2 / TIRS-2); Landsat 7 was decommissioned in June 2025. Sentinel-2 now flies as a triplet: **2A, 2B and 2C** (2C operational since January 2025). Next generation: Landsat Next (26 bands, launch planned for the early 2030s).
:::



---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 90" bg="#F06400" rotate="25"/>

::: title 
## Google Earth Engine
:::

::: block <!-- element style="font-size: 50px;"  -->
- [Online](https://developers.google.com/earth-engine) catalogue of satellite imagery and geospatial imagery
+ [Analysis capabilities through scripting](https://code.earthengine.google.com/) (javascript, python)
+ Free for [noncommercial use](https://earthengine.google.com/noncommercial/) (research, education) – you need a Google account and a registered **Google Cloud project** ([how to get access](https://developers.google.com/earth-engine/guides/access)) – do it **before** the class!
+ Uses the compute power of Google servers and conduct elaborate RS analysis faster
+ [End-to-End](https://courses.spatialthoughts.com/end-to-end-gee.html) course
+ Python: `ee` API + [geemap](https://geemap.org/) in Jupyter; R: rgee (next slide)
:::
![[Pasted image 20230106205837.png|220]]<!-- element drag="25 25" drop="bottomleft"-->

---
<!-- slide template="[[tpl-geo-default-slide]]" -->

<grid drag="13 26" drop="80 53" bg="#ffB73F" rotate="-15"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />
![[Pasted image 20251102204319.png]]
::: title 
## Copernicus Browser
:::

::: block <!-- element style="font-size: 50px;"  -->
- Part of the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (EU / ESA); a free account is required
+ [Copernicus Browser](https://browser.dataspace.copernicus.eu/) to browse and compare full resolution images (Sentinel-1, Sentinel-2 + mosaics, Sentinel-3, Sentinel-5P, DEM)
+ Tools for analysis (compare, timelapse, time series and histograms, import AOI as KML/GeoJSON, export GeoTIFF, 3D view, custom scripts e.g. [NDVI](https://custom-scripts.sentinel-hub.com/sentinel-2/ndvi/), [SAVI](https://custom-scripts.sentinel-hub.com/sentinel-2/savi/))
+ Import imagery into your GIS application (e.g. QGIS, ArcGIS) via WMS/WMTS
+ Successor of **EO Browser** (Sentinel Hub / Sinergise, retired in March 2026); commercial alternative: [Planet Insights Platform](https://www.planet.com/products/planet-insights-platform/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="9 20" drop="90 3" bg="#ffB73F"/>
<grid drag="9 20" drop="97 15" bg="#00ced1"/>
<grid drag="9 20" drop="87 18" bg="#F06400" />

::: title 
# RGEE - Google [Earth Engine with R](https://r-spatial.github.io/rgee/)
:::

![[Pasted image 20230109204730.png|600]]
![[Pasted image 20230109204905.png]]
::: source
source: https://github.com/r-spatial/rgee
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## What next? Surface Classifier! _ML_ GEE machine learning
:::

<grid drag="13 26" drop="80 58" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: block <!-- element style="font-size: 60px; " class="fragment fade-out" data-fragment-index="1"-->
-   **Supervised Classification:** One ML technique for classifying land is to use ground truth examples to teach a model to differentiate between classes. Earth Engine's built-in [supervised classifiers](https://developers.google.com/earth-engine/guides/classification) support this process.
:::
::: block <!-- element style="font-size: 60px;" drag="100" drop="top"  class="fragment fade-in-then-out" data-fragment-index="1"-->
-   **Unsupervised Classification:** In unsupervised classification, no ground truth examples are provided to the training algorithm. Instead, the algorithm divides the available data into clusters based on inherent differences. Earth Engine's [unsupervised classifiers](https://developers.google.com/earth-engine/guides/clustering) are particularly useful when no ground truth data exists, when you do not know the final number of classes or when you want to do quick experimentation.
:::
::: block <!-- element style="font-size: 60px; "  drag="100" drop="top"  class="fragment fade-in-then-out" data-fragment-index="2"-->
-   **Regression:** Whereas a classification model attempts to bucket each input into a discrete class, a regression model attempts to predict a continuous variable for each input. For example, a regression model could predict water quality, percent forest cover, percent cloud cover or crop yield. For more information, please refer to the [Linear Regression section of ee.Reducers](https://developers.google.com/earth-engine/guides/reducers_regression).
:::

::: source
source: https://developers.google.com/earth-engine/guides/machine-learning
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="16 26" drop="80 23" bg="#ffB73F" rotate="-15"/>
<grid drag="12 20" drop="7 75" bg="#00ced1" />
<grid drag="16 26" drop="77 70" bg="#F06400" rotate="15" />

::: title
## Decision Tree ➡️ Random forest
:::
::: block<!-- element  drop="top" -->
![[Drawing 2023-01-10 00.31.47.excalidraw.png]]
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->

<grid drag="16 26" drop="80 23" bg="#ffB73F" rotate="-15"/>
<grid drag="12 20" drop="7 75" bg="#00ced1" />
<grid drag="16 26" drop="77 70" bg="#F06400" rotate="15" />

::: title
## Decision Tree ➡️ Random forest
:::
::: block <!-- element  drop="top" -->
![[Drawing 2023-01-10 00.59.07.excalidraw.png]]
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->

<grid drag="16 26" drop="95 3" bg="#ffB73F" rotate="-15"/>
<grid drag="12 20" drop="0 95" bg="#00ced1" rotate="45"/>
<grid drag="16 26" drop="77 90" bg="#F06400" rotate="15" />

::: title
## Decision Tree ➡️ Random forest
:::
::: block <!-- element  drop="top"  flow="row"-->
![[Drawing 2023-01-10 00.31.47.excalidraw.png]] 
![[Drawing 2023-01-10 00.59.07.excalidraw.png]]
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Decision Tree ➡️ Random forest
:::
::: block <!-- element style="font-size: 60px; " -->
1. We need so called _**training set**_, and we pick random K points
2) Build the decision tree associated to K data points
3) Choose the number Ntree of trees we want to build and repeat STEP 1 & 2
4) For a new data point, make each one of Ntrees predict the category to which the data points belong, and assign the new data point to the category that wins the major vote.
:::

---

<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Regression - simple linear regression
:::

<grid drag="13 26" drop="80 28" bg="#ffB73F"/>
<grid drag="13 26" drop="87 45" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 60" bg="#F06400" />

::: block <!-- element style="font-size: 60px; " class="fragment fade-out" data-fragment-index="1"-->
![[Pasted image 20230109230711.png|1200]]
:::

::: block <!-- element style="font-size: 60px;" drag="80" drop="topleft"  class="fragment fade-in-then-out" data-fragment-index="1"-->
![[Drawing 2023-01-09 23.21.12b.excalidraw.png]]
:::
::: block <!-- element style="font-size: 60px;" drag="80" drop="topleft"  class="fragment fade-in-then-out" data-fragment-index="2"-->
![[Drawing 2023-01-09 23.58.08.excalidraw.png]]
:::

---
::: block
## Home work:
:::

### Watch the following webinars:
::: block<!-- element style="font-size: 50px;color:blue"  -->
- https://www.youtube.com/watch?v=F0lIn5r6ZWk (A short guide to Copernicus Browser)
- https://www.youtube.com/watch?v=GecNCdilbig (Introduction to the CDSE website and Copernicus Browser, facultative)
- https://youtu.be/wn6p9KcOIOI
- https://www.youtube.com/watch?v=Pz-96PMm5x8 (facultative)
- https://www.geo.fu-berlin.de/en/v/geo-it/webinar/Online-Seminar-7/index.html
- Browse [Copernicus Data Space Ecosystem videos](https://www.youtube.com/@copernicusdataspaceecosystem) and [Sentinel Hub Webinars](https://www.sentinel-hub.com/explore/education/webinars/)
- Browse [Earth Engine resources for workshops](https://developers.google.com/earth-engine/tutorials/ttt)
:::
---
::: block 
## Literature:
:::

Landslides:<!-- element style="font-size: 60px; color:brown" align="left"  -->

1. https://journals.openedition.org/belgeo/15944?lang=en#tocto2n4
2. https://nhess.copernicus.org/articles/22/753/2022/nhess-22-753-2022.pdf **(must read)**

Wildfires:<!-- element style="font-size: 60px;color:red"  -->

1. https://medium.com/google-earth/how-to-generate-wildfire-boundary-maps-with-earth-engine-b38eadc97a38
2. https://jfs.agriculturejournals.cz/pdfs/jfs/2022/03/02.pdf
3. https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/burn-severity-earth-engine

---
::: block 
## Literature:
:::
3. Online books - R for Geoinformation:<!-- element style="font-size: 60px;color:blue"  -->

- **“[Advanced R](https://adv-r.hadley.nz/)”** by Hadley Wickham, provides a profound description of R syntax.
- **“[Geocomputation with R](https://r.geocompx.org/)”** by Robin Lovelace, Jakub Nowosad, and Jannes Muenchow, introduces R for manipulating and visualizing geographic data.
- **“[Spatial Data Science](https://r-spatial.org/book/)”** by Edzer Pebesma and Roger Bivand, is another excellent great resource for geographic data but focused on analysis.
- **“[R for Data Science](https://r4ds.hadley.nz/)”** by Hadley Wickham and Garrett Grolemund, introduces you to R as a data science tool, with a particular emphasis on the tidyverse package.

- **"[rgee – Google Earth Engine for R](https://r-spatial.github.io/rgee/)"** (package documentation and tutorials) by [Cesar Aybar](https://github.com/csaybar) et al. – the former "Earth Engine with R" book site is offline.
- **"[Geographic Data Science with R: Visualizing and Analyzing Environmental Change](https://bookdown.org/mcwimberly/gdswr-book/)"** by Michael C. Wimberly
- **"[Landscape Genetic Data Analysis with R](https://bookdown.org/hhwagner1/LandGenCourse_book/)"** _Editor: Helene Wagner (University of Toronto)_
- Hengl, T., MacMillan, R.A., (2019). [Predictive Soil Mapping with R](https://soilmapper.org/). OpenGeoHub foundation, Wageningen, the Netherlands, 370 pages, www.soilmapper.org, ISBN: 978-0-359-30635-0.

---

::: block 
# Thank you :smile:
:::
