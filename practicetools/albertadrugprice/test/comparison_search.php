<?php

function boolConvert($string) {
	if ($string === "true") {
		return True;
	} else {
		return False;
	}
}

function findLastCode($array, $type) {
	// Finds the most specific classification
	if ($type === "ptc") {
		if ($array["ptc_4_text"]) {
			return $array["ptc_4_text"];
		} else if ($array["ptc_3_text"]) {
			return $array["ptc_3_text"];
		} else if ($array["ptc_2_text"]) {
			return $array["ptc_2_text"];
		} else if ($array["ptc_1_text"]) {
			return $array["ptc_1_text"];
		}
	} else if ($type === "atc") {
		if ($array["atc_4_text"]) {
			return $array["atc_4_text"];
		} else if ($array["atc_3_text"]) {
			return $array["atc_3_text"];
		} else if ($array["atc_2_text"]) {
			return $array["atc_2_text"];
		} else if ($array["atc_1_text"]) {
			return $array["atc_1_text"];
		}
	}
}

function queryComplete($db, $urlList, $type) {
	$outputArray = array();
	$params = implode(",", array_fill(0, count($urlList), "?"));
	
	// Generates appropriate query
	if ($type === "atc") {
		$query = "SELECT DISTINCT t1.url, t1.route, t1.generic_name, " . 
				 "t2.atc_1_text, t2.atc_2_text, t2.atc_3_text, t2.atc_4_text " .
				 "FROM price t1 " .
				 "INNER JOIN atc t2 " .
				 "ON t1.url = t2.url " .
				 "WHERE t1.url IN ($params) AND t1.unit_price IS NOT NULL";
	} else if ($type === "ptc") {
		$query = "SELECT DISTINCT t1.url, t1.route, t1.generic_name, " . 
				 "t2.ptc_1_text, t2.ptc_2_text, t2.ptc_3_text, t2.ptc_4_text " .
				 "FROM price t1 " .
				 "INNER JOIN ptc t2 " .
				 "ON t1.url = t2.url " .
				 "WHERE t1.url IN ($params) AND t1.unit_price IS NOT NULL";
	}
	
	$statement = $db->prepare($query);
	$statement->execute($urlList);
	
	// Gathers all the required data to generate final AJAX response
	while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
		$temp['type'] = $type;
		array_push($outputArray, $temp);
	}
	
	return $outputArray;
}

function getAtcUrl($db, $arg) {
	$outputArray = array();
	$urlList = array();
	
	// Converts $args to properly formatted array for PDO execution
	$args = array($arg, $arg, $arg, $arg);
	
	// Finds all the URLs matching the query arguments
	$query = "SELECT url, atc_1_text, atc_2_text, atc_3_text, atc_4_text " . 
			 "FROM atc " . 
			 "WHERE (atc_1_text LIKE ? OR atc_2_text LIKE ? OR " . 
			 "atc_3_text LIKE ? OR atc_4_text LIKE ?)";
	
	$statement = $db->prepare($query);	
	$statement->execute($args);
	
	while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {		   
		array_push($urlList, $temp['url']);
	}
	
	return $urlList;
}

function getPtcUrl($db, $arg) {
	$outputArray = array();
	$urlList = array();
	
	// Converts $args to properly formatted array for PDO execution
	$args = array($arg, $arg, $arg, $arg);
	
	// Finds all the URLs matching the query arguments
	$query = "SELECT url, ptc_1_text, ptc_2_text, ptc_3_text, ptc_4_text " .
			 "FROM ptc " . 
			 "WHERE (ptc_1_text LIKE ? OR ptc_2_text LIKE ? OR " . 
			 "ptc_3_text LIKE ? OR ptc_4_text LIKE ?)";
	
	$statement = $db->prepare($query);	
	$statement->execute($args);
	
	while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {		   
		array_push($urlList, $temp['url']);
	}
	
	return $urlList;
}

function getNameUrl($db, $arg, $type) {
	$outputArray = array();
	$urlList = array();
	$codeList = array();
	
	// Converts $args to properly formatted array for PDO execution
	$args = array($arg, $arg);
	
	// Finds all brand names/generic names matching the search string
	$query = "SELECT DISTINCT t1.url " .
			 "FROM price t1 " .
			 "INNER JOIN price t2 " . 
			 "ON t1.generic_name = t2.generic_name " . 
			 "WHERE (t2.generic_name LIKE ? OR " .
			 "t2.brand_name LIKE ?)";
	
	$statement = $db->prepare($query);	
	$statement->execute($args);
	
	// Isolates the urls found
	while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {		   
		array_push($urlList, $temp['url']);
	}
	
	// Finds all unique ATC & PTC text
	if (count($urlList) > 0) {
		$params = implode(",", array_fill(0, count($urlList), "?"));
		
		// Determine Query
		if ($type === "atc") {
			$query = "SELECT atc_1_text, atc_2_text, atc_3_text, atc_4_text " .
					 "FROM atc " . 
					 "WHERE url in ($params) " .
					 "GROUP BY atc_1_text, atc_2_text, atc_3_text, atc_4_text";
		} else if ($type === "ptc") {
			$query = "SELECT ptc_1_text, ptc_2_text, ptc_3_text, ptc_4_text " .
					 "FROM ptc " . 
					 "WHERE url in ($params) " .
					 "GROUP BY ptc_1_text, ptc_2_text, ptc_3_text, ptc_4_text";
		}
		
		$statement = $db->prepare($query);	
		$statement->execute($urlList);
		
		while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {		   
			$lastCode = findLastCode($temp, $type);
			array_push($codeList, $lastCode);
		}
	}
	
	// Takes the codes and extracts all the matching URLs
	if (count($codeList) > 0 && $type === "atc") {
		foreach ($codeList as $code) {
			$outputArray = array_merge($outputArray, getAtcUrl($db, $code));
		}
	} else if (count($codeList) > 0 && $type === "ptc") {
		foreach ($codeList as $code) {
			$outputArray = array_merge($outputArray, getPtcUrl($db, $code));
		}
	}
	
	return $outputArray;
}

function processAtc($db, $arg) {
	$outputArray = array();
	$urlList = array();
	
	// Get ATC urls
	$urlList = array_merge($urlList, getAtcUrl($db, $arg));
	
	// Get medication name urls
	$urlList = array_merge($urlList, getNameUrl($db, $arg, "atc"));
	
	// Takes the isolated URLs to collect the full data
	if (count($urlList) > 0) {
		$outputArray = queryComplete($db, $urlList, "atc");
	}
	
	return $outputArray;
}

function processPtc($db, $arg) {
	$outputArray = array();
	$urlList = array();
	
	// Get PTC urls
	$urlList = array_merge($urlList, getPtcUrl($db, $arg));
	
	// Get medication name urls
	$urlList = array_merge($urlList, getNameUrl($db, $arg, "ptc"));
	
	// Takes the isolated URLs to collect the full data
	if (count($urlList) > 0) {
		$outputArray = queryComplete($db, $urlList, "ptc");
	}
	
	return $outputArray;
}

$response = "";
$tempArray;
$htmlList = array();

// Get parameters from URL
$searchString = $_GET["search"];
$methodATC = boolConvert($_GET["methodATC"]);
$methodPTC = boolConvert($_GET["methodPTC"]);

// Only run search if $q is not blank
if (strlen($searchString) > 0) {
	$resultArray = array();
	
	// Adding wildcard markers to query
	$q = "%" . $searchString . "%";
	
	// Establish database connection
	$db = new PDO('mysql:host=localhost;dbname=studybuf_abc_dbl',
			  'studybuf_abc_vw',
			  'bbZMZ*Fl%[1ANQqFM~');

	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	
	// ATC Query
	if ($methodATC === true) {
		$tempArray = processAtc($db, $q);
		
		if (count($tempArray) > 0) {
			$resultArray = array_merge($resultArray, $tempArray);
		}
	}
	
	// PTC Query
	if ($methodPTC === true) {
		$tempArray = processPtc($db, $q);
		
		if (count($tempArray) > 0) {
			$resultArray = array_merge($resultArray, $tempArray);
		}
	}
}


// Only continues if at least one result returned
if (count($resultArray) > 0) {
	foreach ($resultArray as $key => $item) {
		// Assemble the common title
		$tempText = findLastCode($item, $item['type']);
		$tempText .= " (" . strtoupper($item['type']) . ")";
		
		// Creates a new array entry for each unique title
		// Entries with the same title have their url and drug name added
		if ($key == 0) {
			$htmlList[0] = array('title' => $tempText,
								  'url' => $item['url'],
								  'drugs' => $item['generic_name']);
		} else {
			$match = FALSE;
			
			for ($i = 0; $i < count($htmlList); $i++) {
				if ($htmlList[$i]['title'] == $tempText) {
					// Appends new URL
					$htmlList[$i]['url'] .= "," . $item['url'];
					
					// Appends generic name if it is unique
					if (strpos($htmlList[$i]['drugs'], $item['generic_name']) === false) {
						$htmlList[$i]['drugs'] .= ", " . $item['generic_name'];
					}
					
					$match = TRUE;
					break;
				}
			}
			
			if ($match == FALSE) {
				$index = count($htmlList);
				$htmlList[$index] = array('title' => $tempText,
										   'url' => $item['url'],
										   'drugs' => $item['generic_name']);
			}
		}
	}
}

// Take newly organized list and create html list for insertion
if (count($htmlList) > 0) {
	$entries = "";
	
	//Creates list for return via AJAX function
	foreach ($htmlList as $index => $item) {
		$entries .= "<li><a id='Comparison-Result-" . $index . "' " .
					"data-url='" . $item['url'] . "' " .
					
					"onclick='chooseComparison(this)'>" .
					"<strong>" . $item['title'] . "</strong><br>" .
					"<em>Examples: " . $item['drugs'] . "</em></a></li>";
	}
	
	$response = "<ul>" . $entries . "</ul>";
} else {
	if ($methodATC === false && $methodPTC === false) {
		$response = "<ul><li><a><strong>" .
					"Please select a classification system above" .
					"</strong></a></li></ul>";
	} else {
		$response = "<ul><li><a><strong>" .
					"No results found" .
					"</strong></a></li></ul>";
	}
}

// Output the response
echo $response;
?>