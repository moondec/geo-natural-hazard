<?php
// Create / update the homework assignments of AGeoHazard (CLI, as admin).
// Usage: docker exec moodle-lab-web-1 php /backups/assignments.php COURSEID
// Creates the assignments that do not exist yet (matched by the "Homework M<n>" prefix) at the end
// of their section and sets dates, grade and submission plugins on all of them. Intro texts are
// pushed separately from course/mcontent/s<n>-assign-<cmid>.intro.html (gpush).
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/mod/assign/locallib.php');

$courseid = (int)($argv[1] ?? 15);
\core\session\manager::set_user(get_admin());
$course = $DB->get_record('course', ['id' => $courseid], '*', MUST_EXIST);
$tz = new DateTimeZone('Europe/Warsaw');
$ts = fn(string $s) => (new DateTime($s, $tz))->getTimestamp();

// n => [section, name, allow from, due, online text (link) enabled]
$SPEC = [
    2 => [2, 'Homework M2: index areas (script link, due 30.11)',                  '2026-11-23 00:00', '2026-11-30 08:00', 1],
    3 => [3, 'Homework M3: classification report (due 7.12)',                      '2026-11-30 00:00', '2026-12-07 08:00', 0],
    4 => [4, 'Homework M4: flood extent map + sensitivity table (due 14.12)',      '2026-12-07 00:00', '2026-12-14 08:00', 0],
    5 => [5, 'Homework M5: landslide heatmap note (due 21.12)',                    '2026-12-14 00:00', '2026-12-21 08:00', 0],
    6 => [6, 'Homework M6: burn severity map + report (due 11.01)',                '2026-12-21 00:00', '2027-01-11 08:00', 0],
    7 => [7, 'Homework M7: capstone notebook or QGIS project (due 25.01, tbc)',    '2027-01-11 00:00', '2027-01-25 23:59', 1],
];
$moduleid = $DB->get_field('modules', 'id', ['name' => 'assign'], MUST_EXIST);

foreach ($SPEC as $n => [$section, $name, $from, $due, $onlinetext]) {
    $existing = $DB->get_record_sql("SELECT a.*, cm.id AS cmid FROM {assign} a JOIN {course_modules} cm ON cm.instance = a.id AND cm.module = ?
        WHERE a.course = ? AND a.name LIKE ?", [$moduleid, $courseid, "Homework M$n%"]);
    if (!$existing) {
        $mi = new stdClass();
        $mi->modulename = 'assign'; $mi->module = $moduleid; $mi->course = $courseid; $mi->section = $section; $mi->visible = 1;
        $mi->name = $name; $mi->introeditor = ['text' => '<p>' . s($name) . '</p>', 'format' => FORMAT_HTML, 'itemid' => 0];
        $mi->alwaysshowdescription = 1; $mi->submissiondrafts = 0; $mi->requiresubmissionstatement = 0; $mi->sendnotifications = 0;
        $mi->sendlatenotifications = 0; $mi->sendstudentnotifications = 1; $mi->duedate = $ts($due); $mi->cutoffdate = 0;
        $mi->gradingduedate = $ts($due) + 7 * DAYSECS; $mi->allowsubmissionsfromdate = $ts($from); $mi->grade = 100;
        $mi->teamsubmission = 0; $mi->requireallteammemberssubmit = 0; $mi->blindmarking = 0; $mi->markingworkflow = 0; $mi->markingallocation = 0;
        $mi->attemptreopenmethod = 'none'; $mi->maxattempts = -1; $mi->completionsubmit = 0; $mi->timelimit = 0;
        $mi->assignsubmission_file_enabled = 1; $mi->assignsubmission_file_maxfiles = 2; $mi->assignsubmission_file_maxsizebytes = 0;
        $mi->assignsubmission_file_filetypes = '.pdf,.docx,.qgz,.ipynb,.zip';
        $mi->assignsubmission_onlinetext_enabled = $onlinetext; $mi->assignsubmission_onlinetext_wordlimit_enabled = 0;
        $mi->assignsubmission_comments_enabled = 1; $mi->assignfeedback_comments_enabled = 1; $mi->assignfeedback_comments_commentinline = 0;
        $mi->assignfeedback_editpdf_enabled = 0; $mi->assignfeedback_file_enabled = 0; $mi->assignfeedback_offline_enabled = 0;
        $mi->visibleoncoursepage = 1; $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0;
        $mi = create_module($mi);
        echo "CREATED M$n cm{$mi->coursemodule} assign {$mi->instance} in section $section\n";
        continue;
    }
    // update dates / name / grade on the existing assignment
    $upd = (object)['id' => $existing->id, 'name' => $name, 'allowsubmissionsfromdate' => $ts($from), 'duedate' => $ts($due),
        'gradingduedate' => $ts($due) + 7 * DAYSECS, 'cutoffdate' => 0, 'grade' => 100, 'timemodified' => time()];
    $DB->update_record('assign', $upd);
    if ($onlinetext) {
        $DB->set_field('assign_plugin_config', 'value', 1, ['assignment' => $existing->id, 'subtype' => 'assignsubmission', 'plugin' => 'onlinetext', 'name' => 'enabled']);
    }
    $cm = get_coursemodule_from_id('assign', $existing->cmid, $courseid, false, MUST_EXIST);
    $assign = new assign(context_module::instance($cm->id), $cm, $course);
    $assign->update_calendar($cm->id);
    echo "UPDATED M$n cm{$existing->cmid}: due $due\n";
}
rebuild_course_cache($courseid, true);
purge_all_caches();
foreach ($DB->get_records_sql("SELECT a.id, a.name, a.duedate, a.allowsubmissionsfromdate, cm.id cmid, cs.section FROM {assign} a
    JOIN {course_modules} cm ON cm.instance = a.id AND cm.module = ? JOIN {course_sections} cs ON cs.id = cm.section WHERE a.course = ? ORDER BY cs.section", [$moduleid, $courseid]) as $a) {
    echo "s{$a->section} cm{$a->cmid} {$a->name} | from ", date('Y-m-d', $a->allowsubmissionsfromdate), " due ", date('Y-m-d H:i', $a->duedate), "\n";
}
