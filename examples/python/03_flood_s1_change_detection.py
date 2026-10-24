"""03 - Sentinel-1 flood extent by change detection (lab 4 in Python).

Mirrors the updated UN-SPIDER script from lab 4, step by step:
  1. Sentinel-1 GRD, IW mode, VH, one orbit direction, before/after mosaics
  2. speckle filter (50 m focal mean)
  3. change: after - before < -3 dB  (the cleaner equivalent of ratio > 1.25)
  4. masks: permanent water (JRC GSW seasonality >= 10), slope >= 5 deg
     (NASADEM), isolated specks (< 8 connected pixels)
  5. flooded area in hectares (pixelArea + reduceRegion)
  6. export of the flood layer to Drive

Default event: Nysa Klodzka valley, south-west Poland, September 2024
(Copernicus EMS activation EMSR756; flood peak around 15-17 September).
"""

import ee

# ---------------------------------------------------------------- parameters
PROJECT = 'ee-your-project'

# Area of interest: rectangle around Nysa and the Nysa Klodzka valley
# [west, south, east, north] in degrees (WGS84).
AOI_BBOX = [17.05, 50.38, 17.75, 50.62]

BEFORE_START, BEFORE_END = '2024-08-20', '2024-09-10'   # normal conditions
AFTER_START, AFTER_END = '2024-09-16', '2024-09-25'     # flood peak onwards

POLARISATION = 'VH'          # VH: open-land floods; VV: flooded vegetation
ORBIT_PASS = 'DESCENDING'    # never mix ASCENDING and DESCENDING
SMOOTH_RADIUS_M = 50         # speckle filter radius
DIFF_THRESHOLD_DB = -3.0     # flooded where after - before < this (dB)
PERMANENT_WATER_MONTHS = 10  # JRC seasonality >= 10 months/yr = permanent
MAX_SLOPE_DEG = 5            # steeper = radar shadow, not water
MIN_CONNECTED_PIXELS = 8     # remove isolated specks
EXPORT_SCALE = 10
# CRS: EPSG code of a METRIC system - Poland 'EPSG:2180'; elsewhere the UTM zone,
# 'EPSG:326' + zone (N) / '327' + zone (S), zone = floor((lon + 180) / 6) + 1; look it up at
# https://epsg.io or in QGIS (Project > Properties > CRS). Never 4326 (degrees) or 3857.
EXPORT_CRS = 'EPSG:2180'
DRIVE_FOLDER = 'gee'

try:
    ee.Initialize(project=PROJECT)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT)

aoi = ee.Geometry.Rectangle(AOI_BBOX)

# ------------------------------------------------- 1. Sentinel-1 collection
s1 = (ee.ImageCollection('COPERNICUS/S1_GRD')
      .filter(ee.Filter.eq('instrumentMode', 'IW'))
      .filter(ee.Filter.listContains('transmitterReceiverPolarisation', POLARISATION))
      .filter(ee.Filter.eq('orbitProperties_pass', ORBIT_PASS))
      .filterBounds(aoi)
      .select(POLARISATION))

s1_before = s1.filterDate(BEFORE_START, BEFORE_END)
s1_after = s1.filterDate(AFTER_START, AFTER_END)
print('before scenes:', s1_before.size().getInfo())
print('after scenes :', s1_after.size().getInfo())
# If one of them is 0: widen the dates or switch ORBIT_PASS.

before = s1_before.mosaic().clip(aoi)
after = s1_after.mosaic().clip(aoi)

# -------------------------------------------------------- 2. speckle filter
before_f = before.focal_mean(SMOOTH_RADIUS_M, 'circle', 'meters')
after_f = after.focal_mean(SMOOTH_RADIUS_M, 'circle', 'meters')

# ------------------------------------------------------ 3. change detection
# Both images are in dB, so the difference is the honest measure.
# UN-SPIDER uses after.divide(before).gt(1.25) - roughly the same as -3 dB.
difference = after_f.subtract(before_f).rename('diff_dB')
flooded_raw = difference.lt(DIFF_THRESHOLD_DB).rename('flooded')

# ------------------------------------------------------------------ 4. masks
jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality')
permanent_water = jrc.gte(PERMANENT_WATER_MONTHS)

dem = ee.Image('NASA/NASADEM_HGT/001').select('elevation')
slope = ee.Terrain.slope(dem)

flooded = (flooded_raw
           .updateMask(flooded_raw)                       # keep only 1s
           .updateMask(permanent_water.unmask(0).Not())   # .Not() - capital in Python
           .updateMask(slope.lt(MAX_SLOPE_DEG))
           .updateMask(flooded_raw.connectedPixelCount(25).gte(MIN_CONNECTED_PIXELS)))

# ------------------------------------------------------- 5. area in hectares
area_ha = (flooded.multiply(ee.Image.pixelArea()).divide(1e4)
           .reduceRegion(reducer=ee.Reducer.sum(), geometry=aoi,
                         scale=EXPORT_SCALE, maxPixels=1e10))
print('flooded area [ha]:', round(area_ha.get('flooded').getInfo(), 1))

# --------------------------------------------------- sensitivity (optional)
# Rerun the threshold for the M4-style table: threshold vs flooded area.
for thr in (-2.0, -3.0, -4.0):
    f = (difference.lt(thr)
         .updateMask(permanent_water.unmask(0).Not())
         .updateMask(slope.lt(MAX_SLOPE_DEG)))
    ha = (f.multiply(ee.Image.pixelArea()).divide(1e4)
          .reduceRegion(ee.Reducer.sum(), aoi, EXPORT_SCALE, maxPixels=1e10)
          .get('diff_dB').getInfo())
    print('threshold %.1f dB -> %.0f ha' % (thr, ha))

# ----------------------------------------------------------- map (notebook)
# import geemap
# m = geemap.Map()
# m.centerObject(aoi, 11)
# m.addLayer(before_f, {'min': -25, 'max': 0}, 'before VH')
# m.addLayer(after_f, {'min': -25, 'max': 0}, 'after VH')
# m.addLayer(difference, {'min': -10, 'max': 10, 'palette': ['red', 'white', 'blue']}, 'diff dB', False)
# m.addLayer(flooded, {'palette': ['0000FF']}, 'flooded')
# m

# ------------------------------------------------------------------ 6. export
task = ee.batch.Export.image.toDrive(
    image=flooded.unmask(0).toByte(),
    description='flood_nysa_klodzka_2024-09_VH_m3dB',
    folder=DRIVE_FOLDER,
    scale=EXPORT_SCALE,
    region=aoi,
    crs=EXPORT_CRS,
    maxPixels=1e10,
)
task.start()
print('export started:', task.status()['state'])
