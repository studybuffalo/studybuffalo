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
	$query = "SELECT `index`, `brand_name`, `strength`, `route`, " . 
			 "`dosage_form`, `generic_name` FROM price WHERE " . 
			 "((brand_name LIKE ? OR generic_name LIKE ?) AND " .
			 "unit_price IS NOT NULL)";

	$statement = $mysqli->prepare($query);	
	$statement->bind_param("ss", $q, $q);
	$statement->execute();
	$statement->bind_result($index, $brandName, $strength, $route, $dosageForm, $genericName);
	
	// Copy server results to array
	$resultArray = array();
	
	while ($statement->fetch()) {
		$tempArray = array('index' => $index,
						   'brand' => $brandName,
						   'strength' => $strength,
						   'route' => $route,
						   'dosage' => $dosageForm,
						   'generic' => $genericName);
					   
		array_push($resultArray, $tempArray);
	}

	// If results were obtained, finish processing
	if (count($resultArray > 0)) {
		// For each group of generic names + strength + route + 
		// dosage form, combines the brand names
		$tempArray = array();

		foreach ($resultArray as $key => $item) {
			$tempText = $item['generic'] . " (" . $item['strength'] . " " . 
						$item['route'] . " " . $item['dosage'] . ")";
						
			if ($key == 0) {
				$tempArray[0] = array('title' => $tempText,
									  'index' => $item['index'],
									  'brand' => $item['brand']);
			} else {
				$match = FALSE;
				
				for ($i = 0; $i < count($tempArray); $i++) {
					if ($tempArray[$i]['title'] == $tempText) {
						$tempArray[$i]['index'] .= ", " . $item['index'];
						$tempArray[$i]['brand'] .= ", " . $item['brand'];
						$match = TRUE;
						break;
					}
				}
				
				if ($match == FALSE) {
					$index = count($tempArray);
					$tempArray[$index] = array('title' => $tempText,
											   'index' => $item['index'],
											   'brand' => $item['brand']);
				}
			}
		}

		$resultArray = array_values($tempArray);
		$entries = "";
		
		//Creates list for return via AJAX function
		foreach ($resultArray as $index => $item) {
			$entries .= "<li><a id='Search-Result-" . $index . "' " .
						"data-index='" . $item['index'] . "' " .
						
						"onclick='chooseResult(this)'>" .
						"<strong>" . $item['title'] . "</strong><br>" .
						"<em>also known as " . $item['brand'] . "</em></a></li>";
		}

		$response = "<ul>" . $entries . "</ul>";
	} else {
		$response="<ul><li><a><strong>No medication found</strong></a></li></ul>";
	}
}

// Output the response
echo $response;
?>