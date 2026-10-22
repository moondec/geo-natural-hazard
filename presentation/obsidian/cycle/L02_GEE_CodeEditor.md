---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 2
summary: "Wykład 2 (2 h, 16.11.2026) – Google Earth Engine, Code Editor, obiekty server-side, kolekcje, filtry, map/reduce, indeksy spektralne, pola powierzchni; wstęp do ćwiczeń 2 i zadania „index areas”"
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

### Lecture 2<!-- element style="letter-spacing: 1.5rem;"-->
## Google Earth Engine: the Code Editor
#### from a pixel to an area statistic

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
1. What Earth Engine is and why it is fast (and why `print` is slow)
2. The Code Editor – panels you will use every week
3. Data model: `Image`, `ImageCollection`, `Geometry`, `Feature`, `FeatureCollection`
4. Filter → map → reduce: the three verbs of every script
5. Clouds first: scene filter, `SCL`, Cloud Score+ and what a bitmask is
6. Spectral indices: NDVI and friends
7. From classes to hectares: `reduceRegion` with `pixelArea`
8. **In the lab**: the full script, step by step; homework "index areas"
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 90" bg="#F06400" rotate="25"/>

::: title 
## Google Earth Engine
:::

::: block <!-- element style="font-size: 46px;"  -->
- [Online catalogue](https://developers.google.com/earth-engine/datasets) of satellite imagery and geospatial data (petabytes, updated daily)
+ [Analysis through scripting](https://code.earthengine.google.com/) (JavaScript in the browser, Python anywhere)
+ Free for [noncommercial use](https://earthengine.google.com/noncommercial/) (research, education) with a registered Google Cloud project
+ Your code runs on Google servers next to the data – you never download an image
+ [End-to-End GEE](https://courses.spatialthoughts.com/end-to-end-gee.html) by Spatial Thoughts – our cookbook
:::
![[Pasted image 20230106205837.png|220]]<!-- element drag="25 25" drop="bottomleft"-->

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Client and server: why Earth Engine is fast
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="50 75" drop="0 15"-->
![[diagram_L02_client_server.svg]]
:::

::: block <!-- element style="font-size:32px" align="left" drag="47 78" drop="52 15" bg="#e8f4f8" pad="12px"-->
- `ee.Image(...)`, `.filter(...)`, `.map(...)` only **describe** a computation. Nothing runs yet (lazy evaluation).
- Computation starts when you ask for a result: `Map.addLayer`, `print`, `Export`, `.getInfo()`.
- `Map.addLayer` computes only the pixels visible at the current zoom → fast.
- `print(collection)` serialises thousands of metadata records → slow. Use `print(collection.size())`.
- Loops `for` over pixels do not exist. You express the operation on the **whole collection** (`map`) and let the server parallelise it.
:::

::: source
source: [Earth Engine guides – client vs. server](https://developers.google.com/earth-engine/guides/client_server)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## The Code Editor
:::

<!-- TODO image: screenshot of code.earthengine.google.com with panels labelled (Scripts / Docs / Assets, editor, Console / Inspector / Tasks, map, geometry tools). Source: your own screenshot. -->

::: block <!-- element style="font-size:30px" align="left" drag="95 75" drop="0 15"-->
| Panel | What for | You will use it in lab… |
|---|---|---|
| **Scripts** | your scripts + shared repositories (End-to-End in *Reader*) | 2 – add the repository |
| **Docs** | every function with its arguments – read it before you google | every week |
| **Assets** | your own uploads: shapefiles, CSV, GeoTIFF | 3 – training points, 6 – fire perimeter |
| **Editor** | JavaScript; `Ctrl+/` comments a line; `Run`; `Get Link` | always |
| **Console** | output of `print()` | always |
| **Inspector** | click the map → pixel values of every layer | 2, 4, 6 – check thresholds |
| **Tasks** | exports to Drive / Assets | 3, 6 – export the map |
| **Geometry tools** | draw points / polygons → `geometry` import; *Import as FeatureCollection* for training data | 2, 3 |
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Data model: five objects you need
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:26px" align="left" drag="95 78" drop="0 15"-->
| Object | Meaning | Example |
|---|---|---|
| `ee.Image` | one raster with many **bands** | one Sentinel-2 scene: `B2 … B12, QA60` |
| `ee.ImageCollection` | a stack of images (time series) | `ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')` |
| `ee.Geometry` | point, line, polygon | `ee.Geometry.Point(16.93, 52.41)` – Poznań |
| `ee.Feature` | geometry + properties (attributes) | a district with `name`, `population` |
| `ee.FeatureCollection` | a table of features (vector layer) | `ee.FeatureCollection('FAO/GAUL/2025/level2')` – admin borders |
:::

::: block <!-- element style="font-size:23px" drag="95 12" drop="0 88" bg="#fff3cd" pad="10px 20px"-->
Catalogue IDs you will use: `COPERNICUS/S2_SR_HARMONIZED` (surface reflectance, L2A), `COPERNICUS/S2_HARMONIZED` (top of atmosphere, L1C), `LANDSAT/LC09/C02/T1_L2`, `COPERNICUS/S1_GRD`, `NASA/NASADEM_HGT/001`.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Which Sentinel-2 level? L1C vs L2A
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="50 70" drop="0 15"-->
**Level-1C** – top-of-atmosphere (TOA) reflectance
- includes the atmosphere (haze, aerosols)
- longer archive (2015 →)
- `COPERNICUS/S2_HARMONIZED`

**Level-2A** – bottom-of-atmosphere (surface) reflectance
- atmospherically corrected (Sen2Cor), plus a scene classification band `SCL`
- global archive from 2017 (Europe), 2018–2019 (world)
- `COPERNICUS/S2_SR_HARMONIZED` ← **use this one** for indices and classification
:::

::: block <!-- element style="font-size:38px" align="left" drag="45 70" drop="53 15" bg="#e8f4f8" pad="15px"-->
"HARMONIZED" = after 25 Jan 2022 ESA shifted all values by +1000 (processing baseline 04.00); the harmonized collections undo this shift, so old and new scenes have the same scale.

Reflectance is stored as integer × 10 000: a value of 2500 = 0.25. Divide by 10 000 before computing anything that is not a normalized ratio.
:::

::: source
source: [Sentinel-2 in the Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Filter → map → reduce
:::

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
![[diagram_L02_filter_map_reduce.svg]]
:::

::: block <!-- element style="font-size:36px" drag="95 12" drop="0 88" bg="#fff3cd" pad="10px 20px"-->
Two different reductions: `.median()` reduces **time** (many images → one), `.reduceRegion()` reduces **space** (many pixels → one number). Every lab script in this course has both.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Filtering: the first lines of every script
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:34px" align="left" drag="55 80" drop="0 15"-->
```javascript
// area of interest: a point with a buffer, or a drawn polygon
var poi = ee.Geometry.Point(16.93, 52.41);
var roi = poi.buffer(5000);          // 5 km around Poznań centre
Map.centerObject(roi, 11);

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterDate('2025-05-01', '2025-09-30')             // when
  .filterBounds(roi)                                   // where
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)); // how cloudy

print('scenes:', s2.size());         // a number, not the whole list

var rgb = {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000};
Map.addLayer(s2.median().clip(roi), rgb, 'S2 median RGB');
```
:::

::: block <!-- element style="font-size:36px" align="left" drag="42 80" drop="58 15" bg="#e8f4f8" pad="15px"-->
- `filterDate` end date is **exclusive**
- `CLOUDY_PIXEL_PERCENTAGE` is a scene-level metadata property – it filters whole scenes, not pixels (pixel masking: next slide)
- `median()` of a stack removes most clouds (bright) and shadows (dark) – the simplest composite
- `clip` only for display; clipping before computation does not speed it up
- `min`/`max` 0–3000 because reflectance × 10 000 and land is rarely brighter than 0.3
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Clouds first: scene filter, SCL, Cloud Score+ and bitmasks
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:26px" align="left" drag="50 78" drop="0 15"-->
Scene-level `CLOUDY_PIXEL_PERCENTAGE` removes cloudy *scenes*. Pixel-level masking uses a **QA band** where each **bit** is a flag:

Sentinel-2 `QA60` (60 m): bit 10 = opaque cloud, bit 11 = cirrus. **Empty for 25 Jan 2022 – 28 Feb 2024** – for those dates use SCL or Cloud Score+. The band value is an integer whose binary digits are the flags: 0 = clear, 1024 = cloud (2¹⁰), 2048 = cirrus (2¹¹), 3072 = both.

```javascript
function maskS2(img) {
  var qa = img.select('QA60');
  var cloud  = 1 << 10;          // 1024
  var cirrus = 1 << 11;          // 2048
  var clear = qa.bitwiseAnd(cloud).eq(0).and(qa.bitwiseAnd(cirrus).eq(0));
  return img.updateMask(clear)
            .select('B.*')
            .copyProperties(img, ['system:time_start']);
}
```
`1 << 10` shifts a 1 ten places left = 1024; `bitwiseAnd` keeps only that bit; `.eq(0)` = the flag is off.
:::

::: block <!-- element style="font-size:24px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Better masks (2026):
- Sentinel-2 L2A **`SCL`** band (20 m): 3 = cloud shadow, 8–9 = cloud, 10 = cirrus, 11 = snow → keep pixels whose `scl` is not 3, 8, 9 or 10 (shadow, cloud, cirrus)
- **Cloud Score+** (`GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED`): per-pixel quality 0–1, link by `system:index`, `cs_cdf >= 0.6` – currently the recommended S2 mask
- Landsat 8/9 `QA_PIXEL`: bit 3 cloud, bit 4 shadow, bit 5 snow – same `bitwiseAnd` trick
- MODIS `state_1km`, VIIRS `QF1`: multi-bit fields (2 bits = 4 states) → `bitwiseAnd(3)` after a shift

Moodle lesson 2, step 5 (*Clouds first*) has the three masks ready to paste; the Python version differs only by `.And()`.
:::

::: source
source: [Working with QA bands and bitmasks in GEE (Spatial Thoughts)](https://spatialthoughts.com/2021/08/19/qa-bands-bitmasks-gee/); [Cloud Score+ dataset](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Spectral indices: why NDVI works
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="48 78" drop="0 15"-->
Healthy vegetation absorbs **red** (chlorophyll) and strongly reflects **near infrared** (leaf structure):

$$ NDVI = \frac{NIR - Red}{NIR + Red} = \frac{B8 - B4}{B8 + B4} $$

| Surface | NDVI |
|---|---|
| water | < 0 |
| bare soil, rock, built-up | 0 – 0.2 |
| sparse vegetation, shrub | 0.2 – 0.4 |
| dense green vegetation | 0.4 – 0.9 |
:::

::: block <!-- element style="font-size:30px" align="left" drag="48 80" drop="52 15" bg="#e8f4f8" pad="12px"-->
Normalized difference = the same pattern for every pair of bands:
- `normalizedDifference(['B8','B4'])` → NDVI (vegetation)
- `['B3','B8']` → NDWI (water, lecture 4)
- `['B3','B11']` → MNDWI (water vs. built-up)
- `['B8','B12']` → NBR (burned area, lecture 6)
- `['B8','B11']` → NDMI (moisture)

Values in [−1, 1], unitless, comparable between dates and sensors – that is why we use them for *before/after* differences.

Full list: [Awesome spectral indices](https://github.com/awesome-spectral-indices/awesome-spectral-indices), [Sentinel Hub custom scripts](https://custom-scripts.sentinel-hub.com/sentinel-2/indexdb/).
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## map(): add a band to every image
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:34px" align="left" drag="55 80" drop="0 15"-->
```javascript
// a function that takes an image and returns it with one more band
var addNDVI = function(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
};

var s2ndvi = s2.map(addNDVI);            // applied to every scene
var ndviMed = s2ndvi.select('NDVI').median();  // one band, one image

var ndviVis = {min: -0.2, max: 0.8,
               palette: ['blue', 'white', 'yellow', 'green', 'darkgreen']};
Map.addLayer(ndviMed.clip(roi), ndviVis, 'NDVI median');
```
:::

::: block <!-- element style="font-size:36px" align="left" drag="42 80" drop="58 15" bg="#e8f4f8" pad="15px"-->
Rules for a function inside `map()`:
- it must **return** an image (or a feature)
- no `print`, no `Map.addLayer` inside – it runs on the server for every element
- no `if` on pixel values – use `.where()`, `.gt()`, `.updateMask()` instead

Use the **Inspector** to click on a field, a lake and a forest and check that the NDVI values match the table from the previous slide. If they do not, your bands or your scale are wrong.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## From continuous index to classes: thresholds
:::

::: block <!-- element style="font-size:34px" align="left" drag="55 80" drop="0 15"-->
```javascript
// 1) one class = one boolean image × its code (the manual way)
var water = ndviMed.lte(0.0).multiply(1);
var bare  = ndviMed.gt(0.0).and(ndviMed.lte(0.2)).multiply(2);
var shrub = ndviMed.gt(0.2).and(ndviMed.lte(0.4)).multiply(3);
var green = ndviMed.gt(0.4).multiply(4);
var classes = water.add(bare).add(shrub).add(green).rename('class');

// 2) the same in one line: count how many thresholds the pixel exceeds
var thresholds = ee.Image([0.0, 0.2, 0.4]);
var classes2 = ndviMed.gt(thresholds).reduce(ee.Reducer.sum()).add(1).toInt();

Map.addLayer(classes2.clip(roi),
  {min: 1, max: 4, palette: ['blue', 'burlywood', 'yellowgreen', 'darkgreen']},
  'NDVI classes');
```
:::

::: block <!-- element style="font-size:36px" align="left" drag="42 80" drop="58 15" bg="#e8f4f8" pad="15px"-->
- `.gt()`, `.lte()` return **0/1 images**; multiply by a code and add them → one class image
- version 2 is what you will use in the homework: change the list of thresholds, nothing else
- thresholds are **your decision** – justify them with Inspector values and the literature, and write it in the report
- next lecture: let a machine learning algorithm choose the thresholds in 10 bands at once
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## From classes to hectares: reduceRegion + pixelArea
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:32px" align="left" drag="55 80" drop="0 15"-->
```javascript
var areaImage = ee.Image.pixelArea().addBands(classes2);  // band 0 = m² of each pixel, band 1 = class

var areas = areaImage.reduceRegion({
  reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'class'}),
  geometry: roi,
  scale: 10,          // Sentinel-2 native resolution, in metres
  maxPixels: 1e10
});

// convert the list of dictionaries into a readable table in hectares
var list = ee.List(areas.get('groups'));
var table = ee.FeatureCollection(list.map(function(d) {
  d = ee.Dictionary(d);
  return ee.Feature(null, {class: d.get('class'),
                           ha: ee.Number(d.get('sum')).divide(1e4).round()});
}));
print('area per class [ha]:', table);
```
:::

::: block <!-- element style="font-size:36px" align="left" drag="42 80" drop="58 15" bg="#e8f4f8" pad="15px"-->
- `ee.Image.pixelArea()` gives the true area of every pixel in m² (it changes with latitude)
- `group` splits the sum by the value of band 1 → one sum per class
- **`scale`** must match the data (10 m). `scale: 1` forces a billion samples and the error *"Too many pixels"* or a wrong, over-smoothed answer
- the sum of all classes must equal the ROI area – check it, it is your first sanity test
- a chart instead of a table: `ui.Chart.feature.byFeature(table, 'class', 'ha')`
:::

::: source
source: [End-to-End GEE – computing area](https://courses.spatialthoughts.com/end-to-end-gee.html#calculating-area)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Vector data: borders instead of a drawn polygon
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:34px" align="left" drag="55 75" drop="0 15"-->
```javascript
// administrative units from FAO GAUL (level 0 = country, 1 = region, 2 = district)
// FAO GAUL 2025 (the 2015 assets are deprecated); names have no diacritics
var admin2 = ee.FeatureCollection('FAO/GAUL/2025/level2');
var poznan = admin2.filter(ee.Filter.eq('GAUL2_NAME', 'Poznanski'));
Map.addLayer(poznan, {color: 'red'}, 'Poznań district');

var roi = poznan.geometry();   // use it exactly like the buffer before
```
:::

::: block <!-- element style="font-size:36px" align="left" drag="42 75" drop="58 15" bg="#e8f4f8" pad="15px"-->
- GAUL names are in the local language, sometimes without diacritics – filter level 1 by `GAUL1_NAME` and print `aggregate_array('GAUL2_NAME')` to see which district names exist
- Your own borders: download from [GADM](https://gadm.org/data.html), upload the shapefile in **Assets** and load it with `ee.FeatureCollection` (the asset path is shown in the Assets panel)
- A drawn polygon is fine for the homework, but a named unit makes the report reproducible
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Typical errors and what they mean
:::

::: block <!-- element style="font-size:36px" align="left" drag="95 78" drop="0 15"-->
| Message / symptom | Cause | Fix |
|---|---|---|
| `Collection.first: no element` / empty map | filters too strict (dates, clouds, AOI) | print `size()` after each filter |
| `Image.select: Pattern 'NDVI' did not match` | you selected a band before adding it | order of `map` and `select` |
| `Too many pixels in the region` | `scale` too small or AOI too big | `scale: 10` (S2), `30` (Landsat), `maxPixels: 1e10` |
| `Computation timed out` | `print` of a huge object or `getInfo` | print `size()`, use `Export` |
| map is grey / black | wrong `min`/`max` or band names | Inspector → read real values |
| `is not a function` | mixing client JS (`for`, `if`, `Math`) with `ee` objects | use `ee.List.map`, `ee.Algorithms.If`, `ee.Number` |
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## In the lab (23.11, 3 h)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. Moodle → *GEE – javascript editor* → lesson: sign-up check, add the End-to-End repository
2. Build the script from this lecture **line by line** on your own AOI (point + buffer or a GAUL district): filter → median RGB → NDVI → classes → area table
3. Verify with the Inspector: 3 pixels (water, field, forest), write down their NDVI
4. Save the script, `Get Link`, paste the link in the quizzes of the lesson
5. **Homework (assignment in Moodle)**: repeat for a *different* index (EVI, NDWI, SAVI, NDMI…), your own ROI (a city, a district, a national park), your own thresholds with justification. Deliverable: the **script link** + a short note with the area table
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title 
## Before next class
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Finish and submit the "index areas" homework (script link)
- [ ] Read End-to-End GEE, module 1 (*Working with Image Collections*, *Filtering Image Collections*) and module 2, section 03 (*Computation on ImageCollections*) (30 min, skim the code, you have already written it)
- [ ] Think of an area 60–100 km² with **at least four clearly different surface types** (water, forest, crops, built-up) – you will classify it next week
- [ ] Optional video: [Module 1: Earth Engine Basics – End-to-End GEE](https://www.youtube.com/watch?v=daYhxVVIpJU) (Spatial Thoughts)
:::

---
::: block 
# Thank you :smile:
:::
