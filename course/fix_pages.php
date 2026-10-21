<?php
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
function deck_block(string $url, string $title): string {
    $u = s($url); $t = s($title);
    return <<<HTML
<div class="iot-deck" data-iot-deck="v1">
<p style="margin:0 0 .6rem"><strong>The lecture slides</strong> are shown below – the same reveal.js deck the lecturer uses in class, published on GitHub Pages with animations, diagrams and navigation.</p>
<p style="font-size:.9em;color:#46586b;margin:.25rem 0 1.1rem">Navigation: click inside the frame, then <kbd>←</kbd> <kbd>→</kbd> or <kbd>space</kbd>; <kbd>Esc</kbd> – slide overview, <kbd>F</kbd> – full screen, <kbd>?</kbd> – help. On a small screen open the deck in a separate window.</p>
<figure class="iot-deck__item" style="margin:0 0 1.5rem">
  <figcaption style="font-weight:600;margin:0 0 .35rem">{$t}</figcaption>
  <div style="position:relative;width:100%;aspect-ratio:16/10;min-height:340px;max-height:78vh;margin:0 0 .5rem;border:1px solid #c9d6e3;border-radius:6px;overflow:hidden;background:#111;box-shadow:0 1px 4px rgba(0,0,0,.18)">
    <iframe src="{$u}" title="{$t} – reveal.js presentation" loading="lazy" allowfullscreen allow="fullscreen"
            referrerpolicy="no-referrer-when-downgrade"
            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;display:block"></iframe>
  </div>
  <p style="margin:0 0 .2rem"><a href="{$u}" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:.45rem .9rem;border:1px solid #0b4f8a;border-radius:6px;text-decoration:none;font-weight:600;color:#fff;background:#0b4f8a">Open the presentation in a new window</a></p>
</figure>
</div>
HTML;
}


$map = [422=>'intro/',423=>'01-kickoff/',424=>'02-gee-code-editor/',425=>'03-ml-classification/',426=>'04-floods/',427=>'05-landslides/',428=>'06-wildfires/',429=>'07-apis/',430=>'08-wrapup/'];
foreach ($map as $cmid => $path) {
    $cm = get_coursemodule_from_id('page', $cmid, 15, false, MUST_EXIST);
    $p = $DB->get_record('page', ['id' => $cm->instance], '*', MUST_EXIST);
    $p->content = deck_block('https://moondec.github.io/geo-natural-hazard/' . $path, $p->name);
    $p->contentformat = FORMAT_HTML; $p->revision = $p->revision + 1; $p->timemodified = time();
    $DB->update_record('page', $p);
    echo "cm $cmid: " . strlen($p->content) . " B
";
}
rebuild_course_cache(15, true); purge_all_caches(); echo "done
";
