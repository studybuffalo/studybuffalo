<?php
//get the q parameter from URL
$q = str_replace("_", " ", $_GET["q"]);

//Establish database connection
$conn = mysqli_connect('localhost','studybuf_dblview','iDBL1403#sb','studybuf_abc_dbl');
if (!$conn)
{
    die('Could not connect: ' . mysqli_error($con));
}

$sql="SELECT `ID`, `DIN`, `BrandName`, `Strength`, `DosageForm`, `GenericName`, " .
"`Manufacturer`, `UnitPrice`, `Interchangeable`, `LCA`, `LCAText`, `UnitIssue`, " .
"`Coverage`, `CoverageCriteria`, `CoverageCriteriaSA`, `CoverageCriteriaP`, `SpecialAuth`, " .
"`SpecialAuthLink`, `Clients1`, `Clients66`, `Clients66A`, `Clients19823`, `Clients19823A`, " .
"`Clients19824`, `Clients20400`, `Clients20403`, `Clients20514`, `Clients22128`, `Clients23609`" .
"FROM `dbl` WHERE GenericName = '" . $q . "'";

$result = mysqli_query($conn, $sql);

//Takes database entries and converts them to a JSON array
$ResultsArray = Array();

while($row = mysqli_fetch_array($result))
{
	$TempArray = array(
		#"ID"=>$row['ID'],
		#"DIN"=>$row['DIN'],
		"BrandName"=>$row['BrandName'],
		"Strength"=>$row['Strength'],
		"DosageForm"=>$row['DosageForm'],
		"GenericName"=>$row['GenericName'],
		"Manufacturer"=>$row['Manufacturer'],
		"UnitPrice"=>$row['UnitPrice'],
		#"Interchangeable"=>$row['Interchangeable'],
		"LCA"=>$row['LCA'],
		"LCAText"=>$row['LCAText'],
		"UnitIssue"=>$row['UnitIssue'],
		"Coverage"=>$row['Coverage'],
		"CoverageCriteria"=>$row['CoverageCriteria'],
		"CoverageCriteriaSA"=>$row['CoverageCriteriaSA'],
		"CoverageCriteriaP"=>$row['CoverageCriteriaP'],
		"SpecialAuth"=>$row['SpecialAuth'],
		"SpecialAuthLink"=>$row['SpecialAuthLink'],
		"Clients1"=>$row['Clients1'],
		"Clients66"=>$row['Clients66'],
		"Clients66A"=>$row['Clients66A'],
		"Clients19823"=>$row['Clients19823'],
		"Clients19823A"=>$row['Clients19823A'],
		"Clients19824"=>$row['Clients19824'],
		"Clients20400"=>$row['Clients20400'],
		"Clients20403"=>$row['Clients20403'],
		"Clients20514"=>$row['Clients20514'],
		"Clients22128"=>$row['Clients22128'],
		"Clients23609"=>$row['Clients23609']
	);
	
	array_push($ResultsArray, $TempArray);
}

#passes JSON array to JavaScript function
echo json_encode($ResultsArray)
?>