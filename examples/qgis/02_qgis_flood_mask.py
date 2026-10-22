# 02_qgis_flood_mask.py - Sentinel-1 flood mask on the QGIS canvas (same method as GEO2/04_floods/03)
# Course: Application of geoinformatics to natural hazards mapping and monitoring - lesson 7, QGIS page
# Run in QGIS: Plugins > Python Console > Show Editor > open > Run. Needs the Google Earth Engine plugin.
# What to change: ROI, BEFORE/AFTER windows, THRESHOLD_DB. Default: September 2024 flood, Nysa Klodzka.

import ee
from ee_plugin import Map

# ---------------------------------------------------------------- PARAMETERS
ROI = ee.Geometry.Rectangle([17.20, 50.40, 17.80, 50.90])
BEFORE = ('2024-08-20', '2024-09-10')
AFTER = ('2024-09-16', '2024-09-28')
PASS = 'DESCENDING'
THRESHOLD_DB = -3          # after - before below this = new water (UN-SPIDER ratio 1.25 ~ -3 dB)
SMOOTH_M = 50

# ---------------------------------------------------------------- SENTINEL-1 VH
s1 = (ee.ImageCollection('COPERNICUS/S1_GRD')
        .filterBounds(ROI)
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .filter(ee.Filter.eq('orbitProperties_pass', PASS))
        .select('VH'))
before = s1.filterDate(*BEFORE).median().focal_median(SMOOTH_M, 'circle', 'meters')
after = s1.filterDate(*AFTER).median().focal_median(SMOOTH_M, 'circle', 'meters')
print('Scenes before / after:', s1.filterDate(*BEFORE).size().getInfo(),
      s1.filterDate(*AFTER).size().getInfo())

# ---------------------------------------------------------------- CHANGE + MASKS
diff = after.subtract(before)
flooded = diff.lt(THRESHOLD_DB)
permanent = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality').gte(10)
slope = ee.Terrain.slope(ee.Image('NASA/NASADEM_HGT/001').select('elevation'))
flooded = (flooded.updateMask(permanent.unmask(0).Not())
                  .updateMask(slope.lt(5))
                  .selfMask()
                  .updateMask(flooded.connectedPixelCount(25).gte(8))
                  .clip(ROI))

ha = (flooded.multiply(ee.Image.pixelArea()).divide(1e4)
      .reduceRegion(ee.Reducer.sum(), ROI, 10, maxPixels=1e10).get('VH'))
print('Flooded area [ha]:', round(ha.getInfo()))

# ---------------------------------------------------------------- SHOW
Map.addLayer(before.clip(ROI), {'min': -25, 'max': -5}, 'S1 VH before (dB)', False)
Map.addLayer(after.clip(ROI), {'min': -25, 'max': -5}, 'S1 VH after (dB)', False)
Map.addLayer(flooded, {'palette': ['0000ff']}, 'Flooded (after - before < %d dB)' % THRESHOLD_DB)
Map.centerObject(ROI, 10)
# Compare with the GeoTIFF exported in lab 4 (Layer > Add Raster Layer) - they must agree.
