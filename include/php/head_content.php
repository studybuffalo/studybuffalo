<?php 
$content = <<<EOD
<meta charset="utf-8">
<meta name="description" content="The home page of the Study Buffalo">
<meta name="author" content="Joshua R. Torrance">
<title>$title</title>
<link rel="stylesheet" type="text/css" href="/include/css/style.css?version=1.0">
<link rel="icon" type="image/png" href="/include/images/favicon.png">

<!-- Javascript Functions -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="/include/js/mobile_menu.js?version=1.0"></script>
<script>(function(d, s, id) {var js, fjs = d.getElementsByTagName(s)[0];if (d.getElementById(id)) return;js = d.createElement(s); js.id = id;js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.5";fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));</script>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?"http":"https";if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document, "script", "twitter-wjs");</script>
<script src="https://apis.google.com/js/platform.js" async defer></script>
EOD;

echo $content;