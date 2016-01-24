<?php
$directory = getcwd();
$directory = str_replace('/home5/studybuf/public_html/studybuffalo/', '', $directory);
$stringCut = strpos($directory, '/');
$directory = ($stringCut ? substr($directory, 0, $stringCut) : $directory);

$menuString = <<<EOT
<nav>
<div id="Menu" class="expanded">
<header id="Menu-Logo"><img src="/include/images/logo.svg" alt="STUDY BUFFALO"></header>
<ul id="Menu-List">
EOT;

$menuString .= (
	$directory === '/home5/studybuf/public_html/studybuffalo' ?
	'<li class="selected"><a href="/">Home</a></li>' :
	'<li><a href="/">Home</a></li>'
);

$menuString .= (
	$directory === 'play' ?
	'<li class="selected"><a href="/play/">Play</a></li>' :
	'<li><a href="/play/">Play</a></li>'
);

$menuString .= (
	$directory === 'studyguides' ?
	'<li class="selected"><a href="/studyguides/">Study Guides</a></li>' :
	'<li><a href="/studyguides/">Study Guides</a></li>'
);

$menuString .= (
	$directory === 'practicetools' ?
	'<li class="selected"><a href="/practicetools/">Practice Tools</a></li>' :
	'<li><a href="/practicetools/">Practice Tools</a></li>'
);

$menuString .= (
	$directory === 'publications' ?
	'<li class="selected"><a href="/publications/">Publications</a></li>' :
	'<li><a href="/publications/">Publications</a></li>'
);

$menuString .= <<<EOT
</ul>
<a id="Menu-Icon"><img  src="/include/images/menu_icon.svg" title="MENU"></a>
</div>
<div id="Menu-Heading">
<h1>$header</h1>
</div>
</nav>
EOT;

echo $menuString;