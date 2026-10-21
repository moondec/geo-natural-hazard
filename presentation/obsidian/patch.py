import sys, io
src = io.open('ApplicationHazards_GEO.orig.md', encoding='utf-8').read()
out = src
def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count:
        sys.exit(f'EXPECTED {count} got {n}: {old[:70]!r}')
    out = out.replace(old, new)

# slide 3
rep('### For other advices visit e.g.', '### For other advice visit e.g.')
rep('[Copernicus Browser](https://dataspace.copernicus.eu/) **We will back later**',
    '[Copernicus Browser](https://browser.dataspace.copernicus.eu/) **We will come back to it later**')
# slide 10
rep('## Idea of tele-detection :smile: HOW EO SATELLITES WORK', '## Idea of remote sensing :smile: HOW EO SATELLITES WORK')
rep('source: http://satellites4everyone.co.uk/?page_id=4402',
    'source: satellites4everyone.co.uk (site offline – [archived copy](https://web.archive.org/web/2023/http://satellites4everyone.co.uk/?page_id=4402))')
# slide 12
rep('![[Kursy/prezentacje/ApplicationHazards_GEO/pliki/Pasted image 20230106213729.png]]\n',
    '![[Kursy/prezentacje/ApplicationHazards_GEO/pliki/Pasted image 20230106213729.png]]\n\n'
    '::: block <!-- element style="font-size: 36px;" class="fragment fade-up" -->\n'
    'Landsat 8 and **Landsat 9** (2021) carry the same bands (OLI-2 / TIRS-2); Landsat 7 was decommissioned in June 2025. '
    'Sentinel-2 now flies as a triplet: **2A, 2B and 2C** (2C operational since January 2025). '
    'Next generation: Landsat Next (26 bands, launch planned for the early 2030s).\n:::\n')
# slide 13 GEE
rep('::: block <!-- element style="font-size: 60px;"  -->\n- [Online](https://developers.google.com/earth-engine)',
    '::: block <!-- element style="font-size: 50px;"  -->\n- [Online](https://developers.google.com/earth-engine)')
rep('+ Available for scientist, researchers and developers',
    '+ Free for [noncommercial use](https://earthengine.google.com/noncommercial/) (research, education) – you need a Google account and a registered **Google Cloud project** ([how to get access](https://developers.google.com/earth-engine/guides/access)) – do it **before** the class!')
rep('+ [End-to-End](https://courses.spatialthoughts.com/end-to-end-gee.html) course\n',
    '+ [End-to-End](https://courses.spatialthoughts.com/end-to-end-gee.html) course\n'
    '+ Python: `ee` API + [geemap](https://geemap.org/) in Jupyter; R: rgee (next slide)\n')
# slide 14 SentinelHUB -> Copernicus Browser
old14 = out[out.index('![[Pasted image 20230108222731.png]] <!-- element drag="25 13" drop="bottomleft"-->'):]
old14 = old14[:old14.index('+ Import Imagery into Your GIS Application (e.g. QGIS, ArcGIS)\n:::') + len('+ Import Imagery into Your GIS Application (e.g. QGIS, ArcGIS)\n:::')]
new14 = '''![[Pasted image 20251102204319.png]]
::: title 
## Copernicus Browser
:::

::: block <!-- element style="font-size: 50px;"  -->
- Part of the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (EU / ESA); a free account is required
+ [Copernicus Browser](https://browser.dataspace.copernicus.eu/) to browse and compare full resolution images (Sentinel-1, Sentinel-2 + mosaics, Sentinel-3, Sentinel-5P, DEM)
+ Tools for analysis (compare, timelapse, time series and histograms, import AOI as KML/GeoJSON, export GeoTIFF, 3D view, custom scripts e.g. [NDVI](https://custom-scripts.sentinel-hub.com/sentinel-2/ndvi/), [SAVI](https://custom-scripts.sentinel-hub.com/sentinel-2/savi/))
+ Import imagery into your GIS application (e.g. QGIS, ArcGIS) via WMS/WMTS
+ Successor of **EO Browser** (Sentinel Hub / Sinergise, retired in March 2026); commercial alternative: [Planet Insights Platform](https://www.planet.com/products/planet-insights-platform/)
:::'''
rep(old14, new14)
# slide 15
rep('# RGEE - Google [Earth Engine with R](https://r-earthengine.com/rgeebook/index.html)',
    '# RGEE - Google [Earth Engine with R](https://r-spatial.github.io/rgee/)')
# slide 16
rep('guides/earth-engine/guides/', 'guides/', 3)
# slide 20
rep('the data points belongs', 'the data points belong')
# slide 22
rep('### Watch follows webinars:', '### Watch the following webinars:')
rep('- https://www.youtube.com/watch?v=eK0OMn5H-kY\n',
    '- https://www.youtube.com/watch?v=F0lIn5r6ZWk (A short guide to Copernicus Browser)\n'
    '- https://www.youtube.com/watch?v=GecNCdilbig (Introduction to the CDSE website and Copernicus Browser, facultative)\n')
rep('- Browse [Sentinel Hub Webinars](https://www.sentinel-hub.com/explore/education/webinars/)',
    '- Browse [Copernicus Data Space Ecosystem videos](https://www.youtube.com/@copernicusdataspaceecosystem) and [Sentinel Hub Webinars](https://www.sentinel-hub.com/explore/education/webinars/)')
# slide 24
rep(' **This book uses its template.**', '')
rep('(https://geocompr.robinlovelace.net/)', '(https://r.geocompx.org/)')
rep('(https://keen-swartz-3146c4.netlify.app/)', '(https://r-spatial.org/book/)')
rep('(http://r4ds.had.co.nz/)', '(https://r4ds.hadley.nz/)')
old_rgee = out[out.index('- **"[Earth Engine with R](https://r-earthengine.com/rgeebook/index.html)"**'):]
old_rgee = old_rgee[:old_rgee.index('\n')]
rep(old_rgee, '- **"[rgee – Google Earth Engine for R](https://r-spatial.github.io/rgee/)"** (package documentation and tutorials) by [Cesar Aybar](https://github.com/csaybar) et al. – the former "Earth Engine with R" book site is offline.')
io.open('ApplicationHazards_GEO.md', 'w', encoding='utf-8', newline='\n').write(out)
print('ok', out.count('\n---\n'))
