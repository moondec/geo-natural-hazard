"""Homework assignment descriptions (assign.intro) for AGeoHazard – writes mcontent/s<n>-assign-<cmid>.intro.html.

Every description has the same four blocks: lead, "What to submit" (task callout), "Report template"
(the common chapter list with the milestone-specific items inside), "Before you upload" (check callout).
Run:  python -I -X utf8 build_assign_intros.py   then  inline-iot-css.py geo.scss mcontent  and gpush.
Assignment modules themselves are created/updated by assignments.php (dates, plugins).
"""
import html, pathlib
OUT = pathlib.Path(__file__).with_name('mcontent')
W = 'http://localhost:8088'
def mod(kind, cmid): return f'{W}/mod/{kind}/view.php?id={cmid}'
def esc(s): return html.escape(s, quote=False)

# The common report skeleton. Each milestone adds its own sub-items to chapters 3–6.
CHAPTERS = [
    ('Title and metadata', 'event or area, dates, your name, the link to the saved script (test it in a private browser window)'),
    ('Aim', 'one sentence: what was mapped and why'),
    ('Data', 'collections and their IDs, acquisition dates, the AOI (area in km², how it was defined), reference data'),
    ('Method', 'the steps in the order of the script; every parameter and threshold with a one-sentence justification'),
    ('Results', 'the map(s) with legend, scale bar and source line; the numbers (tables in hectares, accuracies, counts)'),
    ('Validation and uncertainty', 'comparison with a reference and the sensitivity test where required'),
    ('Limitations and conclusions', 'clouds, phenology, resolution, speckle, sample quality – and two or three sentences on what the map can and cannot be used for'),
]

ASSIGN = {
 2: dict(cmid=392, lesson=('Google Earth Engine', 391),
    lead='Homework after lab 2 (23.11): repeat the lesson workflow (filter → median → index → classes → area table) for an index of your choice and your own area of interest. Due <strong>30.11, at the start of lab 3</strong>. You submit a link to a working Earth Engine script and a short report (.pdf or .docx, 2–3 pages) written to the template below.',
    submit=[
      'Create your own JavaScript code for Earth Engine that calculates the area occupied by the categories of a selected index (e.g. EVI, NDWI, SAVI, NDMI – not NDVI).',
      'Specify an area of interest (AOI) that is not very large: a city, a district or a national park (about 50–500 km²).',
      'Choose your own thresholds and justify them in one or two sentences (histogram, Inspector values, literature).',
      'Save the script, click <em>Get Link</em> and paste the link in the report and in the submission comment.',
      'Upload the report as .pdf or .docx.'],
    specific={'Data': ['the collection (<code>COPERNICUS/S2_SR_HARMONIZED</code>), the date range and the cloud filter used', 'the AOI: how you defined it (polygon, point + buffer, GAUL district)'],
              'Method': ['the index formula and its bands', 'the cloud mask you applied (SCL, Cloud Score+)', 'the thresholds and the class codes', 'the <code>scale</code> used in <code>reduceRegion</code>'],
              'Results': ['the index map and the class map with a legend', 'the area table per class in hectares'],
              'Validation and uncertainty': ['three pixels checked with the Inspector (field, forest, water) and whether they fall in the expected class', 'what happens to the areas when a threshold moves by ±0.05']},
    check='The script link opens without error in a private browser window; the area table sums up to the AOI area; the thresholds in the text are the ones in the code.',
    extra=pathlib.Path(__file__).with_name('fragments').joinpath('m2_indices.html').read_text(encoding='utf-8')),   # index list with Sentinel Hub custom-script links (kept from the old description)
 3: dict(cmid=398, lesson=('Classifiers', 396),
    lead='Milestone M3 – the classification report from lab 3 (30.11), due <strong>7.12, at the start of lab 4</strong>. Submit one .pdf or .docx file with the maps, the accuracy tables and the links to both scripts from the lesson <em>Classifiers</em>, written to the template below.',
    submit=[
      'Select any area (covering 60–100 km²) with different surface types.',
      'Based on Sentinel-2 images, use a supervised (Random Forest) algorithm and make a surface classification on the basis of your own FeatureCollection (put geo-points or small polygons on the map and teach the model the surface characteristics).',
      'Based on Sentinel-2 images, determine the types of surfaces using an unsupervised algorithm (k-means). Use the same area of interest (AOI) and the same composite for both classifications.',
      'For <strong>both</strong> classifiers give the confusion matrix, the overall accuracy and kappa (for k-means after relabelling the clusters to your classes).',
      'Justify briefly the selected number of classes and in one paragraph describe your conclusions about both classifiers. Which one did the job better in your opinion and why? Use the accuracy numbers, not only the look of the map.',
      'Add the links to both scripts.'],
    specific={'Data': ['the composite: collection, date range, cloud filter and mask, bands used', 'the training data: number of sampled pixels per class, how the polygons were drawn'],
              'Method': ['Random Forest settings (number of trees, bands), the 70/30 split', 'k-means settings (k) and the cluster → class mapping you decided on', 'any improvement you tried (indices, DEM, majority filter)'],
              'Results': ['both classified maps with the same legend (0…3)', 'both confusion matrices (4 × 4), overall accuracy, producer\'s and user\'s accuracy, kappa', 'variable importance if you used <code>classifier.explain()</code>'],
              'Validation and uncertainty': ['the comparison paragraph: which classifier did better and why, with the numbers', 'optional: a visual comparison with Dynamic World (<code>GOOGLE/DYNAMICWORLD/V1</code>)']},
    check='Both script links open without error in a private browser window; both maps have a legend; the two confusion matrices are 4 × 4 and the accuracy numbers in the text match them.'),
 4: dict(cmid=431, lesson=('flood mapping', 401),
    lead='Milestone M4 – the flood extent map from lab 4 (7.12), due <strong>14.12, at the start of lab 5</strong>. Submit one .pdf or .docx report written to the template below, with the link to your copy of the UN-SPIDER flood script.',
    submit=[
      'Pick a documented flood event (Copernicus Browser highlights, EMS activation, or south-west Poland, September 2024) and define the AOI.',
      'Run the Sentinel-1 change-detection script (lesson page <em>ICEYE / the lab scripts</em>): before and after periods, polarisation, orbit pass, threshold 1.25, speckle filter, masks.',
      'Produce the flood extent map with the event name and dates, and the flooded area in hectares.',
      'Sensitivity test: repeat with the thresholds 1.15 and 1.40 and with another filter radius (e.g. 30 m and 100 m); put the flooded areas in a table.',
      'Compare your map with the Global Flood Monitoring product or an EMS map of the same event – one paragraph of agreement and disagreement.',
      'Optional: the optical MNDWI map (script 1) for the same event and the two areas side by side.'],
    specific={'Data': ['<code>COPERNICUS/S1_GRD</code>: before period and after period (dates), polarisation (VH/VV), orbit pass (ascending/descending), number of scenes in each period', 'reference: GFM or EMS product used, with its date'],
              'Method': ['speckle filter radius, difference threshold (1.25) and what it means in dB', 'the masks: permanent water (JRC GSW), slope, connected pixels'],
              'Results': ['the flood extent map (legend: flooded / permanent water), event name and dates in the title', 'the flooded area in hectares'],
              'Validation and uncertainty': ['the sensitivity table: threshold (1.15 / 1.25 / 1.40) × filter radius versus flooded area, and how much the area changes (factor)', 'the comparison with GFM or EMS: where do the maps agree and disagree, and why (wind, flooded vegetation, urban areas, shadow)']},
    check='The flood layer lies along the river and not on mountain slopes; permanent lakes are not counted; the area changes by less than a factor of two between the thresholds 1.15 and 1.40; the script link opens in a private browser window.'),
 5: dict(cmid=432, lesson=('landslides', 402),
    lead='Milestone M5 – the landslide heatmap note from lab 5 (14.12), due <strong>21.12, at the start of lab 6</strong>. A short report (.pdf or .docx, 2–4 pages) written to the template below, with one figure and the link to your saved script.',
    submit=[
      'Choose an event with a known date and a reference inventory: one of the cases of Handwerger et al. (2022) (Hokkaido 2018, Hiroshima 2018, Haiti 2021) or an EMS landslide activation.',
      'Run the heatmap script with your AOI, event date, pre-event window (months), post-event window (weeks) and one Sentinel-1 orbit.',
      'Inspect the I_ratio layer on a known landslide and on an untouched slope and note the values.',
      'Vary the percentile threshold (99th, 90th, 80th), the kernel radius (1–3 km) and the length of the pre-event stack; describe how the heatmap changes.',
      'Overlay the reference (EMS grading map or a post-event Sentinel-2 true-colour image) and judge the agreement.',
      'Export the heatmap as GeoTIFF and write the note.'],
    specific={'Data': ['Sentinel-1 orbit (ascending/descending), pre-event window and post-event window with the number of scenes in each', 'the reference inventory or EMS product (name, date)'],
              'Method': ['the log-ratio formula and its sign convention (positive = darker after the event)', 'masks: slope limit, water; the percentile threshold; kernel radius and cell size'],
              'Results': ['one figure: the heatmap with the reference overlaid, AOI outline, scale bar', 'the I_ratio values you read on a landslide and on an untouched slope'],
              'Validation and uncertainty': ['which valleys agree with the reference and which do not', 'how the heatmap changed when you moved the percentile and the kernel radius']},
    check='The heatmap highlights the valleys that the reference shows as hit; I_ratio on untouched slopes stays near zero; flat valley floors are masked out; the GeoTIFF opens in QGIS with the right coordinates; the script link opens in a private browser window.'),
 6: dict(cmid=433, lesson=('fire detection and severity estimation', 403),
    lead='Milestone M6 – the burn severity map and report from lab 6 (21.12), due <strong>11.01, at the start of lab 7</strong>. One .pdf or .docx report written to the template below, with the link to your saved script.',
    submit=[
      'Your fire: start and end dates from FIRMS hotspots; cloud-free pre- and post-fire Sentinel-2 dates from Copernicus Browser; the perimeter from EFFIS or Copernicus EMS.',
      'Run the burn severity script on <code>COPERNICUS/S2_SR_HARMONIZED</code> with your pre and post windows and your AOI; check in the Console how many images were found in each window.',
      'Classify dNBR with the USGS thresholds (−250, −100, 100, 270, 440, 660 on the × 1000 scale), add a legend and compute the area per class in hectares.',
      'Compare the perimeter with EFFIS or EMS: where do they disagree and why (clouds, phenology, agricultural fields)?',
      'Export the severity map as GeoTIFF (scale 20 m) and write the report with the checklist of lesson page 3.',
      'Optional: an NDVI or NBR time series over the perimeter for the years after the fire (recovery).'],
    specific={'Data': ['FIRMS timeline (first and last hotspot), pre and post windows and the number of Sentinel-2 images in each', 'the band used for NIR (B8 or B8A) and SWIR2 (B12); EFFIS/EMS perimeter with its date'],
              'Method': ['the cloud mask, NBR and dNBR formulas, the × 1000 scaling', 'the USGS class thresholds and a remark on their origin (US forests)'],
              'Results': ['the burn severity map with the USGS legend and the perimeter overlaid', 'the area per class in hectares, summing up to the AOI area', 'the dNBR histogram over the perimeter'],
              'Validation and uncertainty': ['the comparison with the EFFIS/EMS perimeter (area inside/outside, reasons for disagreement)', 'the unburned class outside the perimeter as a check of the phenology match']},
    check='The unburned class covers the area outside the perimeter; the dNBR histogram over the perimeter has its unburned peak near 0; the sum of the class areas equals the AOI area; the script link opens in a private browser window.'),
 7: dict(cmid=434, lesson=('Application Programming Interfaces (API) for GEE', 404),
    lead='Milestone M7 – the capstone, due <strong>25.01.2027</strong> (to be confirmed in lecture 8). Pick <strong>one hazard</strong> from labs 4–6 (flood extent, landslide heatmap or burn severity) and reproduce it outside the Code Editor: as a <strong>Colab notebook</strong> (Python, geemap) with text cells, as a <strong>QGIS project</strong> with a PDF map and a short report, or in R (rgee) for volunteers. Paste the notebook link (Drive or GitHub) in the online text and upload the file(s).',
    submit=[
      'Notebook route: a .ipynb (upload) or a shared Colab/GitHub link (online text) that runs from top to bottom after <code>ee.Initialize(project=…)</code>; text cells carry the report chapters below.',
      'QGIS route: the project file (.qgz) and a PDF map from the Print Layout (title, legend, scale bar, north arrow, source line) plus a short report (.pdf or .docx) with the chapters below and the Earth Engine script link.',
      'R route (volunteers): an .Rmd or Quarto notebook rendered to .pdf/.html, same chapters.',
      'Whatever the route: the parameters (AOI, dates, thresholds, collections), the figures (map, histogram or time series), the area numbers and a limitations section.'],
    specific={'Data': ['the hazard and event you reproduced, with the lab (4, 5 or 6) it comes from', 'collections, dates, AOI'],
              'Method': ['the workflow as code cells with a text cell before each step (what and why)', 'differences to the Code Editor version (client vs server objects, exports)'],
              'Results': ['the map as a figure in the notebook (geemap) or the PDF map (QGIS)', 'the area numbers (hectares) and, if applicable, a histogram or time series'],
              'Validation and uncertainty': ['the comparison with a reference as in the original lab (EMS, EFFIS, GFM)', 'one parameter varied and its effect']},
    check='A colleague can open your notebook or project, run all cells from top to bottom after <code>ee.Initialize(project=…)</code> (or <code>ee_Initialize()</code>) and obtain the same map and numbers; every figure has a caption; the limitations section exists.'),
}

def template_html(spec):
    items = []
    for i, (title, desc) in enumerate(CHAPTERS, 1):
        sub = spec['specific'].get(title, [])
        subhtml = ('<ul class="iot-material-list">' + ''.join(f'<li>{s}</li>' for s in sub) + '</ul>') if sub else ''
        items.append(f'<li><strong>{title}</strong> – {desc}.{subhtml}</li>')
    return ('<div class="iot-material-callout">\n<p class="iot-material-callout-title">Report template – the chapters of your report</p>\n'
            '<p>Use these headings in this order (3–6 pages; maps as numbered figures with captions). The same template is used for every homework of the course, so the points you learn here count every time.</p>\n'
            '<ol class="iot-material-list">\n' + '\n'.join(items) + '\n</ol>\n</div>')

for n, a in ASSIGN.items():
    lname, lcm = a['lesson']
    body = ['<div class="iot-material iot-material--page" data-iot-material="v1">',
            f'<p class="iot-material-lead">{a["lead"]}</p>',
            '<div class="iot-material-callout iot-material-callout--task">', '<p class="iot-material-callout-title">What to submit</p>',
            '<ol class="iot-material-list">', *[f'<li>{s}</li>' for s in a['submit']], '</ol>',
            f'<p>The step-by-step instructions are in the lesson <a href="{mod("lesson", lcm)}">{esc(lname)}</a>.</p>', '</div>',
            template_html(a),
            a.get('extra', ''),
            '<div class="iot-material-callout iot-material-callout--check">', '<p class="iot-material-callout-title">Before you upload</p>',
            f'<p>{a["check"]}</p>', '</div>', '</div>']
    (OUT / f's{n}-assign-{a["cmid"]}.intro.html').write_text('\n'.join(body) + '\n', encoding='utf-8', newline='\n')
    print('written', f's{n}-assign-{a["cmid"]}.intro.html')
