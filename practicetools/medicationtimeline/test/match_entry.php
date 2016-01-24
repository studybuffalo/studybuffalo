<?php
/****************************************************************************
 *	generateStringCombo()	Creates an array of strings based on the 		*
 *							provided string									*
 *																			*
 *	$string:	String to be processed into array							*
 *	$type:		Integer representing how to process the string				*
 *					0: Returns array of increasing number of words 			*
 *					   separated by spaces									*
 *					1: Returns array of decreasing number of words			*
 *					   separated by % (wildcard)							*
 ****************************************************************************/
function generateStringCombo($string, $type) {
	$qArray;
	$stringCombos = array();
	$tempText;
	$count;
	$match;
	$prefixList = ['accel', 'ach', 'act', 'ag', 'apo', 'auro', 'ava', 'co',
				   'gd', 'gen', 'ipg', 'jamp', 'mar', 'mint', 'myl', 'mylan',
				   'novo', 'ntp', 'nu', 'odan', 'pendo', 'penta', 'phl', 'pms', 
				   'pro', 'q', 'ran', 'ratio', 'rho', 'rhoxal', 'riva', 
				   'sandoz', 'taro', 'teva', 'van'];
		
	
	if ($type === 0) {
		// Split string into array of words
		$qArray = explode(" ", $string);
		
		// Creates the first entry
		if (count($qArray) > 0) {
			$tempText = $qArray[0];
			array_push($stringCombos, $tempText);
		}
		
		// Builds progressively larger string
		$count = count($qArray);
		for ($i = 1; $i < $count; $i++) {
			$tempText = $tempText . " " . $qArray[$i];
			array_push($stringCombos, $tempText);
		}
	} else if ($type === 1) {
		// Replaces hyphens with spaces to expand search
		$qArray = explode(" ", str_replace("-", " ", $string));
		
		// Creates the first entry
		if (count($qArray) > 1) {
			$tempText = $qArray[0] . "%" . $qArray[1] . "%";
			array_push($stringCombos, $tempText);
		}
		
		// Builds progressively longer string
		for ($i = 2; $i < count($qArray); $i++) {
			$tempText = $tempText . $qArray[$i] . "%";
			array_push($stringCombos, $tempText);
		}
		
		// Creates leading wild card strings for generic company prefixes
		for ($i = 0; $i < count($stringCombos); $i++) {
			foreach ($prefixList as $prefix) {
				$match = '/^' . $prefix . '%/i';
				$stringCombos[$i] = preg_replace($match, '%', $stringCombos[$i]);
			}
		}
		
		// Flips array to allow it to work backwards
		$stringCombos = array_reverse($stringCombos);
	}

	return $stringCombos;
}

/****************************************************************************
 *	generateParams()	Returns string containing a number of "?"			*
 *																			*
 *	$array:	Array used to determine # of ? to generate (# = count of array)	*
 ****************************************************************************/
function generateParams($array) {
	return implode(",", array_fill(0, count($array), "?")); 
}

/****************************************************************************
 *	checkForMatch()		Takes an ingredient array and checks if it the 		*
 *						parent drug is a likely match (by seeing if the 	*
 *						strength and unit appear in the AJAX query			*
 *																			*
 *	$q:					The search string provided by the AJAX query		*
 *	$ingredientArray:	An array containing all the ingredients or a single	*
 *						drug code											*	
 ****************************************************************************/
function checkForMatch($q, $ingredientArray) {
	$match = 0;
	
	foreach($ingredientArray as $ingredient) {
		$tempText = '/((\b|\s)' . $ingredient['strength'] . ' ' . 
					$ingredient['strength_unit'] . '(\b|\s)|(\b|\s)' . 
					$ingredient['strength'] . $ingredient['strength_unit'] . 
					'(\b|\s))/i';
		
		if (preg_match($tempText, $q)) {
			$match++;
		}
	}
	
	return $match;
}

/****************************************************************************
 *	formatStrength()	Strips any trailing zeros from strength field		*
 ****************************************************************************/
function formatStrength($strength) {
	return (float)$strength;
}

/****************************************************************************
 *	sortAICode()	Sorts an ingredient array by ascending AI codes			*
 ****************************************************************************/
function sortAICode($a, $b) {
	return $a['ai_code'] - $b['ai_code'];
}

/****************************************************************************
 *	removeDuplicates()	Cycles through the resultArray and removes any 		*
 *						duplicate entries (based on AI code, strenght, and	*
 *						strenght unit)										*
 ****************************************************************************/
function removeDuplicates($array) {
	$count = count($array);
	$match;
	
	for ($i = 0; $i < $count - 1; $i++) {
		for ($j = $i + 1; $j < $count; $j++) {
			if (isset($array[$i]) && isset($array[$j])) {
				$match = true;
				
				if (count($array[$i]['ingredients']) !==
					count($array[$j]['ingredients'])) {
					$match = false;
				}
				
				for ($k = 0; $k < count($array[$i]['ingredients']); $k++) {
					if (isset($array[$i]['ingredients'][$k]) &&
						isset($array[$j]['ingredients'][$k])) {
						if ($array[$i]['ingredients'][$k]['ai_code'] !== 
							$array[$j]['ingredients'][$k]['ai_code'] ||
							$array[$i]['ingredients'][$k]['strength'] !== 
							$array[$j]['ingredients'][$k]['strength'] ||
							$array[$i]['ingredients'][$k]['strength_unit'] !== 
							$array[$j]['ingredients'][$k]['strength_unit']) {
							$match = false;
						}
					}
				}
				
				if ($match === true) {
					unset($array[$j]);
				}
			}
		}
	}
	
	$array = array_values($array);
	
	return $array;
}




/****************************************************************************
 *	VARIABLE DECLARATIONS													*
 ****************************************************************************/
require_once '../../../../../config/db_config.php';
 
$q = $_GET["q"];
$output;
$stringCombos = array();
$ComboArray;
$resultArray = array();
$drugCodeArray = array();
$maxMatch = 0;
$matches = array();
$count;
$tempText;
$tempArray;
$errorReport;

$errorReport = $q. "\n";


/****************************************************************************
 *	QUICK SEARCH															*/
/****************************************************************************
 *	Runs a query through the netcare_id table looking for a match			*
 *																			*
 *	If match is found, returns a properly formattted output					*
 ****************************************************************************/
// Establish database connection
$db = dbConnect('med_timeline', 'tl_vw');

// Generates the query
$query = "SELECT id " .
		 "FROM netcare_id " .
		 "WHERE netcare_entry = ?";

// Run Query & Retrieve Results
$tempArray = returnResults($db, $query, [$q]);

// Used the extracted ID to reference the drug info
if (count($tempArray) === 1) {
	// Generates the query
	$query = "SELECT ingredient, ai_code, strength, strength_unit, " . 
			 "dosage_form " .
			 "FROM id_reference " .
			 "WHERE id = ?";

	// Run Query & Retrieve Results
	$output = returnResults($db, $query,  [$tempArray[0]['id']]);
}




/****************************************************************************
 *	FIRST INDEPTH SEARCH FOR DRUG CODES										*/
/****************************************************************************
*	Runs a query through the hc_dpd table looking for a match				*
 *	Queries variations of the provided $q looking for an identical match	*
 *																			*
 *	Runs only if a properly formatted output was not generated above		*
 *																			*
 *	Returns an array of drug_codes to used in identifying an exact match of *
 *	the medication data														*
 ****************************************************************************/
if (!isset($output)) {
	$errorReport .= "FIRST INDEPTH SEARCH\n";
	// Establish new database connection
	$db = dbConnect('hc_dpd', 'tl_vw');

	// Generates various string queries
	$stringCombos = generateStringCombo($q, 0);
	
	// Run Query & Retrieve Results
	$params = generateParams($stringCombos);
	$comboArray = array_merge($stringCombos, $stringCombos, $stringCombos);
	$query = "SELECT drug_code " .
			 "FROM drug " .
			 "WHERE brand_name IN ($params) " .
			 "UNION " .
			 "SELECT drug_code " .
			 "FROM drug_ap " .
			 "WHERE brand_name IN ($params) " .
			 "UNION " .
			 "SELECT drug_code " .
			 "FROM drug_ia " .
			 "WHERE brand_name IN ($params)";
	$drugCodeArray = returnResults($db, $query, $comboArray);
}




/****************************************************************************
 *	SECOND INDEPTH SEARCH FOR DRUG CODES									*/
/****************************************************************************
 *	Runs a query through the hc_dpd table looking for a match				*
 *	Queries variations of the provided $q combined with wild cards looking	*
 *	for an identical match													*
 *																			*
 *	Runs only if a properly formatted output was not generated above and 	*
 *	the first indepth search did not turn up results						*
 *																			*
 *	Returns an array of drug_codes to used in identifying an exact match of *
 *	the medication data														*
 ****************************************************************************/
if (!isset($output) && count($drugCodeArray) === 0) {
	$errorReport .= "SECOND INDEPTH SEARCH\n";
	// Establish new database connection
	$db = dbConnect('hc_dpd', 'tl_vw');
	
	// Generates various string queries
	$stringCombos = generateStringCombo($q, 1);
	
	// Run Query & Retrieve Results (cycles through each string query one at a time)
	foreach ($stringCombos as $string) {
		$comboArray = [$string, $string, $string];
		$query = "SELECT drug_code " .
				 "FROM drug " .
				 "WHERE brand_name LIKE (?) " .
				 "UNION " .
				 "SELECT drug_code " .
				 "FROM drug_ap " .
				 "WHERE brand_name LIKE (?) " .
				 "UNION " .
				 "SELECT drug_code " .
				 "FROM drug_ia " .
				 "WHERE brand_name LIKE (?)";
		$drugCodeArray = returnResults($db, $query, $comboArray);
		
		// If match was found, end searching
		if (count($drugCodeArray) > 0) {
			break 1;
		}
	}
}




/****************************************************************************
 *	DRUG CODE SEARCH														*/
/****************************************************************************
 *	Runs a query through the hc_dpd database retrieving the applicable drug	*
 *	information to confirm a proper match									*
 *																			*
 *	Runs only if a drug code was retrieved from the indepth queries			*
 *																			*
 *	Returns an array of drug information to be used in making a match		*
 ****************************************************************************/
// Retrieves associated data for each drug code
if (count($drugCodeArray) > 0) {
	$errorReport .= "DRUG CODE SEARCH\n";
	// Converts drugCodeArray into array of codes for next queries
	$tempArray = array();

	foreach ($drugCodeArray as $code) {
		array_push($tempArray, $code['drug_code']);
	}

	$drugCodeArray = $tempArray;
	
	// Establish new database connection
	$db = dbConnect('hc_dpd', 'tl_vw');
	
	// Run Query & Retrieve Results
	$params = generateParams($drugCodeArray);
	$comboArray = array_merge($drugCodeArray, $drugCodeArray, $drugCodeArray);
	$query = "SELECT t1.drug_code, t1.active_ingredient_code, t1.ingredient, " .
			 "t1.strength, t1.strength_unit, t2.pharmaceutical_form " .
			 "FROM ingred t1 " .
			 "INNER JOIN form t2 " .
			 "ON t1.drug_code = t2.drug_code " .
			 "WHERE t1.drug_code IN ($params) " .
			 "UNION " .
			 "SELECT t1.drug_code, t1.active_ingredient_code, t1.ingredient, " .
			 "t1.strength, t1.strength_unit, t2.pharmaceutical_form " .
			 "FROM ingred_ia t1 " .
			 "INNER JOIN form_ia t2 " .
			 "ON t1.drug_code = t2.drug_code " .
			 "WHERE t1.drug_code IN ($params) " .
			 "UNION " .
			 "SELECT t1.drug_code, t1.active_ingredient_code, t1.ingredient, " .
			 "t1.strength, t1.strength_unit, t2.pharmaceutical_form " .
			 "FROM ingred_ap t1 " .
			 "INNER JOIN form_ap t2 " .
			 "ON t1.drug_code = t2.drug_code " .
			 "WHERE t1.drug_code IN ($params) ";
			 
	$tempArray = returnResults($db, $query, $comboArray);
	
	// Converts results into medication groups based on drug_code
	if (count($tempArray) > 0) {
		$resultArray = array();
		
		// Assemble first entry
		array_push($resultArray, array(
			'drug_code' => $tempArray[0]['drug_code'],
			'ingredients' => array(array(
				'ingredient' => $tempArray[0]['ingredient'],
				'ai_code' => $tempArray[0]['active_ingredient_code'],
				'strength' => formatStrength($tempArray[0]['strength']),
				'strength_unit' => $tempArray[0]['strength_unit'],
				'dosage_form' => $tempArray[0]['pharmaceutical_form'])),
			'match' => 0));
		
		for ($i = 1; $i < count($tempArray); $i++) {
			$match = false;
			
			for ($j = 0; $j < count($resultArray); $j++) {
				if ($tempArray[$i]['drug_code'] === $resultArray[$j]['drug_code']) {
					array_push($resultArray[$j]['ingredients'], array(
						'ingredient' => $tempArray[$i]['ingredient'],
						'ai_code' => $tempArray[$i]['active_ingredient_code'],
						'strength' => formatStrength($tempArray[$i]['strength']),
						'strength_unit' => $tempArray[$i]['strength_unit'],
						'dosage_form' => $tempArray[$i]['pharmaceutical_form']));
						
					$match = true;
				}
			}
			
			if ($match === false) {
				array_push($resultArray, array(
					'drug_code' => $tempArray[$i]['drug_code'],
					'ingredients' => array(array(
						'ingredient' => $tempArray[$i]['ingredient'],
						'ai_code' => $tempArray[$i]['active_ingredient_code'],
						'strength' => formatStrength($tempArray[$i]['strength']),
						'strength_unit' => $tempArray[$i]['strength_unit'],
						'dosage_form' => $tempArray[$i]['pharmaceutical_form'])),
					'match' => 0));
			}
		}
	}
	
	// Sorts the ingredient array by generic_name
	for ($i = 0; $i < count($resultArray); $i++) {
		usort($resultArray[$i]['ingredients'], "sortAICode");
	}
	
	// Removes entries with duplicate ingredients
	$resultArray = removeDuplicates($resultArray);
	
}




/****************************************************************************
 *	FINDING DRUG MATCH														*/
/****************************************************************************
 *	Uses the result array returned above to see if there is a good match	*
 *	A good match means that all the strengths for a drug code match the $q	*
 *	provided and only one such entry meets this requirement					*
 *																			*
 *	Runs only if $resultArray has at least one entry						*
 *																			*
 * 	If a match is found, returns an array of matches						*
 ****************************************************************************/
if (count($resultArray) > 0) {
	$errorReport .= "FINDING DRUG MATCH\n";
	
	// Cycles through all the resultArray entries and determine match status
	for ($i = 0; $i < count($resultArray); $i++) {
		$match = checkForMatch($q, $resultArray[$i]['ingredients']);
		$resultArray[$i]['match'] = $match;
		$maxMatch = $match > $maxMatch ? $match : $maxMatch;
	}
	
	// Determines if there is a single best match
	for ($i = 0; $i < count($resultArray); $i++) {
		if ($resultArray[$i]['match'] === $maxMatch) {
			array_push($matches, $i);
		}
	}
}




/****************************************************************************
 *	MANAGING SEARCH SUCCESS													*/
/****************************************************************************
 *	If a match is returned above, format the output and upload the data to	*
 *	the appropriate tables. Will search for a match in the id_reference 	*
 *	table first to see if a new entry is needed or if it already exists.	*
 *																			*
 *	Runs only if $matches has one entry (a best entry is found)				*
 *																			*
 * 	If a match is found, returns a formatted output							*
 ****************************************************************************/
if (count($matches) === 1) {
	$errorReport .= "MANAGING SEARCH SUCCESS";
	$output = $resultArray[$matches[0]]['ingredients'];
	
	// Establish new database connection
	$db = dbConnect('med_timeline', 'tl_ent');
	
	// Determines if an entry already exists in id_reference
	$idArray = array();
	$tempArray = array();
	
	foreach ($output as $ingredient) {
		$ingredient['ingredient'] = preg_replace('/ \(.*\)/', '', $ingredient['ingredient']);
		array_push($tempArray, $ingredient['ingredient'], 
				   $ingredient['strength'], $ingredient['dosage_form']);
	}
	
	$query = "SELECT DISTINCT id " . 
			 "FROM id_reference " .
			 "WHERE id_reference.id In " . 
			 "(SELECT id from id_reference where ingredient = ? and " . 
			 "strength = ? and dosage_form = ?)";
			 
	for ($i = 1; $i < (count($tempArray)/3); $i++) {
		$query .= "And id_reference.id In " .
				  "(SELECT id from id_reference where ingredient = ? and " .
				  "strength = ? and dosage_form = ?)";
	}
	
	$statement = $db->prepare($query);
	$statement->execute($tempArray);
	
	$idArray = returnResults($db, $query, $tempArray);
	
	// If an entry exists, use the retrieved ID as the reference
	if (count($idArray) > 0) {
		$id = $idArray[0]['id'];
		
		$query = "INSERT INTO netcare_id (netcare_entry, id)" . 
				 "VALUES (?, ?)";
		
		$statement = $db->prepare($query);
		$statement->execute([$q, $id]);
	// Otherwise, create a new entry
	} else {
		// Insert the netcare_entry in the netcare_id
		$query = "INSERT INTO netcare_id (netcare_entry)" . 
				 "VALUES (?)";
		
		$statement = $db->prepare($query);
		$statement->execute([$q]);
		
		// Add the id to the netcare_id table
		$id = $db->lastInsertId();
		
		$query = "UPDATE netcare_id " . 
				 "SET id = ? " .
				 "WHERE ai_id = ?";
		
		$statement = $db->prepare($query);
		$statement->execute([$id, $id]);

		// Upload the medication data with the retrieved ID
		$tempArray = array();
		
		foreach ($output as $item) {
			$item['ingredient'] = preg_replace('/ \(.*\)/', '', $item['ingredient']);
			array_push($tempArray, array($id, 
					   $item['ingredient'], $item['ai_code'], 
					   $item['strength'], $item['strength_unit'], 
					   $item['dosage_form']));
		}
		
		foreach($tempArray as $item) {
			$query = "INSERT INTO id_reference (id, ingredient, ai_code, " . 
					 "strength, strength_unit, dosage_form)" . 
					 "VALUES (?, ?, ?, ?, ?, ?)";
			
			$statement = $db->prepare($query);
			$statement->execute($item);
		}
	}
}





/****************************************************************************
 *	MANAGING SEARCH FAILURES												*/
/****************************************************************************
 *	Takes any failed attempts at finding a match and uploads the 			*
 *	information to the netcare_review for addition to netcare_id			*
 *	Runs only if no output has been generated by this point					*
 ****************************************************************************/
if (!isset($output)) {
	// Establish new database connection
	$db = dbConnect('med_timeline', 'tl_ent');
	
	// Run Query & Retrieve Results
	$tempArray = [$q];
	$query = "INSERT INTO netcare_review (netcare_entry) " . 
			 "VALUES (?)";
	$statement = $db->prepare($query);
	
	try {
		$statement->execute($tempArray);
	} catch (Exception $e) {
		// Catch errors in case entry already exists
		error_log("Attempt to enter duplicate entry: " . $q);
	}
	
	$output = new stdClass();
	$output -> ingredient = $q;
	$output -> ai_code = "";
	$output -> strength = "";
	$output -> strength_unit = "";
	$output -> dosage_form = "";
	$output = array($output);
}

error_log($errorReport);

echo json_encode($output);
?>