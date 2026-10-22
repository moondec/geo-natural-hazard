# 01 - rgee hello (lesson 7, lab 7, for R users)
#
# rgee is a translator: R calls the Python earthengine-api through reticulate.
# Same server-side objects as in JavaScript and Python, `$` instead of `.`.
#
# One-time setup (at home, not on the lab Wi-Fi - about 200 MB):
#   install.packages("rgee")
#   library(rgee)
#   ee_install(py_env = "rgee")   # conda env + earthengine-api (Python >= 3.11); answer Y, restart R
#   # first authentication of a new user needs the gcloud CLI: install it, run `gcloud init`
#   ee_check()                    # python? earthengine-api? credentials?
# If rgee refuses to start: ee_clean_pyenv(); ee_install()

library(rgee)

# ------------------------------------------------------------------ parameters
PROJECT <- "ee-your-project"       # Cloud project id from lab 1
ROI_LON <- 16.93; ROI_LAT <- 52.41 # Poznan
ROI_BUFFER_M <- 5000
DATE_START <- "2025-05-01"; DATE_END <- "2025-09-30"
MAX_CLOUD_PCT <- 30

# ------------------------------------------------------------- initialise
# drive = TRUE unlocks the Drive-based downloads (ee_as_rast via = "drive").
ee_Initialize(project = PROJECT, drive = TRUE)

print(ee$String("Hello from Earth Engine")$getInfo())

# ----------------------------------------------------------------- recipe
roi <- ee$Geometry$Point(ROI_LON, ROI_LAT)$buffer(ROI_BUFFER_M)

s2 <- ee$ImageCollection("COPERNICUS/S2_SR_HARMONIZED")$
  filterDate(DATE_START, DATE_END)$
  filterBounds(roi)$
  filter(ee$Filter$lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PCT))

cat("scenes:", s2$size()$getInfo(), "\n")

# R functions passed to $map must return an ee object
add_ndvi <- function(img) {
  img$addBands(img$normalizedDifference(c("B8", "B4"))$rename("NDVI"))
}

ndvi <- s2$map(add_ndvi)$select("NDVI")$median()$clip(roi)

# ------------------------------------------------------------------ map
Map$centerObject(roi, 11)
Map$addLayer(ndvi,
             list(min = -0.2, max = 0.8,
                  palette = c("blue", "white", "yellow", "green", "darkgreen")),
             "NDVI median")

# ------------------------------------------------------- one number out
stats <- ndvi$reduceRegion(reducer = ee$Reducer$mean(), geometry = roi,
                           scale = 10, maxPixels = 1e9)
print(stats$getInfo())

# ----------------------------------------------------- small raster out
# via = "getDownloadURL" is synchronous and fine for a few MB;
# via = "drive" (default) handles big images in the background.
library(terra)
r <- ee_as_rast(ndvi, region = roi, scale = 10, via = "getDownloadURL")
print(r)
plot(r, main = "NDVI median, Poznan 2025")
writeRaster(r, "ndvi_poznan_2025.tif", overwrite = TRUE)

# Alternative: a stars object
# library(stars)
# st <- ee_as_stars(ndvi, region = roi, scale = 10, via = "getDownloadURL")

# ----------------------------------------- time series -> data.frame
# ee_extract: NDVI per image for a few points -> one row per point,
# one column per date (long format with tidyr, then ggplot2).
library(sf)
pts <- st_as_sf(data.frame(
  id  = 1:3,
  lon = c(16.90, 16.95, 17.00),
  lat = c(52.40, 52.42, 52.45)), coords = c("lon", "lat"), crs = 4326)

ts_wide <- ee_extract(x = s2$map(add_ndvi)$select("NDVI"), y = pts,
                      fun = ee$Reducer$mean(), scale = 10, sf = FALSE)
print(head(ts_wide))
# library(tidyr); library(ggplot2)
# ts_long <- pivot_longer(ts_wide, -id, names_to = "image", values_to = "ndvi")
# ts_long$date <- as.Date(substr(ts_long$image, 2, 9), "%Y%m%d")
# ggplot(ts_long, aes(date, ndvi, colour = factor(id))) + geom_line() + theme_bw()
