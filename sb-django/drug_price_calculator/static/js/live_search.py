"""
    <?php

    require_once '../../../../config/db_config.php';

    $response = "";

    //get the q parameter from URL
    $q = $_GET["q"];

    // Only run search if $q is not blank
    if (strlen($q) > 0) {
	    // Adding wildcard markers to query
	    $q = "%" . $q . "%";
	
	    // Establish database connection
	    $db = db_connect('sb', 'abc_vw');
	
	    // Sending prepared statement to server
	    $query = "SELECT DISTINCT t1.url , t1.brand_name, t1.strength, " . 
			     "t1.route, t1.dosage_form, t1.generic_name " . 
			     "FROM abc_price t1 " . 
			     "INNER JOIN abc_price t2 " .
			     "ON t1.generic_name = t2.generic_name " .
			     "WHERE ((t2.generic_name LIKE ? OR t2.brand_name LIKE ?) " . 
			     "AND t1.unit_price IS NOT NULL)";
	
	    $resultArray = returnResults($db, $query, [$q, $q]);
	
	    // If results were obtained, finish processing
	    if (count($resultArray) > 0) {
		    // For each group of generic names + strength + route + 
		    // dosage form, combines the brand names
		    $tempArray = array();
		
		    foreach ($resultArray as $key => $item) {
			    $tempText = $item['generic_name'] . " (" . $item['strength'] . " " . 
						    $item['route'] . " " . $item['dosage_form'] . ")";
						
			    //Cleans up the tempText in case an item was missing
			    $tempText = str_replace("  ", " ", $tempText);
			    $tempText = str_replace("  ", " ", $tempText);
			    $tempText = str_replace("( ", "(", $tempText);
			    $tempText = str_replace(" )", ")", $tempText);
			    $tempText = str_replace(" ()", "", $tempText);
			
			    if ($key == 0) {
				    $tempArray[0] = array('title' => $tempText,
									      'url' => $item['url'],
									      'brand_name' => $item['brand_name']);
			    } else {
				    $match = FALSE;
				
				    for ($i = 0; $i < count($tempArray); $i++) {
					    if ($tempArray[$i]['title'] == $tempText) {
						    $tempArray[$i]['url'] .= "," . $item['url'];
						    $tempArray[$i]['brand_name'] .= ", " . $item['brand_name'];
						    $match = TRUE;
						    break;
					    }
				    }
				
				    if ($match == FALSE) {
					    $index = count($tempArray);
					    $tempArray[$index] = array('title' => $tempText,
											       'url' => $item['url'],
											       'brand_name' => $item['brand_name']);
				    }
			    }
		    }

		    $resultArray = array_values($tempArray);
		    $entries = "";
		
		    //Creates list for return via AJAX function
		    foreach ($resultArray as $index => $item) {
			    $entries .= "<li><a id='Search-Result-" . $index . "' " .
						    "data-url='" . $item['url'] . "' " .
						
						    "onclick='chooseResult(this)'>" .
						    "<strong>" . $item['title'] . "</strong><br>" .
						    "<em>also known as " . $item['brand_name'] . "</em></a></li>";
		    }
		
		    $response = "<ul>" . $entries . "</ul>";
	    } else {
		    $response = "<ul><li><a><strong>No medication found</strong></a></li></ul>";
	    }
    }

    // Output the response
    echo $response;
    ?>
"""