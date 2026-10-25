# Generates section summaries (s0..s7), lecture-resource intros and ops.tsv for the AGeoHazard course (id=15).
# Run from the course/ directory:  python -I -X utf8 build_summaries.py   then  python -I -X utf8 inline-iot-css.py geo.scss mcontent
import pathlib, html
OUT = pathlib.Path(__file__).parent / 'mcontent'
W = 'http://localhost:8088'
def sec(id_): return f'{W}/course/section.php?id={id_}'
def mod(kind, cmid): return f'{W}/mod/{kind}/view.php?id={cmid}'

SECTION_IDS = {0: 116, 1: 117, 2: 118, 3: 119, 4: 120, 5: 121, 6: 122, 7: 123}

# ---------------------------------------------------------------- modules
MODULES = [
    dict(n=1, short='Kick-off', title='Natural hazards, Earth observation and your accounts',
         lecture=423, hours='3 h',
         lead='Why satellites are the only way to see a flood, a landslide scar or a burned forest in time, and one recipe (before / after) that we will reuse for every hazard. The lab gets your two accounts working and shows you the first real event in Copernicus Browser.',
         outcome='Due in lab 1 – a CDSE account, a registered Google Earth Engine project, one hazard event found in Copernicus Browser (dates, AOI, timelapse) and your first script running in the Code Editor.',
         route=[('Watch lecture 1', 'Hazards, before/after, sensors, where to get data today', mod('page', 423)),
                ('Create your accounts', 'CDSE (Copernicus Browser) and a Google Cloud project for Earth Engine – before the first lab', mod('page', 390)),
                ('Lab 1 – Copernicus Browser', 'Find one wildfire and one flood in Highlights, compare, export a GeoTIFF', None),
                ('Lab 1 – first GEE script', 'Open the Code Editor, load Sentinel-2, add the End-to-End repository', None),
                ('Homework', 'Webinars on the homework page; bring one event you care about', mod('page', 390))],
         links=[('Lecture 1 (slides)', mod('page', 423)),
                ('Homework after lecture 1', mod('page', 390)),
                ('Copernicus Browser', 'https://browser.dataspace.copernicus.eu/'), ('GEE access guide', 'https://developers.google.com/earth-engine/guides/access')],
         extra='''<h5 class="iot-h">What you need before lab 1</h5>
      <ul class="iot-list">
        <li>A free account at <a href="https://dataspace.copernicus.eu/" target="_blank" rel="noopener">dataspace.copernicus.eu</a>; log in once to <a href="https://browser.dataspace.copernicus.eu/" target="_blank" rel="noopener">Copernicus Browser</a>.</li>
        <li>A Google account with a <strong>registered Earth Engine Cloud project</strong> (noncommercial, education): <a href="https://developers.google.com/earth-engine/guides/access" target="_blank" rel="noopener">how to get access</a>. Approval can take a day – do not leave it for the morning of the lab.</li>
        <li>Problems? Ask on the <a href="%s" target="_blank" rel="noopener">forum</a> a few days before the lab.</li>
      </ul>''' % mod('forum', 388)),
    dict(n=2, short='Code Editor', title='Google Earth Engine: from a pixel to an area statistic',
         lecture=424, hours='3 h',
         lead='Earth Engine runs your script next to petabytes of imagery. You learn the three verbs of every script – filter, map, reduce – and turn an index (NDVI) into classes and hectares.',
         outcome='Due at the start of lab 3 – a saved Code Editor script (link) that filters Sentinel-2 over your area, computes an index, classifies it with thresholds and prints the area per class in hectares; homework "index areas" submitted.',
         route=[('Watch lecture 2', 'Client/server, data model, filter → map → reduce, indices, reduceRegion', mod('page', 424)),
                ('Lesson: GEE step by step', 'Sign-up check, End-to-End repository, collections, clouds first, NDVI, areas, quizzes', mod('lesson', 391)),
                ('Lab 2 – build the script', 'Line by line on your own AOI; verify three pixels with the Inspector', mod('lesson', 391)),
                ('Homework "index areas"', 'A different index, your own AOI and thresholds; submit the script link', mod('assign', 392)),
                ('Prepare lab 3', 'Pick an area of 60–100 km² with four clearly different surfaces', None)],
         links=[('Lecture 2 (slides)', mod('page', 424)), ('Lesson: Google Earth Engine', mod('lesson', 391)), ('Course scripts: add the GEO2 repository', 'https://code.earthengine.google.com/?accept_repo=users/marekurbaniak/GEO2'), ('Homework: index areas', mod('assign', 392)),
                ('End-to-End GEE course', 'https://courses.spatialthoughts.com/end-to-end-gee.html'), ('Earth Engine data catalogue', 'https://developers.google.com/earth-engine/datasets')],
         extra=''),
    dict(n=3, short='Machine learning', title='Machine learning for land cover classification',
         lecture=425, hours='3 h',
         lead='Last week you chose the thresholds; this week a Random Forest finds them in ten bands at once, and k-means finds groups without any labels. The number that lets you compare them is the confusion matrix.',
         outcome='Due at the start of lab 4 – a classification report – supervised (Random Forest) and unsupervised (k-means) maps of the same area, both confusion matrices with overall accuracy and kappa, a justified number of classes and one paragraph on which classifier did the job better. Links to both scripts.',
         route=[('Watch lecture 3', 'Supervised vs unsupervised, decision tree → Random Forest, k-means, training data, accuracy', mod('page', 425)),
                ('Lesson: Classifiers', 'ML algorithms, supervised, unsupervised, improving the classification, hazard examples', mod('lesson', 396)),
                ('Lab 3 – classify your area', 'Training polygons, RF (50 trees), k-means (4), confusion matrices, export', mod('lesson', 396)),
                ('Homework – the report', 'Maps, matrices, justification, conclusions; .pdf or .docx', mod('assign', 398)),
                ('Prepare lab 4', 'Read the UN-SPIDER flood practice ("In detail" tab)', None)],
         links=[('Lecture 3 (slides)', mod('page', 425)), ('Lesson: Classifiers', mod('lesson', 396)), ('Short deck: the two classifiers', mod('resource', 397)), ('Homework: classification report', mod('assign', 398)),
                ('GEE guide: supervised classification', 'https://developers.google.com/earth-engine/guides/classification')],
         extra=''),
    dict(n=4, short='Floods', title='Flood mapping: optical water indices and Sentinel-1 radar',
         lecture=426, hours='3 h',
         lead='Floods happen under clouds. Optical indices (NDWI, MNDWI) work on the first clear day; Sentinel-1 radar sees the peak through the clouds – calm water is dark. You run the UN-SPIDER change-detection script and learn where it fails.',
         outcome='Due at the start of lab 5 – a flood extent map of a real event from Sentinel-1 (before/after, threshold, masks), the flooded area in hectares with a threshold-sensitivity table, and a comparison with the Global Flood Monitoring or an EMS map.',
         route=[('Watch lecture 4', 'Water indices, SAR in 15 minutes, Sentinel-1, thresholds, operational services', mod('page', 426)),
                ('Lesson: flood mapping', 'Bands, satellites, water indices, SAR backscatter, InSAR, ICEYE, scripts', mod('lesson', 401)),
                ('Lab 4 – optical', 'MNDWI before/after on Sentinel-2, histogram, threshold, water area', mod('lesson', 401)),
                ('Lab 4 – radar', 'UN-SPIDER script: AOI, dates, orbit; vary the threshold; compare with GFM/EMS', mod('lesson', 401)),
                ('Homework M4 – the report', 'Flood map, hectares, sensitivity table, GFM/EMS comparison; .pdf or .docx', mod('assign', 431)),
                ('Prepare lab 5', 'Read Handwerger et al. 2022 (sections 1–3.1)', None)],
         links=[('Lecture 4 (slides)', mod('page', 426)), ('Lesson: flood mapping', mod('lesson', 401)),
                ('UN-SPIDER: flood mapping with Sentinel-1 in GEE', 'https://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping'),
                ('Global Flood Monitoring', 'https://global-flood.emergency.copernicus.eu/'), ('Quality assessment papers', mod('resource', 399)), ('Homework M4: flood extent map', mod('assign', 431))],
         extra='''<h5 class="iot-h">Error estimation – reading</h5>
      <p>Two papers on the quality of satellite products are attached to this module: <a href="%s" target="_blank" rel="noopener">A procedure for high-resolution satellite imagery quality assessment</a> (Sensors 2009) and <a href="%s" target="_blank" rel="noopener">TATSSI – quality data assessment of EO products</a> (IJGI 2021). They are the background for the "uncertainty" part of your reports.</p>''' % (mod('resource', 399), mod('resource', 400))),
    dict(n=5, short='Landslides', title='Landslide mapping with satellite radar',
         lecture=427, hours='3 h',
         lead='A landslide inventory is the input of every susceptibility model, and after a rain or earthquake event it must be produced in days. You run the Sentinel-1 amplitude-change method of Handwerger et al. (2022) that produces landslide density heatmaps in Earth Engine.',
         outcome='Due at the start of lab 6 – a landslide density heatmap of a documented event (parameters stated), an overlay with a reference inventory or EMS map, and a short note on where the method works and where it fails.',
         route=[('Watch lecture 5', 'Landslide types, triggers, inventory vs susceptibility, SAR change, InSAR, DEM', mod('page', 427)),
                ('Lesson: landslides', 'Understanding landslides; the GEE heatmap script', mod('lesson', 402)),
                ('Lab 5 – run the heatmap', 'Event, AOI, dates, orbit; inspect log-ratio; vary threshold; export', mod('lesson', 402)),
                ('Homework M5 – the note', 'Parameters, one figure with the reference, limitations; .pdf or .docx', mod('assign', 432)),
                ('Prepare lab 6', 'Find a fire with cloud-free pre and post Sentinel-2 dates', None)],
         links=[('Lecture 5 (slides)', mod('page', 427)), ('Lesson: landslides', mod('lesson', 402)),
                ('Handwerger et al. 2022, NHESS (must read)', 'https://nhess.copernicus.org/articles/22/753/2022/'),
                ('Copernicus EMS', 'https://mapping.emergency.copernicus.eu/'), ('International Charter', 'https://disasterscharter.org/'), ('Homework M5: landslide heatmap note', mod('assign', 432))],
         extra=''),
    dict(n=6, short='Wildfires', title='Wildfire detection and burn severity',
         lecture=428, hours='3 h',
         lead='Active fire hotspots tell you when it burned; the Normalized Burn Ratio before and after tells you how badly. You produce a burn severity map with the USGS dNBR classes and check it against EFFIS.',
         outcome='Due at the start of lab 7 – a burn severity map (dNBR, USGS classes) of your fire with the area per class in hectares, a FIRMS timeline, a comparison with the EFFIS perimeter and a short report following the checklist.',
         route=[('Watch lecture 6', 'Intensity vs severity, active fire, NBR, dNBR classes, choosing dates, validation', mod('page', 428)),
                ('Lesson: fire mapping', 'Background, spectral response, burn severity mapping, GEE script', mod('lesson', 403)),
                ('Lab 6 – severity map', 'FIRMS dates, pre/post composites, NBR, dNBR, classes, hectares', mod('lesson', 403)),
                ('Homework M6 – the report', 'Severity map, hectares per class, FIRMS timeline, EFFIS comparison; .pdf or .docx', mod('assign', 433)),
                ('Prepare lab 7', 'Install QGIS 3.44+ and the Google Earth Engine plugin at home; R volunteers: rgee', None)],
         links=[('Lecture 6 (slides)', mod('page', 428)), ('Lesson: fire detection and severity', mod('lesson', 403)),
                ('UN-SPIDER burn severity practice', 'https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/burn-severity-earth-engine'),
                ('NASA FIRMS', 'https://firms.modaps.eosdis.nasa.gov/'), ('EFFIS', 'https://forest-fire.emergency.copernicus.eu/'), ('Homework M6: burn severity map + report', mod('assign', 433))],
         extra=''),
    dict(n=7, short='Python & R', title='GEE beyond the Code Editor – and the wrap-up',
         lecture=429, hours='4 h',
         lead='The same engine from Python (Colab, geemap) and inside QGIS (the Earth Engine plugin, print layouts): reproducible notebooks, your own layers, real maps. The capstone reproduces one hazard workflow as a notebook or a QGIS project. Lecture 8 closes the course with uncertainty, operational services and assessment.',
         outcome='Due on the date set in the assignment (confirmed in lecture 8) – a Colab (or R) notebook that reproduces one of labs 4–6 with text cells, figures, parameters and a limitations section (or a QGIS project with a PDF map and a short report); the API quiz. This is the final deliverable of the course.',
         route=[('Watch lecture 7', 'Why leave the editor, Colab, JS → Python differences, exports, QGIS step by step', mod('page', 429)),
                ('Lesson: APIs for GEE', 'Python/Colab, Colab exercise, CDSE JupyterLab and openEO (for the curious), QGIS 1–4: plugin, console, no-code tools and export, the map (rgee for volunteers), quiz', mod('lesson', 404)),
                ('Lab 7 – Colab + geemap', 'Authenticate, translate your lab-2 script, export', mod('lesson', 404)),
                ('Lab 7 – GEE in QGIS', 'Four pages: plugin and sign-in, Python Console layer, no-code tools and export, the finished map', mod('lesson', 404)),
                ('Lab 7 – capstone', 'Pick flood, landslide or fire and rerun it as a notebook or a QGIS project with a map', mod('lesson', 404)),
                ('Homework M7 – capstone', 'Notebook link + files, or QGIS project + PDF map; report template in the assignment', mod('assign', 434)),
                ('Lecture 8 – wrap-up', 'One workflow, sources of error, uncertainty, what next, assessment', mod('page', 430)),
                ('Final test', '30 questions drawn from the seven lessons, 40 min, two attempts; 40 % of the course grade – opened by the lecturer at the end of the course', None)],
         links=[('Lecture 7 (slides)', mod('page', 429)), ('Lecture 8 – wrap-up (slides)', mod('page', 430)), ('Lesson: APIs for GEE', mod('lesson', 404)), ('Homework M7: capstone', mod('assign', 434)), ('Final test (opens at the end of the course)', mod('quiz', 435)), ('Python, QGIS and R examples (GitHub)', 'https://github.com/moondec/geo-natural-hazard/tree/main/examples'),
                ('Earth Engine Python quickstart', 'https://developers.google.com/earth-engine/guides/quickstart_python'), ('geemap', 'https://geemap.org/'), ('QGIS Earth Engine plugin – user guide', 'https://gee-community.github.io/qgis-earthengine-plugin/'), ('rgee (R volunteers)', 'https://r-spatial.github.io/rgee/'), ('For the curious: CDSE JupyterLab (free, on request)', 'https://dataspace.copernicus.eu/analyse/jupyterlab'), ('openEO Python client – documentation', 'https://open-eo.github.io/openeo-python-client/')],
         extra=''),
]

def module_html(m):
    n = m['n']
    route = ''.join(
        f'<li><div><strong>{html.escape(t)}</strong><span>{html.escape(d)}</span>' + (f' <a href="{u}">open →</a>' if u else '') + '</div></li>'
        for t, d, u in m['route'])
    links = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in m['links'])
    return f'''<div class="iot-module-intro">
  <p class="iot-module-label">Module 0{n} · lecture {n} → lab {n} ({m['hours']})</p>
  <div class="iot-module-grid">
    <div class="iot-module-main">
      <h4 class="iot-module-title">{html.escape(m['title'])}</h4>
      <p>{html.escape(m['lead'])}</p>
      <div class="iot-outcome"><span>M{n}</span><div><strong>Milestone</strong><p>{html.escape(m['outcome'])}</p></div></div>
      <aside class="iot-route" aria-label="Your path in module 0{n}">
        <p class="iot-route-title">Your path</p>
        <ol>{route}</ol>
      </aside>
      {m['extra']}
      <h5 class="iot-h">Materials of this module</h5>
      <ul class="iot-list">{links}</ul>
    </div>
  </div>
</div>
'''

# ---------------------------------------------------------------- course intro (section 0)
roadmap = ''.join(f'<a href="{sec(SECTION_IDS[m["n"]])}"><small>0{m["n"]}</small><strong>{html.escape(m["short"])}</strong></a>' for m in MODULES)
intro = f'''<div class="iot-course-intro">
  <div class="iot-hero">
    <div class="iot-hero-copy">
      <p class="iot-eyebrow">Geoinformation and Spatial Management · winter semester</p>
      <h4 class="iot-title">From satellite pixels to hazard maps.</h4>
      <p class="iot-lead">Seven modules, one recipe: images before and after the event, an index or a radar echo, a threshold, a map with hectares and an honest statement of its uncertainty – for floods, landslides and wildfires, in Google Earth Engine, Copernicus Browser, Python and R.</p>
      <p class="iot-actions"><a class="iot-button" href="{sec(SECTION_IDS[1])}">Start with module 01</a></p>
    </div>
    <figure class="iot-system-map" aria-labelledby="geo-flow-title">
      <figcaption id="geo-flow-title">The workflow you build in every module</figcaption>
      <div class="iot-flow">
        <div class="iot-flow-node"><strong>Before</strong><span>cloud-free composite or radar stack before the event</span></div>
        <span class="iot-flow-arrow" aria-hidden="true">→</span>
        <div class="iot-flow-node"><strong>After</strong><span>the first images after the flood, slide or fire</span></div>
        <div class="iot-flow-node iot-flow-wide"><strong>Difference → threshold → map</strong><span>index or backscatter change, classes, area in hectares, validation against EMS / EFFIS / GFM</span></div>
      </div>
      <p class="iot-map-result">Result: a reproducible hazard map with stated dates, thresholds, accuracy and limitations.</p>
    </figure>
  </div>

  <nav class="iot-start" aria-label="Start here">
    <a class="iot-start-primary" href="{mod('page', 390)}"><small>Step 1 · before the first lab</small><strong>Create your two accounts</strong><span>Copernicus Data Space (free) and a registered Google Earth Engine Cloud project. Approval takes up to a day – do it this week.</span></a>
    <a href="{mod('page', 423)}"><small>Lecture 1</small><strong>Course kick-off</strong><span>Hazards, the before/after recipe, how satellites see, where to get data today.</span></a>
    <a href="https://code.earthengine.google.com/?accept_repo=users/marekurbaniak/GEO2" target="_blank" rel="noopener"><small>Scripts</small><strong>Course script repository</strong><span>Every lab script, one folder per lesson. Click once to add GEO2 to your Code Editor (needs your Earth Engine account).</span></a>
  </nav>

  <nav class="iot-roadmap" aria-label="Roadmap of the seven modules">{roadmap}</nav>

  <div class="iot-principles">
    <div><strong>Lecture, then lab</strong><span>Each lecture prepares the lab of the following week. Watch it, then follow the lesson steps.</span></div>
    <div><strong>One milestone per module</strong><span>M1 accounts and first script · M2 index areas · M3 classification report · M4 flood map · M5 landslide heatmap · M6 burn severity · M7 capstone notebook.</span></div>
    <div><strong>Numbers, not pictures</strong><span>Every map comes with hectares, a threshold you can defend and a comparison with an independent reference.</span></div>
  </div>

  <div class="iot-note iot-note--info">
    <p class="iot-note-title">How you are graded</p>
    <p>Six homework reports (M2–M7) make <strong>60 %</strong> of the course grade (10 % each) and the <strong>final test</strong> (30 questions from the seven lessons, 40 min, two attempts, the better one counts) makes <strong>40 %</strong>. Every report is marked out of 100 against the report template in its assignment; the lesson quizzes are self-checks and do not count. You pass from <strong>60 %</strong>, in each piece and overall. The grade: <strong>5.0</strong> from 92 %, <strong>4.5</strong> from 84 %, <strong>4.0</strong> from 76 %, <strong>3.5</strong> from 68 %, <strong>3.0</strong> from 60 %, <strong>2.0</strong> below. Late homework stays open and is marked as late.</p>
    <p><strong>The grade of the whole course</strong> is not this number alone: the course has two parts, taught by two lecturers. The final grade is the weighted mean of the grade from this part and the grade from the other lecturer's part, each weighted by the number of teaching hours of that part. Both parts have to be passed.</p>
  </div>

  <div class="iot-note iot-note--info">
    <p class="iot-note-title">How to use this page</p>
    <p>Each module below has the same layout: <strong>Milestone</strong> (what you hand in and when), <strong>Your path</strong> (the order of lecture, lesson, lab and homework) and the materials. Deadlines: the milestone of module N is due at the start of lab N+1; the exact dates and times are on the assignment pages and in the course calendar. The capstone date is set in lecture 8. Questions go to the <a href="{mod('forum', 388)}">Announcements forum</a>.</p>
  </div>
</div>
'''

# ---------------------------------------------------------------- write
(OUT / 's0-summary.html').write_text(intro, encoding='utf-8', newline='\n')
for m in MODULES:
    (OUT / f's{m["n"]}-summary.html').write_text(module_html(m), encoding='utf-8', newline='\n')

(OUT / 's7-quiz-435.intro.html').write_text('<div class="iot-material iot-material--label" data-iot-material="v1"><p>The final test of the course: <strong>30 questions</strong> drawn at random from the seven lesson categories (4–5 per lesson: data and accounts, Earth Engine basics, classifiers, floods, landslides, wildfires, APIs), <strong>40 minutes</strong>, <strong>two attempts</strong> – the better one counts. It makes 40 % of the course grade; you pass from 60 %. The questions are the same kind as the self-check quizzes in the lessons, so revise the lesson pages and the lecture summaries. The test is opened by the lecturer at the end of the course.</p></div>\n', encoding='utf-8', newline='\n')
(OUT / 's0-forum-388.intro.html').write_text('<div class="iot-material iot-material--label" data-iot-material="v1"><p>Announcements, deadlines and questions about the labs. Enrolment key for this course: <code>GEO</code>.</p></div>\n', encoding='utf-8', newline='\n')

ops = [
    ('sectionname', 0, 'Start here'),
    ('sectionname', 1, '01 · Kick-off: natural hazards, Earth observation and your accounts'),
    ('sectionname', 2, '02 · Google Earth Engine: the Code Editor'),
    ('sectionname', 3, '03 · Machine learning classifiers'),
    ('sectionname', 4, '04 · Flood mapping'),
    ('sectionname', 5, '05 · Landslide mapping'),
    ('sectionname', 6, '06 · Wildfire mapping'),
    ('sectionname', 7, '07 · Python and R APIs for GEE · wrap-up'),
    # lecture first, then lesson/materials, homework last
    ('sequence', 1, '423,390,422'),  # 422 hidden, kept in the sequence until deleted
    ('sequence', 2, '424,391,394,395,392,393'),
    ('sequence', 3, '425,396,397,398'),
    ('sequence', 4, '426,401,399,400,431'),
    ('sequence', 5, '427,402,432'),
    ('sequence', 6, '428,403,433'),
    ('sequence', 7, '429,404,430,434,435'),  # 435 = Final test (quiz, hidden until the test day)
    ('hide', 422),  # intro presentation retired 22.10.2026 (duplicated lecture 1); delete the module in the UI
    ('rename', 390, 'Homework after lecture 1: accounts and webinars'),
    ('rename', 391, 'Lesson 2: Google Earth Engine step by step'),
    ('rename', 392, 'Homework M2: index areas (script link)'),
    ('rename', 394, 'Tip: administrative borders as a FeatureCollection'),
    ('rename', 395, 'Other data sources (SAR, DEM, rainfall, soil moisture, land cover, landslides)'),
    ('rename', 396, 'Lesson 3: Classifiers'),
    ('rename', 397, 'Short deck: Random Forest and k-means'),
    ('rename', 398, 'Homework M3: classification report'),
    ('rename', 431, 'Homework M4: flood extent map + sensitivity table'),
    ('rename', 432, 'Homework M5: landslide heatmap note'),
    ('rename', 433, 'Homework M6: burn severity map + report'),
    ('rename', 434, 'Homework M7: capstone notebook or QGIS project'),
    # lectures: no dates in module names – the schedule lives in schedule.json and in the Moodle calendar
    ('rename', 423, 'Lecture 1 – Natural hazards and Earth observation: course kick-off'),
    ('rename', 424, 'Lecture 2 – Google Earth Engine: the Code Editor'),
    ('rename', 425, 'Lecture 3 – Machine learning for land cover classification'),
    ('rename', 426, 'Lecture 4 – Flood mapping: optical indices and SAR'),
    ('rename', 427, 'Lecture 5 – Landslide mapping with satellite data'),
    ('rename', 428, 'Lecture 6 – Wildfire detection and burn severity'),
    ('rename', 429, 'Lecture 7 – GEE beyond the Code Editor: Python, Colab, geemap, rgee'),
    ('rename', 430, 'Lecture 8 – From pixels to hazard maps: wrap-up'),
    ('rename', 401, 'Lesson 4: flood mapping – bands, water indices, SAR'),
    ('rename', 402, 'Lesson 5: landslides and the SAR heatmap script'),
    ('rename', 403, 'Lesson 6: fire detection and burn severity'),
    ('rename', 404, 'Lesson 7: APIs for GEE – Python, Colab, QGIS'),
    ('pagetitle', 127, 'QGIS 1 – Install the Google Earth Engine plugin and sign in'),
    ('pagetitle', 128, 'QGIS 4 – From Earth Engine to a finished map (traps; rgee for volunteers)'),
    ('pagetitle', 101, '6. NDVI classes and area'),
    # new lesson pages (created once; skipped when the title exists). Order: B after 127 first, then A after 127 -> 127, A, B, 128
    ('addpage', 404, 127, 'QGIS 3 – No-code tools: Add Image Collection, Data Catalog, Export GeoTIFF', 'newpages/s7-qgis3.html'),
    ('addpage', 404, 127, 'QGIS 2 – Your first Earth Engine layer from the Python Console', 'newpages/s7-qgis2.html'),
    ('addpage', 391, 100, '5. Clouds first: SCL, Cloud Score+ and the QA60 bitmask', 'newpages/s2-clouds.html'),
    ('addpage', 404, 125, 'For the curious: what CDSE JupyterLab and openEO give you beyond Earth Engine (optional)', 'newpages/s7-cdse.html'),
]

# Quizzes in lessons 2 (cm 391) and 7 (cm 404) – Marek, 22.10.2026: answer labels stay plain (no hint on the question page);
# the FEEDBACK shown after answering is coloured: green = correct, red = incorrect. Texts cleaned
# (direct URLs instead of Google redirects, stray "??" emoji and editor junk removed).
QUIZ_ANSWERS = [  # (answer id, label, correct, feedback text)
    (322, 'Level-1C', False, 'Surface reflectance is generated during Level-2A processing. Level-1C is top-of-atmosphere reflectance.'),
    (323, 'Level-2A', True, 'Surface reflectance is generated during Level-2A processing.'),
    (324, 'Level-1B', False, 'Surface reflectance is generated during Level-2A processing. Level-1B is radiometrically corrected radiance, not distributed to users.'),
    (325, 'Level-0', False, 'Surface reflectance is generated during Level-2A processing. Level-0 is raw instrument data.'),
    (326, 'NIR and RED', True, 'NDVI = (NIR − RED) / (NIR + RED); in Sentinel-2 these are bands B8 and B4.'),
    (327, 'NIR and GREEN', False, 'NDVI uses NIR and RED (Sentinel-2 B8 and B4). Learn more: <a href="https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index">NDVI on Wikipedia</a>.'),
    (328, 'NIR and SWIR', False, 'NDVI uses NIR and RED (Sentinel-2 B8 and B4). Learn more: <a href="https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index">NDVI on Wikipedia</a>.'),
    (329, 'BLUE and SWIR', False, 'NDVI uses NIR and RED (Sentinel-2 B8 and B4). Learn more: <a href="https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index">NDVI on Wikipedia</a>.'),
    (330, 'Google Earth', True, 'Google Earth shows high-resolution imagery for exploration; Earth Engine is the analysis platform.'),
    (331, 'Google Earth Engine', False, 'Google Earth Engine is primarily an analytics platform for low and medium resolution public-domain remote sensing datasets.'),
    (332, 'Earth Engine Explorer', False, 'Earth Engine Explorer is a lightweight web app for browsing the Earth Engine catalogue (medium-resolution data), not for exploring high-resolution imagery. Timelapse, once a separate site, is today a feature inside Google Earth (Landsat and Sentinel-2 mosaics 1984–2022).'),
    (333, 'Public Data Catalog', False, 'All of them – the platform is the data catalogue, the co-located storage and computation, the APIs and the Code Editor together. Learn more at <a href="https://earthengine.google.com/platform/">earthengine.google.com/platform</a>.'),
    (334, 'Co-located Data Storage and Computation', False, 'All of them – the platform is the data catalogue, the co-located storage and computation, the APIs and the Code Editor together. Learn more at <a href="https://earthengine.google.com/platform/">earthengine.google.com/platform</a>.'),
    (335, 'Javascript and Python API', False, 'All of them – the platform is the data catalogue, the co-located storage and computation, the APIs and the Code Editor together. Learn more at <a href="https://earthengine.google.com/platform/">earthengine.google.com/platform</a>.'),
    (336, 'Browser-based Code Editor', False, 'All of them – the platform is the data catalogue, the co-located storage and computation, the APIs and the Code Editor together. Learn more at <a href="https://earthengine.google.com/platform/">earthengine.google.com/platform</a>.'),
    (337, 'All of them', True, 'All four systems make up the platform. Learn more at <a href="https://earthengine.google.com/platform/">earthengine.google.com/platform</a>.'),
    (338, 'Data is downloaded, pre-processed and co-located with computational resources', True, 'Removing the need for downloading and pre-processing data, together with the parallel computing architecture, makes Google Earth Engine a very scalable system for data processing.'),
    (339, 'It supports only low-resolution datasets', False, 'While most datasets in the public data catalogue are low and medium resolution imagery, Google Earth Engine is equally capable of processing high-resolution imagery.'),
    (340, 'The API takes advantage of parallel processing', True, 'The computation is distributed over many machines in parallel.'),
    (341, "Google Earth Engine is integrated with Google's AI Platform", False, "Earth Engine can call models hosted on Vertex AI (formerly AI Platform), but that integration is not the reason for its data processing speed."),
    (342, 'Earth Engine Developer Guide', True, 'All of them. See all the support channels at <a href="https://developers.google.com/earth-engine/help">developers.google.com/earth-engine/help</a>.'),
    (343, 'GIS Stack Exchange', True, 'All of them. See all the support channels at <a href="https://developers.google.com/earth-engine/help">developers.google.com/earth-engine/help</a>.'),
    (344, 'Earth Engine Developer Forum', True, 'All of them. See all the support channels at <a href="https://developers.google.com/earth-engine/help">developers.google.com/earth-engine/help</a>.'),
]
def feedback_html(text, correct):
    bg, border, fg, head = ('#d4edda', '#28a745', '#155724', '&#10004; Correct') if correct else ('#f8d7da', '#dc3545', '#721c24', '&#10008; Not correct')
    return (f'<div style="background:{bg};border-left:6px solid {border};color:{fg};padding:10px 16px;border-radius:6px;margin:4px 0">'
            f'<p style="margin:0 0 4px;font-weight:700">{head}</p><p style="margin:0">{text}</p></div>')
# Lesson 7 (cm 404), API quiz page 124 – all four answers are correct
QUIZ_ANSWERS += [
    (403, 'Python', True, 'Google provides the official Earth Engine API for JavaScript and Python.'),
    (404, 'R', True, 'R support comes from the community: <a href="https://github.com/r-spatial/rgee">rgee</a> wraps the Python API.'),
    (405, 'Javascript', True, 'Google provides the official Earth Engine API for JavaScript and Python (the Code Editor uses JavaScript).'),
    (406, 'Julia', True, 'Julia support came from the community: <a href="https://docs.juliahub.com/EarthEngine/">EarthEngine.jl</a> wraps the Python API, but it has not been updated since 2023 – for new work use Python or R.'),
]
# Multi-answer pages: Moodle shows the feedback of EVERY ticked option, and the question counts as correct only when
# exactly the correct set is ticked – so the green feedback must say how many answers are expected.
ANSWER_PAGE = {**{a: 95 for a in (322, 323, 324, 325)}, **{a: 96 for a in (326, 327, 328, 329)}, **{a: 97 for a in (330, 331, 332)},
               **{a: 98 for a in (333, 334, 335, 336, 337)}, **{a: 102 for a in (338, 339, 340, 341)}, **{a: 103 for a in (342, 343, 344)},
               **{a: 124 for a in (403, 404, 405, 406)}}
MULTI_NOTE = {
    95: 'Only this answer is correct – if you also ticked another option, the question counts as incorrect.',
    97: 'Only this answer is correct – if you also ticked another option, the question counts as incorrect.',
    102: 'Two answers are correct (co-located data and parallel processing); the question counts as correct only with exactly these two ticked.',
    103: 'All three answers are correct; the question counts as correct only with all three ticked.',
    124: 'All four answers are correct; the question counts as correct only with all four ticked.',
}
def feedback_for(aid, ok, fb):
    note = MULTI_NOTE.get(ANSWER_PAGE[aid])
    return feedback_html(fb + (f' <em>{note}</em>' if ok and note else ''), ok)
ops += [('answertext', aid, label) for aid, label, ok, fb in QUIZ_ANSWERS]
ops += [('answerresponse', aid, feedback_for(aid, ok, fb)) for aid, label, ok, fb in QUIZ_ANSWERS]
(OUT / 'ops.tsv').write_text(''.join('\t'.join(map(str, o)) + '\n' for o in ops), encoding='utf-8', newline='\n')
print('written: s0..s7 summaries, lecture intros, forum intro, ops.tsv')
