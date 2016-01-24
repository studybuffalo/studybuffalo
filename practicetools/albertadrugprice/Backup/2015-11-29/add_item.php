<?php
$q = $_GET["q"];

// Establish database connection
$mysqli = new mysqli('localhost',
					 'studybuf_abc_vw',
					 'bbZMZ*Fl%[1ANQqFM~',
					 'studybuf_abc_dbl');

if ($mysqli->connect_error) {
	die('Could not connect: ' . $mysqli->connect_error);
}

// Sending prepared statement to server
$query = "SELECT `url`, `din`, `brand_name`, `strength`, `route`, " .
		 "`dosage_form`, `generic_name`, `unit_price`, `lca`, " .
		 "`lca_text`, `unit_issue` FROM price WHERE `index` IN (?)";
		 
$statement = $mysqli->prepare($query);	
$statement->bind_param("s", $q);
$statement->execute();
$statement->bind_result($url, $din, $brandName, $strength, $route, 
						$dosageForm, $genericName, $unitPrice, $lca, 
						$lcaText, $unitIssue);
						
// Copy server results to array
$resultArray = array();

while ($statement->fetch()) {
	$temp = array('url' => $url,
				  'din' => $din,
				  'brandName' => $brandName,
				  'strength' => $strength,
				  'route' => $route,
				  'dosageForm' => $dosageForm,
				  'genericName' => $genericName,
				  'unitPrice' => $unitPrice,
				  'lca' => $lca,
				  'lcaText' => $lcaText,
				  'unitIssue' => $unitIssue);
				   
	array_push($resultArray, $temp);
}

echo json_encode($resultArray);
?>