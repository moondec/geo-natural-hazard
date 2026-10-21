# Plan cyklu wykładów AGeoHazard – semestr zimowy 2026/27 (część Marka: 14 h wykładu, 22 h ćwiczeń)

Źródło godzin: `Zestawienie_zajęć_zima_2026-27_Marek_Urbaniak.xlsx` (stan 9.10.2026), arkusz „Terminy”.
Sala 15, poniedziałki. Pierwsze 6 h wykładu i 18 h ćwiczeń prowadzi koleżanka (założenie: podstawy GIS/QGIS – do potwierdzenia).

## Zasada

Każdy wykład jest **logicznym wstępem do najbliższych ćwiczeń**: kończy się slajdem „In the lab” (co dokładnie zrobimy, krok po kroku) i „Before next class” (co student ma przygotować, żeby nie szukać sam). Student dostaje gotową mapę drogową zamiast linku do kursu End-to-End.

Uwaga do kolejności w dniu: według planu ćwiczenia są 8:30–10:45, a wykład 10:45–12:15, czyli wykład z poniedziałku N wprowadza ćwiczenia z poniedziałku N+1. Układ poniżej jest do tego dopasowany (wykład W1 9.11 bez ćwiczeń, ćwiczenia C7 11.01 przed wykładem zamykającym). Jeśli zamienisz kolejność w dniu (wykład 8:30, ćwiczenia po), plan nadal działa: wtedy W_k → C_k tego samego dnia, a W8 staje się podsumowaniem po ostatnich ćwiczeniach.

## Harmonogram

| Data | Wykład (h) | Tytuł prezentacji | Ćwiczenia, które wprowadza | Sekcja Moodle |
|---|---|---|---|---|
| 9.11.2026 | W1 (1 h, 11:30–12:15) | **L01 Natural hazards and Earth observation: course kick-off** | C1 16.11 (3 h): Copernicus Browser, konto CDSE, rejestracja GEE, pierwszy skrypt | 1 (Presentation, Homework) |
| 16.11.2026 | W2 (2 h) | **L02 Google Earth Engine: the Code Editor** | C2 23.11 (3 h): kolekcje, filtry, NDVI, klasy progowe, pola powierzchni; zadanie „index areas” | 2 (GEE – javascript editor) |
| 23.11.2026 | W3 (2 h) | **L03 Machine learning for land cover classification** | C3 30.11 (3 h): Random Forest + k-means, raport | 3 (ML classifiers) |
| 30.11.2026 | W4 (2 h) | **L04 Flood mapping: optical indices and SAR** | C4 7.12 (3 h): NDWI/MNDWI, Sentinel-1 backscatter, skrypt UN-SPIDER | 4 (Flood mapping) |
| 7.12.2026 | W5 (2 h) | **L05 Landslide mapping with satellite data** | C5 14.12 (3 h): skrypt SAR landslide density (Handwerger et al. 2022) | 5 (Landslides) |
| 14.12.2026 | W6 (2 h) | **L06 Wildfire detection and burn severity** | C6 21.12 (3 h): NBR/dNBR, klasyfikacja USGS, mapa dotkliwości | 6 (Wildfire) |
| 21.12.2026 | W7 (2 h) | **L07 GEE beyond the Code Editor: Python, Colab, geemap, rgee** | C7 11.01 (4 h): Colab + geemap, bitmaski QA, rgee | 7 (API for GEE) |
| 11.01.2027 | W8 (1 h, 11:30–12:15) | **L08 From pixels to hazard maps: wrap-up, uncertainty, operational services** | – (po C7) | 4 (Error estimation), podsumowanie, zaliczenie |

Razem: 1 + 6×2 + 1 = **14 h** wykładu; ćwiczenia 6×3 + 4 = **22 h**. Zgodne z xlsx.

## Co jest nowe względem jednej prezentacji „Part 2” (25 slajdów)

- Stare slajdy zostały rozdzielone: hazardy UN, metodologia before/after, pasywne/aktywne, rozdzielczości, pasma Landsat/Sentinel, Copernicus Browser → **L01**; GEE → **L02**; ML, drzewa, RF, regresja → **L03**; literatura/webinary → rozdzielone po wykładach jako „Before next class”.
- Każdy wykład dostał brakujący wstęp teoretyczny do ćwiczeń (np. jak działa SAR i dlaczego woda jest ciemna, skąd progi dNBR, czym jest confusion matrix, dlaczego `getInfo()` jest wolne, co to są bity QA60).
- Nowe elementy wymagające obrazów są oznaczone `<!-- TODO image: ... -->` z podanym źródłem (CC/public domain), żeby dodać je w Obsidianie (wklejenie do `pliki/`). Bez nich slajdy działają jako tekst/diagram Mermaid.
- Istniejące obrazy z vaulta są użyte przez pełne ścieżki `Kursy/prezentacje/ApplicationHazards_GEO/pliki/...`, więc nowe pliki mogą leżeć w dowolnym podfolderze.

## Pliki

`L01_Kickoff.md` … `L08_Wrapup.md` w tym folderze. Sugerowana lokalizacja w vaulcie: `Kursy/prezentacje/ApplicationHazards_GEO/2026/`. Eksport Advanced Slides każdego pliku osobno → zip → osobny zasób „Lecture N” w odpowiedniej sekcji Moodle (podmiana przez skrypt PHP po Twojej stronie / mojej).

## Do decyzji Marka

1. Czy koleżanka w pierwszych 6 h omawia podstawy teledetekcji (pasywne/aktywne, pasma)? Jeśli tak, w L01 można te 3 slajdy skrócić do 1.
2. Czy w C1 (16.11) studenci rejestrują projekt Google Cloud na zajęciach, czy wcześniej (L01 nakazuje „before the class”; rejestracja bywa opóźniona o 1–2 dni, więc lepiej wcześniej).
3. Egzamin/zaliczenie: L08 ma slajd „Assessment” z placeholderem – wpisać zasady.
