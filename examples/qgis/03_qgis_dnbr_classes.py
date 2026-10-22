# 03_qgis_dnbr_classes.py - burn severity classes (dNBR, USGS) on the QGIS canvas (as GEO2/06_wildfires/02)
# Course: Application of geoinformatics to natural hazards mapping and monitoring - lesson 7, QGIS page
# Run in QGIS: Plugins > Python Console > Show Editor > open > Run. Needs the Google Earth Engine plugin.
# What to change: AOI, PRE/POST windows. Default: Landiras fire, Gironde, July 2022.

import ee
from ee_plugin import Map

# ---------------------------------------------------------------- PARAMETERS
AOI = ee.Geometry.Rectangle([-0.62, 44.36, -0.20, 44.64])
PRE = ('2022-06-15', '2022-07-11')
POST = ('2022-07-26', '2022-08-08')
MAX_CLOUD = 40
THRESHOLDS = [-250, -100, 100, 270, 440, 660]     # USGS dNBR x 1000 class breaks
CLASS_NAMES = ['Enhanced regrowth, high', 'Enhanced regrowth, low', 'Unburned',
               'Low severity', 'Moderate-low', 'Moderate-high', 'High severity']
PALETTE = ['7a8737', 'acbe4d', '0ae042', 'fff70b', 'ffaf38', 'ff641b', 'a41fd6']


# ---------------------------------------------------------------- SENTINEL-2 with SCL mask
def mask_scl(img):
    scl = img.select('SCL')
    good = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return img.updateMask(good).copyProperties(img, ['system:time_start'])


s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(AOI)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD)).map(mask_scl))
pre = s2.filterDate(*PRE).median().clip(AOI)
post = s2.filterDate(*POST).median().clip(AOI)
print('Scenes pre / post:', s2.filterDate(*PRE).size().getInfo(), s2.filterDate(*POST).size().getInfo())


def nbr(img):
    return img.normalizedDifference(['B8', 'B12'])


dnbr = nbr(pre).subtract(nbr(post)).multiply(1000).rename('dNBR')
severity = dnbr.gt(ee.Image.constant(THRESHOLDS)).reduce(ee.Reducer.sum()).toInt().rename('severity')

# hectares per class (0..6)
groups = ee.List(ee.Image.pixelArea().divide(1e4).addBands(severity).reduceRegion(
    reducer=ee.Reducer.sum().group(groupField=1, groupName='class'),
    geometry=AOI, scale=20, maxPixels=1e10).get('groups')).getInfo()
for g in groups:
    print('%-24s %8.0f ha' % (CLASS_NAMES[g['class']], g['sum']))

# ---------------------------------------------------------------- SHOW
Map.addLayer(post, {'bands': ['B12', 'B8', 'B4'], 'min': 0, 'max': 4000}, 'S2 post-fire SWIR composite', False)
Map.addLayer(dnbr, {'min': -500, 'max': 1000, 'palette': ['00ff00', 'ffffff', 'ff0000']}, 'dNBR x1000', False)
Map.addLayer(severity, {'min': 0, 'max': 6, 'palette': PALETTE}, 'Burn severity (USGS classes)')
Map.centerObject(AOI, 11)
# For the map: export severity as a Byte GeoTIFF (EPSG:2180 in Poland) and style it as Paletted in QGIS.
