<?php
$q = explode(",", $_GET["q"]);

// Establish database connection
$db = new PDO('mysql:host=localhost;dbname=studybuf_abc_dbl',
			  'studybuf_abc_vw',
			  'bbZMZ*Fl%[1ANQqFM~');

$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Sending prepared statement to server
$params = implode(",", array_fill(0, count($q), "?"));
$query = "SELECT url, din, brand_name, strength, route, " .
		 "dosage_form, generic_name, unit_price, lca, " .
		 "lca_text, unit_issue FROM price WHERE id IN ($params)";
 
$statement = $db->prepare($query);	
$statement->execute($q);

// Copy server results to array
$resultArray = array();

while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {		   
	array_push($resultArray, $temp);
}

echo json_encode($resultArray);
?>