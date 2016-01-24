<?php
$socialMedia;
$siteAddress = 'http://www.studybuffalo.com' . $_SERVER['REQUEST_URI'];

$socialMedia .= '<div id="Social-Media">';
$socialMedia .= '<h2>Social Media &#38; Stuff</h2>';

//Google Plus Link
$socialMedia .= '<div id="Social-Media-Google">';
$socialMedia .= '<g:plusone href="' . $siteAddress .'"></g:plusone>';
$socialMedia .= '</div>';

//Add Facebook Link
$socialMedia .= '<div id="Social-Media-Facebook">';
$socialMedia .= '<div id="fb-root"></div><div class="fb-like" data-href="' . $siteAddress . '" data-width="200" data-layout="button_count" data-action="like" data-show-faces="false" data-share="true"></div>';
$socialMedia .= '</div>';
 
//Add twitter Link
$socialMedia .= '<div id="Social-Media-Twitter">';
$socialMedia .= '<a href="https://twitter.com/share" class="twitter-share-button" data-via="StudyBuffalo">Tweet</a>';
$socialMedia .= '</div>';

$socialMedia .= '</div></div>';

echo $socialMedia;