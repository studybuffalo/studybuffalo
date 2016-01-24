<?php
$directory = scandir(($_SERVER['DOCUMENT_ROOT'] . '/play/'), 1);
$newest;
for ($i = 0; empty($newest) === true; $i++) {
	if (!preg_match('/[^0-9]/', $directory[$i])) {
		$newest = $directory[$i];
	}
}

include $_SERVER['DOCUMENT_ROOT'] . '/play/' . $newest . '/content.php';