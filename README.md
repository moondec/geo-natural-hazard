# Application of geoinformatics to natural hazards mapping and monitoring

Course materials (lecture slides, Moodle lab content and build tooling) for the course taught at
Poznań University of Life Sciences (Geoinformation and Spatial Management, 2nd year, winter 2026/27).
Author: Marek Urbaniak. Licence: CC BY 4.0 unless stated otherwise on a slide.

**Lectures online:** https://moondec.github.io/geo-natural-hazard/

| Path | What |
|:--|:--|
| `docs/` | Published site (GitHub Pages): `index.html` landing page, one folder per deck, `lib/` shared reveal.js runtime, `assets/` images |
| `presentation/obsidian/cycle/L01…L08_*.md` | Lecture sources – Obsidian Advanced Slides markdown (the vault copy is the one being exported) |
| `presentation/obsidian/cycle/svg/` | Hand-generated SVG diagrams used on the slides (Mermaid is unusable in the plugin) |
| `presentation/obsidian/ApplicationHazards_GEO.md` | Intro presentation (course overview), updated 2026 |
| `presentation/obsidian/cycle/PLAN-cyklu-wykladow.md` | Lecture cycle plan vs. the timetable (Polish) |
| `build_docs.py` | Builds `docs/` from the Advanced Slides exports (`presentation/export/*.zip`, not in git) |
| `course/mcontent/` | Moodle course text fields (section summaries, lesson pages, labels, assignment intros) in the restyled version |
| `course/mcontent-orig/` | The same fields as pulled from the course before the rebuild |
| `course/build_summaries.py`, `course/geo.scss`, `course/inline-iot-css.py`, `course/RULES-geo.md` | Generator of the section summaries, the blue style sheet, CSS inliner and the editing rules |
| `CLAUDE.md` | Working notes for the AI assistant used to maintain the course |

## Workflow

1. Edit a lecture in Obsidian (`Kursy/prezentacje/ApplicationHazards_GEO/ApplicationHazards_GEO_2026_extended_0N_*.md`),
   export with Advanced Slides ("Export as html"), zip the export folder into `presentation/export/`.
2. `python -I -X utf8 build_docs.py` → commit `docs/` → push: GitHub Pages serves it.
3. Moodle: the lecture activities are URL links to the published decks; lab pages are pushed from `course/mcontent/`
   with the pull/push scripts (see `CLAUDE.md`).
