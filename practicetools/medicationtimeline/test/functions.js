/****************************************************************************
 *	loadingBar() 		Returns html code to generate the loading bar 		*
 ****************************************************************************/
function loadingBar() {
	var output = '<div id="warningGradientOuterBarG">' +
				 '<div id="warningGradientFrontBarG"' +
				 'class="warningGradientAnimationG">' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '<div class="warningGradientBarLineG"></div>' +
				 '</div></div>';
	return output;
}

function dateToString(date) {
	var year = date.getFullYear();
	var month = date.getMonth() < 9 ? 
				"0" + (date.getMonth() + 1) : date.getMonth() + 1;
	var day = date.getDate() < 10 ? 
			  "0" + date.getDate() : date.getDate();
	
	return year + "-" + month + "-" + day;
}


function stringToDate(date) {
	var year;
	var month;
	var day;
	var output;
	
	date = date.split("-");
	
	// Set year
	year = parseInt(date[0]);
	
	// Set month
	month = parseInt(date[1] - 1);
	
	// Set day
	day = parseInt(date[2]);
	
	// Assemble Date
	output = new Date(year, month, day);
	
	return output;
}


function processDate(date) {
	var year;
	var month;
	var day;
	var output;
	
	date = date.split("-");
	
	// Set year
	year = parseInt(date[0]);
	
	// Set month
	if (date[1].toUpperCase() === "JAN") {month = 0;}
	else if (date[1].toUpperCase() === "FEB") {month = 1;}
	else if (date[1].toUpperCase() === "MAR") {month = 2;}
	else if (date[1].toUpperCase() === "APR") {month = 3;}
	else if (date[1].toUpperCase() === "MAY") {month = 4;}
	else if (date[1].toUpperCase() === "JUN") {month = 5;}
	else if (date[1].toUpperCase() === "JUL") {month = 6;}
	else if (date[1].toUpperCase() === "AUG") {month = 7;}
	else if (date[1].toUpperCase() === "SEP") {month = 8;}
	else if (date[1].toUpperCase() === "OCT") {month = 9;}
	else if (date[1].toUpperCase() === "NOV") {month = 10;}
	else if (date[1].toUpperCase() === "DEC") {month = 11;}
	
	// Set day
	day = parseInt(date[2]);
	
	// Assemble Date
	output = new Date(year, month, day);
	
	return output;
}


function addDays(date, days) {
	var result = new Date(date);
	
	result.setDate(result.getDate() + days);
	
	return result;
}


function subDays(date, days) {
	var result = new Date(date);
	
	result.setDate(result.getDate() - days);
	
	return result;
}


function differenceDays(endDate, startDate) {
	var msToDay = 1000 * 60 * 60 * 24;
	var difference = Math.round((endDate - startDate) / msToDay);
	
	return difference;
}


function sortDates(a, b) {
	return a.date - b.date;
}


function assessAdherence(oldStart, oldDuration, oldStop, newStart, newDuration, newStop) {
	var averageDuration = (oldDuration + newDuration) / 2;
	var lowerLimit;
	var upperLimit;
	var output;
	var x;
	var start;
	var stop;
	var duration;
	
	if (averageDuration > 30) {
		x = Math.ceil(averageDuration * 0.25);
	} else if (averageDuration > 15) {
		x = Math.ceil(averageDuration * 0.5);
	} else if (averageDuration > 7) {
		x = Math.ceil(averageDuration * 0.75);
	} else if (averageDuration > 0) {
		x = 3;
	}
	
	x = x > 40 ? 40 : x;
	
	lowerLimit = subDays(oldStart, x);
	upperLimit = addDays(oldStop, x);
	
	if ((newStart >= lowerLimit && newStart <= upperLimit) ||
		(newStop >= lowerLimit && newStop <= upperLimit)) {
		start = newStart < oldStart ? newStart : oldStart;
		stop = newStop > oldStop ? newStop : oldStop;
		duration = differenceDays(stop, start);
		
		output = {check: true,
				  start: dateToString(start),
				  stop: dateToString(stop),
				  duration: duration
				 }
	} else {
		output = {check: false};
	}
	
	return output;
}


function extractDispenseData(line1, line2, line3) {
	var startDate;
	var medication;
	var quantity;
	var duration;
	var instructions;
	var tempRegex;
	var tempMatch;
	var output;
	
	// Extract the date
	tempRegex = /\t\s\s(\d{4}-\w{3}-\d{2})/
	tempMatch = line1.match(tempRegex);
	startDate = tempMatch ? processDate(tempMatch[1]) : null;
	
	// Extract the medication
	tempRegex = /\d{4}-\w{3}-\d{2}\s{4}(.*) \t/
	tempMatch = line1.match(tempRegex);
	medication = tempMatch ? tempMatch[1] : null;
	
	// Extract the quantity
	tempRegex = /^(\d+)\s{2,}/
	tempMatch = line2.match(tempRegex);
	quantity = tempMatch ? parseInt(tempMatch[1]) : null;
	
	// Extract the duration
	tempRegex = /   (\d+)  /;
	tempMatch = line2.match(tempRegex);
	duration = tempMatch ? parseInt(tempMatch[1]) : null;
	
	// Extract the sig
	// If there is leading white space, there is no sig
	tempRegex = /^\s{2,}/
	tempMatch = line3.match(tempRegex);
	
	if (!tempMatch) {
		instructions = line3;
	}
	
	output = {netcare: medication,
			  dispenses: [{
					date: startDate,
					quantity: quantity,
					duration: duration,
					sig: instructions}]
	}
	
	return output;
}


function parseProfile(profile) {
	var searchIndex;
	var profileArray;
	var keepEntry;
	var tempArray = [];
	var tempRegex;
	var medicationList = [];
	var match = false;
	
	//	Searches for "PRESCRIPTION LIST" and removes it
	searchIndex = profile.search("PRESCRIPTION LIST");
	
	if (searchIndex > -1) {
		profile = profile.slice(searchIndex);
	}
	
	//	Searches for "- End of Report -" and removes it
	searchIndex = profile.search("- End of Report -");
	
	if (searchIndex > -1) {
		profile = profile.slice(0, searchIndex);
	}
	
	//Divides list into individual lines
	profileArray = profile.split("\n");
	
	//	Removes all entries except for the dispensing information
	//	Removes blank entries and phone numbers
	
	for (var i = 0; i < profileArray.length; i++) {
		keepEntry = true;
		
		//Removes empty array entries
		if (profileArray[i].match(/\w/) === null) {
			keepEntry = false;
		}
		
		//Removes entries containing only phone numbers
		tempRegex = /^\s*\(\d+\)\s\d+-\d+/;
		if (profileArray[i].match(tempRegex) !== null) {
			keepEntry = false;
		}
		
		tempRegex = /^\s*\d{7,11}/;
		if (profileArray[i].match(tempRegex) !== null) {
			keepEntry = false;
		}
		
		//If entry can be kept, copy it to new array
		if (keepEntry === true) {
			tempArray.push(profileArray[i]);
		}
		
	}
	
	profileArray = tempArray;
	tempArray = [];
	
	// Extract data out for each dispense
	for (var i = 0; i < profileArray.length; i++) {
		tempRegex = /\t\s\s\d{4}-\w{3}-\d{2}/;
		if (profileArray[i].match(tempRegex) !== null) {
			medicationList.push(extractDispenseData(profileArray[i],
											   profileArray[i + 1],
											   profileArray[i + 2]));
		}
	}
	
	// Combines all similar generic names into a single group
	tempArray = [];
	
	if (medicationList.length > 0) {
		tempArray.push(medicationList[0])
	}
	
	for (var i = 1; i < medicationList.length; i++) {
		match = false;
		
		for (var j = 0; j < tempArray.length; j++) {
			if (medicationList[i].netcare === tempArray[j].netcare) {
				tempArray[j].dispenses.push(medicationList[i].dispenses[0]);
				match = true;
				break;
			}
		}
		
		if (match === false) {
			tempArray.push(medicationList[i]);
		}
	}
	
	medicationList = tempArray;
	
	// Sorts each item by date
	for (var i = 0; i < medicationList.length; i++) {
		medicationList[i].dispenses.sort(sortDates);
	}
	
	return medicationList;
}


function freqObj(sig, number) {
	this.sig = sig;
	this.dpd = number;
}


function extractDose(strength, unit, sig) {
	var output;
	var verbs = [
		"TAKE",
		"GIVE",
		"INHALE",
		"USE"
	];
	var dosageForms = [
		"CAPSULE",
		"CAPSULES",
		"CAPS",
		"TABS",
		"TABLET",
		"TABLETS"
	];
	var frequency = [
		new freqObj("AT DINNER", 1),
		new freqObj("ONCE DAILY", 1)
	];
	var regex;
	var groups;
	var numberOfDoses;
	sig = sig.toUpperCase();
	
	regex = /^TAKE\b\s*(\d+)/;
	groups = sig.match(regex);
	console.log(groups);
	
	if (groups !== null) {
		console.log("Match Length = " + groups[0].length);
		console.log("Group Length = " + groups[1].length);
		numberOfDoses = parseInt(groups[1]);
		console.log(numberOfDoses + " * " + strength + " = " + (numberOfDoses * strength) + " " + unit);
	}
	
	output = sig;
	
	return output;
}


function processResponse(result, entry) {
	var $row;
	var $netcare;
	var $ingredient;
	var $dosageForm;
	var $strength;
	var $sig
	var $date;
	var $duration;
	var $quantity;
	var outputArray = [];
	var $outputDiv = $("#Output-Div");
	var $medDiv;
	var $medIngredient;
	var medIngredient;
	var $dispenseContainer
	var $medDispense;
	var $medDose;
	var medDose;
	var dose;
	var $medStart;
	var medStart;
	var $medDuration;
	var medDuration;
	var $medStop;
	var medStop;
	var stopDate;
	var match = false;
	
	// Converts each ingredient into one-dimensional array
	$.each(result, function(index, resultItem) {
		$.each(entry.dispenses, function(index, entryItem) {
			outputArray.push({
				netcare: entry.netcare,
				ingredient: resultItem.ingredient,
				dosage_form: resultItem.dosage_form,
				strength: resultItem.strength,
				strength_unit: resultItem.strength_unit,
				sig: entryItem.sig,
				date: entryItem.date,
				duration: entryItem.duration,
				quantity: entryItem.quantity
			});
		});
	});
	
	// Creats DOM elements for each array item
	$.each(outputArray, function(itemIndex, item) {
		match = false;
		
		// Checks if there is already a matching medication
		$.each($outputDiv.children(".Medication-Row"), function(rowIndex, row) {
			rowMedication = $(row).find(".Medication input:first").val();
			
			if (rowMedication === item.ingredient + " (" + item.dosage_form + ")") {
				match = true;
				
				$dispenseContainer = $(row).find(".Dispense-Container:first");
				$medDispense = $("<div></div>");
				$medDose = $("<div></div>");
				medDose = document.createElement("input");
				dose;
				$medStart = $("<div></div>");
				medStart = document.createElement("input");
				$medDuration = $("<div></div>");
				medDuration = document.createElement("input");
				$medStop = $("<div></div>");
				medStop = document.createElement("input");
				
				dose = extractDose(item.strength, item.strength_unit, item.sig);
				
				$(medDose).attr("type", "text")
						  .attr("class", "Dose")
						  .val(dose);
				
				$medDose.append($("<div></div>").append(medDose));
				
				$(medStart).attr("type", "date")
						   .attr("class", "Start-Date")
						   .val(dateToString(item.date));
				
				$medStart.append($("<div></div>").append(medStart));
				
				$(medDuration).attr("type", "text")
							  .attr("class", "Duration")
							  .val(item.duration);
				
				$medDuration.append($("<div></div>").append(medDuration));
				
				stopDate = dateToString(addDays(item.date, item.duration));
				
				$(medStop).attr("type", "date")
						  .attr("class", "Stop-Date")
						  .val(stopDate);
				
				$medStop.append($("<div></div>").append(medStop));
				
				$medDispense.attr("class", "Dispenses")
							.append($medDose)
							.append($medStart)
							.append($medDuration)
							.append($medStop)
							.appendTo($dispenseContainer);
				
				$(row).append($dispenseContainer);
				
				return false;
			}
		});
		
		if (match === false) {
			$medDiv = $("<div></div>");
			$medIngredient = $("<div></div>");
			medIngredient = document.createElement("input");
			$dispenseContainer = $("<div></div>");
			$medDispense = $("<div></div>");
			$medDose = $("<div></div>");
			medDose = document.createElement("input");
			dose;
			$medStart = $("<div></div>");
			medStart = document.createElement("input");
			$medDuration = $("<div></div>");
			medDuration = document.createElement("input");
			$medStop = $("<div></div>");
			medStop = document.createElement("input");
			
			$(medIngredient).attr("type", "text")
							.val(item.ingredient + " (" + item.dosage_form + ")");
							
			$medIngredient.attr("class", "Medication")
						  .append(medIngredient);
			
			dose = extractDose(item.strength, item.strength_unit, item.sig);
			
			$(medDose).attr("type", "text")
					  .attr("class", "Dose")
					  .val(dose);
			
			$medDose.append($("<div></div>").append(medDose));
			
			$(medStart).attr("type", "date")
					   .attr("class", "Start-Date")
					   .val(dateToString(item.date));
			
			$medStart.append($("<div></div>").append(medStart));
			
			$(medDuration).attr("type", "text")
						  .attr("class", "Duration")
						  .val(item.duration);
			
			$medDuration.append($("<div></div>").append(medDuration));
			
			stopDate = dateToString(addDays(item.date, item.duration));
			
			$(medStop).attr("type", "date")
					  .attr("class", "Stop-Date")
					  .val(stopDate);
			
			$medStop.append($("<div></div>").append(medStop));
			
			$medDispense.attr("class", "Dispenses")
						.append($medDose)
						.append($medStart)
						.append($medDuration)
						.append($medStop);
			
			$dispenseContainer.attr("class", "Dispense-Container")
							  .append($medDispense);
			
			$medDiv.attr("class", "Medication-Row")
				   .append($medIngredient)
				   .append($dispenseContainer)
				   .appendTo($outputDiv);
		}
	});
}


function sortMeds(a, b) {
	a = stringToDate($(a).find(".Start-Date").val());
	b = stringToDate($(b).find(".Start-Date").val());
	
	return a - b;
}


function sortDispenseDivs() {
	$.each($("#Output-Div .Medication-Row .Dispense-Container"), function(index, row) {
		$dispenses = $(row).find(".Dispenses");
		$dispenses.detach().sort(sortMeds);
		$(row).append($dispenses);
	});
}


/****************************************************************************
 *	organizeMeds() 		Combines overlapping dates for each medication		*
 ****************************************************************************/
function organizeMeds() {
	var dispenses;
	var length;
	var oldStart;
	var oldDuration;
	var oldStop;
	var newStart;
	var newDuration;
	var newStop;
	var oldSig;
	var newSig;
	var continuous = false;
	var match = true;
	
	$.each($("#Output-Div .Medication-Row .Dispense-Container"), function(index, row) {
		match = true;
		
		while (match === true) {
			match = false;
			$dispenses = $(row).find(".Dispenses");
			length = $dispenses.length - 1;
			
			for (var i = 0; i < length; i++) {
				// If sigs are the same can assess for continuity
				oldSig = $dispenses.eq(i).find(".Dose:first").val();
				newSig = $dispenses.eq(i + 1).find(".Dose:first").val();
					
				if (oldSig.toUpperCase() === newSig.toUpperCase()) {
					// If dates are continuous, can combine
					oldStart = $dispenses.eq(i).find(".Start-Date:first").val();
					oldStart = stringToDate(oldStart);
					
					oldStop = $dispenses.eq(i).find(".Stop-Date:first").val();
					oldStop = stringToDate(oldStop);
					
					oldDuration = $dispenses.eq(i).find(".Duration:first").val();
					
					newStart = $dispenses.eq(i + 1).find(".Start-Date:first").val();
					newStart = stringToDate(newStart);
					
					newStop = $dispenses.eq(i + 1).find(".Stop-Date:first").val();
					newStop = stringToDate(newStop);
					
					newDuration = $dispenses.eq(i + 1).find(".Duration:first").val();
				
					continuous = assessAdherence(oldStart, oldDuration, oldStop, 
												 newStart, newDuration, newStop);
				
					if (continuous.check === true) {
						$dispenses.eq(i).find(".Start-Date:first").val(continuous.start);
						$dispenses.eq(i).find(".Duration:first").val(continuous.duration);
						$dispenses.eq(i).find(".Stop-Date:first").val(continuous.stop);
						
						// Removes matched group and resets loop
						match = true;
						$dispenses.eq(i + 1).remove();
						i = length;
					}
				}
			}
		}
	});
}


function matchEntries(entry) {
	// Extract indices for MySQL query
	var query = entry.netcare
	
	$.ajax({
		url: "match_entry.php",
		data: {q: query},
		type: "GET",
		dataType: "json",
		success: function (results) {
			processResponse(results, entry);
		},
		error: function () {
			console.log("Error");
		},
		async: true
	});
	
	return entry.medication
}


function parse() {
	var $input = $("#input");
	var profile = $input.val();
	var match = false;
	var medicationList = [];
	var tempArray = [];
	
	// Extract medication list from profile
	medicationList = parseProfile(profile);
	
	// Display Results
	for (var i = 0; i < medicationList.length; i++) {
		matchEntries(medicationList[i]);
	}
	
	$(document).ajaxStop(function() {
		sortDispenseDivs();
		organizeMeds();
	});
}



 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/
$(document).ready(function() {
	$("#Process").on(
		"click",
		function(){parse();});
});