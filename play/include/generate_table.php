<?php
	$folderInt = 1;
	$folderExists = true;
	$folderNum = "0001";
	$folderDir = "0001/details.php";
	
	/* 
		Loops through each folder in the directory and includes
		the details.php file to generate the directory table
	*/
	while ($folderExists === true) {
		include $folderDir;
		
		echo '<tr><td><a href="' . $folderNum . '">' . $date . '</a></td>';
		echo '<td><a href="' . $folderNum . '">' . $title . '</a></td>';
		echo '<td><a href="' . $folderNum . '">' . $category . '</a></td></tr>';
		
		// Generates the next file name; ends loop if it doesn't exists
		$folderInt++;
		$folderNum = str_pad($folderInt, 4, "0", STR_PAD_LEFT);
		$folderDir = $folderNum . "/details.php";
		$folderExists = file_exists($folderDir);
	}