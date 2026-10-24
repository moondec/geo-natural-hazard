"""04 - Burn severity with dNBR (lab 6 in Python).

Mirrors the course copy of the UN-SPIDER burn severity script:
  1. Sentinel-2 L2A pre- and post-fire collections (S2_SR_HARMONIZED)
  2. per-pixel cloud mask: SCL (default) or Cloud Score+ (set a flag)
  3. NBR = (B8 - B12) / (B8 + B12) on the median composites
  4. dNBR = NBR_pre - NBR_post, scaled x 1000
  5. USGS severity classes and area per class in hectares
  6. export at 20 m (B12 is a 20 m band)

Default event: Landiras fire, Gironde, France, 12-25 July 2022
(about 14 000 ha of pine forest; a second fire reignited nearby on
9 August 2022, so the post window ends before that).
"""

import ee

# ---------------------------------------------------------------- parameters
PROJECT = 'ee-your-project'

AOI_BBOX = [-0.70, 44.38, -0.30, 44.65]        # Landiras / Hostens, Gironde
PRE_START, PRE_END = '2022-06-15', '2022-07-10'    # before ignition, same season
POST_START, POST_END = '2022-07-26', '2022-08-08'  # smoke gone, ash still there

MAX_CLOUD_PCT = 40            # scene-level pre-filter; the pixel mask does the work
USE_CLOUD_SCORE_PLUS = False  # True -> Cloud Score+ instead of SCL
CS_PLUS_THRESHOLD = 0.6       # keep pixels with cs_cdf >= 0.6
EXPORT_SCALE = 20
# CRS: EPSG code of a METRIC system - Poland 'EPSG:2180'; elsewhere the UTM zone,
# 'EPSG:326' + zone (N) / '327' + zone (S), zone = floor((lon + 180) / 6) + 1; look it up at
# https://epsg.io or in QGIS (Project > Properties > CRS). Never 4326 (degrees) or 3857.
EXPORT_CRS = 'EPSG:2154'      # Lambert-93 for France; use EPSG:2180 in Poland
DRIVE_FOLDER = 'gee'

# USGS classes on the x1000 scale (lab 6, page 3)
CLASS_BREAKS = [-250, -100, 100, 270, 440, 660]
CLASS_NAMES = ['enhanced regrowth, high', 'enhanced regrowth, low', 'unburned',
               'low severity', 'moderate-low severity', 'moderate-high severity',
               'high severity']
CLASS_PALETTE = ['7a8737', 'acbe4d', '0ae042', 'fff70b', 'ffaf38', 'ff641b', 'a41fd6']

try:
    ee.Initialize(project=PROJECT)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=PROJECT)

aoi = ee.Geometry.Rectangle(AOI_BBOX)


# ------------------------------------------------------------ 2. cloud masks
def mask_scl(img):
    """Keep vegetation (4), bare (5), water (6), snow (11); drop clouds,
    shadows, cirrus, unclassified. Add 7 to the list for a looser mask."""
    scl = img.select('SCL')
    keep = scl.remap([4, 5, 6, 11], [1, 1, 1, 1], 0)
    return img.updateMask(keep)


def mask_cs_plus(img):
    """Cloud Score+ mask: the band cs_cdf was linked to the image beforehand."""
    return img.updateMask(img.select('cs_cdf').gte(CS_PLUS_THRESHOLD))


def s2_masked(start, end):
    s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterDate(start, end)
           .filterBounds(aoi)
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD_PCT)))
    if USE_CLOUD_SCORE_PLUS:
        cs_plus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED')
        # linkCollection joins by system:index and adds the cs_cdf band
        s2 = s2.linkCollection(cs_plus, ['cs_cdf']).map(mask_cs_plus)
    else:
        s2 = s2.map(mask_scl)
    return s2


s2_before = s2_masked(PRE_START, PRE_END)
s2_after = s2_masked(POST_START, POST_END)
print('pre scenes :', s2_before.size().getInfo())
print('post scenes:', s2_after.size().getInfo())
# 0 scenes -> widen the window (Sentinel-2 revisit is 5 days).

pre = s2_before.median().clip(aoi)
post = s2_after.median().clip(aoi)


# ------------------------------------------------------------------- 3. NBR
def nbr(img):
    """Normalized Burn Ratio from NIR (B8, 10 m) and SWIR2 (B12, 20 m)."""
    return img.normalizedDifference(['B8', 'B12']).rename('NBR')


nbr_pre = nbr(pre)
nbr_post = nbr(post)

# ------------------------------------------------------------------ 4. dNBR
dnbr = nbr_pre.subtract(nbr_post).multiply(1000).rename('dNBR')

# --------------------------------------------------- 5. classes and areas
# Class 0..6 by counting how many breaks the dNBR value exceeds.
severity = ee.Image.constant(0).rename('severity')
for brk in CLASS_BREAKS:
    severity = severity.add(dnbr.gt(brk))
severity = severity.updateMask(dnbr.mask()).toByte()

# Grouped sum: hectares per class (the grouped reducer from lab 2)
area_img = ee.Image.pixelArea().divide(1e4).addBands(severity)
grouped = area_img.reduceRegion(
    reducer=ee.Reducer.sum().group(groupField=1, groupName='class'),
    geometry=aoi,
    scale=EXPORT_SCALE,
    maxPixels=1e10,
)
groups = grouped.get('groups').getInfo()   # small list -> getInfo is fine
print('\nArea per USGS class [ha]:')
total = 0.0
for g in groups:
    ha = g['sum']
    total += ha
    print('%2d  %-28s %10.0f' % (g['class'], CLASS_NAMES[g['class']], ha))
print('    %-28s %10.0f' % ('total', total))

# dNBR histogram over the AOI (bimodal with the unburned peak near 0?)
hist = dnbr.reduceRegion(
    reducer=ee.Reducer.fixedHistogram(-500, 1300, 36),
    geometry=aoi, scale=100, maxPixels=1e10).get('dNBR').getInfo()
print('\ndNBR histogram (bin start, count) at 100 m:')
for lo, n in hist:
    print('%6.0f %8.0f' % (lo, n))

# ----------------------------------------------------------- map (notebook)
# import geemap
# m = geemap.Map()
# m.centerObject(aoi, 11)
# rgb = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}
# m.addLayer(pre, rgb, 'pre-fire true colour')
# m.addLayer(post, rgb, 'post-fire true colour')
# m.addLayer(dnbr, {'min': -500, 'max': 1300, 'palette': ['white', 'black']}, 'dNBR x1000', False)
# m.addLayer(severity, {'min': 0, 'max': 6, 'palette': CLASS_PALETTE}, 'burn severity (USGS)')
# m.add_legend(title='dNBR severity', labels=CLASS_NAMES, colors=CLASS_PALETTE)
# m

# ------------------------------------------------------------------ 6. export
task = ee.batch.Export.image.toDrive(
    image=severity.unmask(255),
    description='dnbr_severity_landiras_2022-07',
    folder=DRIVE_FOLDER,
    scale=EXPORT_SCALE,
    region=aoi,
    crs=EXPORT_CRS,
    maxPixels=1e10,
)
task.start()
print('export started:', task.status()['state'])
