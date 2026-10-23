"""
05 – For the curious: the lesson-2 NDVI median without Google – CDSE openEO.

Optional companion to lesson 7 ("For the curious: what CDSE JupyterLab and openEO
give you beyond Earth Engine"). It repeats the Poznań NDVI median of lesson 2 on the
Copernicus Data Space Ecosystem: Sentinel-2 L2A straight from ESA, cloud mask from
the SCL band, median over the season, GeoTIFF for QGIS.

Runs in CDSE JupyterLab (kernel "OpenEO", nothing to install), in Colab or locally:
    pip install openeo
Login: authenticate_oidc() prints a link and a code – log in with the CDSE account
from lab 1 (the same one as Copernicus Browser). The refresh token is cached, so the
second run does not ask again.

Compare with the Earth Engine version (examples/python/01_hello_earth_engine.py and
lesson 2): the three verbs are the same – load/filter, map, reduce – but openEO works
on a datacube with named dimensions (x, y, t, bands) and computes only on download().
"""
import openeo

# ---------------------------------------------------------------- parameters
BBOX = {"west": 16.80, "south": 52.33, "east": 17.06, "north": 52.49}   # Poznań, degrees (WGS84)
DATES = ["2025-05-01", "2025-09-30"]
MAX_CLOUD = 30            # scene-level filter, like CLOUDY_PIXEL_PERCENTAGE in Earth Engine
OUT = "ndvi_poznan_2025.tiff"
EXPORT_EPSG = None        # e.g. 2180 for PUWG 1992; None keeps the native UTM grid (EPSG:32633 here).
                          # Where to find the code: https://epsg.io, or QGIS > Project > Properties > CRS.

# ---------------------------------------------------------------- 1. connect and log in
con = openeo.connect("openeo.dataspace.copernicus.eu").authenticate_oidc()

# ---------------------------------------------------------------- 2. load and filter (one call)
s2 = con.load_collection(
    "SENTINEL2_L2A",                       # Earth Engine: COPERNICUS/S2_SR_HARMONIZED
    spatial_extent=BBOX,
    temporal_extent=DATES,
    bands=["B04", "B08", "SCL"],           # two-digit band names (B04, not B4)
    max_cloud_cover=MAX_CLOUD,
)
# A WARNING "Failed to get/parse queryables ..." may appear here: the client could not download the
# list of filterable properties from CDSE and skips its local check. The filter is still applied; ignore it.

# ---------------------------------------------------------------- 3. map: cloud mask + NDVI per scene
scl = s2.band("SCL")
clouds = (scl == 3) | (scl == 8) | (scl == 9) | (scl == 10)   # shadow, cloud medium/high, cirrus (lesson 2, step 5)
ndvi = s2.ndvi(nir="B08", red="B04").mask(clouds)             # mask() hides pixels where the mask is True

# ---------------------------------------------------------------- 4. reduce: median over time
ndvi_median = ndvi.reduce_dimension(dimension="t", reducer="median")
if EXPORT_EPSG:
    ndvi_median = ndvi_median.resample_spatial(projection=EXPORT_EPSG, resolution=10)

# ---------------------------------------------------------------- 5. get the result
# download() is synchronous and limited to small requests (a city at 10 m is fine).
# For a district or a year use a batch job – the openEO equivalent of Export in the Code Editor:
#     job = ndvi_median.execute_batch(OUT, title="NDVI median Poznan 2025")
ndvi_median.download(OUT)
print("written", OUT, "- open it in QGIS next to the Earth Engine export")
# Where is the file? In the working directory of the Python you ran: Colab -> /content (Files panel on
# the left, three dots -> Download, or files.download(OUT); it vanishes with the session, so copy it
# to Drive); CDSE JupyterLab -> next to the notebook (keep it in mystorage/); locally -> the folder
# you started the script from.

# What CDSE gives you that Earth Engine does not: the same scenes a day earlier, Sentinel-1 SLC
# (InSAR), the original products as files, an open API that also runs on non-Google backends.
# What it does not give you: the thousand-dataset catalogue, built-in classifiers, unlimited quota.
