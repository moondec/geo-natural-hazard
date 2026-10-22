"""02 - geemap: the map, the split map, the exporter (lesson 7, lab 7).

Shows the three things geemap adds to the plain ee API:
  1. an interactive map in the notebook (geemap.Map, addLayer)
  2. a split map to compare two layers (true colour vs NDVI)
  3. getting a raster out: a small GeoTIFF straight to disk with
     geemap.ee_export_image, or a bigger one to Drive with ee.batch.Export.

In Colab run: !pip install geemap --quiet   (if import fails).
The map widget only renders inside a notebook (Colab / Jupyter);
run as a plain script it still computes and exports.
"""

import ee
import geemap

# ---------------------------------------------------------------- parameters
PROJECT = 'ee-your-project'
ROI_LON, ROI_LAT = 16.93, 52.41      # Poznan
ROI_BUFFER_M = 5000
DATE_START, DATE_END = '2025-05-01', '2025-09-30'
MAX_CLOUD_PCT = 30
EXPORT_SCALE = 10                    # m; B4/B8 are 10 m bands
# CRS: EPSG code of a METRIC system - Poland 'EPSG:2180'; elsewhere the UTM zone,
# 'EPSG:326' + zone (N) / '327' + zone (S), zone = floor((lon + 180) / 6) + 1; look it up at
# https://epsg.io or in QGIS (Project > Properties > CRS). Never 4326 (degrees) or 3857.
EXPORT_CRS = 'EPSG:2180'             # Polish national grid - opens in QGIS with other PL data
LOCAL_TIF = 'ndvi_poznan_2025.tif'   # small export to disk (ee_export_image, < 32 MB)
DRIVE_FOLDER = 'gee'                 # Drive folder for the background export

try:
    ee.Initialize(project=PROJECT)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT)

# ------------------------------------------------------------------ data
roi = ee.Geometry.Point(ROI_LON, ROI_LAT).buffer(ROI_BUFFER_M)

s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterDate(DATE_START, DATE_END)
      .filterBounds(roi)
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD_PCT)))


def add_ndvi(img):
    return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'))


with_ndvi = s2.map(add_ndvi)
ndvi = with_ndvi.select('NDVI').median().clip(roi)
rgb = with_ndvi.select(['B4', 'B3', 'B2']).median().clip(roi)

ndvi_vis = {'min': -0.2, 'max': 0.8,
            'palette': ['blue', 'white', 'yellow', 'green', 'darkgreen']}
rgb_vis = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}

# ------------------------------------------------------------ 1. the map
m = geemap.Map(center=[ROI_LAT, ROI_LON], zoom=11)
m.addLayer(rgb, rgb_vis, 'S2 true colour (median)')
m.addLayer(ndvi, ndvi_vis, 'NDVI median')
m.addLayer(roi, {'color': 'red'}, 'ROI', False)
m  # noqa: B018  - last expression in a notebook cell displays the map

# ------------------------------------------------------ 2. the split map
# Left: true colour, right: NDVI. Drag the slider in the notebook.
left = geemap.ee_tile_layer(rgb, rgb_vis, 'true colour')
right = geemap.ee_tile_layer(ndvi, ndvi_vis, 'NDVI')
m2 = geemap.Map(center=[ROI_LAT, ROI_LON], zoom=11)
m2.split_map(left_layer=left, right_layer=right)
m2  # noqa: B018

# --------------------------------------------- 3a. small GeoTIFF to disk
# Synchronous download through getDownloadURL - fine for a few MB.
# ROI of 10 km diameter at 10 m = about 1e6 pixels, one float band -> OK.
geemap.ee_export_image(
    ndvi,
    filename=LOCAL_TIF,
    scale=EXPORT_SCALE,
    region=roi,
    crs=EXPORT_CRS,
    file_per_band=False,
)
print('written', LOCAL_TIF)

# ------------------------------------------- 3b. bigger raster to Drive
# Asynchronous: starts a task, continue working, check task.status().
# maxPixels default (1e8) is exceeded by a 10 m export of a district.
task = ee.batch.Export.image.toDrive(
    image=ndvi,
    description='ndvi_poznan_2025_median',   # becomes the file name
    folder=DRIVE_FOLDER,
    scale=EXPORT_SCALE,
    region=roi,
    crs=EXPORT_CRS,
    maxPixels=1e10,
)
task.start()
print('Drive export started:', task.status()['state'])
# later: print(task.status()['state'])  -> READY / RUNNING / COMPLETED / FAILED
