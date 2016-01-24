<?php
$response = "";

//get the q parameter from URL
$q = $_GET["q"];

// Only run search if $q is not blank
if (strlen($q) > 0) {
	// Adding wildcard markers to query
	$q = "%" . $q . "%";
	
	// Establish database connection
	$mysqli = new mysqli('localhost',
						 'studybuf_abc_vw',
						 'bbZMZ*Fl%[1ANQqFM~',
						 'studybuf_abc_dbl');

	if ($mysqli->connect_error) {
		die('Could not connect: ' . $mysqli->connect_error);
	}
	
	// Sending prepared statement to server
	$query = "SELECT DISTINCT t1.id , t1.brand_name, t1.strength, " . 
			 "t1.route, t1.dosage_form, t1.generic_name " . 
			 "FROM price t1 " . 
			 "INNER JOIN price t2 " .
			 "ON t1.generic_name = t2.generic_name " .
			 "WHERE ((t2.generic_name LIKE ? OR t2.brand_name LIKE ?) " . 
			 "AND t1.unit_price IS NOT NULL)";
	
	$statement = $mysqli->prepare($query);
	$statement->bind_param("ss", $q, $q);
	$statement->execute();
	$statement->bind_result($id, $brandName, $strength, $route, $dosageForm, $genericName);
	
	// Copy server results to array
	$resultArray = array();
	
	while ($statement->fetch()) {
		$tempArray = array('id' => $id,
						   'brand' => $brandName,
						   'strength' => $strength,
						   'route' => $route,
						   'dosage' => $dosageForm,
						   'generic' => $genericName);
					   
		array_push($resultArray, $tempArray);
	}
	
	// If results were obtained, finish processing
	if (count($resultArray) > 0) {
		// For each group of generic names + strength + route + 
		// dosage form, combines the brand names
		$tempArray = array();
		
		foreach ($resultArray as $key => $item) {
			$tempText = $item['generic'] . " (" . $item['strength'] . " " . 
						$item['route'] . " " . $item['dosage'] . ")";
						
			if ($key == 0) {
				$tempArray[0] = array('title' => $tempText,
									  'id' => $item['id'],
									  'brand' => $item['brand']);
			} else {
				$match = FALSE;
				
				for ($i = 0; $i < count($tempArray); $i++) {
					if ($tempArray[$i]['title'] == $tempText) {
						$tempArray[$i]['id'] .= "," . $item['id'];
						$tempArray[$i]['brand'] .= ", " . $item['brand'];
						$match = TRUE;
						break;
					}
				}
				
				if ($match == FALSE) {
					$index = count($tempArray);
					$tempArray[$index] = array('title' => $tempText,
											   'id' => $item['id'],
											   'brand' => $item['brand']);
				}
			}
		}

		$resultArray = array_values($tempArray);
		$entries = "";
		
		//Creates list for return via AJAX function
		foreach ($resultArray as $index => $item) {
			$entries .= "<li><a id='Search-Result-" . $index . "' " .
						"data-id='" . $item['id'] . "' " .
						
						"onclick='chooseResult(this)'>" .
						"<strong>" . $item['title'] . "</strong><br>" .
						"<em>also known as " . $item['brand'] . "</em></a></li>";
		}
		
		$response = "<ul>" . $entries . "</ul>";
	} else {
		$response = "<ul><li><a><strong>No medication found</strong></a></li></ul>";
	}
	
}

// Output the response
echo $response;
?>