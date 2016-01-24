<?php
/****************************************************************************
 *	VARIABLE DECLARATIONS													*
 ****************************************************************************/
require_once '../../../../../config/db_config.php';

$tableData = "";
 
/****************************************************************************
 *	DATA EXTRACTION															*
 ****************************************************************************/
 
// Establish database connection
$db = dbConnect('med_timeline', 'tl_vw');

// Generates the query
$query = "SELECT id, netcare_entry " .
		 "FROM netcare_review ";

// Run Query & Retrieve Results
$statement = $db->prepare($query);
$statement->execute();

while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
	$tableData .= "<tr>" .
				  "<td><span class='Id'>" . $temp['id'] . "</span></td>" .
				  "<td><span class='Netcare-Entry'>" . $temp['netcare_entry'] . "</span></td>" .
				  "<td><input type='text' class='Ingredient'></td>" .
				  "<td><input type='text' class='AI-Code'></td>" .
				  "<td><input type='text' class='Strength'></td>" .
				  "<td><input type='text' class='Strength-Unit'></td>" .
				  "<td><input type='text' class='Dosage-Form'></td>" .
				  "<td><input type='text' class='Route'></td>" .
				  "<td><input type='button' class='Add-Button' value='Add Row'></td>" .
				  "</tr>";
}

echo $tableData;
?>