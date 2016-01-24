<?php
/****************************************************************************
 *	VARIABLE DECLARATIONS													*
 ****************************************************************************/
require_once '../../../../../config/db_config.php';

$id;
$netcareEntry = $_GET["netcare_entry"];
$ingredient = $_GET["ingredient"];
$aiCode = $_GET["ai_code"];
$strength = $_GET["strength"];
$strengthUnit = $_GET["strength_unit"];
$dosageForm = $_GET["dosage_form"];
$route = $_GET["route"];
$parameters;
$tempArray;
$db = dbConnect('med_timeline', 'tl_ent');
$query = "";



/****************************************************************************
 *	UPLOAD DATA TO TABLE													*/
/****************************************************************************
 *	Uploads entry to the netcare_id table									*
 ****************************************************************************/

$parameters = array();
$tempArray = array();

// Determines if an entry already exists in id_reference
for ($i = 0, $count = count($ingredient); $i < $count; $i++) {
	array_push($parameters, $ingredient[$i], $strength[$i]);
}

$query = "SELECT DISTINCT id " . 
		 "FROM id_reference " .
		 "WHERE id_reference.id In " . 
		 "(SELECT id from id_reference where ingredient = ? and strength = ?)";
		 
for ($i = 2; $i < count($tempArray); $i = $i + 2) {
	$query .= "And id_reference.id In " .
			  "(SELECT id from id_reference where ingredient = ? and strength = ?)";
}

$tempArray = returnResults($db, $query, $parameters);

// If an entry exists, use the retrieved ID as the reference
if (count($tempArray) === 1) {
	$id = $tempArray[0]['id'];
	$parameters = array($netcareEntry[0], $id);
	$query = "INSERT INTO netcare_id (netcare_entry, id)" . 
			 "VALUES (?, ?)";
	
	$statement = $db->prepare($query);
	$statement->execute([$netcareEntry[0], $id]);
// Otherwise, create a new entry
} else {
	// Insert the netcare_entry in the netcare_id
	$parameters = array($netcareEntry[0]);
	$query = "INSERT INTO netcare_id (netcare_entry)" . 
			 "VALUES (?)";
	
	$statement = $db->prepare($query);
	$statement->execute($parameters);
	
	// Add the id to the netcare_id table
	$id = $db->lastInsertId();
	$parameters = array($id, $id);
	$query = "UPDATE netcare_id " . 
			 "SET id = ? " .
			 "WHERE ai_id = ?";
	
	$statement = $db->prepare($query);
	$statement->execute($parameters);

	// Upload the medication data with the retrieved ID
	$parameters = array();
	
	for ($i = 0, $count = count($ingredient); $i < $count; $i++) {
		array_push($parameters, array($id, $ingredient[$i], 
				   $aiCode[$i], $strength[$i], $strengthUnit[$i],
				   $dosageForm[$i], $route[$i]));
	}
	
	foreach($parameters as $item) {
		$query = "INSERT INTO id_reference (id, ingredient, ai_code, " . 
				 "strength, strength_unit, dosage_form, route)" . 
				 "VALUES (?, ?, ?, ?, ?, ?, ?)";
		
		$statement = $db->prepare($query);
		$statement->execute($item);
	}
}


/****************************************************************************
 *	REMOVE ENTRY FROM TABLE													*/
/****************************************************************************
 *	Deletes the entry from the netcare_review									*
 ****************************************************************************/
// Generate Query and Execute
$parameters = array($netcareEntry[0]);
$query = "DELETE FROM netcare_review " .
		 "WHERE netcare_entry = ?";
$statement = $db->prepare($query);

try {
	$statement->execute($parameters);
} catch (Exception $e) {
	// Catch errors in case entry already deleted
}
?>