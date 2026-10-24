# 01_qgis_console_ndvi.py - Earth Engine inside QGIS (Google Earth Engine plugin >= 0.3, QGIS >= 3.44)
# Course: Application of geoinformatics to natural hazards mapping and monitoring - lesson 7, QGIS page
# Run in QGIS: Plugins > Python Console > Show Editor (notepad icon) > open this file > Run script.
# The plugin signs you in once (browser) and asks for your Cloud project (Code Editor > Project Info).
# What to change: AOI, dates, cloud threshold.

import ee
from ee_plugin import Map          # the plugin's Map: addLayer / centerObject like geemap

# ---------------------------------------------------------------- PARAMETERS
aoi = ee.Geometry.Point(16.93, 52.41).buffer(5000)   # Poznan; replace with your area
START, END = '2025-05-01', '2025-09-30'
MAX_CLOUD = 30

# ---------------------------------------------------------------- COMPUTE (server side)
s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi).filterDate(START, END)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD)))


def add_ndvi(img):
    return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'))


ndvi = s2.map(add_ndvi).select('NDVI').median().clip(aoi)
print('Scenes used:', s2.size().getInfo())          # printed in the QGIS Python console

# ---------------------------------------------------------------- SHOW (tiles on the canvas)
Map.addLayer(s2.median().clip(aoi), {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000},
             'S2 median true colour', False)
Map.addLayer(ndvi, {'min': -0.2, 'max': 0.8,
             'palette': ['blue', 'white', 'yellow', 'green', 'darkgreen']}, 'NDVI median 2025')
Map.centerObject(aoi, 11)

# The layers are rendered by Earth Engine on the fly - zoom and overlay, do not measure.
# To get a file: Processing > Google Earth Engine > Export GeoTIFF, or Export from the Code Editor.
