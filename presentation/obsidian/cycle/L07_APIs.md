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
summary: "Wykład 7 (2 h, 21.12.2026) – GEE poza Code Editorem: API Pythona, Google Colab, geemap, różnice JS/Python, obiekty klienta vs serwera, maski chmur i bity QA, eksport, GEE w QGIS (wtyczka i eksport do kompozycji mapy), rgee dla chętnych, CDSE JupyterLab/openEO dla zainteresowanych; wstęp do ćwiczeń 7 (4 h, Colab + geemap + rgee)"
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
#### Python, Colab, geemap and QGIS

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
2. The same engine, many clients: JavaScript, Python (`ee`), QGIS (plugin), R (`rgee`)
3. Google Colab and Jupyter: a notebook in 5 minutes
4. `geemap`: the map, the translator, the exporter
5. JavaScript → Python: the seven differences
6. Getting data out: exports, `getInfo`, time series to pandas / data.frame
7. QGIS step by step: plugin and sign-in, Python Console, no-code tools and export, the finished map
8. Traps of the plugin; rgee for R volunteers
9. **In the lab (4 h)**: Colab notebook + four QGIS pages + capstone
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
::: title
## GEE in QGIS: two doors
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:28px" align="left" drag="47 80" drop="0 15"-->
**Door A – export, then QGIS (always works)**
1. `Export.image.toDrive({image: severity.toByte(), region: AOI, scale: 20, crs: 'EPSG:2180'})` – Tasks → Run; EPSG code from [epsg.io](https://epsg.io) or the QGIS CRS selector: Poland 2180, elsewhere UTM 326 + zone
2. Download from Drive, *Layer → Add Raster Layer*; the CSV of hectares as a delimited text layer
3. *Symbology → Paletted / Unique values*: class names and colours; no-data transparent
4. *Print Layout*: title, legend, scale bar, source line, your vectors (EMS / EFFIS perimeter) → PDF
5. Vectors: `Export.table.toDrive({..., fileFormat: 'GeoJSON'})` → intersection, area in hectares

Earth Engine computes, QGIS makes the map – the format of M4–M7.
:::

::: block <!-- element style="font-size:24px" align="left" drag="50 80" drop="49 15" bg="#e8f4f8" pad="12px"-->
**Door B – the Google Earth Engine plugin** (0.3.3, Aug 2026; QGIS ≥ 3.44)
*Plugins → Manage and Install → "Google Earth Engine"* → sign in → paste your Cloud project (Code Editor → *Project Info*)
<pre><code class="language-python">import ee
from ee_plugin import Map              # instead of geemap.Map
roi = ee.Geometry.Point(16.93, 52.41).buffer(5000)
s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(roi).filterDate('2025-05-01', '2025-09-30'))
ndvi = s2.map(lambda i: i.normalizedDifference(['B8', 'B4'])).median()
Map.addLayer(ndvi.clip(roi), {'min': -0.2, 'max': 0.8,
   'palette': ['blue', 'white', 'yellow', 'green', 'darkgreen']}, 'NDVI')
Map.centerObject(roi, 11)
</code></pre>
No code: *Data Catalog*, Processing → *Add EE Image / Image Collection / Feature Collection*, *Export GeoTIFF*. Layers are tiles: look and overlay, export to measure.
:::

::: source
source: [QGIS Earth Engine plugin – user guide](https://gee-community.github.io/qgis-earthengine-plugin/); Moodle lesson page 4; examples/qgis on GitHub
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Traps: QGIS, and rgee for R volunteers
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:26px" align="left" drag="47 80" drop="0 15"-->
**QGIS + plugin**
- QGIS < 3.44 (lab machines!) → nothing loads; use Door A
- QGIS has its **own Python** (OSGeo4W): never `pip install earthengine-api` into it – the plugin ships its copy ("SRE module mismatch")
- stale or wrong-account token in `~/.config/earthengine/credentials` → delete it, `import ee; ee.Authenticate()` in the console, re-enable the plugin
- "Project … is not registered" → the registered project from lab 1, name from *Project Info*
- **tiles are not data**: no measuring, no zonal stats on plugin layers – export with explicit scale and CRS; areas in a metric CRS (EPSG:2180), never 4326
- big exports time out → Drive tasks from the Code Editor; proxies / firewalls → Door A; macOS: *Install Certificates.command*
:::

::: block <!-- element style="font-size:24px" align="left" drag="50 80" drop="49 15" bg="#e8f4f8" pad="12px"-->
**rgee** (R calls the Python API through reticulate; <code>&#36;</code> instead of <code>.</code>; results → terra, sf, data.frame) – for those whose thesis is in R
<pre><code class="language-r">install.packages(&quot;rgee&quot;); library(rgee)
ee_install(py_env = &quot;rgee&quot;)   # once, ~200 MB, restart R
ee_check(); ee_Initialize(project = &quot;your-project-id&quot;, drive = TRUE)
</code></pre>
- a **second Python**: reticulate may pick Anaconda / QGIS / system Python – `ee_check()` shows which; reset with `ee_clean_pyenv(); ee_install()`
- first sign-in needs the **gcloud CLI** (`gcloud init`), any OS
- **version lag**: CRAN 1.1.8 (2025), community-maintained; after an API update pin an older `earthengine-api` (`ee_install_upgrade`)
- Drive / GCS extras (`googledrive`) for `ee_as_rast(via = "drive")`, `ee_extract`
- R functions in `map()` must return `ee` objects; spaces or Polish letters in the Windows user folder break Miniconda
:::

::: source
source: [plugin troubleshooting](https://gee-community.github.io/qgis-earthengine-plugin/troubleshooting/); [rgee installation vignette](https://r-spatial.github.io/rgee/articles/rgee01.html)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## For the curious: beyond Google – CDSE JupyterLab and openEO
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:26px" align="left" drag="56 80" drop="0 15"-->
**Optional, not assessed.** The Copernicus Data Space Ecosystem (your lab-1 account) also has a free hosted **JupyterLab** (on request, 2 working days; kernels Python / Geo Science / OpenEO / Sentinel Hub; 10 GB `mystorage`, server stops after 8 h idle) and **openEO**, an open cloud-processing API.

| CDSE gives you | Earth Engine |
|---|---|
| Sentinel scenes **at the source**, hours after acquisition | mirrored with a delay |
| **Sentinel-1 SLC** → InSAR (deformation, coherence) | GRD only, no phase |
| the **original products** as files (S3, download) | derived exports only |
| **openEO**: one process graph, several backends (Terrascope, EODC…) | Google only |
| EU account, **no Google Cloud project** | registered project required |
| | **1000+ datasets**, classifiers, instant map, free quota |

Use it when the thesis needs InSAR or the original product, when Google is not allowed, or when yesterday's scene matters. Moodle lesson 7 has the optional page; `examples/python/05_cdse_openeo_ndvi.py`.
:::

::: block <!-- element style="font-size:22px" align="left" drag="39 80" drop="58 15" bg="#e8f4f8" pad="12px"-->
The lesson-2 NDVI median, written for openEO:
<pre><code class="language-python">import openeo
con = openeo.connect("openeo.dataspace.copernicus.eu").authenticate_oidc()
s2 = con.load_collection("SENTINEL2_L2A",
    spatial_extent={"west":16.80,"south":52.33,"east":17.06,"north":52.49},
    temporal_extent=["2025-05-01","2025-09-30"],
    bands=["B04","B08","SCL"], max_cloud_cover=30)
scl = s2.band("SCL")
clouds = (scl==3)|(scl==8)|(scl==9)|(scl==10)
ndvi = s2.ndvi(nir="B08", red="B04").mask(clouds)
ndvi.reduce_dimension(dimension="t", reducer="median") \
    .download("ndvi_poznan_2025.tiff")
</code></pre>
Same three verbs – load/filter, map, reduce – on a **datacube** (x, y, t, bands); nothing runs until `download()`. Big areas: `execute_batch()` = Export.
:::

::: source
source: [CDSE JupyterLab](https://dataspace.copernicus.eu/analyse/jupyterlab); [openEO Python client](https://open-eo.github.io/openeo-python-client/)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Which client, when?
:::

::: block <!-- element style="font-size:26px" align="left" drag="95 78" drop="0 15"-->
| Need | Code Editor | Python + geemap | QGIS (plugin / export) |
|---|---|---|---|
| explore a dataset, test an idea | **best** | ok | Data Catalog, Add EE Image |
| interactive map with layers | built in | `geemap.Map()` | canvas tiles + your own layers |
| repeat for many areas / dates | scripting with lists | **best** (loops, functions, parameters) | Processing models, console |
| join with field data, statistics, ML outside GEE | no | pandas, scikit-learn, xarray | **best** for overlay and joins (after export) |
| report / thesis with code | copy-paste | Jupyter, Quarto | Print Layout → PDF, Atlas |
| share with a non-programmer | Earth Engine **Apps** (`ui.*`) | Streamlit, Solara (geemap) | QGIS project, QField |
| setup effort | zero | low (Colab) / medium (local) | low (plugin) / zero (export) |

Everything in this course can be done in all of them (R users: rgee, community-maintained; CDSE openEO for the curious) – choose what your thesis needs.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (11.01, 4 h)
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. **Colab** (45 min): new notebook, `ee.Authenticate()` with your project; translate your lab 2 script with `geemap.js_snippet_to_py`; fix what the translator missed; the map appears
2. **QGIS 1–2** (45 min): install the plugin, sign in, set the project; the NDVI median from the Python Console; identify tool
3. **QGIS 3** (45 min): Add Image Collection without code, Data Catalog, Export Image to GeoTIFF in EPSG:2180; the flood or dNBR script of your event
4. **QGIS** (60 min): plugin or export path; NDVI in the Python Console; the map of your M4–M6 result with legend, scale bar and hectares (Print Layout → PDF)
5. **Capstone** (rest): pick one of labs 4–6 (flood, landslide, fire) and rerun it as a Python notebook or a QGIS project with a PDF map and a short report (R volunteers: rgee) – this is the final deliverable of the course
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
- [ ] Install QGIS ≥ 3.44 and the **Google Earth Engine** plugin at home, sign in once; R volunteers: `install.packages("rgee")`, gcloud CLI, `ee_install()`
- [ ] Decide which hazard your capstone notebook will reproduce; have the AOI and dates ready
- [ ] Optional reading: [End-to-End GEE – Python module](https://courses.spatialthoughts.com/end-to-end-gee.html#python-api); [geemap tutorials](https://geemap.org/tutorials/); [QGIS plugin user guide](https://gee-community.github.io/qgis-earthengine-plugin/); [Geocomputation with R](https://r.geocompx.org/) ch. 1–2 for R volunteers
:::

---
::: block 
# Thank you :smile:
:::
