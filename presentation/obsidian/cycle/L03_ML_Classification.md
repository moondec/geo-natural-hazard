---
date_create: 2026-10-21
tags:
  - Geo
  - GEE
  - ML
topic: 👨🏼‍🏫  Wykład
type: wyklad
author: Marek Urbaniak
lecture: 3
summary: "Wykład 3 (2 h, 23.11.2026) – uczenie maszynowe do klasyfikacji pokrycia terenu w GEE: nadzorowana (Random Forest), nienadzorowana (k-means), dane treningowe, ocena dokładności, poprawa klasyfikacji, regresja; wstęp do ćwiczeń 3 i raportu"
timeForPresentation: 5400
theme: beige
width: 1920
height: 1200
margin: 0
maxScale: 4
transition: zoom
course: Application of geoinformatics to natural hazards mapping and monitoring
---

<!-- slide data-background-image=![[sateliteGEEbanner.png|1920]] -->
<grid drag="64 58" drop="0 27" bg="#EEB73F" align="left" pad="60px 60px 60px 300px">

### Lecture 3<!-- element style="letter-spacing: 1.5rem;"-->
## Machine learning for land cover classification
#### supervised, unsupervised, and how to know which is better

#### Marek Urbaniak

</grid>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Today (90 min)
:::
<grid drag="13 26" drop="92 55" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1"/>

::: block <!-- element style="font-size: 44px" align="left" drag="80 80" drop="0 15"-->
1. Last week: thresholds on one band. This week: a machine chooses them in ten bands
2. Supervised vs. unsupervised vs. regression
3. Decision tree → Random Forest (how the "votes" work)
4. k-means (how the clusters form)
5. Training data: how many, where, which mistakes to avoid
6. Accuracy: confusion matrix, overall accuracy, kappa – the number your report needs
7. Improving the classification: masks, indices, elevation, normalisation
8. **In the lab**: RF + k-means on your area, report
:::

<style>.reveal table{max-width:100%;border-collapse:collapse}.reveal table th,.reveal table td{padding:3px 8px;line-height:1.25}</style>

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## What is machine learning (for us)?
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="55 75" drop="0 15"-->
**Machine learning** = statistical techniques that let a computer *learn* a rule from data instead of being given the rule.

Last week **you** wrote the rule: `NDVI > 0.4 → forest`.
This week you give the computer *examples* (pixels with known class) and it finds the rule in **all bands** at once: B2…B12, NDVI, NDWI, elevation, slope…

Each pixel = one row of a table; each band = one column (a *feature*, *predictor*); the class = the *label*.
:::

::: block <!-- element style="font-size:30px" align="left" drag="44 75" drop="56 15" bg="#e8f4f8" pad="12px"-->
| | Input | Output | GEE |
|---|---|---|---|
| **Supervised classification** | labelled pixels | discrete class | `smileRandomForest` |
| **Unsupervised classification** | pixels only | cluster id | `wekaKMeans` |
| **Regression** | labelled values | a continuous number | `linearFit` reducer, or any classifier in `REGRESSION` mode |
:::

::: source
source: [Earth Engine – machine learning overview](https://developers.google.com/earth-engine/guides/machine-learning)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Supervised / unsupervised / regression
:::

<grid drag="13 26" drop="80 58" bg="#ffB73F"/>
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>
<grid drag="13 26" drop="77 90" bg="#F06400" />

::: block <!-- element style="font-size: 52px; " class="fragment fade-out" data-fragment-index="1"-->
-   **Supervised classification:** ground-truth examples teach a model to differentiate between classes. Earth Engine's built-in [supervised classifiers](https://developers.google.com/earth-engine/guides/classification) support this process. You decide the classes and their meaning.
:::
::: block <!-- element style="font-size: 52px;" drag="100" drop="top"  class="fragment fade-in-then-out" data-fragment-index="1"-->
-   **Unsupervised classification:** no ground truth. The algorithm divides the data into clusters based on inherent differences ([unsupervised classifiers](https://developers.google.com/earth-engine/guides/clustering)). Useful when you have no field data, do not know the number of classes, or want a quick look. **You** must name the clusters afterwards.
:::
::: block <!-- element style="font-size: 52px; "  drag="100" drop="top"  class="fragment fade-in-then-out" data-fragment-index="2"-->
-   **Regression:** predicts a continuous variable per pixel – water quality, percent forest cover, crop yield, burn severity as a number. See [linear regression reducers](https://developers.google.com/earth-engine/guides/reducers_regression).
:::

::: source
source: https://developers.google.com/earth-engine/guides/machine-learning
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="16 26" drop="80 23" bg="#ffB73F" rotate="-15"/>
<grid drag="12 20" drop="7 75" bg="#00ced1" />
<grid drag="16 26" drop="77 70" bg="#F06400" rotate="15" />

::: title
## Decision Tree ➡️ Random forest
:::
::: block<!-- element  drop="top" -->
![[Drawing 2023-01-10 00.31.47.excalidraw.png]]
:::

note:
A decision tree asks one question per node ("is NIR > 0.3?"), splits the pixels, and asks again, until the leaves are (almost) pure. It is fast and readable, but a single tree memorises the training pixels (overfitting).

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
<grid drag="16 26" drop="95 3" bg="#ffB73F" rotate="-15"/>
<grid drag="12 20" drop="0 95" bg="#00ced1" rotate="45"/>
<grid drag="16 26" drop="77 90" bg="#F06400" rotate="15" />

::: title
## Decision Tree ➡️ Random forest
:::
::: block <!-- element  drop="top"  flow="row"-->
![[Drawing 2023-01-10 00.31.47.excalidraw.png]] 
![[Drawing 2023-01-10 00.59.07.excalidraw.png]]
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Random Forest in four steps
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size: 46px; " align="left" drag="55 75" drop="0 15"-->
1. Take the **training set**; draw a random sample of pixels with replacement (bootstrap)
2. Grow a decision tree on that sample, choosing at **each split** from a random subset of the bands (`variablesPerSplit`; the default is the square root of the number of bands)
3. Repeat for `numberOfTrees` (e.g. 50–200) trees – each one slightly different
4. For a new pixel every tree votes; the class with the **majority vote** wins
:::

::: block <!-- element style="font-size: 36px;" align="left" drag="42 75" drop="58 15" bg="#e8f4f8" pad="15px"-->
```javascript
var classifier = ee.Classifier.smileRandomForest(50)
  .train({features: labelledPixels, classProperty: 'landcover',
          inputProperties: composite.bandNames()});
var classified = composite.classify(classifier);
```
Why it is the default choice in remote sensing:
- robust to noise and to correlated bands
- no scaling needed, few parameters
- gives *variable importance* (`classifier.explain()`) – which band mattered
- weakness: cannot predict a class it has never seen; needs good training data
:::

::: source
source: Breiman, L. (2001). Random Forests. *Machine Learning* 45, 5–32.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## k-means: clustering without labels
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size: 44px; " align="left" drag="52 75" drop="0 15"-->
1. Choose **k** (number of clusters) – e.g. 4, the same as your supervised classes
2. Put k centres at random in the band space
3. Assign every pixel to the nearest centre
4. Move each centre to the mean of its pixels
5. Repeat 3–4 until nothing moves
:::

<!-- TODO image: simple 2-D scatter (NIR vs red) with 4 colored clusters and centroids. Could be drawn in Excalidraw in the same style as the RF drawings. -->

::: block <!-- element style="font-size: 36px;" align="left" drag="45 75" drop="55 15" bg="#e8f4f8" pad="15px"-->
```javascript
var clusterSample = composite.sample({region: aoi, scale: 10, numPixels: 5000});
var clusterer = ee.Clusterer.wekaKMeans(4).train(clusterSample);
var clusters = composite.cluster(clusterer);
```
- cluster **numbers mean nothing** – cluster 2 is not "forest" until you look at the map and say so
- the result depends on the bands you give it and on k; try k = 4, 6, 8
- the computer finds *spectral* groups, not *land cover* classes: sunlit and shaded forest can be two clusters, wheat and grass one
- good for: a first look at an unknown area, finding how many classes are really separable
:::

::: source
source: [Earth Engine – unsupervised classification](https://developers.google.com/earth-engine/guides/clustering)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Training data: the part that decides the result
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size: 34px; " align="left" drag="50 78" drop="0 15"-->
In the Code Editor: geometry tools → new layer per class → **Import as FeatureCollection** → add property `landcover` = 0, 1, 2, 3 → draw polygons/points.

Rules:
- the same number of classes you will defend in the report (4 is fine)
- **spread** the samples over the whole area, not one corner
- every class gets a similar number of pixels (polygons of similar total area)
- pure pixels: inside a lake, inside a forest – not on edges
- use the median composite, not a single date, so the samples represent the season
:::

::: block <!-- element style="font-size: 32px;" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
var labelledPixels = composite.addBands(clusters).sampleRegions({  // bands + k-means cluster
  collection: trainingSamples,        // your 4 merged FeatureCollections
  properties: ['landcover'],
  scale: 10
});
// keep 30 % aside for validation
var withRandom = labelledPixels.randomColumn('random');
var trainSet = withRandom.filter(ee.Filter.lt('random', 0.7));
var testSet  = withRandom.filter(ee.Filter.gte('random', 0.7));
```
Common mistakes: *Import as Geometry* instead of FeatureCollection; a forgotten `landcover` property; classes named `1, 2, 3, 4` in one layer and `0…3` in another.
:::

::: source
source: [End-to-End GEE – supervised classification](https://courses.spatialthoughts.com/end-to-end-gee.html#supervised-classification)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Accuracy assessment: the confusion matrix
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size: 29px; " align="left" drag="50 78" drop="0 15"-->
Classify the **test set** (pixels the model has not seen) and compare predicted vs. true class:

| true \ predicted | water | urban | crops | forest | **PA** |
|---|---|---|---|---|---|
| water | 48 | 1 | 1 | 0 | 96 % |
| urban | 0 | 40 | 8 | 2 | 80 % |
| crops | 0 | 6 | 42 | 2 | 84 % |
| forest | 0 | 1 | 3 | 46 | 92 % |
| **UA** | 100 % | 83 % | 78 % | 92 % | |

Overall accuracy = diagonal / total = 176 / 200 = **88 %**
:::

::: block <!-- element style="font-size: 27px;" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
var testClassified = testSet.classify(classifier);
var confusionMatrix = testClassified.errorMatrix('landcover', 'classification');
print('confusion matrix', confusionMatrix);
print('overall accuracy', confusionMatrix.accuracy());
print('kappa', confusionMatrix.kappa());
print('producer accuracy', confusionMatrix.producersAccuracy());
print('consumer accuracy', confusionMatrix.consumersAccuracy());
```
- **Producer's accuracy** (recall): of the real crops, how many did we find?
- **User's accuracy** (precision): of the pixels we called crops, how many are crops?
- **kappa**: agreement corrected for chance (0 = random, 1 = perfect); 0.81–1 "almost perfect" on the Landis & Koch (1977) scale – optional and criticised (Foody 2020): report overall, producer's and user's accuracy first
- this is the number that lets you say *which classifier did the job better* in the report – not "it looks nicer"
:::

::: source
source: Congalton, R.G. (1991). *Remote Sensing of Environment* 37, 35–46; Landis & Koch (1977). *Biometrics* 33, 159–174; Foody (2020). *Remote Sensing of Environment* 239, 111630.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Comparing supervised and unsupervised results
:::

::: block <!-- element style="font-size: 32px; " align="left" drag="95 78" drop="0 15"-->
| Question | Random Forest | k-means |
|---|---|---|
| Do I need field / reference data? | yes (training + test) | no (but you need them to *name* and *check* the clusters) |
| Who decides the number of classes? | you | you (k) – but the data may disagree |
| Can I compute accuracy? | yes, confusion matrix on test set | only after you map clusters → classes; then yes |
| Typical problem | bad or biased training samples | spectrally similar classes merge; one class splits into several clusters |
| Time | 20 min drawing samples | 2 min |
| Use in hazards | land cover before/after, damage classes | first look, stratification, finding anomalies |

A fair comparison in the report: same AOI, same composite, same 4 classes, **a confusion matrix for both** (for k-means: relabel clusters to classes first with `remap`).
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Improving the classification
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size: 29px; " align="left" drag="50 78" drop="0 15"-->
1. **Cloud masking** per pixel before the median: `SCL` (classes 3, 8, 9, 10) or, better, Cloud Score+ (`cs_cdf` ≥ 0.6) – not `QA60`, which is empty for 2022–Feb 2024 scenes; lecture 7 explains the bits
2. **Add spectral indices** as extra bands: NDVI, NDBI (built-up), MNDWI (water), BSI (bare soil)
3. **Add elevation and slope** from a DEM (`NASA/NASADEM_HGT/001`, `ee.Terrain.slope`) – forests and crops rarely share the same slope
4. **Normalise** inputs to 0–1 (divide by the band maximum) – needed for SVM / neural nets, harmless for RF
5. **More trees** (100–200) and more, better-distributed samples
6. Post-processing: majority filter (`focal_mode`) to remove salt-and-pepper pixels
:::

::: block <!-- element style="font-size: 24px;" align="left" drag="45 78" drop="53 15" bg="#e8f4f8" pad="15px"-->
```javascript
var ndvi  = composite.normalizedDifference(['B8','B4']).rename('ndvi');
var mndwi = composite.normalizedDifference(['B3','B11']).rename('mndwi');
var ndbi  = composite.normalizedDifference(['B11','B8']).rename('ndbi');
var dem   = ee.Image('NASA/NASADEM_HGT/001').select('elevation');
var slope = ee.Terrain.slope(dem).rename('slope');
var stack = composite.addBands([ndvi, mndwi, ndbi, dem, slope]);
```
Ready examples in Moodle (lesson *Classifiers*, page 4): k-means, RF + k-means, RF difference matrix.
Check which input mattered: `print(classifier.explain())` → `importance`.
:::

::: source
source: [End-to-End GEE – improving the classification](https://courses.spatialthoughts.com/end-to-end-gee.html#improving-the-classification)
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Regression: when the answer is a number
:::
<grid drag="13 26" drop="80 28" bg="#ffB73F"/>
<grid drag="13 26" drop="87 45" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size: 60px; " class="fragment fade-out" data-fragment-index="1"-->
![[Pasted image 20230109230711.png|1200]]
:::
::: block <!-- element style="font-size: 60px;" drag="80" drop="topleft"  class="fragment fade-in-then-out" data-fragment-index="1"-->
![[Drawing 2023-01-09 23.21.12b.excalidraw.png]]
:::
::: block <!-- element style="font-size: 60px;" drag="80" drop="topleft"  class="fragment fade-in-then-out" data-fragment-index="2"-->
![[Drawing 2023-01-09 23.58.08.excalidraw.png]]
:::

note:
Examples in hazards: percent of a pixel burned, flood depth from SAR backscatter, landslide susceptibility as a probability. In GEE: `ee.Reducer.linearFit()` on a time series, or any classifier with `.setOutputMode('REGRESSION')`.

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## ML for hazards: two papers you will reproduce
:::

::: block <!-- element style="font-size: 42px; " align="left" drag="95 75" drop="0 15"-->
- **Landslides** – Handwerger et al. (2022), *Generating landslide density heatmaps for rapid detection using open-access satellite radar data in Google Earth Engine*, [NHESS 22, 753–773](https://nhess.copernicus.org/articles/22/753/2022/) – SAR change + thresholds, no training data. Lab 5.
- **Wildfires** – burn severity from dNBR with the [UN-SPIDER recommended practice](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/burn-severity-earth-engine) and, as an ML extension, RF classification of damage classes. Lab 6.
- The same task – per-pixel land cover from Sentinel-2 – is what [Dynamic World](https://dynamicworld.app/) (Google / WRI) does in near real time at 10 m, with a convolutional neural network instead of a Random Forest – `GOOGLE/DYNAMICWORLD/V1` in the catalogue, a ready reference layer for your reports.
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## In the lab (30.11, 3 h)
:::
<grid drag="13 26" drop="87 75" bg="#00ced1" rotate="-15"/>

::: block <!-- element style="font-size:40px" align="left" drag="95 78" drop="0 15"-->
1. Pick your area (60–100 km², ≥ 4 surface types); build the cloud-light Sentinel-2 median composite for one season
2. **Supervised**: draw training polygons for 4 classes (FeatureCollection, property `landcover`), split 70/30, train `smileRandomForest(50)`, classify, confusion matrix + overall accuracy + kappa
3. **Unsupervised**: `wekaKMeans(4)` on the same composite; relabel clusters to your classes; confusion matrix
4. Export both maps to Drive (`Export.image.toDrive`, scale 10) for the report figure
5. **Homework (assignment)**: report .pdf/.docx – maps, the two confusion matrices, number of classes justified, one paragraph: *which classifier did the job better and why*; links to both scripts
:::

---
<!-- slide template="[[tpl-geo-default-slide]]" -->
::: title
## Before next class
:::
<grid drag="13 26" drop="80 53" bg="#ffB73F"/>

::: block <!-- element style="font-size:42px" align="left" drag="95 75" drop="0 15"-->
- [ ] Submit the classification report
- [ ] Open Moodle → *Classifiers* lesson → page *ML algorithms* → the short "GEO_ML_Classifiers" slides (10 min)
- [ ] Read End-to-End GEE module 3, *Supervised classification* and *Accuracy assessment* (skim; you did it in the lab)
- [ ] Next week is about **floods** and **radar**: watch [Sentinel-1 for flood mapping, UN-SPIDER](https://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping) (read the *In detail* tab, 15 min)
:::

---
::: block 
# Thank you :smile:
:::
