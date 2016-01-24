<?php
$directory = scandir(($_SERVER['DOCUMENT_ROOT'] . '/practicetools/'));

foreach ($directory as &$folder) {
	$file = $folder . '/details.php';
	
	if (file_exists($file) === true) {
		include $file;
		
		echo '<tr><td><a href="' . $folder . '">' . $title . '</a></td>';
		echo '<td><a href="' . $folder . '">' . $description . '</a></td>';
		echo '<td><a href="' . $folder . '">' . $update . '</a></td></tr>';
	}
}