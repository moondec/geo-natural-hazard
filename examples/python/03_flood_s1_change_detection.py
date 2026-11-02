"""03 - Sentinel-1 flood extent by change detection (lab 4 in Python).

Python version of the lab 4 script GEO2/04_floods/03_sentinel1_flood_change_detection
(same AOI, dates, filters and masks, so the hectares must agree), step by step:
  1. Sentinel-1 GRD, IW mode, 10 m, VH, one orbit track, sar_before/sar_after mosaics
  2. speckle filter (50 m focal median)
  3. change: sar_after - sar_before < -3 dB  (UN-SPIDER uses the ratio > 1.25 instead)
  4. masks: permanent water (JRC GSW seasonality >= 10), slope >= 5 deg
     (Copernicus DEM GLO-30), isolated specks (< 8 connected pixels)
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
AOI_BBOX = [17.20, 50.40, 17.80, 50.90]

BEFORE_START, BEFORE_END = '2024-08-20', '2024-09-10'   # normal conditions
AFTER_START, AFTER_END = '2024-09-16', '2024-09-28'     # flood peak onwards, >= 12 days

POLARISATION = 'VH'          # VH: open-land floods; VV: flooded vegetation
ORBIT_PASS = 'ASCENDING'     # never mix ASCENDING and DESCENDING
RELATIVE_ORBIT = 175         # one track (GEO2 script 02); None = all tracks of that pass,
                             # which mixes viewing geometries (false changes)
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
      .filter(ee.Filter.eq('resolution_meters', 10))
      .filterBounds(aoi)
      .select(POLARISATION))
if RELATIVE_ORBIT is not None:
    s1 = s1.filter(ee.Filter.eq('relativeOrbitNumber_start', RELATIVE_ORBIT))

s1_before = s1.filterDate(BEFORE_START, BEFORE_END)
s1_after = s1.filterDate(AFTER_START, AFTER_END)


def scene_dates(col):
    """Acquisition dates of a collection as a client-side list of strings."""
    return (col.aggregate_array('system:time_start')
            .map(lambda t: ee.Date(t).format('YYYY-MM-dd')).getInfo())


print('before scenes:', s1_before.size().getInfo(), scene_dates(s1_before))
print('after scenes :', s1_after.size().getInfo(), scene_dates(s1_after))
# If one of them is 0: widen the dates, or change ORBIT_PASS / RELATIVE_ORBIT (GEO2 script 02).

sar_before = s1_before.mosaic().clip(aoi)
sar_after = s1_after.mosaic().clip(aoi)

# -------------------------------------------------------- 2. speckle filter
# focal_median keeps field and river edges sharper than focal_mean.
sar_before_smooth = sar_before.focal_median(SMOOTH_RADIUS_M, 'circle', 'meters')
sar_after_smooth = sar_after.focal_median(SMOOTH_RADIUS_M, 'circle', 'meters')

# ------------------------------------------------------ 3. change detection
# Both images are in dB, so the difference is the honest measure.
# UN-SPIDER uses after.divide(before).gt(1.25) - roughly the same as -3 dB.
difference = sar_after_smooth.subtract(sar_before_smooth).rename('diff_dB')
flooded_raw = difference.lt(DIFF_THRESHOLD_DB).rename('flooded')

# ------------------------------------------------------------------ 4. masks
jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality')
permanent_water = jrc.gte(PERMANENT_WATER_MONTHS).unmask(0)

# Copernicus DEM GLO-30 is a collection of tiles: mosaic it and give the mosaic
# back a projection, otherwise the slope depends on the zoom level.
dem_tiles = ee.ImageCollection('COPERNICUS/DEM/GLO30_2024_1').select('DEM')
dem = dem_tiles.mosaic().setDefaultProjection(dem_tiles.first().projection())
slope = ee.Terrain.slope(dem)


def mask_flood(flood_raw):
    """Masks of step 4; the speck filter goes last, so specks left by the
    water and slope masks are removed as well."""
    masked = (flood_raw.selfMask()                          # keep only 1s
              .updateMask(permanent_water.Not())            # .Not() - capital in Python
              .updateMask(slope.lt(MAX_SLOPE_DEG)))
    connected = masked.connectedPixelCount(25, True)        # 8-neighbourhood
    return masked.updateMask(connected.gte(MIN_CONNECTED_PIXELS))


flooded = mask_flood(flooded_raw)

# ------------------------------------------------------- 5. area in hectares
flood_area = (flooded.multiply(ee.Image.pixelArea()).divide(1e4)
              .reduceRegion(reducer=ee.Reducer.sum(), geometry=aoi,
                            scale=EXPORT_SCALE, maxPixels=1e10))
print('flooded area [ha]:', round(flood_area.get('flooded').getInfo(), 1))

# --------------------------------------------------- sensitivity (optional)
# Rerun the threshold for the M4-style table: threshold vs flooded area,
# with exactly the same masks as above (the -3 dB row equals the main result).
for thr in (-2.0, -3.0, -4.0):
    f = mask_flood(difference.lt(thr).rename('flooded'))
    ha = (f.multiply(ee.Image.pixelArea()).divide(1e4)
          .reduceRegion(ee.Reducer.sum(), aoi, EXPORT_SCALE, maxPixels=1e10)
          .get('flooded').getInfo())
    print('threshold %.1f dB -> %.0f ha' % (thr, ha))

# ----------------------------------------------------------- map (notebook)
# import geemap
# m = geemap.Map()
# m.centerObject(aoi, 11)
# m.addLayer(sar_before_smooth, {'min': -25, 'max': 0}, 'before VH')
# m.addLayer(sar_after_smooth, {'min': -25, 'max': 0}, 'after VH')
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
