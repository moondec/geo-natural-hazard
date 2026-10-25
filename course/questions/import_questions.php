<?php
// Import final_test.xml into the question bank of a course (CLI, as admin).
// Usage: docker exec -i moodle-lab-web-1 php -- /dev/stdin COURSEID /path/in/container/final_test.xml < import_questions.php
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->libdir . '/questionlib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');

[$courseid, $file] = [(int)($argv[1] ?? 15), $argv[2] ?? '/tmp/final_test.xml'];
if (!is_readable($file)) { fwrite(STDERR, "cannot read $file\n"); exit(1); }

\core\session\manager::set_user(get_admin());
$course  = $DB->get_record('course', ['id' => $courseid], '*', MUST_EXIST);
$context = context_course::instance($courseid);
$category = question_make_default_categories([$context]);   // "Default for <course>" under top

$qformat = new qformat_xml();
$qformat->setCategory($category);
$qformat->setContexts([$context]);
$qformat->setCourse($course);
$qformat->setFilename($file);
$qformat->setRealfilename(basename($file));
$qformat->setMatchgrades('error');
$qformat->setCatfromfile(true);        // categories come from the <question type="category"> entries
$qformat->setContextfromfile(false);
$qformat->setStoponerror(true);

ob_start();
$ok = $qformat->importpreprocess() && $qformat->importprocess() && $qformat->importpostprocess();
$log = strip_tags(str_replace(['<br />', '<br>', '</li>'], "\n", ob_get_clean()));
echo preg_replace("/\n{2,}/", "\n", trim($log)), "\n";
echo $ok ? "IMPORT OK\n" : "IMPORT FAILED\n";

$n = $DB->count_records_sql("SELECT COUNT(*) FROM {question_bank_entries} qbe
    JOIN {question_categories} qc ON qc.id = qbe.questioncategoryid WHERE qc.contextid = ?", [$context->id]);
echo "questions in course question bank: $n\n";
foreach ($DB->get_records('question_categories', ['contextid' => $context->id], 'id') as $c) {
    $k = $DB->count_records('question_bank_entries', ['questioncategoryid' => $c->id]);
    echo "  cat {$c->id} {$c->name}: $k\n";
}
exit($ok ? 0 : 2);
