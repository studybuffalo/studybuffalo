<?php

require_once '../../../../config/db_config.php';

$q = explode(",", $_GET["q"]);
$resultArray = array();
$urlArray = array();

// Establish database connection
$db = db_connect('sb', 'abc_vw');

// Sending prepared statement to server
$params = implode(",", array_fill(0, count($q), "?"));
$query = "SELECT DISTINCT t1.url, t1.brand_name, t1.strength, t1.route, " .
		 "t1.dosage_form, t1.generic_name, t1.unit_price, t1.lca, " .
		 "t1.unit_issue, t2.criteria, t2.coverage, t2.criteria_sa, " .
		 "t2.group_1, t2.group_66, t2.group_66a, t2.group_19823, " .
		 "t2.group_19823a, t2.group_19824, t2.group_20400, t2.group_20403, " .
		 "t2.group_20514, t2.group_22128, t2.group_23609 " .
		 "FROM abc_price t1 " .
		 "JOIN abc_coverage t2 " .
		 "ON t1.url = t2.url " .
		 "WHERE t1.url IN ($params) AND t1.unit_price IS NOT NULL";

$statement = $db->prepare($query);	
$statement->execute($q);

// Copy server results to array
while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
	// Creates special auth entry in results
	$temp['special_auth'] = array();
	
	// Adds results to array
	array_push($resultArray, $temp);
	
	// Collects all URLs for special auth query
	array_push($urlArray, $temp['url']);
}

// Collects retrieved URLs and retrieves special auth information
$params = implode(",", array_fill(0, count($urlArray), "?"));
$query = "SELECT url, title, link " .
		 "FROM abc_special_authorization " .
		 "WHERE url IN ($params) AND title IS NOT NULL";

$statement = $db->prepare($query);
$statement->execute($urlArray);

// Matches the special auth data to the appropriate $resultArray entries
while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
	for ($i = 0; $i < count($resultArray); $i++) {
		if ($resultArray[$i]['url'] === $temp['url']) {
			array_push($resultArray[$i]['special_auth'], $temp);
		}
	}
}

echo json_encode($resultArray);
?>