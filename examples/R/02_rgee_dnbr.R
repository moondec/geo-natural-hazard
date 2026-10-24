# 02 - Burn severity with dNBR in R / rgee (lab 6 reproduced in R)
#
# Same steps as examples/python/04_dnbr_burn_severity.py:
#   pre/post Sentinel-2 L2A medians with an SCL cloud mask, NBR, dNBR x 1000,
#   USGS classes, hectares per class, raster out to terra.
# Default event: Landiras fire, Gironde (France), 12-25 July 2022.

library(rgee)
library(terra)

# ------------------------------------------------------------------ parameters
PROJECT <- "ee-your-project"
AOI_BBOX <- c(-0.70, 44.38, -0.30, 44.65)          # west, south, east, north
PRE_START  <- "2022-06-15"; PRE_END  <- "2022-07-10"
POST_START <- "2022-07-26"; POST_END <- "2022-08-08"
MAX_CLOUD_PCT <- 40
EXPORT_SCALE <- 20                                  # B12 (SWIR2) is a 20 m band

CLASS_BREAKS <- c(-250, -100, 100, 270, 440, 660)   # USGS, x1000 scale
CLASS_NAMES <- c("enhanced regrowth, high", "enhanced regrowth, low", "unburned",
                 "low severity", "moderate-low severity",
                 "moderate-high severity", "high severity")
CLASS_PALETTE <- c("7a8737", "acbe4d", "0ae042", "fff70b", "ffaf38", "ff641b", "a41fd6")

ee_Initialize(project = PROJECT, drive = TRUE)

aoi <- ee$Geometry$Rectangle(AOI_BBOX)

# ------------------------------------------------------------- cloud mask
mask_scl <- function(img) {
  scl <- img$select("SCL")
  keep <- scl$remap(c(4L, 5L, 6L, 11L), c(1L, 1L, 1L, 1L), 0L)
  img$updateMask(keep)
}

s2_masked <- function(start, end) {
  ee$ImageCollection("COPERNICUS/S2_SR_HARMONIZED")$
    filterDate(start, end)$
    filterBounds(aoi)$
    filter(ee$Filter$lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PCT))$
    map(mask_scl)
}

s2_before  <- s2_masked(PRE_START, PRE_END)
s2_after <- s2_masked(POST_START, POST_END)
cat("pre scenes :", s2_before$size()$getInfo(), "\n")
cat("post scenes:", s2_after$size()$getInfo(), "\n")

pre  <- s2_before$median()$clip(aoi)
post <- s2_after$median()$clip(aoi)

# -------------------------------------------------------------- NBR, dNBR
nbr <- function(img) img$normalizedDifference(c("B8", "B12"))$rename("NBR")
dnbr <- nbr(pre)$subtract(nbr(post))$multiply(1000)$rename("dNBR")

# --------------------------------------------------------------- classes
severity <- ee$Image$constant(0)$rename("severity")
for (brk in CLASS_BREAKS) severity <- severity$add(dnbr$gt(brk))
severity <- severity$updateMask(dnbr$mask())$toByte()

# ----------------------------------------------------- hectares per class
area_img <- ee$Image$pixelArea()$divide(1e4)$addBands(severity)
grouped <- area_img$reduceRegion(
  reducer = ee$Reducer$sum()$group(groupField = 1, groupName = "class"),
  geometry = aoi, scale = EXPORT_SCALE, maxPixels = 1e10)
groups <- grouped$get("groups")$getInfo()

areas <- data.frame(
  class = sapply(groups, function(g) g$class),
  name  = sapply(groups, function(g) CLASS_NAMES[g$class + 1]),
  ha    = sapply(groups, function(g) g$sum))
print(areas)
cat("total [ha]:", round(sum(areas$ha)), "\n")

# -------------------------------------------------------------------- map
rgb <- list(min = 0, max = 3000, bands = c("B4", "B3", "B2"))
Map$centerObject(aoi, 11)
Map$addLayer(pre, rgb, "pre-fire true colour") +
  Map$addLayer(post, rgb, "post-fire true colour") +
  Map$addLayer(severity, list(min = 0, max = 6, palette = CLASS_PALETTE),
               "burn severity (USGS)")

# ------------------------------------------------- raster out to terra
# About 32 x 30 km at 20 m = 2.4e6 pixels, one byte band: fine for
# getDownloadURL; switch to via = "drive" for larger areas.
sev_r <- ee_as_rast(severity$unmask(255L), region = aoi, scale = EXPORT_SCALE,
                    via = "getDownloadURL")
sev_r[sev_r == 255] <- NA
plot(sev_r, col = paste0("#", CLASS_PALETTE), main = "dNBR severity, Landiras 2022")
writeRaster(sev_r, "dnbr_severity_landiras_2022.tif", overwrite = TRUE)

# dNBR histogram in R (the checklist: bimodal, unburned peak near 0?)
dnbr_r <- ee_as_rast(dnbr, region = aoi, scale = 100, via = "getDownloadURL")
hist(values(dnbr_r), breaks = 50, main = "dNBR x 1000", xlab = "dNBR")
abline(v = CLASS_BREAKS, col = "red", lty = 2)
