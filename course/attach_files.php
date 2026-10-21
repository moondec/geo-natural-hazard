<?php
// Attach files from /tmp/newfiles/<fieldstem>/<file> to the Moodle file area of that field (course 15).
// Field stems as in the mcontent naming: s4-lesson-401-p111, s2-label-393, s1-page-390, s3-lesson-396 (intro), s2-assign-392 (intro).
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
$courseid = 15; $dir = '/tmp/newfiles';
$apply = in_array('--apply', $argv ?? []);
$fs = get_file_storage();
foreach (glob("$dir/*", GLOB_ONLYDIR) as $d) {
    $stem = basename($d);
    if (!preg_match('/^s\d+-([a-z]+)-(\d+)(?:-p(\d+))?$/', $stem, $m)) { echo "SKIP $stem\n"; continue; }
    [$all, $mod, $cmid, $pageid] = $m + [3 => null];
    $cm = get_coursemodule_from_id($mod, (int)$cmid, $courseid, false, MUST_EXIST);
    $ctx = context_module::instance($cm->id);
    if ($mod === 'lesson' && $pageid) { $component = 'mod_lesson'; $area = 'page_contents'; $itemid = (int)$pageid; }
    elseif ($mod === 'page') { $component = 'mod_page'; $area = 'content'; $itemid = 0; }
    else { $component = 'mod_' . $mod; $area = 'intro'; $itemid = 0; }
    foreach (array_filter(glob("$d/*"), 'is_file') as $f) {
        $name = basename($f);
        $exists = $fs->get_file($ctx->id, $component, $area, $itemid, '/', $name);
        echo "$stem -> $component/$area/$itemid/$name (" . round(filesize($f) / 1024) . " kB)" . ($exists ? ' [replace]' : '') . "\n";
        if (!$apply) continue;
        if ($exists) $exists->delete();
        $fs->create_file_from_pathname(['contextid' => $ctx->id, 'component' => $component, 'filearea' => $area, 'itemid' => $itemid, 'filepath' => '/', 'filename' => $name], $f);
    }
}
echo $apply ? "done\n" : "DRY RUN\n";
