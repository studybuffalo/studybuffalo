<?php
$link1 = '2010-11-02.jpg';
$link2 = '2010-11-03.jpg';
$content = <<<EOD
<div class="center-content">
<a href="/play/images/highres/$link1"><img src="/play/images/$link1" title="Zzzzz...."></a><br>
After finally finishing the first study season the Study Buffalo take a well-deserved rest.<br>
<br>
<a href="/play/images/highres/$link2"><img src="/play/images/$link2" title="Omnonomnom"></a><br>
Following their rest, the Study Buffalo decide to enjoy themselves. They raid the human food supplies and celebrate with bubble tea and muffins.
</div>
EOD;

echo $content;