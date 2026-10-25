<?php
// Create / update the homework assignments of AGeoHazard (CLI, as admin) from schedule.json.
// Usage: docker exec moodle-lab-web-1 php /backups/assignments.php COURSEID /backups/schedule.json
// - creates the assignments that do not exist yet (matched by the "Homework M<n>" prefix) at the end of section n,
// - sets name (no dates in names), dates, grade and submission plugins on all of them,
// - never sets a cut-off date: late submissions stay possible and are marked late,
// - sets the course start date to schedule.course_start (the anchor Moodle uses to shift dates on restore).
// Intro texts are pushed separately from course/mcontent/s<n>-assign-<cmid>.intro.html (gpush).
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/mod/assign/locallib.php');
require_once($CFG->dirroot . '/mod/assign/lib.php');

$courseid = (int)($argv[1] ?? 15);
$schedule = json_decode(file_get_contents($argv[2] ?? '/backups/schedule.json'), true) or die("cannot read schedule.json\n");
\core\session\manager::set_user(get_admin());
$course = $DB->get_record('course', ['id' => $courseid], '*', MUST_EXIST);
$tz = new DateTimeZone($schedule['timezone']);
$ts = fn(string $s) => (new DateTime($s, $tz))->getTimestamp();
$labstart = $schedule['lab_start_time'];
// "lab N" -> the lab day at lab_start_time; otherwise an explicit "Y-m-d H:i"
$when = fn(string $d) => preg_match('/^lab (\d)$/', $d, $m) ? $ts($schedule['labs'][$m[1]] . ' ' . $labstart) : $ts($d);
$moduleid = $DB->get_field('modules', 'id', ['name' => 'assign'], MUST_EXIST);

foreach ($schedule['homework'] as $n => $h) {
    $n = (int)$n;
    $due = $when($h['due']);
    $from = $ts($schedule['labs'][$n] . ' 00:00');          // open from the day of lab n
    $existing = $DB->get_record_sql("SELECT a.*, cm.id AS cmid FROM {assign} a JOIN {course_modules} cm ON cm.instance = a.id AND cm.module = ?
        WHERE a.course = ? AND a.name LIKE ?", [$moduleid, $courseid, "Homework M$n%"]);
    if (!$existing) {
        $mi = new stdClass();
        $mi->modulename = 'assign'; $mi->module = $moduleid; $mi->course = $courseid; $mi->section = $n; $mi->visible = 1;
        $mi->name = $h['name']; $mi->introeditor = ['text' => '<p>' . s($h['name']) . '</p>', 'format' => FORMAT_HTML, 'itemid' => 0];
        $mi->alwaysshowdescription = 1; $mi->submissiondrafts = 0; $mi->requiresubmissionstatement = 0; $mi->sendnotifications = 0;
        $mi->sendlatenotifications = 0; $mi->sendstudentnotifications = 1; $mi->duedate = $due; $mi->cutoffdate = 0;
        $mi->gradingduedate = $due + 7 * DAYSECS; $mi->allowsubmissionsfromdate = $from; $mi->grade = 100;
        $mi->teamsubmission = 0; $mi->requireallteammemberssubmit = 0; $mi->blindmarking = 0; $mi->markingworkflow = 0; $mi->markingallocation = 0;
        $mi->attemptreopenmethod = 'none'; $mi->maxattempts = -1; $mi->completionsubmit = 0; $mi->timelimit = 0;
        $mi->assignsubmission_file_enabled = 1; $mi->assignsubmission_file_maxfiles = 2; $mi->assignsubmission_file_maxsizebytes = 0;
        $mi->assignsubmission_file_filetypes = '.pdf,.docx,.qgz,.ipynb,.zip';
        $mi->assignsubmission_onlinetext_enabled = (int)$h['onlinetext']; $mi->assignsubmission_onlinetext_wordlimit_enabled = 0;
        $mi->assignsubmission_comments_enabled = 1; $mi->assignfeedback_comments_enabled = 1; $mi->assignfeedback_comments_commentinline = 0;
        $mi->assignfeedback_editpdf_enabled = 0; $mi->assignfeedback_file_enabled = 0; $mi->assignfeedback_offline_enabled = 0;
        $mi->visibleoncoursepage = 1; $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0;
        $mi = create_module($mi);
        echo "CREATED M$n cm{$mi->coursemodule} assign {$mi->instance} in section $n\n";
        continue;
    }
    $upd = (object)['id' => $existing->id, 'name' => $h['name'], 'allowsubmissionsfromdate' => $from, 'duedate' => $due,
        'gradingduedate' => $due + 7 * DAYSECS, 'cutoffdate' => 0, 'grade' => 100, 'timemodified' => time()];
    $DB->update_record('assign', $upd);
    if ($h['onlinetext']) {
        $DB->set_field('assign_plugin_config', 'value', 1, ['assignment' => $existing->id, 'subtype' => 'assignsubmission', 'plugin' => 'onlinetext', 'name' => 'enabled']);
    }
    $cm = get_coursemodule_from_id('assign', $existing->cmid, $courseid, false, MUST_EXIST);
    $assign = new assign(context_module::instance($cm->id), $cm, $course);
    $assign->update_calendar($cm->id);
    assign_grade_item_update($DB->get_record('assign', ['id' => $existing->id]));   // sync the grade item name with the new name
    echo "UPDATED M$n cm{$existing->cmid}: {$h['name']} | due ", userdate($due, '%Y-%m-%d %H:%M', $schedule['timezone']), "\n";
}
// course start date = first lecture: the anchor for the date shift when the .mbz is restored for the next term
$start = $ts($schedule['course_start'] . ' 00:00');
if ((int)$course->startdate !== $start) {
    $DB->set_field('course', 'startdate', $start, ['id' => $courseid]);
    echo "course start date set to {$schedule['course_start']} (was ", date('Y-m-d', $course->startdate), ")\n";
}
rebuild_course_cache($courseid, true);
purge_all_caches();
foreach ($DB->get_records_sql("SELECT a.id, a.name, a.duedate, a.cutoffdate, a.allowsubmissionsfromdate, cm.id cmid, cs.section FROM {assign} a
    JOIN {course_modules} cm ON cm.instance = a.id AND cm.module = ? JOIN {course_sections} cs ON cs.id = cm.section WHERE a.course = ? ORDER BY cs.section", [$moduleid, $courseid]) as $a) {
    echo "s{$a->section} cm{$a->cmid} {$a->name} | from ", userdate($a->allowsubmissionsfromdate, '%Y-%m-%d', $schedule['timezone']),
         " due ", userdate($a->duedate, '%Y-%m-%d %H:%M', $schedule['timezone']), " cutoff {$a->cutoffdate}\n";
}
