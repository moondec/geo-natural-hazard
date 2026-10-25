<?php
// Grading system of AGeoHazard (CLI, as admin): Polish academic scale as grade letters, weighted course total, final test.
// Usage: docker exec moodle-lab-web-1 php /backups/grading.php COURSEID
// Idempotent: re-running updates letters, settings, weights and the quiz settings; the quiz is created only once.
//   letters (course context):  5.0 >= 92 %, 4.5 >= 84, 4.0 >= 76, 3.5 >= 68, 3.0 >= 60, 2.0 below 60
//   course total: weighted mean – Homework M2..M7 10 % each (60 %), Final test 40 %; lesson grade items weight 0 and hidden
//   every assignment and the test: grade to pass 60; display "points (grade)" for items, the grade alone for the course total
//   final test: hidden quiz in section 7, 30 random questions (4-5 per lesson category), 1 mark each, max grade 100,
//   40 min, 2 attempts (highest counts), deferred feedback, overall feedback = the grade for the band
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->libdir . '/gradelib.php');
require_once($CFG->libdir . '/grade/grade_category.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/mod/quiz/lib.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');

$courseid = (int)($argv[1] ?? 15);
\core\session\manager::set_user(get_admin());
$course = $DB->get_record('course', ['id' => $courseid], '*', MUST_EXIST);
$ctx = context_course::instance($courseid);

// ---------------------------------------------------------------- 1. grade letters
$LETTERS = ['5.0' => 92, '4.5' => 84, '4.0' => 76, '3.5' => 68, '3.0' => 60, '2.0' => 0];
$DB->delete_records('grade_letters', ['contextid' => $ctx->id]);
foreach ($LETTERS as $letter => $low) {
    $DB->insert_record('grade_letters', (object)['contextid' => $ctx->id, 'lowerboundary' => $low, 'letter' => $letter]);
}
echo "letters: ", implode(', ', array_map(fn($l, $b) => "$l>=$b", array_keys($LETTERS), $LETTERS)), "\n";

// ---------------------------------------------------------------- 2. course grade settings
grade_set_setting($courseid, 'displaytype', GRADE_DISPLAY_TYPE_REAL_LETTER);   // items: "78.0 (4.0)"
grade_set_setting($courseid, 'decimalpoints', 0);
grade_set_setting($courseid, 'aggregationposition', 1);                       // course total at the bottom
echo "course grade display: real (letter), 0 decimals\n";

// ---------------------------------------------------------------- 3. final test quiz (created once)
$quizmodule = $DB->get_field('modules', 'id', ['name' => 'quiz'], MUST_EXIST);
$QUIZNAME = 'Final test: 30 questions from lessons 1–7';
$quiz = $DB->get_record_sql("SELECT q.*, cm.id AS cmid FROM {quiz} q JOIN {course_modules} cm ON cm.instance = q.id AND cm.module = ?
    WHERE q.course = ? AND q.name LIKE 'Final test%'", [$quizmodule, $courseid]);
// per-lesson categories of the question bank: name prefix => number of random questions
$PICK = ['L1 ' => 4, 'L2 ' => 4, 'L3 ' => 4, 'L4 ' => 5, 'L5 ' => 4, 'L6 ' => 4, 'L7 ' => 5];
if (!$quiz) {
    $mi = new stdClass();
    $mi->modulename = 'quiz'; $mi->module = $quizmodule; $mi->course = $courseid; $mi->section = 7; $mi->visible = 0;  // hidden until the test day
    $mi->name = $QUIZNAME;
    $mi->introeditor = ['text' => '<p>' . s($QUIZNAME) . '</p>', 'format' => FORMAT_HTML, 'itemid' => 0];
    $mi->showdescription = 1;
    $mi->timeopen = 0; $mi->timeclose = 0; $mi->timelimit = 40 * MINSECS; $mi->overduehandling = 'autosubmit'; $mi->graceperiod = 0;
    $mi->preferredbehaviour = 'deferredfeedback'; $mi->canredoquestions = 0; $mi->attempts = 2; $mi->attemptonlast = 0;
    $mi->grademethod = QUIZ_GRADEHIGHEST; $mi->decimalpoints = 0; $mi->questiondecimalpoints = -1;
    $mi->questionsperpage = 0; $mi->navmethod = QUIZ_NAVMETHOD_FREE; $mi->shuffleanswers = 1;
    $mi->quizpassword = ''; $mi->subnet = ''; $mi->browsersecurity = '-'; $mi->delay1 = 0; $mi->delay2 = 0;
    $mi->showuserpicture = 0; $mi->showblocks = 0; $mi->allowofflineattempts = 0;
    $mi->completionattemptsexhausted = 0; $mi->completionminattempts = 0; $mi->completionpassgrade = 0; $mi->completionusegrade = 0;
    $mi->grade = 100; $mi->gradepass = 60; $mi->sumgrades = 0;
    // review options: the attempt, marks, correctness and the feedback texts right after the attempt and later; right answers never
    foreach (['attempt', 'correctness', 'marks', 'specificfeedback', 'generalfeedback', 'overallfeedback'] as $f) {
        $mi->{$f . 'during'} = 0; $mi->{$f . 'immediately'} = 1; $mi->{$f . 'open'} = 1; $mi->{$f . 'closed'} = 1;
    }
    foreach (['rightanswer'] as $f) { $mi->{$f . 'during'} = 0; $mi->{$f . 'immediately'} = 0; $mi->{$f . 'open'} = 0; $mi->{$f . 'closed'} = 0; }
    // overall feedback per grade band
    $bands = [['92%', '<p><strong>5.0</strong> – excellent. You read hazard maps and their uncertainty like a professional.</p>'],
              ['84%', '<p><strong>4.5</strong> – very good.</p>'],
              ['76%', '<p><strong>4.0</strong> – good.</p>'],
              ['68%', '<p><strong>3.5</strong> – satisfactory plus.</p>'],
              ['60%', '<p><strong>3.0</strong> – satisfactory: passed.</p>'],
              [null,  '<p><strong>2.0</strong> – not passed (below 60 %). Review the lesson pages and the lecture summaries, then use your second attempt.</p>']];
    $mi->feedbacktext = []; $mi->feedbackboundaries = [];
    foreach ($bands as $i => [$b, $t]) { $mi->feedbacktext[$i] = ['text' => $t, 'format' => FORMAT_HTML]; if ($b !== null) $mi->feedbackboundaries[$i] = $b; }
    $mi->visibleoncoursepage = 1; $mi->cmidnumber = ''; $mi->groupmode = 0; $mi->groupingid = 0;
    $mi = create_module($mi);
    $quiz = $DB->get_record('quiz', ['id' => $mi->instance]); $quiz->cmid = $mi->coursemodule;
    echo "CREATED quiz {$quiz->id} cm{$quiz->cmid} in section 7 (hidden)\n";
    // random questions: one page per lesson category
    $structure = \mod_quiz\quiz_settings::create($quiz->id)->get_structure();
    $page = 1;
    foreach ($PICK as $prefix => $n) {
        $cat = $DB->get_record_sql("SELECT * FROM {question_categories} WHERE contextid = ? AND " . $DB->sql_like('name', '?'), [$ctx->id, $prefix . '%'], MUST_EXIST);
        $structure->add_random_questions($page, $n, ['filter' => ['category' => ['jointype' => \core\output\datafilter::JOINTYPE_ANY,
            'values' => [(int)$cat->id], 'filteroptions' => ['includesubcategories' => false]]]]);
        echo "  page $page: $n random of '{$cat->name}'\n";
        $page++;
    }
    $quiz = $DB->get_record('quiz', ['id' => $quiz->id]); $quiz->cmid = $mi->coursemodule;
    quiz_update_sumgrades($quiz);
    $quiz = $DB->get_record('quiz', ['id' => $quiz->id]); $quiz->cmid = $mi->coursemodule;
    echo "  sumgrades {$quiz->sumgrades}, grade {$quiz->grade}\n";
} else {
    echo "quiz exists: {$quiz->id} cm{$quiz->cmid}\n";
}
quiz_grade_item_update($quiz);

// ---------------------------------------------------------------- 4. course total: weighted mean, weights, pass grades, display
$coursecat = grade_category::fetch_course_category($courseid);
$coursecat->aggregation = GRADE_AGGREGATE_WEIGHTED_MEAN;
$coursecat->aggregateonlygraded = 1;
$coursecat->update();
$total = $coursecat->get_grade_item();
$total->display = GRADE_DISPLAY_TYPE_LETTER; $total->decimals = 0; $total->gradepass = 60; $total->grademax = 100; $total->grademin = 0; $total->update();   // weighted mean: the total is 0-100 (was 200 from the natural sum)

// Two parts of the subject, weighted by teaching hours (20 h lecture + 40 h lab = 60 h):
//   part A – the other lecturer, first weeks: 6 h lecture + 18 h lab = 24 h -> 40 %   (a manual grade item, filled in by hand)
//   part B – this Moodle course:            14 h lecture + 22 h lab = 36 h -> 60 %   (a grade category: homework 10 % each, final test 40 %)
$PARTA = 'Part A: grade from the first weeks of the semester (other lecturer, 24 h)';
$PARTB = 'Part B: satellite hazard mapping – this course (36 h)';
$partb = grade_category::fetch(['courseid' => $courseid, 'fullname' => $PARTB]);
if (!$partb) {
    $partb = new grade_category(['courseid' => $courseid, 'fullname' => $PARTB, 'parent' => $coursecat->id], false);
    $partb->aggregation = GRADE_AGGREGATE_WEIGHTED_MEAN; $partb->aggregateonlygraded = 1;
    $partb->insert();
    echo "created grade category: $PARTB\n";
} else {
    $partb->aggregation = GRADE_AGGREGATE_WEIGHTED_MEAN; $partb->aggregateonlygraded = 1; $partb->update();
}
$bitem = $partb->get_grade_item();
$bitem->aggregationcoef = 60; $bitem->grademax = 100; $bitem->grademin = 0; $bitem->gradepass = 60;
$bitem->display = GRADE_DISPLAY_TYPE_REAL_LETTER; $bitem->decimals = 0; $bitem->update();

$aitem = grade_item::fetch(['courseid' => $courseid, 'itemtype' => 'manual', 'itemname' => $PARTA]);
if (!$aitem) {
    $aitem = new grade_item(['courseid' => $courseid, 'itemtype' => 'manual', 'itemname' => $PARTA, 'categoryid' => $coursecat->id,
        'gradetype' => GRADE_TYPE_VALUE, 'grademax' => 100, 'grademin' => 0,
        'iteminfo' => 'Grade (0-100) of the first weeks of the semester, entered by the lecturer; weight 24/60 of the teaching hours.'], false);
    $aitem->insert();
    echo "created manual grade item: $PARTA\n";
}
$aitem->aggregationcoef = 40; $aitem->gradepass = 60; $aitem->display = GRADE_DISPLAY_TYPE_REAL_LETTER; $aitem->decimals = 0; $aitem->hidden = 0;
$aitem->categoryid = $coursecat->id; $aitem->update();

$items = grade_item::fetch_all(['courseid' => $courseid, 'itemtype' => 'mod']);
foreach ($items as $gi) {
    if ($gi->itemmodule === 'assign' && preg_match('/^Homework M\d/', $gi->itemname)) {
        $gi->categoryid = $partb->id;
        $gi->aggregationcoef = 10; $gi->gradepass = 60; $gi->display = GRADE_DISPLAY_TYPE_REAL_LETTER; $gi->decimals = 0; $gi->hidden = 0;
    } else if ($gi->itemmodule === 'quiz') {
        $gi->categoryid = $partb->id;
        $gi->aggregationcoef = 40; $gi->gradepass = 60; $gi->display = GRADE_DISPLAY_TYPE_REAL_LETTER; $gi->decimals = 0; $gi->hidden = 0;
    } else {   // lesson self-checks and anything else: no weight, not shown to students
        $gi->aggregationcoef = 0; $gi->hidden = 1;
    }
    $gi->update();
    printf("  %-8s cat=%d w=%2d pass=%2d hidden=%d | %s\n", $gi->itemmodule, $gi->categoryid, $gi->aggregationcoef, $gi->gradepass, $gi->hidden, $gi->itemname);
}
echo "course total = 40 % part A (manual) + 60 % part B (category)\n";
grade_regrade_final_grades($courseid);
rebuild_course_cache($courseid, true);
purge_all_caches();
echo "course total: weighted mean, display letter, pass 60\n";
echo "QUIZCM={$quiz->cmid}\n";
