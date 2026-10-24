"""01 - Hello Earth Engine (lesson 7, lab 7).

Minimal Python script: authenticate, initialise with your Cloud project,
load Sentinel-2 L2A (COPERNICUS/S2_SR_HARMONIZED), filter, compute a
median NDVI and fetch one number with getInfo().

Run in Colab or locally (Python >= 3.11, pip install earthengine-api).
Everything after ee.Initialize() is line by line the same as the
JavaScript from lecture 2 - compare the two.
"""

import ee

# ---------------------------------------------------------------- parameters
PROJECT = 'ee-your-project'          # the Cloud project id from lab 1
AOI_LON, AOI_LAT = 16.93, 52.41      # Poznan, Poland
AOI_BUFFER_M = 5000                  # radius of the study area in metres
DATE_START, DATE_END = '2025-05-01', '2025-09-30'
MAX_CLOUD_PCT = 30                   # scene-level filter (CLOUDY_PIXEL_PERCENTAGE)

# ---------------------------------------------------- authenticate / initialise
# ee.Authenticate() opens a browser window the first time (Colab: every new
# session; locally the token is cached, or run `earthengine authenticate`).
# The project id must be copied exactly from the Cloud console (not the name).
try:
    ee.Initialize(project=PROJECT)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT)

print(ee.String('Hello from Earth Engine').getInfo())

# ----------------------------------------------------------------- the recipe
aoi = ee.Geometry.Point(AOI_LON, AOI_LAT).buffer(AOI_BUFFER_M)

s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterDate(DATE_START, DATE_END)
      .filterBounds(aoi)
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD_PCT)))

# s2.size() is a server object; .getInfo() brings the value to Python.
print('scenes:', s2.size().getInfo())


def add_ndvi(img):
    """Add an NDVI band (B8 = NIR, B4 = red) to a Sentinel-2 image."""
    return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'))


ndvi = s2.map(add_ndvi).select('NDVI').median()

# One small dictionary -> getInfo is fine. Images never go through getInfo.
stats = ndvi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=aoi,
    scale=10,
    maxPixels=1e9,
)
print('mean NDVI in the AOI:', stats.getInfo())
