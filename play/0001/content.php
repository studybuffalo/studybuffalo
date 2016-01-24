<?php
$link1 = '2010-10-23.jpg';
$link2 = '2010-10-24.jpg';
$content = <<<EOD
<div class="center-content">
<a href="/play/images/highres/$link1"><img src="/play/images/$link1"></a><br>
The Study Buffalo begin grazing in late October.<br>
<br>
<a href="/play/images/highres/$link2"><img src="/play/images/$link2"></a><br>
After many long hours, the Study Buffalo continue to graze. They are not fazed by the sinking sun.
</div>
EOD;

echo $content;