<?php
//studybuf_abc_vw	bbZMZ*Fl%[1ANQqFM~
//get the q parameter from URL
$q=$_GET["q"];

//Establish database connection
$conn = mysqli_connect('localhost','studybuf_dblview','iDBL1403#sb','studybuf_abc_dbl');
if (!$conn)
{
    die('Could not connect: ' . mysqli_error($con));
}

$sql="SELECT `BrandName`, `GenericName` FROM dbl WHERE (BrandName LIKE '%" . $q . "%' OR GenericName LIKE '%" . $q . "%')";
$result = mysqli_query($conn, $sql);

//
//lookup all links from the xml file if length of q>0
if (strlen($q) > 0)
{
	$entries = "";
	
	$ResultArray = array();
	
	//Create a list out of results
	while($row = mysqli_fetch_array($result))
	{
		$TempArray = array("BrandName"=>$row['BrandName'], "GenericName"=>$row['GenericName']);
		array_push($ResultArray, $TempArray);
	}
	
	//Removes entries from array that are duplicate brand names
	$TempArray1 = array();
	
	foreach ($ResultArray as &$InnerArray)
	{
		if (!isset($TempArray1[$InnerArray['BrandName']]))
		{
			$TempArray1[$InnerArray['BrandName']] = &$InnerArray;
		}
	}
	
	//Converts the final unique array back to original array
	$ResultArray = array_values($TempArray1);
	
	//For each group of generic names, combines the brand names
	$TempArray2 = Array();

	foreach ($ResultArray as $key => $InnerArray)
	{
		if ($key == 0)
		{
			$TempArray2[0] = $InnerArray;
		}
		else
		{
			$match = FALSE;
			for ($i = 0; $i < count($TempArray2); $i++)
			{
				if ($TempArray2[$i]['GenericName'] == $InnerArray['GenericName'])
				{
					$TempArray2[$i]['BrandName'] = $TempArray2[$i]['BrandName'] . ", " . $InnerArray['BrandName'];
					$match = TRUE;
					break;
				}
			}
			
			if ($match == FALSE)
			{
				array_push($TempArray2, $InnerArray);
			}
		}
	}
	
	//Creates list for return via AJAX function
	foreach ($TempArray2 as &$InnerArray)
	{
		$entries .= "<li><a id='" . str_replace(" ", "_", $InnerArray['GenericName']) . "' onclick='ChooseResult(this.id)'><b>" . $InnerArray['GenericName'] . "</b><br><i>also known as " . $InnerArray['BrandName'] . "</a></i>";
	}
}

// Set output to "no suggestion" if no hint was found or to the correct values
if ($entries=="")
{
	$response="<ul><li><a><b>No medication found</b></a></ul>";
}
else
{
	$response = "<ul>" . $entries . "</ul>";
}

//output the response
echo $response;
?>