<?php
// Rebuild the navigation buttons of every content page (qtype 20) of the AGeoHazard lessons (course 15).
// Button order on every page: Start | Previous | <topic buttons> | Next | End of lesson.
// Start/Previous are omitted on the first page, Next on a page without a next page, and a topic button
// is omitted on the page(s) it points to. Quiz pages and end-of-lesson pages are not touched.
// Usage: docker exec -i moodle-lab-web-1 php < course/lesson_nav.php            (dry run, prints the plan)
//        docker exec -i moodle-lab-web-1 php -- --apply < course/lesson_nav.php  (writes the buttons)
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
$apply = in_array('--apply', $argv ?? [], true);
const COURSE = 15;

// lesson id => [reading order of content pages, topics: [label, target page, pages where the button is hidden]]
$nav = [
    17 => ['order' => [93, 99, 94, 100, 131, 101],
           'topics' => [['1 Sign-up', 93], ['2 Repository', 99], ['3 Collection', 94], ['4 Filters', 100],
                        ['5 Clouds', 131], ['6 NDVI and area', 101]]],
    18 => ['order' => [105, 108, 106, 107, 109],
           'topics' => [['Overview', 105], ['Supervised', 108], ['Unsupervised', 106], ['Improving', 107], ['Advanced', 109]]],
    19 => ['order' => [110, 111, 112, 113, 114, 115, 116],
           'topics' => [['Bands', 110], ['Satellites', 111], ['Water indices', 112], ['Other indices', 113],
                        ['SAR', 114], ['InSAR', 115], ['Lab 4 script', 116]]],
    20 => ['order' => [117, 118],
           'topics' => [['Landslides', 117], ['Lab 5 script', 118]]],
    21 => ['order' => [119, 120, 121, 122],
           'topics' => [['Background', 119], ['Spectral', 120], ['Burn severity', 121], ['Lab 6 script', 122]]],
    22 => ['order' => [123, 125, 132, 127, 130, 129, 128, 126],
           'topics' => [['Python', 123], ['Colab', 125], ['CDSE / openEO', 132],
                        ['QGIS', 127, [127, 130, 129, 128]], ['Capstone', 126]]],
];

$now = time();
foreach ($nav as $lessonid => $cfg) {
    $lesson = $DB->get_record('lesson', ['id' => $lessonid, 'course' => COURSE], '*', MUST_EXIST);
    $first = $cfg['order'][0];
    $maxbuttons = 0;
    echo "\n## L{$lessonid} {$lesson->name}\n";
    foreach ($cfg['order'] as $pageid) {
        $page = $DB->get_record('lesson_pages', ['id' => $pageid, 'lessonid' => $lessonid], '*', MUST_EXIST);
        if ((int)$page->qtype !== 20) {
            throw new Exception("page $pageid is not a content page (qtype {$page->qtype})");
        }
        $buttons = [];
        if ($pageid !== $first) {
            $buttons[] = ['Start', $first];
            $buttons[] = ['Previous', -40];
        }
        foreach ($cfg['topics'] as $t) {
            $hidden = $t[2] ?? [$t[1]];
            // the Start button already leads to the first page, so its topic button would be a duplicate
            if ($t[1] !== $first && !in_array($pageid, $hidden, true)) {
                $buttons[] = [$t[0], $t[1]];
            }
        }
        if ((int)$page->nextpageid !== 0) {
            $buttons[] = ['Next', -1];
        }
        $buttons[] = ['End of lesson', -9];
        $maxbuttons = max($maxbuttons, count($buttons));
        $old = $DB->get_records('lesson_answers', ['pageid' => $pageid], 'id');
        $oldtxt = implode(' ; ', array_map(fn($a) => trim(strip_tags($a->answer)) . '[' . $a->jumpto . ']', $old));
        $newtxt = implode(' ; ', array_map(fn($b) => $b[0] . '[' . $b[1] . ']', $buttons));
        echo "p{$pageid} {$page->title}\n   old: {$oldtxt}\n   new: {$newtxt}\n";
        if (!$apply) {
            continue;
        }
        $DB->delete_records('lesson_answers', ['pageid' => $pageid]);
        foreach ($buttons as $b) {
            $DB->insert_record('lesson_answers', (object)[
                'lessonid' => $lessonid, 'pageid' => $pageid, 'jumpto' => $b[1], 'grade' => 0, 'score' => 0, 'flags' => 0,
                'timecreated' => $now, 'timemodified' => 0, 'answer' => $b[0], 'answerformat' => FORMAT_MOODLE,
                'response' => '', 'responseformat' => FORMAT_MOODLE,
            ]);
        }
        $DB->set_field('lesson_pages', 'timemodified', $now, ['id' => $pageid]);
    }
    if ($apply && (int)$lesson->maxanswers < $maxbuttons) {
        $DB->set_field('lesson', 'maxanswers', $maxbuttons, ['id' => $lessonid]);
        echo "   maxanswers {$lesson->maxanswers} -> {$maxbuttons}\n";
    } else {
        echo "   buttons per page: up to {$maxbuttons} (maxanswers {$lesson->maxanswers})\n";
    }
    if ($apply) {
        $DB->set_field('lesson', 'timemodified', $now, ['id' => $lessonid]);
    }
}
echo $apply ? "\nAPPLIED\n" : "\nDRY RUN - nothing written (add --apply)\n";
