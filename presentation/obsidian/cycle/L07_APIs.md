---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - Python
  - R
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 7
summary: "Wykład 7 (2 h, 21.12.2026) – GEE poza Code Editorem: API Pythona, Google Colab, geemap, różnice JS/Python, obiekty klienta vs serwera, maski chmur i bity QA, eksport, rgee w R; wstęp do ćwiczeń 7 (4 h, Colab + geemap + rgee)"
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

### Lecture 7<!-- element style="letter-spacing: 1.5rem;"-->
## GEE beyond the Code Editor
#### Python, Colab, geemap and rgee

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
1. Why leave the Code Editor? (reproducibility, your own data, statistics, automation)
2. The same engine, three clients: JavaScript, Python (`ee`), R (`rgee`)
3. Google Colab and Jupyter: a notebook in 5 minutes
4. `geemap`: the map, the translator, the exporter
5. JavaScript → Python: the seven differences
6. Cloud masking properly: QA bands and bitmasks
7. Getting data out: exports, `getInfo`, time series to pandas / data.frame
8. `rgee` for R users: install once, authenticate, run
9. **In the lab (4 h)**: Colab notebook + bitmask exercise + rgee
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Why leave the Code Editor?
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:39px" align="left" drag="50 78" drop="0 15"-->
The Code Editor is perfect for exploring. It is weak when you need to:
- **repeat** an analysis for 50 events or 10 years (loops, parameters, scheduling)
- combine satellite results with **your own data** (field plots, gauges, a CSV from Excel)
- do **statistics and plots** beyond `ui.Chart` (scikit-learn, pandas, ggplot2)
- write a **report or a thesis** where code, figures and text live together (Jupyter, Quarto)
- share a **reproducible** workflow (a notebook on GitHub runs the same for everyone)
:::

::: block <!-- element style="font-size:37px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
![[diagram_L07_three_clients.svg|620]]
Same catalogue, same functions, same server-side objects. Only the syntax around them changes. Everything from labs 2–6 can be pasted into Python with small edits (and `geemap` will do the edits for you).
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Google Colab: a notebook in 5 minutes
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:36px" align="left" drag="48 80" drop="0 15"-->
- [colab.research.google.com](https://colab.research.google.com/) – free Jupyter in the browser, Python 3; `ee` and `geemap` preinstalled or one pip away; notebooks saved to your Drive
- Cells: code (`Shift+Enter` runs) and text (Markdown) – the report writes itself
- Authenticate once per session with **your Cloud project**:
```python
import ee, geemap
ee.Authenticate()   # opens a browser window
ee.Initialize(project='your-project-id')  # from lab 1
```
- Local alternative: Jupyter / VS Code / Positron; install `earthengine-api` and `geemap` from conda-forge
- Colab can also run R (`%%R` magic with `rpy2`) – Moodle lesson page 1
:::

::: block <!-- element style="font-size:24px" align="left" drag="47 80" drop="53 15" bg="#e8f4f8" pad="12px"-->
```python
roi = ee.Geometry.Point(16.93, 52.41).buffer(5000)
s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterDate('2025-05-01', '2025-09-30')
        .filterBounds(roi)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)))
print('scenes:', s2.size().getInfo())

def add_ndvi(img):
    return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'))

ndvi = s2.map(add_ndvi).select('NDVI').median()

m = geemap.Map(center=[52.41, 16.93], zoom=11)
m.addLayer(ndvi.clip(roi), {'min': -0.2, 'max': 0.8,
           'palette': ['blue', 'white', 'yellow', 'green', 'darkgreen']}, 'NDVI')
m
```
Compare with the JavaScript from lecture 2 – line by line the same.
:::

::: source
source: [Earth Engine Python quickstart](https://developers.google.com/earth-engine/guides/quickstart_python); [geemap.org](https://geemap.org/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## JavaScript → Python: the seven differences
:::

::: block <!-- element style="font-size:22px" align="left" drag="95 80" drop="0 15"-->
| | JavaScript (Code Editor) | Python (`ee`) |
|---|---|---|
| 1. variables | `var x = …;` | `x = …` |
| 2. functions | `function f(img) { return …; }` | `def f(img):` + indentation, `return` |
| 3. line continuation | free | wrap in `( … )` or use `\` |
| 4. logical ops | `.and()`, `.or()`, `.not()` | **`.And()`, `.Or()`, `.Not()`** (capital – `and` is a keyword) |
| 5. dictionaries / vis params | `{min: 0, max: 3000}` | `{'min': 0, 'max': 3000}` (quoted keys) |
| 6. map and print | `Map.addLayer`, `print(obj)` | `m = geemap.Map(); m.addLayer(...)`; `print(obj.getInfo())` |
| 7. `true/false/null` | lower case | `True / False / None` |

Everything else (`ee.Image`, `filterDate`, `normalizedDifference`, `reduceRegion`, `ee.Reducer.sum().group(...)`) is **identical**. `geemap.js_snippet_to_py(js_code)` converts a Code Editor script automatically – Moodle lesson page 2.
:::

::: source
source: [Python API – differences from JavaScript](https://developers.google.com/earth-engine/guides/python_install#syntax)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Client vs. server objects (the bug you will meet)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:40px" align="left" drag="50 78" drop="0 15"-->
```python
n = s2.size()            # ee.Number – lives on the server, no value yet
print(n)                 # <ee.Number object>  – not 37
print(n.getInfo())       # 37  – one round trip to Google

# WRONG: Python 'if' on a server object (always True – the object exists)
if s2.size() > 10: ...
# RIGHT: bring the number to the client first, or use server-side logic
if s2.size().getInfo() > 10: ...
img = ee.Algorithms.If(s2.size().gt(10), s2.median(), ee.Image(0))
```
:::

::: block <!-- element style="font-size:40px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
- `ee.*` objects are **recipes** sent to the server; Python only sees a handle
- `.getInfo()` fetches the value – small things only (a number, a dictionary, a list of 100 dates). An image or a big collection → use **Export**
- Python loops `for` over a *client* list are fine (e.g. over a list of years you typed); loops over server lists → `ee.List.map` or `collection.map`
- the same rule existed in JavaScript (lecture 2); Python just makes it more visible because `print` does not evaluate
:::

::: source
source: [Earth Engine – client vs. server](https://developers.google.com/earth-engine/guides/client_server)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Cloud masking properly: QA bands and bitmasks
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:26px" align="left" drag="50 78" drop="0 15"-->
Scene-level `CLOUDY_PIXEL_PERCENTAGE` removes cloudy *scenes*. Pixel-level masking uses a **QA band** where each **bit** is a flag:

Sentinel-2 `QA60` (60 m): bit 10 = opaque cloud, bit 11 = cirrus. **Empty for 25 Jan 2022 – 28 Feb 2024** – for those dates use SCL or Cloud Score+. The band value is an integer whose binary digits are the flags: 0 = clear, 1024 = cloud (2¹⁰), 2048 = cirrus (2¹¹), 3072 = both.

```python
def mask_s2(img):
    qa = img.select('QA60')
    cloud  = 1 << 10          # 1024
    cirrus = 1 << 11          # 2048
    clear = qa.bitwiseAnd(cloud).eq(0).And(qa.bitwiseAnd(cirrus).eq(0))
    return (img.updateMask(clear)
               .select('B.*')
               .copyProperties(img, ['system:time_start']))
```
`1 << 10` shifts a 1 ten places left = 1024; `bitwiseAnd` keeps only that bit; `.eq(0)` = the flag is off.
:::

::: block <!-- element style="font-size:24px" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
Better masks (2026):
- Sentinel-2 L2A **`SCL`** band (20 m): 3 = cloud shadow, 8–9 = cloud, 10 = cirrus, 11 = snow → `img.select('SCL').remap([4,5,6,7,11],[1,1,1,1,1],0)` keeps vegetation, bare, water, unclassified, snow
- **Cloud Score+** (`GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED`): per-pixel quality 0–1, link by `system:index`, `cs_cdf >= 0.6` – currently the recommended S2 mask
- Landsat 8/9 `QA_PIXEL`: bit 3 cloud, bit 4 shadow, bit 5 snow – same `bitwiseAnd` trick
- MODIS `state_1km`, VIIRS `QF1`: multi-bit fields (2 bits = 4 states) → `bitwiseAnd(3)` after a shift

Moodle lesson page 3 has the JS and Python versions side by side.
:::

::: source
source: [Working with QA bands and bitmasks in GEE (Spatial Thoughts)](https://spatialthoughts.com/2021/08/19/qa-bands-bitmasks-gee/); [Cloud Score+ dataset](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Getting data out
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:26px" align="left" drag="52 82" drop="0 15"-->
```python
# 1) a time series as a pandas DataFrame (small: one value per date)
ts = s2.map(add_ndvi).select('NDVI').map(lambda i: ee.Feature(None, {
        'date': i.date().format('YYYY-MM-dd'),
        'ndvi': i.reduceRegion(ee.Reducer.mean(), roi, 10).get('NDVI')}))
df = geemap.ee_to_df(ee.FeatureCollection(ts))      # -> pandas
df.plot(x='date', y='ndvi')

# 2) a raster to Google Drive (big: runs in the background, Tasks tab / task.status())
task = ee.batch.Export.image.toDrive(image=ndvi.clip(roi), description='ndvi_poznan',
         folder='gee', scale=10, region=roi, crs='EPSG:2180', maxPixels=1e10)
task.start()

# 3) a small raster straight to the notebook / disk
geemap.ee_export_image(ndvi.clip(roi), filename='ndvi.tif', scale=10, region=roi)

# 4) a vector table to Drive
ee.batch.Export.table.toDrive(collection=table, description='areas', fileFormat='CSV').start()
```
:::

::: block <!-- element style="font-size:31px" align="left" drag="45 82" drop="53 15" bg="#e8f4f8" pad="15px"-->
Rules:
- `getInfo` / `ee_to_df` for **small** results (< a few thousand rows); exports for rasters
- always set `scale` and `region`; set `crs` (EPSG:2180 for Poland) if the GeoTIFF goes to QGIS with other national data
- `maxPixels` default is 1e8 – a 10 m export of a district exceeds it
- exports are asynchronous: start them, continue working, check `task.status()['state']`
- naming: `description` becomes the file name – include the date and the parameter
:::

::: source
source: [Exporting data](https://developers.google.com/earth-engine/guides/exporting_images); [geemap – export](https://geemap.org/notebooks/11_export_image/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="9 20" drop="90 3" bg="#ffB73F"/>
<grid drag="9 20" drop="97 15" bg="#00ced1"/>
<grid drag="9 20" drop="87 18" bg="#F06400" />

::: title 
## rgee – Google [Earth Engine with R](https://r-spatial.github.io/rgee/)
:::

![[Pasted image 20230109204730.png|600]]
![[Pasted image 20230109204905.png]]
::: source
source: https://github.com/r-spatial/rgee (CRAN 1.1.8, 2025; maintainer M. Stigler)
:::

note:
rgee is a translator: R calls the Python `ee` API through reticulate. Same objects, <code>&#36;</code> instead of <code>.</code>: <code>ee&#36;ImageCollection('COPERNICUS/S2_SR_HARMONIZED')&#36;filterDate(...)</code>. The benefit: results go straight into `sf`, `terra`, `ggplot2`, `tmap`, Shiny.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## rgee: install once, authenticate, run
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:24px" align="left" drag="52 82" drop="0 15"-->
<pre><code class="language-r">install.packages(&quot;rgee&quot;)      # once
library(rgee)
ee_install(py_env = &quot;rgee&quot;)   # once: conda env + earthengine-api; answer Y, restart R
ee_check()                    # python? earthengine-api? credentials?
ee_Initialize(project = &quot;your-project-id&quot;, drive = TRUE)   # each session

roi &lt;- ee&#36;Geometry&#36;Point(16.93, 52.41)&#36;buffer(5000)
s2  &lt;- ee&#36;ImageCollection(&quot;COPERNICUS/S2_SR_HARMONIZED&quot;)&#36;
         filterDate(&quot;2025-05-01&quot;, &quot;2025-09-30&quot;)&#36;filterBounds(roi)&#36;
         filter(ee&#36;Filter&#36;lt(&quot;CLOUDY_PIXEL_PERCENTAGE&quot;, 30))
ndvi &lt;- s2&#36;map(function(i) i&#36;normalizedDifference(c(&quot;B8&quot;,&quot;B4&quot;)))&#36;median()

Map&#36;centerObject(roi, 11)
Map&#36;addLayer(ndvi, list(min = -0.2, max = 0.8,
             palette = c(&quot;blue&quot;,&quot;white&quot;,&quot;yellow&quot;,&quot;green&quot;,&quot;darkgreen&quot;)), &quot;NDVI&quot;)

r &lt;- ee_as_rast(ndvi&#36;clip(roi), region = roi, scale = 10)  # terra SpatRaster
</code></pre>
:::

::: block <!-- element style="font-size:26px" align="left" drag="45 82" drop="54 15" bg="#e8f4f8" pad="12px"-->
Known traps (Moodle lesson page 4 has the screenshots):
- the first authentication needs the **gcloud CLI** (any OS, per the rgee README) – install it before the lab, run `gcloud init`
- `ee_install` asks about Miniconda – say yes unless you manage Python yourself
- <code>&#36;</code> replaces <code>.</code>; R functions in `map` must return an `ee` object
- bridges to R: `ee_as_sf`, `ee_as_rast` (terra), `ee_extract` (time series → data.frame)
- if rgee refuses to start: `ee_clean_pyenv(); ee_install()` and read the error

When R? When the rest of your thesis is in R (statistics, ggplot, sf). Otherwise Python + geemap has more users and tutorials in 2026.
:::

::: source
source: [rgee installation vignette](https://r-spatial.github.io/rgee/articles/rgee01.html); Moodle lesson page 4
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Which client, when?
:::

::: block <!-- element style="font-size:26px" align="left" drag="95 78" drop="0 15"-->
| Need | Code Editor | Python + geemap | rgee |
|---|---|---|---|
| explore a dataset, test an idea | **best** | ok | ok |
| interactive map with layers | built in | `geemap.Map()` | <code>Map&#36;addLayer</code> |
| repeat for many areas / dates | scripting with lists | **best** (loops, functions, parameters) | good |
| join with field data, statistics, ML outside GEE | no | pandas, scikit-learn, xarray | sf, terra, tidymodels |
| report / thesis with code | copy-paste | Jupyter, Quarto | R Markdown, Quarto |
| share with a non-programmer | Earth Engine **Apps** (`ui.*`) | Streamlit, Solara (geemap) | Shiny |
| setup effort | zero | low (Colab) / medium (local) | medium–high |

Everything in this course can be done in all three – choose the one your thesis needs.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (11.01, 4 h)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. **Colab** (60 min): new notebook, `ee.Authenticate()` with your project; translate your lab 2 script with `geemap.js_snippet_to_py`; fix what the translator missed; the map appears
2. **Bitmasks** (45 min): add the `QA60` mask and the `SCL` mask, compare composites with and without; count masked pixels per month (`ui.Chart` → `geemap.ee_to_df` + pandas plot)
3. **Export** (30 min): NDVI median to Drive in EPSG:2180 and open it in QGIS; time series to CSV
4. **rgee** (60 min, those with R): `ee_check()`, the NDVI example, `ee_extract` of NDVI for 5 points into a data.frame, a ggplot
5. **Capstone** (rest): pick one of labs 4–6 (flood, landslide, fire) and rerun it in Python or R as a notebook with text cells – this is the final deliverable of the course
6. API quiz in the Moodle lesson
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before the last class
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Make sure `ee.Initialize(project=...)` works in Colab **before** 11.01 (two minutes at home saves twenty in the lab)
- [ ] R users: `install.packages("rgee")`, gcloud SDK, `ee_install()` at home; bring the output of `ee_check()`
- [ ] Decide which hazard your capstone notebook will reproduce; have the AOI and dates ready
- [ ] Optional reading: [End-to-End GEE – Python module](https://courses.spatialthoughts.com/end-to-end-gee.html#python-api); [geemap tutorials](https://geemap.org/tutorials/); [Geocomputation with R](https://r.geocompx.org/) ch. 1–2 for R users
:::

---
::: block 
# Thank you :smile:
:::
