<?php
// Replace the lecture URL modules of course 15 with Page modules that embed the deck (first slide visible)
// and offer a button opening it in a new window – the IoT-course pattern. Usage: php to_pages.php [--apply]
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/mod/page/lib.php');
require_once($CFG->dirroot . '/lib/resourcelib.php');
$courseid = 15;
$apply = in_array('--apply', $argv ?? []);
$course = get_course($courseid);
\core\session\manager::set_user(get_admin());

function deck_block(string $url, string $title): string {
    $u = s($url); $t = s($title);
    return <<<HTML
<div class="iot-deck" data-iot-deck="v1">
<p style="margin:0 0 .6rem"><strong>The lecture slides</strong> are shown below – the same reveal.js deck the lecturer uses in class, published on GitHub Pages with animations, diagrams and navigation.</p>
<p style="font-size:.9em;color:#46586b;margin:.25rem 0 1.1rem">Navigation: click inside the frame, then <kbd>←</kbd> <kbd>→</kbd> or <kbd>space</kbd>; <kbd>Esc</kbd> – slide overview, <kbd>F</kbd> – full screen, <kbd>?</kbd> – help. On a small screen open the deck in a separate window.</p>
<figure class="iot-deck__item" style="margin:0 0 1.5rem">
  <figcaption style="font-weight:600;margin:0 0 .35rem">{$t}</figcaption>
  <div style="position:relative;width:100%;aspect-ratio:16/10;min-height:340px;max-height:78vh;margin:0 0 .5rem;border:1px solid #c9d6e3;border-radius:6px;overflow:hidden;background:#111;box-shadow:0 1px 4px rgba(0,0,0,.18)">
    <iframe src="{$u}" title="{$t} – reveal.js presentation" loading="lazy" allowfullscreen allow="fullscreen"
            referrerpolicy="no-referrer-when-downgrade"
            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;display:block"></iframe>
  </div>
  <p style="margin:0 0 .2rem"><a href="{$u}" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:.45rem .9rem;border:1px solid #0b4f8a;border-radius:6px;text-decoration:none;font-weight:600;color:#fff;background:#0b4f8a">Open the presentation in a new window</a></p>
</figure>
</div>
HTML;
}

$urlmod = $DB->get_field('modules', 'id', ['name' => 'url']);
$urls = $DB->get_records_sql("SELECT cm.id AS cmid, u.name, u.externalurl, cm.section AS sectionid FROM {url} u JOIN {course_modules} cm ON cm.instance = u.id AND cm.module = ? WHERE u.course = ? AND cm.deletioninprogress = 0 AND u.externalurl LIKE 'https://moondec.github.io/geo-natural-hazard/%' ORDER BY cm.id", [$urlmod, $courseid]);
foreach ($urls as $u) {
    $sectionnum = $DB->get_field('course_sections', 'section', ['id' => $u->sectionid]);
    $exists = $DB->get_record_sql("SELECT cm.id FROM {page} p JOIN {course_modules} cm ON cm.instance = p.id AND cm.module = (SELECT id FROM {modules} WHERE name='page') WHERE p.course = ? AND p.name = ? AND cm.deletioninprogress = 0", [$courseid, $u->name]);
    echo "section $sectionnum: url cm {$u->cmid} '{$u->name}' -> page" . ($exists ? " [exists cm {$exists->id}]" : '') . "\n";
    if (!$apply) continue;
    if ($exists) { echo "map {$u->cmid} {$exists->id}\n"; continue; }
    $mi = new stdClass();
    $mi->modulename = 'page'; $mi->module = $DB->get_field('modules', 'id', ['name' => 'page']);
    $mi->course = $courseid; $mi->section = $sectionnum; $mi->visible = 1; $mi->visibleoncoursepage = 1;
    $mi->name = $u->name;
    $mi->intro = ''; $mi->introformat = FORMAT_HTML;
    $mi->page = ['text' => deck_block($u->externalurl, $u->name), 'format' => FORMAT_HTML, 'itemid' => 0];
    $mi->display = RESOURCELIB_DISPLAY_OPEN; $mi->printintro = 0; $mi->printlastmodified = 0;
    $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0; $mi->completion = 0;
    $mi = add_moduleinfo($mi, $course);
    $section = $DB->get_record('course_sections', ['id' => $u->sectionid]);
    $seq = array_values(array_filter(explode(',', $section->sequence)));
    $seq = array_values(array_diff($seq, [(string)$mi->coursemodule]));
    $pos = array_search((string)$u->cmid, $seq);
    array_splice($seq, $pos === false ? count($seq) : $pos, 0, [(string)$mi->coursemodule]);
    $DB->set_field('course_sections', 'sequence', implode(',', $seq), ['id' => $section->id]);
    course_delete_module($u->cmid);
    echo "map {$u->cmid} {$mi->coursemodule}\n";
}
if ($apply) { rebuild_course_cache($courseid, true); purge_all_caches(); echo "done\n"; } else echo "DRY RUN\n";
