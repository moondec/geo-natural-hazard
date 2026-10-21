# Kurs „Application of geoinformatics to natural hazards mapping and monitoring” (AGeoHazard)

Celem projektu jest ulepszenie kursu Moodle (id 313 na https://elearning2.up.poznan.pl, Moodle 4.5.4+)
na testowym Moodle, a potem przeniesienie go na serwer uczelni jako kopia `.mbz`.
Rozmawiaj z użytkownikiem po polsku; treść kursu jest po angielsku.

## Źródło

- Kopia kursu (pełna, z użytkownikami, 344 MB): `~/Documents/moodle/backup-moodle2-course-313-ageohazard-20261021-1400.mbz`.
- Sekcje: Ogłoszenia (forum); lecture: Use GEE, EO Browser and JUPYTER; GEE - javascript editor;
  machine learning classifiers; Flood / Landslides / Wildfire mapping approaches; API for GEE.
  Moduły: 6 lesson, 4 resource, 2 assign, 3 label, 1 page, 1 forum.
- `.scratch_mbz_meta/moodle_backup.xml` — wyciągnięty manifest kopii (do podglądu, nie edytować .mbz ręcznie).

## Testowy Moodle (WSL Ubuntu-20.04 + Docker)

- http://localhost:8088, Moodle 4.5.4+ (Build 20250516), katalog `/home/marek/.hermes/moodle-lab`
  (docker-compose, `.env`, `scripts/restore-course.sh`). Kontenery `moodle-lab-web-1` (PHP 8.3),
  `moodle-lab-db-1` (mariadb 10.11), `moodle-lab-mailpit-1` (http://localhost:8025).
- `/home/marek/.hermes/inbox` jest w kontenerze jako `/backups` (read-only). Kopię kursu tam skopiowano.
- **Kurs roboczy: id=15, shortname AGeoHazard** (przywrócony 21.10.2026 z CLI, z użytkownikami: 8 studentów, 1 editingteacher, 1 teacher, 1 manager; 17 modułów, 6 lekcji / 36 stron, 399 MB plików). http://localhost:8088/course/view.php?id=15
- Limity PHP: upload 200M / post 206M — kopia 344 MB **nie wejdzie przez UI**, przywracaj z CLI:
  `docker exec moodle-lab-web-1 php admin/cli/restore_backup.php --file=/backups/<plik>.mbz --categoryid=1`.
- Kopia do wysłania: `docker exec moodle-lab-web-1 php admin/cli/backup.php --courseid=N --destination=/backups`
  (jeśli read-only, użyj katalogu w kontenerze i `docker cp`). Na produkcję przywraca użytkownik sam przez UI.
- Hasło admina zna tylko użytkownik; w przeglądarce loguje się sam. Web services są wyłączone.
  Zmian konfiguracji Moodle (motyw, ustawienia serwisu) nie rób bez zgody użytkownika. Usuwanie kursów — użytkownik.

## Sposób pracy (przejęty z projektu IoT, `~/Documents/iot_lectures`)

- Edycja treści skryptami PHP: `docker exec -i moodle-lab-web-1 php < skrypt.php`
  (`define('CLI_SCRIPT', true); require '/var/www/html/config.php';` potem API Moodle / `$DB`). Po zmianach purge caches.
- Narzędzia z sesji IoT w `/home/marek/.hermes/build`: `mpull.sh` (eksport stron/etykiet/opisów sekcji do `mcontent/`,
  repo git — każda zmiana ma diff), `mpush.sh` (dry run) / `mpush.sh --apply`, `check-mcontent.py`, `gsweep.php`,
  `tablerender.sh`. Sprawdź, czy są sparametryzowane id kursu, zanim użyjesz.
- Treści HTML generuj skryptami Pythona, style inline (motywu nie zmieniamy).
- Z Git Bash działa `timeout N wsl.exe -e bash -c '...'`; `wsl.exe bash -lc` gubi zmienne i ścieżki.
  Python na Windows: `PYTHONUTF8=1`, pliki z LF.
- Sprawdzone narzędzia: Bash + docker exec + PHP CLI, Playwright, claude-in-chrome (tylko gdy trzeba w przeglądarce
  użytkownika). MCP serena i github nie łączą się — do GitHuba `gh`. Zbędne tu: chrome-devtools, obsidian,
  huggingface, microsoft-docs, graphify.
