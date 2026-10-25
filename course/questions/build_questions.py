"""Question bank for the final test of AGeoHazard – generates final_test.xml (Moodle XML).

Run:  python -I -X utf8 build_questions.py      (in this folder)
Import on the test Moodle (course 15) with import_questions.php (CLI, question/format/xml).

Conventions: everything in English; one category per lesson; every question has a general
feedback that explains the answer; multi-answer questions give negative credit for wrong ticks.
Question types: mc (one correct), mcm (several correct), tf (true/false), num (numerical).
"""
import html, pathlib

TOP = 'AGeoHazard – final test'
BANK = []           # (category, [questions])

def cat(name, qs):
    BANK.append((name, qs))

def mc(name, text, answers, fb, single=True):
    """answers: list of (text, correct) – or (text, fraction) when fraction given explicitly."""
    return dict(type='multichoice', name=name, text=text, answers=answers, fb=fb, single=single)

def mcm(name, text, answers, fb):
    return mc(name, text, answers, fb, single=False)

def tf(name, text, answer, fb):
    return dict(type='truefalse', name=name, text=text, answer=answer, fb=fb)

def num(name, text, value, tol, fb):
    return dict(type='numerical', name=name, text=text, value=value, tol=tol, fb=fb)

# --------------------------------------------------------------------------- Lesson 1
cat('L1 Data and accounts', [
    mc('L1-01 Copernicus Browser', 'Which tool did Copernicus Browser replace in 2026?',
       [('EO Browser', True), ('Google Earth Engine Explorer', False), ('SNAP Desktop', False), ('Copernicus Open Access Hub (SciHub)', False)],
       'EO Browser (Sentinel Hub) was retired in March 2026; Copernicus Browser of the Copernicus Data Space Ecosystem (CDSE) offers the same tools – compare, timelapse, time series, custom scripts.'),
    mc('L1-02 Code Editor requirement', 'What do you need before the Earth Engine Code Editor opens without an error?',
       [('A Google Cloud project registered for Earth Engine (noncommercial use)', True), ('A paid Google Cloud billing account', False),
        ('A CDSE account', False), ('An installed Python environment with earthengine-api', False)],
       'Earth Engine access is tied to a Google Cloud project. Noncommercial (education) registration is free but takes 20–30 minutes and is periodically re-verified.'),
    mc('L1-03 Processing levels', 'Which Sentinel-2 processing level contains surface (bottom-of-atmosphere) reflectance?',
       [('Level-2A', True), ('Level-1C', False), ('Level-1B', False), ('Level-0', False)],
       'Level-1C is top-of-atmosphere reflectance; Level-2A adds the atmospheric correction (surface reflectance) and the SCL scene classification band. In Earth Engine: COPERNICUS/S2_SR_HARMONIZED.'),
    mc('L1-04 SCL band', 'What is the SCL band of a Sentinel-2 Level-2A product?',
       [('A per-pixel scene classification (cloud, shadow, water, vegetation …) produced by the atmospheric correction', True),
        ('The surface reflectance in the short-wave infrared', False), ('A cloud probability in percent', False), ('The viewing angle of the sensor', False)],
       'SCL (scene classification layer) codes each pixel; classes 3, 8, 9 and 10 are cloud shadow, medium and high probability cloud and cirrus – the classes masked in lesson 2.'),
    mc('L1-05 Revisit', 'What is the revisit time of the Sentinel-2 constellation at the equator?',
       [('5 days', True), ('1 day', False), ('16 days', False), ('30 days', False)],
       'One Sentinel-2 satellite repeats every 10 days; with two satellites in the same orbit the revisit is 5 days (shorter at higher latitudes where swaths overlap). Landsat 8/9 together: 8 days.'),
    mc('L1-06 Band resolution', 'Which Sentinel-2 bands have a 10 m pixel?',
       [('B2, B3, B4 and B8 (blue, green, red, broad NIR)', True), ('B11 and B12 (SWIR)', False), ('B5, B6, B7 (red edge)', False), ('All bands', False)],
       'B2/B3/B4/B8 are 10 m, the red-edge bands, B8A and the SWIR bands B11/B12 are 20 m, B1/B9/B10 are 60 m. An index that uses B11 or B12 (MNDWI, NBR) is effectively a 20 m product.'),
    tf('L1-07 Open data', 'Sentinel-1 and Sentinel-2 data are free and open for anyone, including commercial use.', True,
       'Copernicus data are distributed under a free, full and open licence. The constraint in this course is compute and account access, not data licensing.'),
    mcm('L1-08 Two accounts', 'Which two accounts does the course require before lab 1? (select all that apply)',
        [('A CDSE account (Copernicus Browser)', True), ('A Google account with a registered Earth Engine project', True),
         ('A Sentinel Hub paid subscription', False), ('An ESA EO College account', False)],
        'Milestone M1: a CDSE account for Copernicus Browser and a Google account with a Cloud project registered for Earth Engine.'),
])

# --------------------------------------------------------------------------- Lesson 2
cat('L2 Earth Engine basics and NDVI', [
    mc('L2-01 Image vs collection', 'In Earth Engine, what is the difference between an ee.Image and an ee.ImageCollection?',
       [('An ee.Image is one raster with one or more bands; an ee.ImageCollection is a stack of images (e.g. all Sentinel-2 scenes)', True),
        ('An ee.Image is a single band; an ee.ImageCollection is a multi-band image', False),
        ('An ee.ImageCollection is an image downloaded to your computer', False), ('There is no difference', False)],
       'COPERNICUS/S2_SR_HARMONIZED is a collection of millions of scenes; filterDate / filterBounds select scenes, median() turns the collection into one ee.Image.'),
    tf('L2-02 filterDate', "In filterDate('2025-05-01', '2025-09-30') the end date is exclusive – scenes acquired on 30 September are NOT included.", True,
       'The end date of filterDate is exclusive; use the day after the last day you want.'),
    mc('L2-03 CLOUDY_PIXEL_PERCENTAGE', "What does .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 35)) do?",
       [('Removes whole scenes whose metadata says more than 35 % cloud – it does not mask any pixel', True),
        ('Masks every cloudy pixel in every scene', False), ('Keeps only pixels with less than 35 % cloud probability', False), ('Removes scenes with less than 35 % cloud', False)],
       'It is a scene-level filter on a metadata property. Per-pixel masking needs a cloud mask: SCL classes, Cloud Score+ (cs_cdf) or the QA60 bitmask (lesson 2, step 5).'),
    mc('L2-04 Cloud Score+', 'In the Cloud Score+ mask the rule image.select(\'cs_cdf\').gte(0.6) keeps pixels …',
       [('… that are likely clear; a higher threshold (e.g. 0.65) is stricter, a lower one (0.5) keeps more pixels', True),
        ('… that are likely cloudy', False), ('… with reflectance above 0.6', False), ('… acquired after 60 % of the season', False)],
       'cs_cdf is a 0–1 clear-sky score: 1 = certainly clear. gte(0.6) keeps pixels with score ≥ 0.6; the collection is joined with linkCollection.'),
    tf('L2-05 QA60 gap', 'The Sentinel-2 QA60 cloud bitmask is reliable for all scenes in the archive.', False,
       'QA60 is unpopulated for scenes from 25 January 2022 to 28 February 2024. Use the SCL band or Cloud Score+ for that period.'),
    mc('L2-06 normalizedDifference', "What does image.normalizedDifference(['B8', 'B4']) compute?",
       [('(B8 − B4) / (B8 + B4), i.e. NDVI for Sentinel-2', True), ('(B4 − B8) / (B4 + B8)', False), ('B8 / B4', False), ('B8 − B4', False)],
       'normalizedDifference(A, B) = (A − B) / (A + B). With NIR = B8 and red = B4 it is NDVI, ranging from −1 to 1; dense vegetation > 0.4, water < 0.'),
    mc('L2-07 map()', 'What does s2MaskedCS.map(addNDVI) do?',
       [('Runs the function addNDVI on every image of the collection on the server and returns a new collection', True),
        ('Adds a layer to the map panel', False), ('Downloads the collection and runs the function locally', False), ('Runs the function on the median image only', False)],
       'map() is the Earth Engine way of looping over a collection; nothing is computed until a result is requested (print, Map.addLayer, Export).'),
    mc('L2-08 median()', 'ndviCollection.median() returns …',
       [('… one ee.Image whose pixel values are the per-pixel median over time', True), ('… an ee.ImageCollection with half of the images', False),
        ('… a number: the median NDVI of the area', False), ('… the middle scene of the collection', False)],
       'A reducer over time collapses the collection into a single image. The median is robust to the remaining clouds and shadows.'),
    mc('L2-09 scale', 'In reduceRegion, why must scale be 10 for Sentinel-2 rather than 1?',
       [('scale is the pixel size in metres at which the computation runs; 1 m forces a hundred times more samples than real pixels and ends with "Too many pixels"', True),
        ('scale is the number of bands to use', False), ('scale is a multiplication factor for the result', False), ('Earth Engine ignores scale', False)],
       'The scale must match the data: 10 m for Sentinel-2, 30 m for Landsat. A too small scale oversamples and fails; a too large one smooths the result.'),
    mc('L2-10 pixelArea', 'How do you get the area of a class in hectares in Earth Engine?',
       [('Sum ee.Image.pixelArea() (m² per pixel) over the class pixels with a grouped reducer and divide by 10 000', True),
        ('Count the pixels and multiply by 10', False), ('Use image.area()', False), ('Export the image and read the file size', False)],
       'ee.Image.pixelArea() gives each pixel its area in m²; ee.Reducer.sum().group({groupField: 1}) sums it per class code; 1 ha = 10 000 m².'),
    num('L2-11 NDVI value', 'A pixel has reflectance B8 = 0.40 and B4 = 0.10. What is its NDVI? (two decimals)', 0.6, 0.01,
        'NDVI = (0.40 − 0.10) / (0.40 + 0.10) = 0.30 / 0.50 = 0.60 – dense green vegetation.'),
    mcm('L2-12 Three verbs', 'Which three operations form the skeleton of nearly every Earth Engine script in this course? (select all that apply)',
        [('Load and filter a collection', True), ('map() a function over the images', True), ('Reduce the collection to one image (median) or a number', True),
         ('Download all scenes to the local disk', False)],
        'Load/filter → map → reduce; the same three verbs appear in Python, in the QGIS console and in openEO.'),
])

# --------------------------------------------------------------------------- Lesson 3
cat('L3 Classifiers and accuracy', [
    mc('L3-01 Label vs feature', 'In a pixel-based classification, what is the difference between a feature and a label?',
       [('A feature is an input column (a band value, an index, slope); the label is the class we want to predict', True),
        ('A feature is the class; the label is the pixel coordinate', False), ('They are synonyms', False), ('A feature is a vector layer; a label is its name', False)],
       'Each pixel is a row of a table: the bands and indices are the features (predictors), the land cover code is the label.'),
    mc('L3-02 Supervised vs unsupervised', 'Which statement about Random Forest and k-means in Earth Engine is correct?',
       [('Random Forest needs labelled training pixels; k-means needs no labels and returns cluster ids', True),
        ('k-means needs labelled training pixels; Random Forest does not', False), ('Both need labelled training data', False), ('Neither needs any reference data', False)],
       'ee.Classifier.smileRandomForest is supervised (labelled data); ee.Clusterer.wekaKMeans is unsupervised – you name the clusters afterwards.'),
    tf('L3-03 Cluster is not a class', 'A k-means cluster number is a land cover class.', False,
       'k-means finds spectral groups. Sunlit and shaded forest may become two clusters, wheat and grass one. You must inspect the map and relabel clusters to classes before any accuracy can be computed.'),
    mc('L3-04 Train/test split', 'Why do you keep 30 % of the samples aside as a test set?',
       [('To measure the accuracy on pixels the model has never seen – otherwise the accuracy is meaningless', True),
        ('To speed up the training', False), ('Because Earth Engine cannot train on more than 70 % of the samples', False), ('To create the legend', False)],
       'randomColumn() and a 0.7 split give training and test sets; the confusion matrix is computed on the test set only.'),
    num('L3-05 Overall accuracy', 'A confusion matrix of 200 test pixels has 176 on the diagonal. What is the overall accuracy in percent?', 88, 0.5,
        'Overall accuracy = correctly classified / total = 176 / 200 = 0.88 = 88 %.'),
    mc('L3-06 Producer vs user', "What does producer's accuracy of the class crops tell you?",
       [('Of the real crop pixels, how many did the map find (recall)', True), ('Of the pixels the map calls crops, how many are really crops (precision)', False),
        ('The share of crops in the whole area', False), ('The number of training polygons for crops', False)],
       "Producer's accuracy = recall (omission errors); user's accuracy = precision (commission errors). Both are read from the confusion matrix."),
    mc('L3-07 Kappa', 'What does a kappa value of 0 mean?',
       [('Agreement no better than chance', True), ('Perfect agreement', False), ('All pixels misclassified', False), ('The matrix is empty', False)],
       'Kappa corrects the agreement for chance: 0 = random, 1 = perfect. Report overall, producer\'s and user\'s accuracy; kappa is optional (Foody 2020).'),
    mc('L3-08 Import as', 'When you draw training polygons in the Code Editor, how must the geometry layers be imported for sampleRegions to work?',
       [('As FeatureCollection with a property (e.g. landcover = 0 … 3)', True), ('As Geometry', False), ('As Image', False), ('As a CSV table', False)],
       'Import as Geometry gives no properties, so sampleRegions returns nothing useful. Use one FeatureCollection per class with the same property name and codes 0 … 3 everywhere.'),
    mcm('L3-09 Improvements', 'Which actions typically improve a Random Forest land cover classification? (select all that apply)',
        [('Masking clouds per pixel before taking the median composite', True), ('Adding spectral indices (NDVI, MNDWI, NDBI) and elevation/slope as bands', True),
         ('More and better-distributed training samples', True), ('Training and testing on the same pixels', False)],
        'Cloud masking, extra bands, more trees and better samples help; validating on the training pixels only inflates the accuracy.'),
    mc('L3-10 focal_mode', 'What does classified.focal_mode({radius: 1, kernelType: \'square\', units: \'pixels\'}) do?',
       [('A majority filter that removes isolated salt-and-pepper pixels', True), ('A cloud mask', False), ('An edge detector', False), ('A resampling to 1 m', False)],
       'The mode of the 3 × 3 neighbourhood replaces each pixel – post-processing that smooths the classified map.'),
    mc('L3-11 Dynamic World', 'What is Dynamic World (GOOGLE/DYNAMICWORLD/V1)?',
       [('A near-real-time per-pixel land cover product from Sentinel-2 made with a convolutional neural network', True),
        ('A digital elevation model', False), ('A cloud mask collection', False), ('A collection of training polygons', False)],
       'Dynamic World (Google / WRI, Brown et al. 2022) does the lab 3 task with a neural network and is a convenient reference layer for your report.'),
    mc('L3-12 Common mistake', 'You added NDVI and slope to the image as stack = composite.addBands([…]) but the accuracy did not change at all. Most likely …',
       [('… you still trained on composite.bandNames() and classified composite, so the model never saw the new bands', True),
        ('… the new bands are identical to the old ones', False), ('… Random Forest cannot use more than 6 bands', False), ('… the test set is too large', False)],
       'Use stack.bandNames() in inputProperties and classify stack; classifier.explain() then shows the importance of the new inputs.'),
])

# --------------------------------------------------------------------------- Lesson 4
cat('L4 Floods – water indices and SAR', [
    mc('L4-01 Water spectrum', 'Why does water appear dark in the near-infrared and short-wave infrared bands?',
       [('Water absorbs NIR and SWIR almost completely, while vegetation and soil reflect them strongly', True),
        ('Water reflects NIR strongly', False), ('The sensor is not sensitive to NIR over water', False), ('Water is always covered by clouds', False)],
       'This contrast is the basis of every water index: green (reflected a little) versus NIR or SWIR (absorbed).'),
    mc('L4-02 MNDWI formula', 'Which formula is MNDWI for Sentinel-2?',
       [('(B3 − B11) / (B3 + B11): green minus SWIR', True), ('(B3 − B8) / (B3 + B8): green minus NIR', False), ('(B8 − B4) / (B8 + B4)', False), ('(B8 − B12) / (B8 + B12)', False)],
       'MNDWI (Xu 2006) replaces the NIR of NDWI (B3, B8) by SWIR (B11), which suppresses built-up areas that also reflect little NIR.'),
    mc('L4-03 Why MNDWI', 'Why is MNDWI often preferred to NDWI in flooded towns?',
       [('Buildings reflect little NIR like water, but more SWIR than water – so MNDWI separates water from built-up areas', True),
        ('MNDWI has 10 m resolution, NDWI 20 m', False), ('NDWI cannot be computed in Earth Engine', False), ('MNDWI works through clouds', False)],
       'NDWI cannot suppress the built-up signal; MNDWI can. Note that B11 is a 20 m band, so MNDWI is a 20 m product.'),
    mc('L4-04 Why SAR', 'Why is Sentinel-1 radar the main tool for mapping the flood peak?',
       [('Its C-band microwaves (about 5.6 cm) pass through clouds and work day and night – the peak is usually under the clouds that caused it', True),
        ('It has a higher spatial resolution than Sentinel-2', False), ('It measures water depth directly', False), ('It is the only free satellite', False)],
       'Optical data are good for the situation after the event and for permanent water; the peak itself falls between Sentinel-2 passes and under clouds.'),
    mc('L4-05 Dark water', 'Why is calm water dark in a Sentinel-1 image?',
       [('Specular reflection: the smooth surface bounces the pulse away from the antenna, so very little backscatter returns (below about −18 dB)', True),
        ('Water absorbs microwaves completely', False), ('The satellite switches off over water', False), ('Water is cold', False)],
       'Typical VH values: water around −22 dB, land around −12 dB – a bimodal histogram that can be thresholded.'),
    mc('L4-06 Double bounce', 'A flooded forest or a flooded street between buildings appears in SAR …',
       [('… brighter than before, because of double-bounce reflection between the water surface and trunks or walls', True),
        ('… darker than open water', False), ('… exactly like open water', False), ('… transparent', False)],
       'Double bounce (water + vertical structure) increases the backscatter; it is one reason why flooded vegetation and urban floods are missed by the "water is dark" rule. VV reacts most.'),
    tf('L4-07 Orbits', 'In SAR change detection you may freely mix ascending and descending Sentinel-1 scenes in the before and after stacks.', False,
       'Never mix orbit directions: the viewing geometry differs, so the backscatter of the same pixel differs. Filter one orbit pass, one mode (IW) and one polarisation.'),
    mc('L4-08 VV or VH', 'Which polarisation does the lesson recommend for floods in open land, and why?',
       [('VH – the land/water contrast is larger', True), ('VV – it is the only one in the catalogue', False), ('HH – the standard over land', False), ('It makes no difference', False)],
       'VH (volume scattering from vegetation) gives a bigger contrast between land and open water; VV is better for flooded vegetation (double bounce).'),
    mc('L4-09 Ratio 1.25', 'In the UN-SPIDER script the flood is where after_dB / before_dB exceeds 1.25. What does that mean?',
       [('The after value is at least 25 % more negative (e.g. −12 → −15 dB, about 3 dB darker); it is a ratio of dB values, not of physical backscatter', True),
        ('The water is 1.25 m deep', False), ('The pixel is 25 % water', False), ('The after image is 25 % brighter', False)],
       'The dB values are already logarithms, so the ratio is a convention. A difference threshold in dB (e.g. −3 dB) does the same more transparently.'),
    mcm('L4-10 Masks', 'Which masks does the UN-SPIDER flood script apply to the change layer? (select all that apply)',
        [('Permanent water from the JRC Global Surface Water seasonality layer', True), ('Slopes steeper than 5° (radar shadow is not water)', True),
         ('Isolated groups of fewer than 8 connected pixels', True), ('Built-up areas from OpenStreetMap', False)],
        'JRC GSW removes lakes and rivers, the HydroSHEDS DEM slope mask removes shadow on slopes, connectedPixelCount removes specks. There is no built-up mask.'),
    mc('L4-11 Speckle', 'Why does the script apply a 50 m focal mean to the SAR images?',
       [('To reduce speckle – the salt-and-pepper noise inherent to radar images', True), ('To convert dB to linear units', False), ('To change the orbit', False), ('To increase the resolution', False)],
       'Speckle must always be filtered before thresholding; the radius is a trade-off between noise and detail (sensitivity test: 30 m vs 100 m).'),
    mc('L4-12 Sensitivity table', 'Why does milestone M4 require the flooded area for thresholds 1.15, 1.25 and 1.40?',
       [('To show the uncertainty of the map – how much the area depends on an arbitrary parameter', True), ('Because the server needs three runs', False),
        ('To compute the average depth', False), ('To calibrate the satellite', False)],
       'A map whose area changes by less than a factor of two between the thresholds is robust; a large change means the threshold matters more than the data.'),
    mc('L4-13 InSAR', 'What does SAR interferometry (InSAR) measure that backscatter analysis does not?',
       [('The phase of the signal – giving topographic height and ground displacement with millimetre accuracy', True),
        ('The colour of the surface', False), ('The temperature of the ground', False), ('The amount of rainfall', False)],
       'Backscatter uses the amplitude (how much echo returns); InSAR uses the phase (how far it travelled). DEMs (SRTM, TanDEM-X → Copernicus DEM) and subsidence maps come from InSAR.'),
    mc('L4-14 S1 collection', 'Which Earth Engine collection holds Sentinel-1 ground-range-detected backscatter, and in which unit?',
       [('COPERNICUS/S1_GRD, values already in dB, 10 m pixels in IW mode', True), ('COPERNICUS/S2_SR_HARMONIZED, reflectance', False),
        ('COPERNICUS/S1_SLC, complex phase', False), ('LANDSAT/LC09/C02/T1_L2, radiance', False)],
       'GRD = amplitude only, terrain corrected; the SLC products with phase are not in Earth Engine (CDSE has them – lesson 7, optional page).'),
])

# --------------------------------------------------------------------------- Lesson 5
cat('L5 Landslides', [
    mc('L5-01 Definition', 'What is a landslide?',
       [('The downslope movement of soil, rock and organic material under gravity, and the landform that results from it', True),
        ('Any flood on a slope', False), ('An earthquake', False), ('The erosion of a river bank by water', False)],
       'USGS definition. From orbit you see the scar (bare, bright source area), the track and the deposit.'),
    mc('L5-02 Varnes classification', 'In the Varnes (1978) scheme used by the USGS Landslide Handbook, landslides are classified by …',
       [('… the type of material (rock, earth, debris) and the type of movement (fall, topple, slide, flow, spread)', True),
        ('… their size in hectares', False), ('… the season in which they occur', False), ('… the satellite that detected them', False)],
       'Material: rock or soil (earth = fine, debris = coarse). Movement: fall, topple, slide (rotational or translational), flow, spread, complex.'),
    mc('L5-03 Cause vs trigger', 'Which of the following is a trigger of a landslide, not a precondition?',
       [('Intense or prolonged rainfall', True), ('Slope angle', False), ('Clay-rich flysch lithology', False), ('An old landslide on the same slope', False)],
       'Preconditions answer "why here" (slope, lithology, land cover, road cuts) and are the predictors of a susceptibility model; triggers answer "why now" (rainfall, earthquakes, snowmelt).'),
    mc('L5-04 Three products', 'Which product answers the question "Where did landslides happen after event X?"',
       [('An inventory – from before/after change detection or visual mapping', True), ('A susceptibility map', False), ('A hazard/risk map', False), ('A DEM', False)],
       'Inventory (where did it happen), susceptibility (where could it happen), hazard/risk (how likely, how often, what is exposed). The lab produces an inventory-type heatmap – the input of everything else.'),
    mc('L5-05 Handwerger method', 'What input does the landslide density heatmap method of Handwerger et al. (2022) use?',
       [('Sentinel-1 SAR amplitude (VH) before and after the event, same orbit – no training data', True),
        ('Sentinel-2 NDVI only', False), ('Labelled training polygons and a Random Forest', False), ('InSAR phase', False)],
       'Pre- and post-event stacks reduced to their medians, the log-ratio of the two, masks for flat terrain and water, the 99th percentile flagged and turned into a kernel density heatmap.'),
    mc('L5-06 I_ratio sign', 'I_ratio = 10·log10(I_pre / I_post) = I_pre − I_post in dB. A strongly positive value means …',
       [('… the backscatter decreased after the event – vegetation removed, a fresh scar: a landslide candidate', True),
        ('… the backscatter increased – new buildings', False), ('… nothing changed', False), ('… the pixel is permanent water', False)],
       'A positive log-ratio = darker after the event. There is no absolute threshold; the paper uses the 99th percentile of the AOI.'),
    mcm('L5-07 Masks', 'Which pixels does the heatmap script mask out? (select all that apply)',
        [('Flat terrain (slope below 5–10°)', True), ('Permanent water', True), ('Built-up areas', False), ('Forest', False)],
        'Slope, curvature and water masks from NASADEM; there is no built-up mask, so urban change can appear in the heatmap.'),
    mc('L5-08 Slow creep', 'Why can a slow, creeping landslide not be mapped with the before/after method of the lab?',
       [('There is no event date, so there is no sharp before/after pair; slow movement needs InSAR time series instead', True),
        ('Creeping landslides are invisible to all satellites', False), ('Sentinel-1 does not cover mountains', False), ('The method only works in winter', False)],
       'Rain- or earthquake-triggered events give a sharp date; creep over years is an InSAR (phase) problem – lecture 5.'),
    mc('L5-09 Pre-event stack', 'What happens when you lengthen the pre-event Sentinel-1 stack from 2 to 8 months?',
       [('The pre-event median has less speckle noise, so the ratio is cleaner – at the cost of more seasonal mixing', True),
        ('The heatmap becomes blockier', False), ('The method stops working', False), ('The post-event image changes', False)],
       'More images → a smoother median; a too short stack gives a noisy, blocky heatmap everywhere.'),
    mc('L5-10 Poland', 'Where are about 95 % of the landslides of Poland?',
       [('In the Carpathian flysch', True), ('In the Masurian lake district', False), ('Along the Baltic coast', False), ('In the Sudetes only', False)],
       'The SOPO inventory of the Polish Geological Institute holds more than 70 000 landslides (2023), almost all in the Carpathians.'),
    mc('L5-11 Empty collection', 'The Console prints an empty image collection for the post-event window. What should you do first?',
       [('Widen the window or switch the orbit direction – there is no Sentinel-1 scene of that orbit in the window', True),
        ('Change the satellite to Sentinel-2', False), ('Increase the kernel radius', False), ('Lower the percentile threshold', False)],
       'Sentinel-1 repeats every 6–12 days per orbit; a short window may contain no scene of the chosen pass.'),
])

# --------------------------------------------------------------------------- Lesson 6
cat('L6 Wildfires and burn severity', [
    mc('L6-01 Intensity vs severity', 'What is the difference between fire intensity and burn severity?',
       [('Intensity is the energy released during the fire (kW/m, FRP); severity is the effect on the ecosystem measured after the fire', True),
        ('They are synonyms', False), ('Intensity is measured after the fire, severity during', False), ('Severity is the area burned', False)],
       'dNBR maps severity (after). Fire Radiative Power from thermal sensors is an intensity measure (during). Soil burn severity drives post-fire erosion and debris flows.'),
    mc('L6-02 Three products', 'Which of the three fire products needs a before/after image pair?',
       [('Burn severity (dNBR)', True), ('Active fire hotspots (FIRMS)', False), ('Burned area (MCD64A1)', False), ('All three', False)],
       'Active fire: thermal emission during the fire (VIIRS 375 m, MODIS 1 km). Burned area: monthly reflectance change + hotspots. Severity: NBR pre minus NBR post.'),
    mc('L6-03 Spectral change', 'How does the reflectance of a forest change after a fire?',
       [('NIR drops (leaves gone), SWIR rises (char, ash, dry soil)', True), ('NIR rises, SWIR drops', False), ('Both rise', False), ('Only the visible bands change', False)],
       'The two bands move in opposite directions – exactly what NBR exploits.'),
    mc('L6-04 NBR formula', 'Which formula is the Normalized Burn Ratio for Sentinel-2?',
       [('(B8 − B12) / (B8 + B12): NIR minus SWIR2', True), ('(B8 − B4) / (B8 + B4)', False), ('(B3 − B11) / (B3 + B11)', False), ('(B12 − B8) / (B12 + B8)', False)],
       'NBR = (NIR − SWIR2) / (NIR + SWIR2); for Landsat 8/9 SR_B5 and SR_B7. The UN-SPIDER page uses B8A instead of B8 – both acceptable, state which.'),
    mc('L6-05 dNBR', 'dNBR = NBR_pre − NBR_post. A strongly positive dNBR means …',
       [('… loss of vegetation: the pixel burned', True), ('… regrowth', False), ('… a cloud in the post image', False), ('… permanent water', False)],
       'Positive = vegetation loss, negative = enhanced regrowth. By convention dNBR is often scaled × 1000.'),
    mc('L6-06 USGS class', 'A pixel has dNBR = 0.50 (500 on the × 1000 scale). Which USGS burn severity class is it?',
       [('Moderate–high severity (0.44 – 0.66)', True), ('Low severity (0.10 – 0.27)', False), ('High severity (> 0.66)', False), ('Unburned (−0.10 – 0.10)', False)],
       'USGS classes: < −0.25 regrowth high; −0.25…−0.10 regrowth low; −0.10…0.10 unburned; 0.10…0.27 low; 0.27…0.44 moderate–low; 0.44…0.66 moderate–high; > 0.66 high.'),
    mc('L6-07 Effective resolution', 'Why should a Sentinel-2 NBR map be exported at 20 m rather than 10 m?',
       [('B12 (SWIR2) is a 20 m band, so the index is effectively a 20 m product', True), ('Earth Engine does not allow 10 m exports', False),
        ('Fires are never smaller than 20 m', False), ('B8 is a 20 m band', False)],
       'An index inherits the coarsest band it uses. Exporting at 10 m only resamples the 20 m information.'),
    mc('L6-08 Why not NDVI', 'Why is NBR preferred to NDVI for burn severity?',
       [('NDVI saturates in dense forest and recovers quickly with grass; the SWIR2 band of NBR reacts to char and soil moisture and stays changed for months', True),
        ('NDVI cannot be computed from Sentinel-2', False), ('NBR has a higher resolution', False), ('NDVI only works at night', False)],
       'NDVI difference remains a useful second opinion in grassland.'),
    mc('L6-09 Post-fire date', 'For an initial assessment, when should the post-fire image be acquired?',
       [('1–4 weeks after containment: smoke gone, ash still there', True), ('During the fire', False), ('Two years later', False), ('The same day as the pre image', False)],
       'An extended assessment uses the next growing season with the same phenology as the pre image and measures mortality rather than char.'),
    mc('L6-10 Cloud in pre', 'Your dNBR map shows high severity everywhere, also far outside the fire perimeter. The most likely cause is …',
       [('… a cloud in the pre-fire composite (bright, high NBR before → large drop); mask clouds per pixel and check the true-colour view', True),
        ('… the fire was very large', False), ('… the thresholds are too high', False), ('… the AOI is too small', False)],
       'Low severity everywhere outside the perimeter instead points to a phenology difference between the pre and post dates.'),
    mc('L6-11 Collections', 'The public UN-SPIDER script loads COPERNICUS/S2. Why does the course copy use COPERNICUS/S2_SR_HARMONIZED?',
       [('COPERNICUS/S2 is Level-1C top-of-atmosphere reflectance; the harmonised Level-2A surface reflectance is consistent with labs 2–5 and across the 2022 processing change', True),
        ('COPERNICUS/S2 has no B12 band', False), ('COPERNICUS/S2 is a Landsat collection', False), ('There is no difference', False)],
       'Same sensor, same processing level, same band set for pre and post; never mix Landsat pre with Sentinel post without harmonisation.'),
    mc('L6-12 EFFIS', 'What does EFFIS provide for your report?',
       [('Burnt area perimeters for Europe (fires ≥ 30 ha, Sentinel-2 based since 2018) to compare with your dNBR perimeter', True),
        ('Daily rainfall', False), ('A DEM', False), ('Training polygons for Random Forest', False)],
       'EFFIS (European Forest Fire Information System) and Copernicus EMS perimeters are the reference; FIRMS hotspots give the start and end dates.'),
    mc('L6-13 RdNBR', 'What is the purpose of RdNBR = dNBR / √|NBR_pre|?',
       [('To normalise for the amount of pre-fire vegetation, making forest and grassland comparable', True), ('To convert to hectares', False),
        ('To remove clouds', False), ('To scale dNBR by 1000', False)],
       'The USGS thresholds were derived for US forests; RdNBR is fairer when vegetation density varies across the perimeter.'),
])

# --------------------------------------------------------------------------- Lesson 7
cat('L7 APIs – Python, QGIS, CDSE', [
    mc('L7-01 API', 'What is an API in the context of Earth Engine?',
       [('A software interface through which programs (Code Editor, Python, QGIS plugin, R) talk to the same Earth Engine servers', True),
        ('A satellite', False), ('A file format for rasters', False), ('A map projection', False)],
       'Earth Engine has one engine and several clients: JavaScript (Code Editor), Python (ee, also inside Colab and the QGIS plugin), R (rgee, community).'),
    mcm('L7-02 Official clients', 'Which Earth Engine client libraries are provided by Google itself? (select all that apply)',
        [('JavaScript (Code Editor)', True), ('Python (ee)', True), ('R (rgee)', False), ('Julia (EarthEngine.jl)', False)],
        'Python and JavaScript are official; rgee (active) and EarthEngine.jl (unmaintained since 2023) are community wrappers of the Python API.'),
    mc('L7-03 Initialize', 'What must run at the start of every Colab session before any Earth Engine call?',
       [('ee.Authenticate() once, then ee.Initialize(project=\'your-project-id\') with the registered Cloud project id', True),
        ('pip install qgis', False), ('Map.addLayer()', False), ('Export.image.toDrive()', False)],
       'Use the project id exactly as in the Cloud console, not the project name.'),
    mcm('L7-04 JS to Python', 'Which changes are needed when translating a Code Editor script to Python? (select all that apply)',
        [('.and() / .or() / .not() become .And() / .Or() / .Not()', True), ('Dictionary keys must be quoted: {\'min\': 0, \'max\': 3000}', True),
         ('true / false / null become True / False / None', True), ('Band names change from B8 to B08', False)],
        'Server-side objects are identical; only syntax changes. Band names stay B4/B8 in Earth Engine (openEO uses B04/B08).'),
    mc('L7-05 getInfo', 'In Python, print(s2.size()) shows <ee.Number object> instead of 37. Why?',
       [('ee objects are server-side recipes; .getInfo() fetches the value from the server', True), ('The collection is empty', False),
        ('Python cannot print numbers', False), ('The project is not registered', False)],
       'Use .getInfo() for small values only; images and big collections go out through Export, never through getInfo().'),
    tf('L7-06 if on server object', 'In Python, an if statement on an Earth Engine server object (for example: if s2.size() > 0) evaluates the real value.', False,
       'A Python if on a server object is always true – the object exists, its value is unknown until getInfo(). Use .getInfo() or server-side ee.Algorithms.If.'),
    mc('L7-07 js_snippet_to_py', 'What does geemap.js_snippet_to_py() do?',
       [('Translates a Code Editor JavaScript snippet into Python code that you still have to check and fix', True),
        ('Runs JavaScript inside Python', False), ('Exports a map to Drive', False), ('Installs the QGIS plugin', False)],
       'The translator handles the syntax table of lesson 7; you fix what it missed (quoted keys, .And(), getInfo()).'),
    mc('L7-08 Plugin layers', 'A layer added with Map.addLayer in the QGIS Earth Engine plugin …',
       [('… is streamed as tiles from Earth Engine: you can view and overlay it, but not measure it or run zonal statistics – export a GeoTIFF for that', True),
        ('… is a GeoTIFF on your disk', False), ('… is editable like a shapefile', False), ('… works offline', False)],
       'Two doors to a real file: Export Image to GeoTIFF in the Processing Toolbox (small areas) or Export.image.toDrive in the Code Editor / Python (large areas).'),
    mc('L7-09 Poland CRS', 'Which CRS should you choose for an export covering Poland that will be measured in metres in QGIS?',
       [('EPSG:2180 (PUWG 1992)', True), ('EPSG:4326 (WGS 84 degrees)', False), ('EPSG:3857 (Web Mercator)', False), ('EPSG:32654', False)],
       'EPSG:4326 is in degrees (pixel size meaningless), EPSG:3857 inflates areas with latitude. Elsewhere use the UTM zone of the area.'),
    num('L7-10 UTM zone', 'Hokkaido lies at about 142° E. Which UTM zone number is it? (zone = ⌊(longitude + 180) / 6⌋ + 1)', 54, 0,
        '(142 + 180) / 6 = 53.67 → floor 53 → zone 54; northern hemisphere → EPSG:32654.'),
    mc('L7-11 Export location', 'Where does Export.image.toDrive run and where does the file land?',
       [('On Google\'s servers (Tasks tab / task.start()); the GeoTIFF appears in the Google Drive folder you named', True),
        ('On your computer; the file lands in Downloads', False), ('In QGIS; the file is added to the canvas', False), ('In Copernicus Browser', False)],
       'The plugin\'s Export Image to GeoTIFF instead downloads through your computer – fine for a few kilometres, not for a voivodeship.'),
    mcm('L7-12 CDSE adds', 'What does the Copernicus Data Space Ecosystem (openEO, JupyterLab) offer that Earth Engine does not? (select all that apply)',
        [('Sentinel-1 SLC data with phase (InSAR)', True), ('Whole Sentinel scenes as original files', True),
         ('An open standard API (openEO) that runs on several backends, no Google account', True), ('Built-in classifiers and a thousand-dataset catalogue', False)],
        'CDSE gives Copernicus data at the source and an EU-hosted, standards-based workflow; Earth Engine gives the catalogue, classifiers and free compute.'),
    mc('L7-13 Cell magic', 'In Colab, where must the %%R cell magic be placed?',
       [('In the very first line of the cell', True), ('At the end of the cell', False), ('Anywhere in the cell', False), ('In a text cell', False)],
       'A cell magic (%%) must be the first line; a line magic (%R) runs a single line and can copy an R variable to Python.'),
])

# --------------------------------------------------------------------------- XML
def esc(s): return html.escape(s, quote=False)
def ftext(s): return f'<text><![CDATA[<p>{esc(s)}</p>]]></text>'   # texts are plain; < > & are escaped for HTML

def q_xml(q):
    out = [f'  <question type="{q["type"]}">', f'    <name><text>{esc(q["name"])}</text></name>',
           f'    <questiontext format="html">{ftext(q["text"])}</questiontext>',
           f'    <generalfeedback format="html">{ftext(q["fb"])}</generalfeedback>',
           '    <defaultgrade>1</defaultgrade><penalty>0.3333333</penalty><hidden>0</hidden>']
    if q['type'] == 'multichoice':
        k = sum(1 for _, c in q['answers'] if c); n = len(q['answers'])
        out += [f'    <single>{"true" if q["single"] else "false"}</single><shuffleanswers>true</shuffleanswers><answernumbering>abc</answernumbering>',
                '    <correctfeedback format="html"><text>Correct.</text></correctfeedback>',
                '    <partiallycorrectfeedback format="html"><text>Partially correct.</text></partiallycorrectfeedback>',
                '    <incorrectfeedback format="html"><text>Not correct.</text></incorrectfeedback>']
        if not q['single']: out.append('    <shownumcorrect/>')
        for text, correct in q['answers']:
            if q['single']: frac = 100 if correct else 0
            else: frac = round(100 / k, 5) if correct else -round(100 / k, 5)
            out.append(f'    <answer fraction="{frac}" format="html">{ftext(text)}<feedback format="html"><text></text></feedback></answer>')
    elif q['type'] == 'truefalse':
        for label, ok in (('true', q['answer']), ('false', not q['answer'])):
            out.append(f'    <answer fraction="{100 if ok else 0}" format="moodle_auto_format"><text>{label}</text><feedback format="html"><text></text></feedback></answer>')
    elif q['type'] == 'numerical':
        out.append(f'    <answer fraction="100" format="moodle_auto_format"><text>{q["value"]}</text><tolerance>{q["tol"]}</tolerance><feedback format="html"><text></text></feedback></answer>')
        out.append('    <unitgradingtype>0</unitgradingtype><unitpenalty>0.1</unitpenalty><showunits>3</showunits><unitsleft>0</unitsleft>')
    out.append('  </question>')
    return '\n'.join(out)

def cat_xml(path):
    return f'  <question type="category">\n    <category><text>{esc(path)}</text></category>\n    <info format="html"><text></text></info>\n  </question>'

parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<quiz>']
total = 0
for name, qs in BANK:
    parts.append(cat_xml(f'$course$/top/{TOP}/{name}'))
    parts += [q_xml(q) for q in qs]; total += len(qs)
parts.append('</quiz>')
out = pathlib.Path(__file__).with_name('final_test.xml')
out.write_text('\n'.join(parts) + '\n', encoding='utf-8', newline='\n')
print(f'written {out.name}: {len(BANK)} categories, {total} questions')
for name, qs in BANK: print(f'  {name}: {len(qs)}')
