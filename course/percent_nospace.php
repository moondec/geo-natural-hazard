<?php
// Typography rule (Marek, 2026-11-06): no space between a number and the percent sign ("2%", not "2 %").
// Scans every text field of one course in the database and removes the space (also &nbsp;, U+00A0, U+202F).
// Usage: docker exec moodle-lab-web-1 php /tmp/percent_nospace.php COURSEID [--apply]   (dry run without --apply)
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';

$courseid = (int)($argv[1] ?? 15);
$apply = in_array('--apply', $argv, true);
$RE = '/(?<=[0-9)\]*])(?: |\x{00A0}|\x{202F}|&nbsp;|&#160;|&#8239;)+%/u';
$ctx = context_course::instance($courseid);
$ctxlike = $ctx->path . '/%';

// table => [fields, WHERE clause selecting the rows of this course, params]
$Q = "questionid IN (SELECT qv.questionid FROM {question_versions} qv JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
      JOIN {question_categories} qc ON qc.id = qbe.questioncategoryid JOIN {context} c ON c.id = qc.contextid WHERE c.id = ? OR c.path LIKE ?)";
$targets = [
    'question'                  => [['name', 'questiontext', 'generalfeedback'], str_replace('questionid IN', 'id IN', $Q), [$ctx->id, $ctxlike]],
    'question_answers'          => [['answer', 'feedback'], 'question IN' . substr($Q, strlen('questionid IN')), [$ctx->id, $ctxlike]],
    'qtype_multichoice_options' => [['correctfeedback', 'partiallycorrectfeedback', 'incorrectfeedback'], $Q, [$ctx->id, $ctxlike]],
    'question_hints'            => [['hint'], $Q, [$ctx->id, $ctxlike]],
    'quiz'                      => [['name', 'intro'], 'course = ?', [$courseid]],
    'quiz_feedback'             => [['feedbacktext'], 'quizid IN (SELECT id FROM {quiz} WHERE course = ?)', [$courseid]],
    'lesson'                    => [['name', 'intro'], 'course = ?', [$courseid]],
    'lesson_pages'              => [['title', 'contents'], 'lessonid IN (SELECT id FROM {lesson} WHERE course = ?)', [$courseid]],
    'lesson_answers'            => [['answer', 'response'], 'lessonid IN (SELECT id FROM {lesson} WHERE course = ?)', [$courseid]],
    'assign'                    => [['name', 'intro', 'activity'], 'course = ?', [$courseid]],
    'page'                      => [['name', 'intro', 'content'], 'course = ?', [$courseid]],
    'label'                     => [['name', 'intro'], 'course = ?', [$courseid]],
    'forum'                     => [['name', 'intro'], 'course = ?', [$courseid]],
    'resource'                  => [['name', 'intro'], 'course = ?', [$courseid]],
    'url'                       => [['name', 'intro'], 'course = ?', [$courseid]],
    'course_sections'           => [['name', 'summary'], 'course = ?', [$courseid]],
    'course'                    => [['fullname', 'summary'], 'id = ?', [$courseid]],
    'grade_items'               => [['itemname', 'iteminfo'], 'courseid = ?', [$courseid]],
    'grade_categories'          => [['fullname'], 'courseid = ?', [$courseid]],
];
$total = 0;
foreach ($targets as $table => [$fields, $where, $params]) {
    $rows = $DB->get_records_select($table, $where, $params, '', 'id, ' . implode(', ', $fields));
    foreach ($rows as $r) {
        foreach ($fields as $f) {
            if ($r->$f === null || $r->$f === '') continue;
            $new = preg_replace($RE, '%', $r->$f, -1, $n);
            if (!$n) continue;
            $total += $n;
            preg_match($RE, $r->$f, $m, PREG_OFFSET_CAPTURE);
            printf("%-26s #%-5d %-15s %2d× …%s\n", $table, $r->id, $f, $n, str_replace("\n", ' ', substr($r->$f, max(0, $m[0][1] - 35), 50)));
            if ($apply) $DB->set_field($table, $f, $new, ['id' => $r->id]);
        }
    }
}
echo ($apply ? 'applied: ' : 'dry run: '), "$total replacement(s)\n";
if ($apply) { rebuild_course_cache($courseid, true); purge_all_caches(); }
