<?php
$siteAddress = $_SERVER['REQUEST_URI'];
$pageNum = substr($siteAddress, 6, 4);
$navigation;
$first = "0001";
$last;
$previous = str_pad(($pageNum - 1), 4, "0", STR_PAD_LEFT);
$next = str_pad(($pageNum + 1), 4, "0", STR_PAD_LEFT);
$random;

$directory = scandir(($_SERVER['DOCUMENT_ROOT'] . '/play/'), 1);
for ($i = 0; empty($last) === true; $i++) {
	if (!preg_match('/[^0-9]/', $directory[$i])) {
		$last = $directory[$i];
	}
}

$navigation .= '<div id="Navigation-Bar"><ul>';

//Generates "First" link
//If current link is first, dont generate link
if ($first === $pageNum) {
	$navigation .= '<li id="Navigation-First"></li>';
} else {
	$navigation .= '<li id="Navigation-First"><a href="../' . $first. '/"></a></li>';
}

//Generates "Previous" link
//If previous doesn't exist, don't make link
if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/play/' . $previous) === true) {
	$navigation .= '<li id="Navigation-Back"><a href="../' . $previous . '/"></a></li>';
} else {
	$navigation .= '<li id="Navigation-Back"></li>';
}

//Generates "Random" link
$random = rand(0, ($last + 0));
$random = str_pad($random, 4, "0", STR_PAD_LEFT);
$navigation .= '<li id="Navigation-Random"><a href="../' . $random . '/"></a></li>';

//Generates "Next" link
//If next doesn't exist, don't make link
if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/play/' . $next) === true) {
	$navigation .= '<li id="Navigation-Next"><a href="../' . $next . '/"></a></li>';
} else {
	$navigation .= '<li id="Navigation-Next"></li>';
}

//Generates "Last" link
//If current link is last, dont generate link
if ($last === $pageNum) {
	$navigation .= '<li id="Navigation-Last"></li>';
} else {
	$navigation .= '<li id="Navigation-Last"><a href="../' . $last. '/"></a></li>';
}
$navigation .= '</ul></div>';

echo $navigation;