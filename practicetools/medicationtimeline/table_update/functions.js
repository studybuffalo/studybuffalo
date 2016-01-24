function addRow(addButton) {
	var $row = $(addButton).closest("tr");
	var $id = $row.find(".Id").closest("td");
	var $netcareEntry = $row.find(".Netcare-Entry").closest("td");
	var $ingredient = $row.find(".Ingredient").closest("td");
	var $aiCode = $row.find(".AI-Code").closest("td");
	var $strength = $row.find(".Strength").closest("td");
	var $strengthUnit = $row.find(".Strength-Unit").closest("td");
	var $dosageForm = $row.find(".Dosage-Form").closest("td");
	var $route = $row.find(".Route").closest("td");
	
	// Add extra input for each row
	$ingredient.append("<br><input class='Ingredient'>");
	$aiCode.append("<br><input class='AI-Code'>");
	$strength.append("<br><input class='Strength'>");
	$strengthUnit.append("<br><input class='Strength-Unit'>");
	$dosageForm.append("<br><input class='Dosage-Form'>");
	$route.append("<br><input class='Route'>");
}


function ajaxUpload($row, netcareEntry, ingredient, aiCode,
					strength, strengthUnit, dosageForm, route) {
	$.ajax({
		url: "upload_entry.php",
		data: {netcare_entry: netcareEntry,
			   ingredient: ingredient,
			   ai_code: aiCode,
			   strength: strength,
			   strength_unit: strengthUnit,
			   dosage_form: dosageForm,
			   route: route},
		type: "GET",
		success: function (results) {
			$row.remove();
		},
		error: function () {
			// Place holder for now
		}
	});
}


function uploadData() {
	var $tableRows = $("#Entry-Table tbody tr");
	var $row;
	var $netcareEntry;
	var $ingredient;
	var $aiCode;
	var $strength;
	var $strengthUnit;
	var $dosageForm;
	var $route;
	var netcareEntry;
	var ingredient;
	var aiCode;
	var strength;
	var strengthUnit;
	var dosageForm;
	var route;
	
	$tableRows.each(function () {
		$row = $(this);
		route = [];
		netcareEntry = [];
		ingredient = [];
		aiCode = [];
		strength = [];
		strengthUnit = [];
		dosageForm = [];
		route = [];
		
		$netcareEntry = $row.find(".Netcare-Entry");
		$ingredient = $row.find(".Ingredient");
		$ingredient.each(function(index, elem) {
			netcareEntry.push($netcareEntry.text());
			ingredient.push($(elem).val());
		});
		
		$aiCode = $row.find(".AI-Code");
		$aiCode.each(function(index, elem) {
			aiCode.push($(elem).val());
		});
		
		$strength = $row.find(".Strength");
		$strength.each(function(index, elem) {
			strength.push($(elem).val());
		});
		
		$strengthUnit = $row.find(".Strength-Unit");
		$strengthUnit.each(function(index, elem) {
			strengthUnit.push($(elem).val());
		});
		
		$dosageForm = $row.find(".Dosage-Form");
		$dosageForm.each(function(index, elem) {
			dosageForm.push($(elem).val());
		});
		
		$route = $row.find(".Route");
		$route.each(function(index, elem) {
			route.push($(elem).val());
		});
		console.log(ingredient);
		if (ingredient[0] !== "") {
			ajaxUpload($row, netcareEntry, ingredient, aiCode, strength, 
					   strengthUnit, dosageForm, route);
		}
	});
}


 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/
$(document).ready(function() {
	$("#Update").on(
		"click",
		function(){uploadData();});
	
	$(".Add-Button").on(
		"click",
		function(){addRow(this);});
});