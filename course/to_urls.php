<?php
// Replace the reveal.js resource modules of course 15 with URL modules pointing to GitHub Pages.
// Usage: php to_urls.php [--apply]   Prints "map <oldcm> <newcm>" lines.
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/mod/url/lib.php');
require_once($CFG->dirroot . '/mod/url/locallib.php');
$courseid = 15;
$base = 'https://moondec.github.io/geo-natural-hazard/';
$apply = in_array('--apply', $argv ?? []);
$course = get_course($courseid);
\core\session\manager::set_user(get_admin());
$map = [
    389 => ['intro/', 'Intro presentation: the course on 25 slides'],
    405 => ['01-kickoff/', null], 406 => ['02-gee-code-editor/', null], 407 => ['03-ml-classification/', null],
    408 => ['04-floods/', null], 409 => ['05-landslides/', null], 410 => ['06-wildfires/', null],
    411 => ['07-apis/', null], 412 => ['08-wrapup/', null],
];
foreach ($map as $oldcm => [$path, $newname]) {
    $cm = get_coursemodule_from_id('resource', $oldcm, $courseid, false, MUST_EXIST);
    $res = $DB->get_record('resource', ['id' => $cm->instance], '*', MUST_EXIST);
    $name = $newname ?? $cm->name;
    $url = $base . $path;
    $exists = $DB->get_record_sql("SELECT cm.id FROM {url} u JOIN {course_modules} cm ON cm.instance = u.id AND cm.module = (SELECT id FROM {modules} WHERE name='url') WHERE u.course = ? AND u.externalurl = ? AND cm.deletioninprogress = 0", [$courseid, $url]);
    echo "section {$cm->sectionnum}: resource cm $oldcm '{$cm->name}' -> url '$name' $url" . ($exists ? " [exists cm {$exists->id}]" : '') . "\n";
    if (!$apply) continue;
    if ($exists) { echo "map $oldcm {$exists->id}\n"; continue; }
    $mi = new stdClass();
    $mi->modulename = 'url'; $mi->module = $DB->get_field('modules', 'id', ['name' => 'url']);
    $mi->course = $courseid; $mi->section = $cm->sectionnum; $mi->visible = 1; $mi->visibleoncoursepage = 1;
    $mi->name = $name;
    $mi->intro = '<div class="iot-material iot-material--label" data-iot-material="v1"><p>Slides online (reveal.js, opens in a new tab). Arrows move between slides, <code>F</code> full screen, <code>?</code> help, <code>Esc</code> overview.</p></div>';
    $mi->introformat = FORMAT_HTML;
    $mi->externalurl = $url;
    $mi->display = RESOURCELIB_DISPLAY_NEW; $mi->printintro = 1;
    $mi->parameters = []; $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0; $mi->completion = 0;
    $mi = add_moduleinfo($mi, $course);
    // place the url module where the resource was, then delete the resource
    $section = $DB->get_record('course_sections', ['course' => $courseid, 'section' => $cm->sectionnum]);
    $seq = array_values(array_filter(explode(',', $section->sequence)));
    $seq = array_diff($seq, [(string)$mi->coursemodule]);
    $pos = array_search((string)$oldcm, $seq);
    array_splice($seq, $pos === false ? count($seq) : $pos, 0, [(string)$mi->coursemodule]);
    $DB->set_field('course_sections', 'sequence', implode(',', $seq), ['id' => $section->id]);
    course_delete_module($oldcm);
    echo "map $oldcm {$mi->coursemodule}\n";
}
if ($apply) { rebuild_course_cache($courseid, true); purge_all_caches(); echo "done\n"; }
else echo "DRY RUN\n";
