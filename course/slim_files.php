<?php
// Slim down the AGeoHazard course (course 15) before the .mbz backup:
//  - drop the 143 MB page_contents image of lesson page 93 (a Firefox new-tab screenshot, already removed from the text),
//  - delete the "Short deck" resource (cm 397: a 60 MB reveal.js export that duplicates Lecture 3),
//  - empty the course recycle bin (old lecture pages replaced on 2026-10-21).
// Usage: dry run  docker exec -i moodle-lab-web-1 php < course/slim_files.php
//        apply    docker exec -i -u www-data moodle-lab-web-1 php -- --apply < course/slim_files.php
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once $CFG->dirroot . '/course/lib.php';
$apply = in_array('--apply', $argv ?? [], true);
const COURSE = 15;
$fs = get_file_storage();
$coursectx = context_course::instance(COURSE);

// 1. lesson page image
$imgs = $fs->get_area_files(context_module::instance(391)->id, 'mod_lesson', 'page_contents', 93, 'filename', false);
foreach ($imgs as $f) {
    if ($f->get_filename() !== 'signupgee.png') { continue; }
    printf("page 93 image %s %.1f MB -> delete\n", $f->get_filename(), $f->get_filesize() / 1048576);
    if ($apply) { $f->delete(); }
}

// (the course overview banner stays as it is - rule in CLAUDE.md)

// 3. Short deck resource
$cm = get_coursemodule_from_id('resource', 397, COURSE, false, IGNORE_MISSING);
if ($cm) {
    $size = 0;
    foreach ($fs->get_area_files(context_module::instance(397)->id, 'mod_resource', 'content', 0, 'filename', false) as $f) { $size += $f->get_filesize(); }
    printf("cm 397 resource \"%s\" %.1f MB in %d files -> delete module\n", $cm->name, $size / 1048576, count($fs->get_area_files(context_module::instance(397)->id, 'mod_resource', 'content', 0, 'filename', false)));
    if ($apply) { course_delete_module(397); }
} else {
    echo "cm 397 already gone\n";
}

// 4. recycle bin
if (class_exists('\tool_recyclebin\course_bin')) {
    $bin = new \tool_recyclebin\course_bin(COURSE);
    $items = $bin->get_items();
    printf("recycle bin: %d item(s) -> empty\n", count($items));
    // delete_all_items() checks tool/recyclebin:deleteitems, which the CLI user does not hold, so delete item by item
    if ($apply) { foreach ($items as $item) { $bin->delete_item($item); } }
}

if ($apply) {
    rebuild_course_cache(COURSE, true);
    echo "APPLIED\n";
} else {
    echo "DRY RUN - nothing written (add --apply)\n";
}
