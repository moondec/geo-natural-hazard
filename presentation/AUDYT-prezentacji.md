# Audyt prezentacji wstępnej „Application of geoinformatics to natural hazards…” (21.10.2026)

Źródło: moduł „Presentation” (cm 389, sekcja 1) kursu id=15 na localhost:8088. Plik `ApplicationHazards_GEO.zip` (71,6 MB) +
rozpakowane `index.html` — eksport z Obsidian Advanced Slides (reveal.js, motyw beige, 25 slajdów, fragmenty animowane).
Kopia robocza: `presentation/src/ApplicationHazards_GEO/`, zrzuty: `presentation/shots/slideNN.jpg`,
wyciągnięty markdown: `presentation/slides_extracted.md`.

## A. Nieaktualne merytorycznie (do poprawy)

| Slajd | Problem | Stan faktyczny (zweryfikowany 21.10.2026) | Propozycja |
|---|---|---|---|
| 14 „SentinelHUB” | „Developed and maintained by Sinergise Laboratory”, logo i link **EO Browser**, „(Sentinel, Landsat, MODIS…)” | Sinergise przejęte przez Planet (2023). **EO Browser wyłączony 20.03.2026** (ogłoszenie Planet 5.02.2026); apps.sentinel-hub.com/eo-browser pokazuje tylko komunikat „deprecated”. Następcy: **Copernicus Browser** (ESA/CDSE, darmowy, wymaga konta) oraz **Planet Insights Platform** (komercyjny, 30 dni trial). Copernicus Browser ma S1, S2 (+mozaiki), S3, S5P, DEM 30/90 — **bez Landsat i MODIS** w przeglądarce. | Przebudować slajd na „Copernicus Browser (Copernicus Data Space Ecosystem)”: kto utrzymuje (ESA/EC, operator CDSE), kolekcje, funkcje (compare, timelapse, custom scripts, GeoTIFF, pins/Highlights, 3D, statystyki, import AOI), konto darmowe. Usunąć logo EO Browser i sentinelhub; wspomnieć Planet Insights jako wersję komercyjną. |
| 22 „Home work” | 1. link = „Sentinel Hub Webinar: EO Browser” | Narzędzie już nie istnieje | Zastąpić tutorialem Copernicus Browser (kanał CDSE/ESA) |
| 13 „Google Earth Engine” | „Available for scientist, researchers and developers” | GEE wymaga projektu Google Cloud i rejestracji niekomercyjnej; od **27.04.2026** tiery: Community (domyślny), Contributor (1000 EECU-h, wymaga konta billingowego, bez opłat), Partner. Kurs End-to-End (Spatial Thoughts) nadal darmowy do samodzielnej nauki. | Dodać punkt o rejestracji projektu Cloud (studenci muszą to zrobić przed zajęciami) + link do „noncommercial tiers”. Dodać Python: `ee` + **geemap**. |
| 12 „Compare Landsat and Sentinel bands” | Tylko Landsat 8 | Landsat 9 (2021) ma identyczne pasma; **Landsat 7 wyłączony 4.06.2025**; Sentinel-2 to dziś tryplet 2A/2B/2C (2C operacyjny od 21.01.2025, 2A przedłużony do końca 2027). | Podpis „Landsat 8/9”, notka o 2C i o Landsat Next (26 pasm, start ~2030+). |
| 15 „RGEE” + 24 | Link do książki `r-earthengine.com/rgeebook` | Domena nie istnieje. rgee żyje: CRAN 1.1.8 (15.10.2025), nowy opiekun M. Stigler. | Link → https://r-spatial.github.io/rgee/ ; usunąć pozycję książki z slajdu 24 lub podać, że offline. |
| 3 | Podpis przypisu „For this purpose we can use Copernicus Browser” linkuje do dataspace.copernicus.eu | Działa, ale bezpośredni adres to https://browser.dataspace.copernicus.eu/ | Podmienić link; spójnie z slajdem 14. |
| stopka | „© 2025 Pracownia Meteorologii” | | 2026 |

## B. Martwe / błędne linki

| Slajd | Link | Status | Zamiana |
|---|---|---|---|
| 16 | developers.google.com/earth-engine/guides/earth-engine/guides/{classification,clustering,reducers_regression} | **404** (podwojona ścieżka) | …/earth-engine/guides/classification, …/clustering, …/reducers_regression (200) |
| 10 | satellites4everyone.co.uk (źródło ilustracji) | domena nie istnieje | Podać archiwalne źródło (web.archive.org) albo zastąpić ilustrację (np. ESA/NASA, CC) |
| 15, 24 | r-earthengine.com/rgeebook | domena nie istnieje | r-spatial.github.io/rgee |
| 14 | sinergise.com | 503 | usunąć |
| 24 | geocompr.robinlovelace.net | przekierowanie | https://r.geocompx.org/ (2. wyd.) |
| 24 | keen-swartz-3146c4.netlify.app | działa, ale adres tymczasowy | https://r-spatial.org/book/ (Pebesma & Bivand 2023, CRC) |
| 24 | r4ds.had.co.nz | 1. wydanie | https://r4ds.hadley.nz/ (2. wyd. 2023) |
| 23 | medium.com (wildfire boundary maps), researchgate | 403 dla botów — prawdopodobnie OK w przeglądarce | sprawdzić ręcznie |

Pozostałe 35 linków: 200 OK (UN-SPIDER, FU Berlin, custom-scripts.sentinel-hub.com, YouTube ×3 — tytuły zweryfikowane, bookdown ×3, soilmapper, NHESS, Belgeo, JFS).

## C. Drobne (język, układ)

- Sl. 3: „For other advices” → „For other advice”; „We will back later” → „We will come back to it later”; „Regarding to” (etykieta w Moodle) → „Regarding”.
- Sl. 10: „Idea of tele-detection” → „Idea of remote sensing”; emotka w tytule.
- Sl. 20: „the category to which the data points belongs” → „belong”.
- Sl. 24: „This book uses its template.” — pozostałość, do usunięcia.
- Sl. 16: trzy punkty (Supervised / Unsupervised / Regression) są fragmentami, które się nakładają — na zrzucie widać tylko „Regression”; sprawdzić, czy to zamierzone (fade-in-then-out) — na wydruku/PDF student zobaczy tylko ostatni.
- Sl. 1: widoczne hasło zapisu „pass to moodle: geo” — jeśli prezentacja jest publiczna, lepiej je usunąć (w kursie i tak jest).
- Dekoracyjne kwadraty (motyw) nachodzą na treść na sl. 6, 8, 9, 14 (zrzuty); kosmetyka.
- Obrazy slajdów 6–8 (Copernicus Browser v1.25, listopad 2025) są aktualne — zostawić.

## D. Propozycje rozszerzeń (opcjonalne)

1. **Slajd „Where to get data in 2026”** — tabela: Copernicus Browser (GUI, free), CDSE API (openEO / STAC / S3, free quota), Google Earth Engine (cloud, noncommercial tiers), Planet Insights (commercial). Spójne z sekcjami kursu (GEE JS editor, API for GEE).
2. **Slajd SAR / Sentinel-1** — dla powodzi i osuwisk (sekcje 4–5 kursu); konstelacja 1C/1D (1A kończy 29.06.2026), produkt GFM (Global Flood Monitoring, CEMS).
3. **Slajd „Operational services”** — CEMS Rapid Mapping, EFFIS (pożary), GloFAS/EFAS (powodzie), Copernicus Browser „Highlights” jako gotowe przykłady zdarzeń (zastępują „saved locations” z EO Browser).
4. Sl. 5: dodać progi dNBR wg USGS (Key & Benson) obok mapy — ułatwia zadanie domowe z burn severity.
5. Sl. 13/15: Python + geemap jako drugi, dziś najczęstszy sposób pracy z GEE; rgee zostawić jako opcję dla R.

## E. Jak wprowadzić zmiany

Źródłem jest markdown w `<script type="text/template">` w `index.html` (eksport Obsidian). Dwie drogi:
- **(zalecana)** edycja w vaultcie Obsidian (`Kursy/prezentacje/ApplicationHazards_GEO.md`) i ponowny eksport Advanced Slides → zip → podmiana pliku w module Moodle (resource, cm 389).
- edycja `index.html` bezpośrednio (markdown w szablonach) + nowe obrazy do `Kursy/prezentacje/ApplicationHazards_GEO/pliki/`, re-zip, podmiana w Moodle przez skrypt PHP (file API). Szybsza, ale rozjeżdża się z vaultem Obsidian.
