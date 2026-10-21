"""Build docs/ (GitHub Pages) from the Advanced Slides exports in presentation/export/*.zip.

Layout:  docs/lib/{css,dist,plugin}  shared reveal.js runtime (taken from the first export, verified identical)
         docs/assets/Kursy/...        union of the images of all decks
         docs/<slug>/index.html       each deck, asset paths rewritten to ../lib and ../assets
         docs/index.html              landing page with the list of lectures
Run:  python -I -X utf8 build_docs.py
"""
import hashlib, html, io, pathlib, re, shutil, zipfile

ROOT = pathlib.Path(__file__).parent
EXPORT = ROOT / 'presentation' / 'export'
DOCS = ROOT / 'docs'
DECKS = [  # zip stem, slug, title, date
    ('ApplicationHazards_GEO_2026', 'intro', 'Course overview: tools, methods, literature', 'intro presentation'),
    ('ApplicationHazards_GEO_2026_extended_01_Kickoff', '01-kickoff', 'Lecture 1 · Natural hazards and Earth observation: course kick-off', '9.11.2026'),
    ('ApplicationHazards_GEO_2026_extended_02_GEE_CodeEditor', '02-gee-code-editor', 'Lecture 2 · Google Earth Engine: the Code Editor', '16.11.2026'),
    ('ApplicationHazards_GEO_2026_extended_03_ML_Classification', '03-ml-classification', 'Lecture 3 · Machine learning for land cover classification', '23.11.2026'),
    ('ApplicationHazards_GEO_2026_extended_04_Floods', '04-floods', 'Lecture 4 · Flood mapping: optical indices and SAR', '30.11.2026'),
    ('ApplicationHazards_GEO_2026_extended_05_Landslides', '05-landslides', 'Lecture 5 · Landslide mapping with satellite data', '7.12.2026'),
    ('ApplicationHazards_GEO_2026_extended_06_Wildfires', '06-wildfires', 'Lecture 6 · Wildfire detection and burn severity', '14.12.2026'),
    ('ApplicationHazards_GEO_2026_extended_07_APIs', '07-apis', 'Lecture 7 · GEE beyond the Code Editor: Python, Colab, geemap, rgee', '21.12.2026'),
    ('ApplicationHazards_GEO_2026_extended_08_Wrapup', '08-wrapup', 'Lecture 8 · From pixels to hazard maps: wrap-up', '11.01.2027'),
]
LIB_DIRS = ('css/', 'dist/', 'plugin/')
# links that changed after the decks were exported (applied to every deck)
LINK_FIXES = {'https://emergency.copernicus.eu/': 'https://mapping.emergency.copernicus.eu/'}
# strings that must not be published (course enrolment key)
STRIP = [re.compile(r'<blockquote class="notification">\s*<p>pass to moodle: <code>geo</code></p>\s*</blockquote>', re.I),
         re.compile(r'> \[!notification\] pass to moodle: `geo`\s*', re.I)]

if DOCS.exists():
    shutil.rmtree(DOCS)
(DOCS / 'lib').mkdir(parents=True)
(DOCS / 'assets').mkdir()
lib_hashes = {}
asset_hashes = {}
for stem, slug, title, date in DECKS:
    z = zipfile.ZipFile(EXPORT / f'{stem}.zip')
    names = z.namelist()
    index = z.read('index.html').decode('utf-8')
    # drop the whole Obsidian callout that carries the course enrolment key
    index, n = re.subn(r'<div class="callout callout-color-default">(?:(?!<div class="callout callout-color-default">).)*?pass to moodle.*?</div>\s*</div>\s*<div class="callout-content">.*?</div>\s*</div>', '', index, flags=re.S | re.I)
    if n:
        print(f'  {slug}: stripped enrolment key callout ({n})')
    assert 'pass to moodle' not in index.lower(), slug
    for a, b in LINK_FIXES.items():
        index = index.replace(a, b)
    # rewrite asset references
    for d in LIB_DIRS:
        index = re.sub(r'(["\'(])' + re.escape(d), r'\1../lib/' + d, index)
    index = index.replace('Kursy/prezentacje/', '../assets/Kursy/prezentacje/').replace('../assets/../assets/', '../assets/')
    index = index.replace('Excalidraw/', '../assets/Excalidraw/')
    leftover = re.findall(r'(?:src|href)="(?!\.\./|https?:|#|data:)[^"]+"', index)
    if leftover:
        print(f'  {slug}: unhandled relative refs: {leftover[:5]}')
    out = DOCS / slug
    out.mkdir()
    (out / 'index.html').write_text(index, encoding='utf-8', newline='\n')
    for n in names:
        if n.endswith('/') or n == 'index.html':
            continue
        data = z.read(n)
        h = hashlib.sha1(data).hexdigest()
        if n.startswith(LIB_DIRS):
            if n in lib_hashes:
                if lib_hashes[n] != h:
                    print(f'  WARNING lib file differs between decks: {n} ({slug})')
                continue
            lib_hashes[n] = h
            dest = DOCS / 'lib' / n
        elif n.startswith(('Kursy/', 'Excalidraw/')):
            if n in asset_hashes:
                if asset_hashes[n] != h:
                    print(f'  WARNING asset differs between decks: {n} ({slug})')
                continue
            asset_hashes[n] = h
            dest = DOCS / 'assets' / n
        else:
            print(f'  {slug}: unexpected file {n}')
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    print(f'{slug}: ok ({len(names)} entries)')

# landing page
items = ''.join(f'<li><a href="{slug}/"><strong>{html.escape(title)}</strong><span>{html.escape(date)}</span></a></li>' for _, slug, title, date in DECKS)
landing = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Geoinformatics for Natural Hazards – lectures</title>
<style>
:root{{--bg:#f4f7fb;--fg:#15202b;--accent:#0b4f8a;--muted:#5a6a7a;--card:#fff;--line:#c9d6e3}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#10213a;--fg:#e6eef8;--accent:#9ec5ef;--muted:#b5c6d8;--card:#182c48;--line:#2c4466}}}}
:root[data-theme="dark"]{{--bg:#10213a;--fg:#e6eef8;--accent:#9ec5ef;--muted:#b5c6d8;--card:#182c48;--line:#2c4466}}
body{{margin:0;padding:32px 16px;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
main{{max-width:860px;margin:0 auto}}h1{{font-size:clamp(1.6rem,4vw,2.4rem);letter-spacing:-.03em;margin:0 0 6px}}
p.lead{{color:var(--muted);margin:0 0 24px}}ul{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}
li a{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:14px 18px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--fg);text-decoration:none}}
li a:hover{{border-color:var(--accent)}}li a strong{{color:var(--accent)}}li a span{{color:var(--muted);font-size:.9rem;white-space:nowrap}}
footer{{margin-top:28px;color:var(--muted);font-size:.85rem}}
</style>
</head>
<body>
<main>
<h1>Application of geoinformatics to natural hazards mapping and monitoring</h1>
<p class="lead">Lecture slides (reveal.js) · Geoinformation and Spatial Management, 2nd year, winter 2026/27 · Poznań University of Life Sciences · Marek Urbaniak. In a deck: arrows move between slides, <kbd>F</kbd> full screen, <kbd>?</kbd> help, <kbd>Esc</kbd> overview.</p>
<ul>{items}</ul>
<footer>Course materials in Moodle (UPP e-learning); sources and build scripts on <a href="https://github.com/moondec/geo-natural-hazard">GitHub</a>. Licence CC BY 4.0 unless stated otherwise on a slide.</footer>
</main>
</body>
</html>
'''
(DOCS / 'index.html').write_text(landing, encoding='utf-8', newline='\n')
(DOCS / '.nojekyll').write_text('', encoding='utf-8')
def du(p):
    return sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
print(f'lib {du(DOCS / "lib") / 1e6:.1f} MB, assets {du(DOCS / "assets") / 1e6:.1f} MB, total {du(DOCS) / 1e6:.1f} MB')
