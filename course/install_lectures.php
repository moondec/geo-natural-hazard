<?php
// Installs the 2026 lecture cycle into course 15:
//  - replaces the file area of resource cm 389 ("Presentation") with ApplicationHazards_GEO_2026.zip (unzipped, index.html = main file)
//  - adds 8 new resources "Lecture N – title" (unzipped reveal.js exports) in the given sections
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/mod/resource/lib.php');
require_once($CFG->dirroot . '/mod/resource/locallib.php');
require_once($CFG->libdir . '/filelib.php');

$courseid = 15;
$zipdir = '/backups/lectures2026';
$apply = in_array('--apply', $argv ?? []);
$course = get_course($courseid);
$admin = get_admin();
\core\session\manager::set_user($admin);
$fs = get_file_storage();
$packer = get_file_packer('application/zip');

function fill_area_from_zip($fs, $packer, $contextid, $component, $filearea, $itemid, $zippath) {
    $fs->delete_area_files($contextid, $component, $filearea, $itemid);
    $zip = $fs->create_file_from_pathname(['contextid' => $contextid, 'component' => $component, 'filearea' => $filearea,
        'itemid' => $itemid, 'filepath' => '/', 'filename' => basename($zippath)], $zippath);
    $res = $zip->extract_to_storage($packer, $contextid, $component, $filearea, $itemid, '/');
    $zip->delete();
    $ok = 0; $bad = 0;
    foreach ($res as $name => $status) { if ($status === true) $ok++; else { $bad++; echo "   extract problem: $name => " . var_export($status, true) . "\n"; } }
    $index = $fs->get_file($contextid, $component, $filearea, $itemid, '/', 'index.html');
    if (!$index) { throw new Exception("no index.html in root of $zippath"); }
    file_set_sortorder($contextid, $component, $filearea, $itemid, '/', 'index.html', 1);
    return [$ok, $bad];
}

// 1) replace Presentation (cm 389)
$cm = get_coursemodule_from_id('resource', 389, $courseid, false, MUST_EXIST);
$ctx = context_module::instance($cm->id);
$zip = "$zipdir/ApplicationHazards_GEO_2026.zip";
echo "cm 389 '{$cm->name}': replace with $zip (" . round(filesize($zip) / 1e6) . " MB)\n";
if ($apply) {
    list($ok, $bad) = fill_area_from_zip($fs, $packer, $ctx->id, 'mod_resource', 'content', 0, $zip);
    $DB->set_field('resource', 'revision', $DB->get_field('resource', 'revision', ['id' => $cm->instance]) + 1, ['id' => $cm->instance]);
    $DB->set_field('resource', 'timemodified', time(), ['id' => $cm->instance]);
    resource_set_mainfile((object)['id' => $cm->instance, 'coursemodule' => $cm->id]);
    echo "   files extracted: $ok, problems: $bad\n";
}

// 2) new lecture resources
$lectures = [
    ['01_Kickoff', 1, 'Lecture 1 – Natural hazards and Earth observation: course kick-off'],
    ['02_GEE_CodeEditor', 2, 'Lecture 2 – Google Earth Engine: the Code Editor'],
    ['03_ML_Classification', 3, 'Lecture 3 – Machine learning for land cover classification'],
    ['04_Floods', 4, 'Lecture 4 – Flood mapping: optical indices and SAR'],
    ['05_Landslides', 5, 'Lecture 5 – Landslide mapping with satellite data'],
    ['06_Wildfires', 6, 'Lecture 6 – Wildfire detection and burn severity'],
    ['07_APIs', 7, 'Lecture 7 – GEE beyond the Code Editor: Python, Colab, geemap, rgee'],
    ['08_Wrapup', 7, 'Lecture 8 – From pixels to hazard maps: wrap-up'],
];
foreach ($lectures as [$key, $section, $name]) {
    $zip = "$zipdir/ApplicationHazards_GEO_2026_extended_$key.zip";
    $exists = $DB->get_records_sql("SELECT r.id, cm.id AS cmid FROM {resource} r JOIN {course_modules} cm ON cm.instance = r.id AND cm.module = (SELECT id FROM {modules} WHERE name = 'resource') WHERE r.course = ? AND r.name = ? AND cm.deletioninprogress = 0", [$courseid, $name]);
    echo "section $section: '$name' <- $zip (" . round(filesize($zip) / 1e6) . " MB)" . ($exists ? "  [ALREADY EXISTS cm " . reset($exists)->cmid . ", skipping]" : "") . "\n";
    if (!$apply || $exists) continue;
    $usercontext = context_user::instance($admin->id);
    $draftitemid = file_get_unused_draft_itemid();
    list($ok, $bad) = fill_area_from_zip($fs, $packer, $usercontext->id, 'user', 'draft', $draftitemid, $zip);
    $mi = new stdClass();
    $mi->modulename = 'resource'; $mi->module = $DB->get_field('modules', 'id', ['name' => 'resource']);
    $mi->course = $courseid; $mi->section = $section; $mi->visible = 1; $mi->visibleoncoursepage = 1;
    $mi->name = $name; $mi->intro = '<p>Presentation (key F – full screen, ? – help). Open in a new window; the arrows move between slides.</p>'; $mi->introformat = FORMAT_HTML;
    $mi->files = $draftitemid;
    $mi->display = RESOURCELIB_DISPLAY_OPEN; $mi->printintro = 1; $mi->showsize = 0; $mi->showtype = 0; $mi->showdate = 0; $mi->filterfiles = 0;
    $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0; $mi->completion = 0;
    $mi = add_moduleinfo($mi, $course);
    echo "   created cm {$mi->coursemodule} (files $ok, problems $bad)\n";
}
if ($apply) { purge_all_caches(); echo "caches purged\n"; }
else echo "DRY RUN – rerun with --apply\n";
