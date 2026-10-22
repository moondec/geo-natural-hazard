# Examples for lesson 7 – APIs for Google Earth Engine (Python, Colab, QGIS, rgee)

Companion code for lab 7 of *Application of geoinformatics to natural hazards
mapping and monitoring* and for the capstone notebook (milestone M7). Every
script repeats, in Python or R, something you already did in the Code Editor
in labs 2–6; compare them line by line with your JavaScript.

| File | What it does |
|---|---|
| `python/01_hello_earth_engine.py` | authenticate, `ee.Initialize(project=...)`, Sentinel-2 L2A median NDVI around Poznań, one number via `getInfo()` |
| `python/02_geemap_ndvi_map.py` | `geemap.Map`, layers, split map, GeoTIFF export (`geemap.ee_export_image` and `ee.batch.Export.image.toDrive`) |
| `python/03_flood_s1_change_detection.py` | lab 4 in Python: Sentinel-1 VH before/after, difference in dB (< −3 dB), JRC permanent-water and NASADEM slope masks, flooded hectares, export – Nysa Kłodzka, September 2024 |
| `python/04_dnbr_burn_severity.py` | lab 6 in Python: pre/post Sentinel-2 with SCL (or Cloud Score+) mask, NBR, dNBR × 1000, USGS classes, hectares per class – Landiras fire, Gironde, July 2022 |
| `notebooks/07_capstone_template.ipynb` | template for the capstone notebook: text cells (event, data, method, results, limitations) + the code of 03/04 inline so it runs standalone in Colab |
| `qgis/01_qgis_console_ndvi.py` | QGIS Python Console with the Google Earth Engine plugin: NDVI median as a live layer |
| `qgis/02_qgis_flood_mask.py` | Sentinel-1 before/after flood mask on the QGIS canvas (lab 4 method) |
| `qgis/03_qgis_dnbr_classes.py` | dNBR burn severity classes and hectares per class in QGIS (lab 6 method) |
| `R/01_rgee_hello.R` | rgee: `ee_Initialize(project=...)`, NDVI median, `Map$addLayer`, `ee_as_rast`, `ee_extract` |
| `R/02_rgee_dnbr.R` | dNBR burn severity in R with rgee, hectares per class, raster to terra |

All parameters (project id, ROI, dates, thresholds) sit at the top of each
file. Replace `ee-your-project` with the Cloud project id you registered in
lab 1 (copy the **id**, not the project name, from the Cloud console).

## Open in Google Colab

1. Go to [colab.research.google.com](https://colab.research.google.com/) and sign in with the Google account that has Earth Engine access.
2. *File → Open notebook → GitHub*, enter `moondec/geo-natural-hazard`, choose `examples/notebooks/07_capstone_template.ipynb`.
   Direct link: `https://colab.research.google.com/github/moondec/geo-natural-hazard/blob/main/examples/notebooks/07_capstone_template.ipynb`
3. Run the first cell (installs `geemap` if missing, then `ee.Authenticate()` and `ee.Initialize(project=...)`). A browser window asks you to sign in once per session.
4. *File → Save a copy in Drive* before editing – the GitHub copy is read-only.

To run a `.py` script in Colab: paste its content into a code cell (remove nothing; `ee.Authenticate()` is called automatically when `ee.Initialize` fails), or upload it and run `%run 03_flood_s1_change_detection.py`.

## Local setup (Jupyter, VS Code, Positron)

Python 3.11 or newer is required by the current `earthengine-api`.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/macOS: source .venv/bin/activate
pip install earthengine-api geemap jupyterlab
earthengine authenticate      # once; the token is cached in your home directory
```

Then in Python:

```python
import ee
ee.Initialize(project='your-project-id')
print(ee.String('Hello from Earth Engine').getInfo())
```

The first `earthengine authenticate` may ask for the **gcloud CLI**
(Google Cloud SDK); install it from cloud.google.com/sdk and run `gcloud init`.
`conda install -c conda-forge earthengine-api geemap` is the alternative
to pip. The `geemap.Map` widget renders only inside a notebook; run as a
plain script the examples still print the numbers and start the exports.

## Which CRS? (EXPORT_CRS, UTM_CRS, GRID_CRS)

Use the EPSG code of a metric system: Poland `EPSG:2180` (PUWG 1992); elsewhere the
UTM zone of your area, `EPSG:326` + zone (northern hemisphere) or `327` + zone (southern),
zone = floor((longitude + 180) / 6) + 1 (Poznan 33 -> 32633, Gironde 30 -> 32630,
Hokkaido 54 -> 32654). Look codes up at https://epsg.io or in QGIS (Project > Properties
> CRS); `image.projection().getInfo()` shows the native CRS of a dataset. Never export in
`EPSG:4326` (degrees) or `EPSG:3857` (Web Mercator) - `scale` in metres and areas are only
right in a metric CRS.

## QGIS and the Google Earth Engine plugin

Needs QGIS 3.44 or newer (QGIS 4 works). *Plugins → Manage and Install Plugins → All*,
search "Google Earth Engine" (version 0.3.3, August 2026), install. On first start the
plugin opens a browser tab to sign in and then asks for your Cloud project name
(Code Editor → account name → *Project Info* → *Cloud Project*). Run the `qgis/*.py`
scripts from *Plugins → Python Console → Show Editor*. Layers added by the plugin are
Earth Engine tiles (view only); export with *Processing → Google Earth Engine → Export
GeoTIFF* or with `Export.image.toDrive` in the Code Editor and open the file in QGIS.

Traps: old QGIS (< 3.44) → use the export path; do not `pip install earthengine-api`
into the QGIS Python (the plugin ships its own); stale credentials → delete
`~/.config/earthengine/credentials`, run `import ee; ee.Authenticate()` in the console;
unregistered Cloud project; tiles are not data (measure only exported files, in a
metric CRS such as EPSG:2180). User guide and troubleshooting:
https://gee-community.github.io/qgis-earthengine-plugin/

## R and rgee (volunteers)

```r
install.packages("rgee")
library(rgee)
ee_install(py_env = "rgee")   # once (about 200 MB, do it at home); answer Y, restart R
ee_check()                    # Python >= 3.11, earthengine-api, credentials
ee_Initialize(project = "your-project-id", drive = TRUE)
```

The first authentication of a new user needs the gcloud CLI on every operating
system (see the lesson page *rgee*). If rgee refuses to start:
`ee_clean_pyenv(); ee_install()` and read the error message.
`R/01_rgee_hello.R` also needs `terra` and `sf` (`install.packages(c("terra", "sf"))`).

## Data used

| Asset id | Used for |
|---|---|
| `COPERNICUS/S2_SR_HARMONIZED` | Sentinel-2 Level-2A surface reflectance (NDVI, NBR, SCL mask) |
| `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` | Cloud Score+ per-pixel quality (`cs_cdf >= 0.6`), optional mask in 04 |
| `COPERNICUS/S1_GRD` | Sentinel-1 GRD backscatter in dB (flood change detection) |
| `JRC/GSW1_4/GlobalSurfaceWater` | permanent water mask (`seasonality >= 10`) |
| `NASA/NASADEM_HGT/001` | DEM for the slope mask (< 5°) |

## Capstone notebook (M7)

Pick one hazard from labs 4–6 and reproduce it in Python or R as a notebook
with text cells: introduction and method, the parameters (AOI, dates,
thresholds, collections), figures (map, histogram or time series), the area
numbers and a section on limitations (clouds, phenology, resolution,
validation). Start from `notebooks/07_capstone_template.ipynb`, delete the
workflow you do not use, and share the link (Drive or GitHub) in Moodle. A
colleague must be able to run all cells top to bottom after
`ee.Initialize(project=...)` and get the same map and numbers.

Nothing here contains credentials; never commit a token or a service-account key.
