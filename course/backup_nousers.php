<?php
// Course backup WITHOUT user data (CLI, as admin) – the copy that goes to the university server.
// admin/cli/backup.php takes the site default backup_general_users (=1 here), which would carry the enrolled students
// of the course restored from production; this script switches users and all user-dependent settings off.
// Usage: docker exec -u www-data moodle-lab-web-1 php /backups/backup_nousers.php COURSEID /tmp/mbzout
define('CLI_SCRIPT', true);
require '/var/www/html/config.php';
require_once($CFG->dirroot . '/backup/util/includes/backup_includes.php');

$courseid = (int)($argv[1] ?? 15);
$dest = rtrim($argv[2] ?? '/tmp/mbzout', '/');
$admin = get_admin();
\core\session\manager::set_user($admin);

$bc = new backup_controller(backup::TYPE_1COURSE, $courseid, backup::FORMAT_MOODLE, backup::INTERACTIVE_YES,
    backup::MODE_GENERAL, $admin->id);
$plan = $bc->get_plan();
// 'users' first: the other user settings depend on it and get locked once it is off
foreach (['users' => 0, 'anonymize' => 0, 'role_assignments' => 0, 'comments' => 0, 'badges' => 0,
          'userscompletion' => 0, 'logs' => 0, 'grade_histories' => 0] as $name => $value) {
    if (!$plan->setting_exists($name)) continue;
    $s = $plan->get_setting($name);
    if ($s->get_status() == base_setting::NOT_LOCKED) $s->set_value($value);
    printf("  %-17s = %s\n", $name, var_export($s->get_value(), true));
}
$filename = backup_plan_dbops::get_default_backup_filename(backup::FORMAT_MOODLE, backup::TYPE_1COURSE, $courseid, false, false);
$plan->get_setting('filename')->set_value($filename);
$bc->finish_ui();
$bc->execute_plan();
$file = $bc->get_results()['backup_destination'];
$file->copy_content_to("$dest/$filename");
$file->delete();   // do not keep a copy in the course backup area
$bc->destroy();
echo "$dest/$filename\n";
