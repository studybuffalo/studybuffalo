<?php

require_once '../../../../config/db_config.php';

$resultArray = array();
$urlArray = array();
$outputList = array();
$q = explode(",", $_GET["q"]);

// Establish database connection
$db = dbConnect('abc_dbl', 'abc_vw');

// Sending prepared statement to server
$params = implode(",", array_fill(0, count($q), "?"));
$query = "SELECT DISTINCT t1.url, t1.strength, t1.generic_name, " .
		 "t1.unit_price, t1.lca, t2.coverage, t2.criteria_sa, " .
		 "t2.criteria_p, t2.group_1, t2.group_66, t2.group_66a, " .
		 "t2.group_19823, t2.group_19823a, t2.group_19824, " .
		 "t2.group_20400, t2.group_20403, t2.group_20514, " .
		 "t2.group_22128, t2.group_23609 " .
		 "FROM price t1 " .
		 "JOIN coverage t2 " .
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
		 "FROM special_authorization " .
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

/*
	Group each drug by generic name
	Create drop downs for each available strength
	Each strength linked to the LCA
*/

// Format results into an array for html processing
if (count($resultArray) > 0) {
	foreach ($resultArray as $key => $item) {
		// Groups each entry by generic name and strength
		if ($key == 0) {
			$outputArray[0] = array('generic_name' => $item['generic_name'],
									'strength' => array());
			$outputArray[0]['strength'][0]['strength'] = $item['strength'];
			$outputArray[0]['strength'][0]['unit_price'] = $item['unit_price'];
			$outputArray[0]['strength'][0]['lca'] = $item['lca'];
			$outputArray[0]['strength'][0]['coverage'] = $item['coverage'];
			$outputArray[0]['strength'][0]['criteria_sa'] = $item['criteria_sa'];
			$outputArray[0]['strength'][0]['criteria_p'] = $item['criteria_p'];
			$outputArray[0]['strength'][0]['group_1'] = $item['group_1'];
			$outputArray[0]['strength'][0]['group_66'] = $item['group_66'];
			$outputArray[0]['strength'][0]['group_66a'] = $item['group_66a'];
			$outputArray[0]['strength'][0]['group_19823'] = $item['group_19823'];
			$outputArray[0]['strength'][0]['group_19823a'] = $item['group_19823a'];
			$outputArray[0]['strength'][0]['group_19824'] = $item['group_19824'];
			$outputArray[0]['strength'][0]['group_20400'] = $item['group_20400'];
			$outputArray[0]['strength'][0]['group_20403'] = $item['group_20403'];
			$outputArray[0]['strength'][0]['group_20514'] = $item['group_20514'];
			$outputArray[0]['strength'][0]['group_22128'] = $item['group_22128'];
			$outputArray[0]['strength'][0]['group_23609'] = $item['group_23609'];
			$outputArray[0]['strength'][0]['special_auth'] = $item['special_auth'];
		} else {
			$genericMatch = FALSE;
			$strengthMatch = FALSE;

			// Checks for matching generic name
			for ($i = 0; $i < count($outputArray); $i++) {
				if ($outputArray[$i]['generic_name'] == $item['generic_name']) {
					$genericMatch = TRUE;

					// Then checks for matching strength
					for ($j = 0; $j < count($outputArray[$i]['strength']); $j++) {
						if ($outputArray[$i]['strength'][$j]['strength'] == $item['strength']) {
							$strengthMatch = TRUE;

							// If unit price is lower, replaces the array contents
							if ($item['unit_price'] < $outputArray[$i]['strength'][$j]['unit_price']) {
								$outputArray[$i]['strength'][$j]['unit_price'] = $item['unit_price'];
								$outputArray[$i]['strength'][$j]['lca'] = $item['lca'];
								$outputArray[$i]['strength'][$j]['coverage'] = $item['coverage'];
								$outputArray[$i]['strength'][$j]['criteria_sa'] = $item['criteria_sa'];
								$outputArray[$i]['strength'][$j]['criteria_p'] = $item['criteria_p'];
								$outputArray[$i]['strength'][$j]['group_1'] = $item['group_1'];
								$outputArray[$i]['strength'][$j]['group_66'] = $item['group_66'];
								$outputArray[$i]['strength'][$j]['group_66a'] = $item['group_66a'];
								$outputArray[$i]['strength'][$j]['group_19823'] = $item['group_19823'];
								$outputArray[$i]['strength'][$j]['group_19823a'] = $item['group_19823a'];
								$outputArray[$i]['strength'][$j]['group_19824'] = $item['group_19824'];
								$outputArray[$i]['strength'][$j]['group_20400'] = $item['group_20400'];
								$outputArray[$i]['strength'][$j]['group_20403'] = $item['group_20403'];
								$outputArray[$i]['strength'][$j]['group_20514'] = $item['group_20514'];
								$outputArray[$i]['strength'][$j]['group_22128'] = $item['group_22128'];
								$outputArray[$i]['strength'][$j]['group_23609'] = $item['group_23609'];
								$outputArray[$i]['strength'][$j]['special_auth'] = $item['special_auth'];
							}

							break;
						}
					}

					// If no strength match was found, adds it to this generic entry
					if ($strengthMatch === FALSE) {
						$index = count($outputArray[$i]['strength']);
						$outputArray[$i]['strength'][$index] = array(
								'strength' => $item['strength'],
								'unit_price' => $item['unit_price'],
								'lca' => $item['lca'],
								'coverage' => $item['coverage'],
								'criteria_sa' => $item['criteria_sa'],
								'criteria_p' => $item['criteria_p'],
								'group_1' => $item['group_1'],
								'group_66' => $item['group_66'],
								'group_66a' => $item['group_66a'],
								'group_19823' => $item['group_19823'],
								'group_19823a' => $item['group_19823a'],
								'group_19824' => $item['group_19824'],
								'group_20400' => $item['group_20400'],
								'group_20403' => $item['group_20403'],
								'group_20514' => $item['group_20514'],
								'group_22128' => $item['group_22128'],
								'group_23609' => $item['group_23609'],
								'special_auth' => $item['special_auth']);
					}

					break;
				}
			}

			// If no generic match was found, adds it to the array
			if ($genericMatch == FALSE) {
				$index = count($outputArray);
				$outputArray[$index] = array('generic_name' => $item['generic_name'],
											 'strength' => array());
				$outputArray[$index]['strength'][0]['strength'] = $item['strength'];
				$outputArray[$index]['strength'][0]['unit_price'] = $item['unit_price'];
				$outputArray[$index]['strength'][0]['lca'] = $item['lca'];
				$outputArray[$index]['strength'][0]['coverage'] = $item['coverage'];
				$outputArray[$index]['strength'][0]['criteria_sa'] = $item['criteria_sa'];
				$outputArray[$index]['strength'][0]['criteria_p'] = $item['criteria_p'];
				$outputArray[$index]['strength'][0]['group_1'] = $item['group_1'];
				$outputArray[$index]['strength'][0]['group_66'] = $item['group_66'];
				$outputArray[$index]['strength'][0]['group_66a'] = $item['group_66a'];
				$outputArray[$index]['strength'][0]['group_19823'] = $item['group_19823'];
				$outputArray[$index]['strength'][0]['group_19823a'] = $item['group_19823a'];
				$outputArray[$index]['strength'][0]['group_19824'] = $item['group_19824'];
				$outputArray[$index]['strength'][0]['group_20400'] = $item['group_20400'];
				$outputArray[$index]['strength'][0]['group_20403'] = $item['group_20403'];
				$outputArray[$index]['strength'][0]['group_20514'] = $item['group_20514'];
				$outputArray[$index]['strength'][0]['group_22128'] = $item['group_22128'];
				$outputArray[$index]['strength'][0]['group_23609'] = $item['group_23609'];
				$outputArray[$index]['strength'][0]['special_auth'] = $item['special_auth'];
			}
		}
	}
}

// Sorts the strength items from lowest to highest
if (count($outputArray) > 0) {
	function sortFunction($a, $b) {
		$pattern = '/([\d|\.]+\b)/';

		if (preg_match($pattern, $a['strength'], $matches)) {
			$a = $matches[1];
		} else {
			$a = $a['strength'];
		}

		if (preg_match($pattern, $b['strength'], $matches)) {
			$b = $matches[1];
		} else {
			$b = $b['strength'];
		}

		if ($a == $b) {
			return 0;
		} else if ($a < $b) {
			return -1;
		} else {
			return 1;
		}
	}

	for ($i = 0; $i < count($outputArray); $i++) {
		usort($outputArray[$i]['strength'], 'sortFunction');
	}
}

echo json_encode($outputArray);
?>