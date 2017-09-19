/****************************************************************************
 *	GENERAL FUNCTIONS FOR PAGE												*
 ****************************************************************************/
 /****************************************************************************
 *	eventSupported()	Takes an event name and tests if it is valid in the *
 *						users browser										*
 *																			*
 *	eventName:	the name of the event to be tested (including "on")			*
 *																			*
 *	Returns true or false													*
 ****************************************************************************/
function eventSupported(eventName) {
	var testEl = document.createElement("input");
	testEl.type = "text";
	var isSupported = (eventName in testEl);
	
	if (!isSupported) {
		testEl.setAttribute(eventName, 'return;');
		isSupported = typeof testEl[eventName] == 'function';
	}
	
	testEl = null;
	
	return isSupported;
}

/****************************************************************************
 *	getElementIndex()	Finds the index of an element in an array of		*
 *						elements.											*
 *																			*
 *	elem:		The element to identify the index for.						*
 *	elemArray:	The array of elements which the elem belongs to.			*
 *																			*
 *	Returns the element index as an integer									*
 ****************************************************************************/
function getElementIndex(elem, elemArray) {
	return $(elemArray).index(elem);
}

/****************************************************************************
 *	calculateFees()	Calculates the how much ABC will pay for a medication	*
 *																			*
 *	mac:		The maximum allowable cost that will be paid by ABC			*
 *	thirdParty:	A string representing the ABC coverage to apply				*
 *																			*
 *	Returns a float value for the amount paid by the third party coverage	*
 ****************************************************************************/
function calculateThirdParty(mac, thirdParty) {
	var patientPays;
	var thirdPartyPays;
	
	if (thirdParty == "1") {
		// http://www.health.alberta.ca/services/drugs-non-group.html
		// 70% coverage; $25.00 max per prescription; no annual maximum
		
		patientPays = mac * 0.30;
		patientPays = patientPays > 25 ? 25.00 : patientPays;
	} else if ((thirdParty == "66") || (thirdParty == "66a")) {
		// http://www.health.alberta.ca/services/drugs-seniors.html
		// 70% thirdParty; $25.00 max per prescription; no annual maximum
		
		patientPays = mac * 0.30;
		patientPays = patientPays > 25 ? 25.00 : patientPays;
	} else if (thirdParty == "20514") {
		// http://www.health.alberta.ca/services/drugs-palliative-care.html
		// 70% thirdParty; $25.00 max per prescription; no annual maximum
		
		patientPays = mac * 0.30;
		patientPays = patientPays > 25 ? 25.00 : patientPays;
	} else if (thirdParty == "19823") {
		// http://humanservices.alberta.ca/financial-support/2085.html
		// 100% thirdParty; no annual maximum
		
		patientPays = 0;
	} else if (thirdParty == "19823a") {
		// http://humanservices.alberta.ca/disability-services/aish.html
		// 100% thirdParty; no annual maximum
		
		patientPays = 0;
	} else if ((thirdParty == "19824") || (thirdParty == "20400") ||
			   (thirdParty == "20401") || (thirdParty == "20401") ||
			   (thirdParty == "20403") || (thirdParty == "22128")) {
		// http://humanservices.alberta.ca/financial-support/2073.html
		// 100% thirdParty; no annual maximum
		
		patientPays = 0;
	} else if (thirdParty == "23609") {
		// http://humanservices.alberta.ca/financial-support/2076.html
		// 100% thirdParty; no annual maximum
		
		patientPays = 0;
	} else {
		patientPays = mac;
	}
	
	thirdPartyPays = Math.round((mac - patientPays) * 100) / 100;
	
	return thirdPartyPays;
}

/****************************************************************************
 *	calculateFees()	Calculates the dispensing price of a medication			*
 *																			*
 *	costPerUnit:	The cost per unit for the medication					*
 *	quantity:		The number of units to be dispensed						*
 *	Returns object of the various fees and prices as float numbers			*
 ****************************************************************************
 *	Fee Calculation															*
 *		Upcharge #1:	3% of the drug cost								*
 *		Upcharge #2:	Percentage of the drug cost + upcharge #1. 			*
 *						Percentage varies based on date as marked (value in *
 *						parenthesis notes Unix Timestamp for this date):	*
 *							5.5% until 2015-04-01 (1427868000000)			*
 *							6.0% until 2016-04-01 (1459490400000)			*
 *							6.5% until 2017-04-01 (1491026400000)			*
 *							7.0% thereafter									*
 *						Upcharge #2 has a total maximum of $100.00			*
 *		Dispensing Fee:	A $12.30 dispensing fee is added on top of the 		*
 *						noted upcharges.									*
 ****************************************************************************/
function calculateFees(costPerUnit, quantity) {
	var today = new Date();
	var drugPrice;
	var upcharge1 = 0.03;
	var upcharge2 = today < 1427868000000 ? 0.055 :
					today < 1459490400000 ? 0.06 :
					today < 1491026400000 ? 0.065 :
					0.07;
	var fee1;
	var fee2;
	var returnPrice = {
		drugCost: 0,
		upcharge1: 0,
		upcharge2: 0,
		dispensingFee: 0,
		grossPrice: 0
	}
	
	// Calculates total gross price
	if (!isNaN(costPerUnit) && costPerUnit > 0 && !isNaN(quantity) && quantity > 0) {
		drugPrice = costPerUnit * quantity;
		fee1 = drugPrice * upcharge1;
		fee2 = (drugPrice + fee1) * upcharge2;
		fee2 = fee2 > 100 ? 100 : fee2;
		grossPrice = drugPrice + fee1 + fee2 + 12.3;
		
		returnPrice.drugCost = Math.round(drugPrice * 100) / 100;
		returnPrice.upcharge1 = Math.round(fee1 * 100) / 100;
		returnPrice.upcharge2 = Math.round(fee2 * 100) / 100;
		returnPrice.dispensingFee = Math.round(12.3 * 100) / 100;
		returnPrice.grossPrice = Math.round(grossPrice * 100) / 100;
	}
	
	return returnPrice
}

/****************************************************************************
 *	calculatePrice()	Calculates the total price of a medication			*
 *																			*
 *	drugPrice:	The cost of the medication (excluding any fees)				*
 *	thirdParty:	String of the third party coverage to apply					*
 *	benefits:	Array of strings of the benefits applicable to this drug	*
 *																			*
 *	Returns object of the various fees and prices as float numbers			*
 ****************************************************************************
 *	Fee Calculation															*
 *		Upcharge #1:	0.03% of the drug cost								*
 *		Upcharge #2:	Percentage of the drug cost + upcharge #1. 			*
 *						Percentage varies based on date as marked (value in *
 *						parenthesis notes Unix Timestamp for this date):	*
 *							5.5% until 2015-04-01 (1427868000000)			*
 *							6.0% until 2016-04-01 (1459490400000)			*
 *							6.5% until 2017-04-01 (1491026400000)			*
 *							7.0% thereafter									*
 *						Upcharge #2 has a total maximum of $100.00			*
 *		Dispensing Fee:	A $12.30 dispensing fee is added on top of the 		*
 *						noted upcharges.									*
 ****************************************************************************/
function calculatePrice(costPerUnit, quantity, mac, thirdParty, benefits) {
	var coverageMatch = false;
	var fees;
	var thirdPartyPays;
	var netPrice;
	var benefitResult;
	var returnPrice = {
		drugCost: 0,
		upcharge1: 0,
		upcharge2: 0,
		dispensingFee: 0,
		grossPrice: 0,
		thirdParty: 0,
		netPrice: 0,
		benefit: "N/A"
	}
	var tempPrice;
	
	// Calculate total drug price
	tempPrice = calculateFees(costPerUnit, quantity);
	returnPrice.drugCost = tempPrice.drugCost;
	returnPrice.upcharge1 = tempPrice.upcharge1;
	returnPrice.upcharge2 = tempPrice.upcharge2;
	returnPrice.dispensingFee = tempPrice.dispensingFee;
	returnPrice.grossPrice = tempPrice.grossPrice;
	
	// Calculates the third party pays amount
	if (thirdParty) {
		// Compares third party coverage against benefits to see if match
		for (var i = 0; i < benefits.length; i++) {
			if (thirdParty === benefits[i]) {coverageMatch = true;}
		}
		
		// Calculates the MAC
		fees = calculateFees(mac, quantity);
		
		// Calculates net price based on coverage information
		if (coverageMatch === false) {
			thirdPartyPays = 0;
		} else {
			thirdPartyPays = calculateThirdParty(fees.grossPrice, thirdParty);
			returnPrice.thirdParty = thirdPartyPays;
		}
	} else {
		thirdPartyPays = 0;
	}
	
	// Determines if drug is a benefit or not
	if (thirdParty === "") {
		benefitResult = "N/A";
	} else if (coverageMatch === false) {
		benefitResult = "No";
	} else {
		benefitResult = "Yes";
	}
	
	returnPrice.benefit = benefitResult;
	
	// Calculates the net price
	netPrice = returnPrice.grossPrice - thirdPartyPays;
	returnPrice.netPrice = Math.round(netPrice * 100) / 100;
	
	return returnPrice;
}

/****************************************************************************
 *	getTodaysDate()		Returns todays date in YYYY-MM-DD format			*
 ****************************************************************************/
function getTodaysDate() {
	var today = new Date();
	var day = today.getDate();
	var month = today.getMonth() + 1;
	var year = today.getFullYear();
	
	day = day < 10 ? "0" + day : day;
	month = month < 10 ? "0" + month : month;
	
	return year + "-" + month + "-" + day;
}

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




/****************************************************************************
 *	FUNCTIONS GENERAL TO TABLES												*
 ****************************************************************************/
 /****************************************************************************
 *	changePriceTable()	Updates column display properites depending on the 	*
 *						calcultaion method selected							*
 ****************************************************************************/
function changePriceTableCols(table) {
	var index = $("#" + table + "-Method")[0].selectedIndex;
	var $table = $("#" + table);
	
	if (index === 0) {
		$table.attr("class", "methodDay");
	} else if (index === 1) {
		$table.attr("class", "methodQuantity");
	}
}

/****************************************************************************
 *	processDosesPerDay()	Converts doses per day fraction inputs to a		*
 *							number											*
 *																			*
 *	value:	The dosesPerDay input value to be converted						*
 ****************************************************************************/
function processDosesPerDay(value) {
	var output;
	var match;
	var tempNums;
	
	if (isNaN(value)) {
		match = value.match(/^\d+\/\d+$/);
		
		if (match) {
			tempNums = value.split("/");
			output = Number(tempNums[0]) / Number(tempNums[1]);
		}
	} else {
		output = value;
	}
	
	return output;
}

/****************************************************************************
 *	priceUpdateDay()	Updates the price for a "day supply" price span		*
 *																			*
 *	input:		the input that changed										*
 *	elemIndex:	the index of the trigger input (optional)					*
 *	cost:		the cost per unit for the applicable medication (optional)	*
 ****************************************************************************/
function priceUpdateDay(input) {
	var table = $(input).closest("table").attr("id");
	var $row = $(input).closest("tr");
	var inputArray = $row.find("." + $(input).attr("class"));
	var index = getElementIndex(input, inputArray);
	var $priceSpan = $row.find(".dayPrice").eq(index);
	var $infoButton = $row.find(".info");
	var $thirdParty = $("#" + table + "-Third-Party");
	var $dataSelect;
	
	var cost = Number($row.find(".cost").attr("data-cost")) ||
			   Number($row.find(".cost").val());
	var mac;
	var dosesPerDay = $row.find(".dosesPerDay").eq(index).val();
	var daySupply = Number($row.find(".daySupply").eq(index).val());
	var quantity;
	var thirdParty = $thirdParty.children("option:selected").val();
	var benefits = [];
	var price;
	
	// Determines the proper dataSelect
	if (table === "Price-Table") {
		$dataSelect = $row.find(".brandName").first().children("option:selected");
	} else if (table === "Comparison-Table") {
		$dataSelect = $row.find(".strength").first().children("option:selected");
	}
	
	// Calculate the total number of doses
	quantity = processDosesPerDay(dosesPerDay) * daySupply;
	
	// Extract the MAC
	mac = $dataSelect.attr("data-mac");
	
	// Assemble list of benefits for this medication;
	if ($dataSelect.attr("data-group-1") == "1") {benefits.push("1");}
	if ($dataSelect.attr("data-group-66") === "1") {benefits.push("66");}
	if ($dataSelect.attr("data-group-66a") === "1") {benefits.push("66a");}
	if ($dataSelect.attr("data-group-19823") === "1") {benefits.push("19823");}
	if ($dataSelect.attr("data-group-19823a") === "1") {benefits.push("19823a");}
	if ($dataSelect.attr("data-group-19824") === "1") {benefits.push("19824");}
	if ($dataSelect.attr("data-group-20400") === "1") {benefits.push("20400");}
	if ($dataSelect.attr("data-group-20403") === "1") {benefits.push("20403");}
	if ($dataSelect.attr("data-group-20514") === "1") {benefits.push("20514");}
	if ($dataSelect.attr("data-group-22128") === "1") {benefits.push("22128");}
	if ($dataSelect.attr("data-group-23609") === "1") {benefits.push("23609");}
	
	// Uses the determined index to calculate the price and update the span
	price = calculatePrice(cost, quantity, mac, thirdParty, benefits);
	
	$priceSpan.text("$" + price.netPrice.toFixed(2))
			  .attr("data-drug-cost", price.drugCost)
			  .attr("data-upcharge-1", price.upcharge1)
			  .attr("data-upcharge-2", price.upcharge2)
			  .attr("data-dispensing-fee", price.dispensingFee)
			  .attr("data-gross-price", price.grossPrice)
			  .attr("data-third-party", price.thirdParty)
			  .attr("data-net-price", price.netPrice)
			  .attr("data-benefit", price.benefit);
	
	// Updates the total price
	totalUpdate($priceSpan);
	
	// Updates the info button class to notify of special info
	if (price.benefit === "No") {
		$infoButton.attr("class", "info warning");
	} else if ($dataSelect.attr("data-criteria-sa") || $dataSelect.attr("data-criteria-p")
			   || $dataSelect.attr("data-special-auth-title-1")) {
		$infoButton.attr("class", "info notice");
	} else {
		$infoButton.attr("class", "info");
	}
}

/****************************************************************************
 *	priceUpdateQuantity()	Updates the price for a "quantity" price span	*
 *																			*
 *	quantityInput:	the input that changed									*
 *	elemIndex:	the index of the trigger input (optional)					*
 *	cost:		the cost per unit for the applicable medication (optional)	*
 ****************************************************************************/
function priceUpdateQuantity(input) {
	var table = $(input).closest("table").attr("id");
	var $row = $(input).closest("tr");
	var inputArray = $row.find("." + $(input).attr("class"));
	var index = getElementIndex(input, inputArray);
	var $priceSpan = $row.find(".quantityPrice").eq(index);
	var $infoButton = $row.find(".info");
	var $dataSelect;
	var $thirdParty = $("#" + table + "-Third-Party");
	var cost = Number($row.find(".cost").attr("data-cost")) ||
			   Number($row.find(".cost").val());
	var mac;
	var quantity = Number($row.find(".quantity").eq(index).val());
	var benefits = [];
	var thirdParty = $thirdParty.children("option:selected").val();
	var price;
	
	// Determines the proper dataSelect
	if (table === "Price-Table") {
		$dataSelect = $row.find(".brandName").first().children("option:selected");
	} else if (table === "Comparison-Table") {
		$dataSelect = $row.find(".strength").first().children("option:selected");
	}
	
	// Extract the MAC
	mac = $dataSelect.attr("data-mac");
	
	// Assemble list of benefits for this medication;
	if ($dataSelect.attr("data-group-1") === "1") {benefits.push("1");}
	if ($dataSelect.attr("data-group-66") === "1") {benefits.push("66");}
	if ($dataSelect.attr("data-group-66a") === "1") {benefits.push("66a");}
	if ($dataSelect.attr("data-group-19823") === "1") {benefits.push("19823");}
	if ($dataSelect.attr("data-group-19823a") === "1") {benefits.push("19823a");}
	if ($dataSelect.attr("data-group-19824") === "1") {benefits.push("19824");}
	if ($dataSelect.attr("data-group-20400") === "1") {benefits.push("20400");}
	if ($dataSelect.attr("data-group-20403") === "1") {benefits.push("20403");}
	if ($dataSelect.attr("data-group-20514") === "1") {benefits.push("20514");}
	if ($dataSelect.attr("data-group-22128") === "1") {benefits.push("22128");}
	if ($dataSelect.attr("data-group-23609") === "1") {benefits.push("23609");}
	
	// Uses the determined index to calculate the price and update the span
	price = calculatePrice(cost, quantity, mac, thirdParty, benefits);
	
	$priceSpan.text("$" + price.netPrice.toFixed(2))
			  .attr("data-drug-cost", price.drugCost)
			  .attr("data-upcharge-1", price.upcharge1)
			  .attr("data-upcharge-2", price.upcharge2)
			  .attr("data-dispensing-fee", price.dispensingFee)
			  .attr("data-gross-price", price.grossPrice)
			  .attr("data-third-party", price.thirdParty)
			  .attr("data-net-price", price.netPrice)
			  .attr("data-benefit", price.benefit);
	
	// Updates the total price
	totalUpdate($priceSpan);
	
	// Updates the info button class to notify of special info
	if (price.benefit === "No") {
		$infoButton.attr("class", "info warning");
	} else if ($dataSelect.attr("data-criteria-sa") || $dataSelect.attr("data-criteria-p")
			   || $dataSelect.attr("data-special-auth-title-1")) {
		$infoButton.attr("class", "info notice");
	} else {
		$infoButton.attr("class", "info");
	}
}

/****************************************************************************
 *	totalUpdate()	Updates the relevant "total price" span					*
 *																			*
 *	priceArray:	the array of spans containing the updated price				*
 *	totalSpan:	the "total price" span array containing the span to be 		*
 *				updated														*
 *	elemIndex:	the index of the trigger element							*
 *	numRows:	the number of rows in the table								*
 *																			*
 *	Returns a JSON array with the selected database entries					*
 ****************************************************************************/
function totalUpdate(priceSpan) {
	// Determines which column needs to be updated based on the passed span
	var $cell = $(priceSpan).closest("td");
	var $cells = $cell.closest("tr").children("td");
	var $rows = $("#Price-Table tbody:first tr")
	var colIndex = getElementIndex($cell, $cells);
	var $totalSpan = $("#Price-Table tfoot th:eq(" + colIndex + ") span");
	var finalTotal = 0;
	var tempPrice;
	
	$rows.each(function(index, row) {
		tempPrice = Number($(row).children("td").eq(colIndex)
							  .find("span").attr("data-net-price"));
		
		if (!isNaN(tempPrice) && tempPrice > 0) {
			finalTotal += tempPrice;
		}
	});
	
	$totalSpan.text("$" + finalTotal.toFixed(2));
}

/****************************************************************************
 *	changeThirdParty()	Updates the prices in all columns based on new 		*
 *						third party coverage								*
 ****************************************************************************/
function changeThirdParty(table) {
	var $rows = $("#" + table + " tbody tr");
	var $dataSelect;
	
	$rows.each(function(index, row) {
		if (table === "Price-Table") {
			$dataSelect = $(row).find(".brandName").first();
			brandUpdate($dataSelect);
		} else if (table === "Comparison-Table") {
			$dataSelect = $(row).find(".strength").first();
			comparisonStrength($dataSelect);
		}
	});
}

/****************************************************************************
 *	closeQuantity()		Closes the popup window that was generated to take	*
 *						the users input to update a column's quantities		*
 *																			*
 *	e:			The element triggering the function							*
 ****************************************************************************/
function closeQuantityPopup(e) {
	var $popupDiv = $("#Popup-Veil")[0];
	var $changeButton = $("#Popup-Change")[0];
	var $closeButton = $("#Popup-Close")[0];
	
	if (e === undefined ||
		e.target === $popupDiv || 
		e.target === $changeButton ||
		e.target === $closeButton) {
			$("#Popup-Veil").remove();
	}
}

/****************************************************************************
 *	changeQuantity()	Updates the quantities in an entire column			*
 *																			*
 *	amount:			The input element containing the new quantity to apply	*
 *	buttonInput:	The button that generated the popup window				*
 *	type:			Name dictating if this is a day supply or quantity 		*
 *					column													*
 *	table:			The table ID containing the columns to update			*
 ****************************************************************************/
function changeQuantity(amount, colIndex, type, table) {
	var $rows = $("#" + table + " tbody tr");
	
	$rows.each(function(index, row) {
		$input = $(row).children("td").eq(colIndex).children("input:first");
		$input.val(amount.value);
		
		if (type === "supply") {
			priceUpdateDay($input, table);
		} else if (type === "quantity") {
			priceUpdateQuantity($input, table);
		}
	});
	
	// Closes Popup
	$(amount).parent().parent().remove();
}

/****************************************************************************
 *	changeQuantityKeypress()	Adds keyboard functionality to popup		*
 *																			*
 *	amount:			The text input with the quantity						*
 *	buttonInput:	The submit button										*
 *	name:			The name of the column (days supply or quantity)		*
 *	table:			The table ID containing the columns to update			*
 *	e:				The triggering event									*
 ****************************************************************************/
function changeQuantityKeypress(amount, colIndex, type, table, e) {
	if (e.which == 13 || e.keycode == 13) {
		changeQuantity(amount, colIndex, type, table);
	} else if (e.which == 27 || e.keycode == 27) {
		closeQuantityPopup(undefined);
	} else {
		false;
	}
}

/****************************************************************************
 *	changeQuantityPopup()	Updates all of a columns quantities/day			*
 *							supplies										*
 *																			*
 *	buttonInput:	The button trigger the change							*
 *	name:			The calculation method this button applies to			*
 ****************************************************************************/
function changeQuantityPopup(buttonInput, type) {
	// Collect page, viewport, and element dimensions/coordinates
	var pageHt = $(document).height();
	var pageWid = $(document).width();
	var screenWid = $(window).width();
	var scrollHt = document.body.scrollTop ||
				   document.documentElement.scrollTop;		   
	var buttonTop = $(buttonInput).offset().top
	var buttonLeft = $(buttonInput).offset().left;
	var inputHt = 200;
	var inputWid = 300;
	
	var $coverDiv = $("<div></div>");
	var $inputDiv = $("<div></div>");
	var $inputLabel = $("<span></span>");
	var inputText = document.createElement("input");
	var inputButton = document.createElement("input");
	var inputClose = document.createElement("input");
	
	var $cell = $(buttonInput).closest("td");
	var $cells = $cell.closest("tr").children("td");
	var table = $cell.closest("table").attr("id");
	var colIndex = getElementIndex($cell, $cells);
	
	// Position cover div to fill entire page
	$coverDiv.attr("id", "Popup-Veil")
			 .height(pageHt)
			 .width(pageWid)
			 .on("click", function(e){closeQuantityPopup(e);})
			 .on("keydown", function(e) {changeQuantityKeypress(
				 inputText, colIndex, type, table, e);});
	
	// Popup div positions to left of trigger button
	$inputDiv.attr("id","Change-Popup")
			 .css({"min-width": inputWid + "px",
				  "right": ((screenWid - buttonLeft) + 10) + "px",
				  "top": (buttonTop) + "px"});
	
	// Creating popup window input elements
	$inputLabel.text("Enter new amount: ");
	
	inputText.type = "text";
	
	inputButton.type = "button";
	$(inputButton).attr("id", "Popup-Change")
				  .val("Change Amounts")
				  .on("click", function() {changeQuantity(
					  inputText, colIndex, type, table);});
	
	inputClose.type = "button";
	$(inputClose).attr("id","Popup-Close")
				 .val("Cancel")
				 .on("click", function(e){closeQuantityPopup(e);});
	
	// Assembling popup window
	$coverDiv.appendTo("body");
	$inputDiv.appendTo($coverDiv)
			 .append($inputLabel)
			 .append(inputText)
			 .append(inputButton)
			 .append(inputClose);
	
	// Bring focus to popup
	inputText.focus();
}

/****************************************************************************
 *	closeInfoPopup()	Closes the popup window generated to dispaly drug 	*
 *						info												*
 ****************************************************************************/
function closeInfoPopup() {
	var $popupDiv = $("#Popup-Veil");
	
	$popupDiv.remove();
}

/****************************************************************************
 *	showInfo()		Generates popup showing additional info on the			*
 *					selected row									 		*
 *																			*
 *	infoButton:		the button that was clicked								*
 ****************************************************************************/
 function showInfo(infoButton) {
	var table = $(infoButton).closest("table").attr("id");
	var $row = $(infoButton).closest("tr");
	var method = $("#" + table + "-Method")[0].selectedIndex;
	var $dataSelect;
	var $optionSelect;
	var $price;
	
	// Collect page, viewport, and element dimensions/coordinates
	var pageHt = $(document).height();
	var pageWid = $(document).width();
	var screenWid = $(window).width();
	var scrollHt = document.body.scrollTop ||
				   document.documentElement.scrollTop;		   
	var buttonTop = $(infoButton).offset().top
	var buttonLeft = $(infoButton).offset().left;

	
	var $coverDiv = $("<div></div>");
	var $infoDiv = $("<div></div>");
	var $title = $("<h3></h3>");
	var $coverage = $("<p></p>");
	var $benefit = $("<p></p>");
	var $feeTitle = $("<p></p>");
	var $feeTable = $("<table></table>");
	var $feeDrug = $("<tr></tr>");
	var $feeUpcharge1 = $("<tr></tr>");
	var $feeUpcharge2 = $("<tr></tr>");
	var $feeDispensing = $("<tr></tr>");
	var $feeGross = $("<tr></tr>");
	var $feeTP = $("<tr></tr>");
	var $feeNet = $("<tr></tr>");
	var $criteriaSA = $("<a></a>");
	var $criteriaP = $("<a></a>");
	var $saFormTitle = $("<p></p>");
	var $saForm = $("<ul></ul>");
	var $saFormTemp;
	var saFormTest = true;
	var saFormAttrT;
	var saFormAttrL;
	var saCounter = 1;
	var saFormName;
	var saFormLink;
	var $close = $("<div></div>");
	var closeButton = document.createElement("input");
	
	var tempText;
	
	// Determines which dataSelect to retrieve data from
	var tpIndex = 0;

	if (table === "Price-Table") {
		$dataSelect = $row.find($(".brandName")).first();
		tpIndex = document.getElementById("Price-Table-Third-Party").selectedIndex
	} else if (table === "Comparison-Table") {
		$dataSelect = $row.find($(".strength")).first();
		tpIndex = document.getElementById("Comparison-Table-Third-Party").selectedIndex
	}
	
	$optionSelect = $dataSelect.children("option:selected");
	
	var coverageText =  $optionSelect.attr("data-coverage");
	var criteriaSA = $optionSelect.attr("data-criteria-sa");
	var criteriaP = $optionSelect.attr("data-criteria-p");
	
	// Determines which price span to retrieve data from
	if (method === 0) {
		$price = $row.find(".cellDay.cellPrice").children().first();
	} else if (method === 1) {
		$price = $row.find(".cellQuantity.cellPrice").children().first();
	}
	
	// Position cover div to fill entire page
	$coverDiv.attr("id", "Popup-Veil")
			 .height(pageHt)
			 .width(pageWid)
			 .on("click", function(e){closeQuantityPopup(e);})
			 .on("keydown", function(e) {changeQuantityKeypress(
				 inputText, colIndex, type, e);})
			 .appendTo("body");
	
	// Popup div positions to left of trigger button
	$infoDiv.attr("id","Info-Popup")
			.css({"right": ((screenWid - buttonLeft) + 10) + "px",
				  "top": (buttonTop) + "px"})
			.appendTo($coverDiv);
	
	// Pop Up Title
	$title.text("Coverage Information")
		  .appendTo($infoDiv);
	
	// Benefit Type
	coverageText = coverageText ?  coverageText : "Not a benefit";
	$coverage.append($("<strong></strong>").text("Benefit Type: "))
			 .append($("<span></span>").text(coverageText))
			 .appendTo($infoDiv);
	
	// If this drug is a benefit or not
	tempText = $price.attr("data-benefit")
	tempText = tempText ? tempText : "N/A";
	
	$benefit.append($("<strong></strong>").text("Benefit: "))
			.append($("<span></span>").text(tempText))
			.appendTo($infoDiv);
	
 	// Adds drug cost & MAC if drug plan selected
	if (tpIndex > 0) {
		var $cost = $("<p></p>");
		var $mac = $("<p></p>");
		var cost = $optionSelect.attr("data-cost");
		var mac = $optionSelect.attr("data-mac");
		var unit = $optionSelect.attr("data-unit");

		// Replaces unit with "unit" if blank
		unit = unit === "" ? unit : "unit";

		tempText = "$" + cost + " per " + unit;
		$cost.append($("<strong></strong>").text("Cost: "))
			 .append($("<span></span>").text(tempText))
			 .appendTo($infoDiv);

		tempText = "$" + mac + " per " + unit;
		$mac.append($("<strong></strong>").text("MAC: "))
			.append($("<span></span>").text(tempText))
			.appendTo($infoDiv);
	}

	//  Coverage Criteria
	if (criteriaSA) {
		$criteriaSA.text("Click here for coverage criteria")
				   .attr("href", criteriaSA)
				   .attr("target", "_blank")
		
		$("<p></p>").append($criteriaSA)
					.appendTo($infoDiv)
					.addClass("MT05em");
	}
	
	// Paliative Care Link
	if (criteriaP) {
		$criteriaP.text("Click here for Palliative program information")
				  .attr("href", criteriaP)
				  .attr("target", "_blank")
		
		$("<p></p>").append($criteriaP)
					.appendTo($infoDiv)
					.addClass("MT05em");
	}
	
	// Price Information
	$feeTitle.append($("<strong></strong>").text("Price Breakdown"))
			 .addClass("MT1em")
			 .appendTo($infoDiv);
	
	$feeTable.appendTo($infoDiv);
	
	// Drug Costs
	tempText = Number($price.attr("data-drug-cost"))
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeDrug.append($("<td></td>").text("Drug Cost:"))
	$feeDrug.append($("<td></td>"))
		    .append($("<td></td>").text(tempText))
			.appendTo($feeTable);
	
	// Upcharge #1
	tempText = Number($price.attr("data-upcharge-1"));	
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeUpcharge1.append($("<td></td>").text("Upcharge #1:"))
				 .append($("<td></td>").text("+"))
				 .append($("<td></td>").text(tempText))
				 .appendTo($feeTable);
	
	// Upcharge #2
	tempText = Number($price.attr("data-upcharge-2"));
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeUpcharge2.append($("<td></td>").text("Upcharge #2:"))
				 .append($("<td></td>").text("+"))
				 .append($("<td></td>").text(tempText))
				 .appendTo($feeTable);
	
	// Dispensing Fee
	tempText = Number($price.attr("data-dispensing-fee"));
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeDispensing.append($("<td></td>").text("Dispensing Fee:"))
				  .append($("<td></td>").text("+"))
				  .append($("<td></td>").text(tempText))
				  .appendTo($feeTable);
	
	// Gross Price
	tempText = Number($price.attr("data-gross-price"));
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeGross.append($("<td></td>").text("Sub-Total:"))
			 .append($("<td></td>"))
			 .append($("<td></td>").text(tempText))
			 .addClass("totalRow")
			 .appendTo($feeTable);
	
	// Insurance Pays Portion
	tempText = Number($price.attr("data-third-party"));
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeTP.append($("<td></td>").text("Third Party Portion:"))
		  .append($("<td></td>").text("-"))
		  .append($("<td></td>").text(tempText))
		  .appendTo($feeTable);
	
	// Patient Pays Portion
	tempText = Number($price.attr("data-net-price"));
	tempText = isNaN(tempText) ? "$0.00" : "$" + tempText.toFixed(2);
	
	$feeNet.append($("<td></td>").text("Patient Pays:"))
		   .append($("<td></td>"))
		   .append($("<td></td>").text(tempText))
		   .addClass("totalRow")
		   .appendTo($feeTable);
	
	// Special Authorization Form Links
	while (saFormTest === true) {
		saFormAttrL = "data-special-auth-link-" + saCounter;
		saFormAttrT = "data-special-auth-title-" + saCounter;
		
		if ($optionSelect.attr(saFormAttrL)) {
			if (saCounter === 1) {
				$saFormTitle.append($("<strong></strong>").text("Special Authorization Forms"))
							.addClass("MT1em")
							.appendTo($infoDiv);
							
				$saForm.appendTo($infoDiv);
			}
			
			$saFormTemp = $("<a></a>");
			saFormLink = $optionSelect.attr(saFormAttrL);
			saFormName = $optionSelect.attr(saFormAttrT);
			
			$saFormTemp.text(saFormName)
				   .attr("href", saFormLink)
				   .attr("target", "_blank");
			
			$("<li></li>").append($saFormTemp).appendTo($saForm);
			
			saCounter++
		} else {
			saFormTest = false;
		}
	}
	
	// Close Button
	closeButton.type = "button";
	$(closeButton).val("Close")
				  .on("click", function(){closeInfoPopup();})
				  .appendTo($close);
	
	$close.attr("class", "close")
		  .appendTo($infoDiv);
}




/****************************************************************************
 *	FUNCTIONS SPECIFIC TO PRICE-TABLE										*
 ****************************************************************************/
/****************************************************************************
 *	addFreeformEntry()	Adds input elements to allow user to enter freeform *
 *						medication prices.									*
 ****************************************************************************/
function addFreeformEntry() {
	var $tbody = $("#Price-Table tbody:first");
	var $row = $("<tr></tr>");
	var $medicationCell = $("<td></td>");
	var medicationInput = document.createElement("input");
	var $brandCell = $("<td></td>");
	var $brandSpan = $("<span></span>");
	var $costCell = $("<td></td>");
	var costInput = document.createElement("input");
	var $dosesCell = $("<td></td>");
	var dosesInput = document.createElement("input");
	var $supplyCell = $("<td></td>");
	var supplyInput = document.createElement("input");
	var $dayPriceCell = $("<td></td>");
	var $dayPriceSpan = $("<span></span>");
	var $quantityCell = $("<td></td>");
	var quantityInput = document.createElement("input");
	var $quantityPriceCell = $("<td></td>");
	var $quantityPriceSpan = $("<span></span>");
	var $infoCell = $("<td></td>");
	var $infoButton = $("<span></span>");
	var $deleteCell = $("<td></td>");
	var $deleteButton = $("<span></span>");
	var $colDay = $("#Price-Table thead th.cellDay.cellPrice");
	var $colQuantity = $("#Price-Table thead th.cellQuantity.cellPrice");
	var $tempText;
	var $tempOption;
	
	// Medication Name
	medicationInput.type = "text";
	
	$medicationCell.append(medicationInput)
				   .appendTo($row);
	
	// Brand Name
	$brandSpan.addClass("brandName")
			  .text("N/A");
	
	$brandCell.append($brandSpan);
	$brandCell.appendTo($row);
	
	// Cost
	
	// Cost
	costInput.type = "text";
	$(costInput).addClass("cost")
				.on("keyup", function() {costUpdate(this, "#Price-Table");});

	$costCell.append(costInput);
	$costCell.appendTo($row);
	
	// Doses per day
	dosesInput.type= "text";
	$(dosesInput).addClass("dosesPerDay")
				 .val(1)
				 .on("keyup", function() {priceUpdateDay(this, "#Price-Table");});
			
	// Day Supply
	supplyInput.type = "text";
	$(supplyInput).addClass("daySupply")
				  .val("100")
				  .on("keyup", function() {priceUpdateDay(this, "#Price-Table");});
	// Price
	$dayPriceSpan.addClass("dayPrice");
	
	// Adds the required number of elements
	$colDay.each(function() {
		$dosesCell.addClass("cellDay")
				  .append(dosesInput)
				  .appendTo($row);
		
		$supplyCell.addClass("cellDay")
				   .append(supplyInput)
				   .appendTo($row);
		
		$dayPriceCell.addClass("cellDay cellPrice")
					 .append($dayPriceSpan)
					 .appendTo($row);
	});
	
	// Quantity
	quantityInput.type = "text";
	$(quantityInput).addClass("quantity")
					.val("100")
					.on("keyup", function() {priceUpdateQuantity(this);});
	
	// Price
	$quantityPriceSpan.addClass("quantityPrice")
		
	$colQuantity.each(function() {
		$quantityCell.addClass("cellQuantity")
					 .append(quantityInput)
					 .appendTo($row);
		
		$quantityPriceCell.addClass("cellQuantity cellPrice")
						  .append($quantityPriceSpan)
						  .appendTo($row);
	});
	
	// Info
	$infoButton.addClass("info")
				 .text(" ")
				 .on("click", function() {showInfo(this);});
				 
	$infoCell.append($infoButton)
			 .appendTo($row);
	
	// Delete
	$deleteButton.addClass("delete")
				 .html(" ")
				 .on("click", function() {removeRow(this);});
				 
	$deleteCell.append($deleteButton)
			   .appendTo($row);
			   
	//Adds row to table
	$tbody.append($row);
	
	medicationInput.focus();
}

/****************************************************************************
 *	brandUpdate()	Updates the Cost per Unit after a new brand is selected *
 *																			*
 *	brandSelect:	The select object that was changed.						*
 ****************************************************************************/
function brandUpdate(brandSelect) {
	var $row = $(brandSelect).closest("tr");
	var $costSpan = $row.find(".cost");
	var $macSpan = $row.find(".mac");
	var $brandOption = $(brandSelect).children("option:selected");
	var cost = $brandOption.attr("data-cost");
	var mac = $brandOption.attr("data-mac");
	var unit = $brandOption.attr("data-unit");
	var $daySupply = $row.find(".daySupply");
	var $quantity = $row.find(".quantity");
	var tempText;
	
	// Updates the cost/unit span
	tempText = "$" + cost + "<br>(per " + unit + ")";
	$costSpan.html(tempText)
			 .attr("data-cost", cost);
	
	// Updates the mac/unit span
	tempText = "$" + mac + "<br>(per " + unit + ")";
	$macSpan.html(tempText)
			.attr("data-mac", mac);

	// Updates day supply pricing
	$daySupply.each(function(index, elem) {
		priceUpdateDay(elem);
	});
	
	// Updates quantity pricing
	$quantity.each(function(index, elem) {
		priceUpdateQuantity(elem);
	});
}

/****************************************************************************
 *	costUpdate()	Updates the price when the Cost per Unit is changed		*
 *																			*
 *	costInput:		The input object that was changed.						*
 ****************************************************************************/
function costUpdate(costInput) {
	var $row = $(costInput).closest("tr");
	var cost = costInput.value;
	var $daySupply = $row.find(".daySupply");
	var $quantity = $row.find(".quantity");
	
	// Updates day supply pricing
	$daySupply.each(function(index, elem) {
		priceUpdateDay(elem);
	});
	
	// Updates quantity pricing
	$quantity.each(function(index, elem) {
		priceUpdateQuantity(elem);
	});
}

/****************************************************************************
 *	removeRow()		Removes the row containing the clicked button	 		*
 *																			*
 *	deleteButton:	the button that was clicked								*
 ****************************************************************************/
function removeRow(deleteButton) {
	var $row = $(deleteButton).closest("tr");
	var $cells = $(deleteButton).closest("tbody").children("tr:first");
	var $spans = $cells.find("td.cellPrice span");
	
	// Removes row
	$row.remove();
	
	// Updates total prices
	$spans.each(function(index, span) {
		totalUpdate(span)
	});
}




/****************************************************************************
 *	FUNCTIONS SPECIFIC TO THE DRUG PRICE COMPARISON TABLE					*
 ****************************************************************************/
/****************************************************************************
 *	comparisonStrength()	Updates comparison table prices based on 		*
 *							selected strength								*
 *																			*
 *	strengtSelect:	The strength select to update							*
 ****************************************************************************/
function comparisonStrength(strengthSelect) {
	var $row = $(strengthSelect).closest("tr");
	var $costSpan = $row.find(".cost");
	var $strengthOption = $(strengthSelect).children("option:selected");
	var cost = $strengthOption.attr("data-cost");
	var $daySupply = $row.find(".daySupply");
	var $quantity = $row.find(".quantity");
	
	// Updates the cost/unit span
	$costSpan.text("$" + cost)
			 .attr("data-cost", cost);
	
	// Updates day supply pricing
	$daySupply.each(function(index, elem) {
		priceUpdateDay(elem, "#Comparison-Table");
	});
	
	// Updates quantity pricing
	$quantity.each(function(index, elem) {
		priceUpdateQuantity(elem, "#Comparison-Table");
	});
}




/****************************************************************************
 *	FUNCTIONS SPECIFIC TO THE SEARCH BAR									*
 ****************************************************************************/
/****************************************************************************
 *	showSearchResult()	Function handling the AJAX call to the database to 	*
 *						retieve the search results							*
 *																			*
 *	searchString:	Text entered into the search bar						*
 *																			*
 *	Returns MySQL query results, formatted for use in the search result div *
 ****************************************************************************/
function showSearchResults(searchString) {
	var $searchResults = $("#Search-Results");
	
	if (searchString.length > 0) {
		// 200 ms Timeout applied to prevent firing during typing
		clearTimeout(ajaxTimer);
		
		ajaxTimer = setTimeout(function() {
			$.ajax({
				url: "live-search/",
				data: {q: searchString},
				type: "GET",
				dataType: "html",
				beforeSend: function() {
					$searchResults.html("<ul><li><a>" + 
										loadingBar() + 
										"</a></li></ul>");
				},
				success: function (results) {
					if ($("#Search-Bar").val() == searchString) {
						$searchResults.html(results);
					}
				},
				error: function () {
					$searchResults.empty();
					var error = "Sorry we have experienced an error with our " +
								"server. Please refresh your page and try " +
								"again. If you continue to run into issues, " +
								"please contact us at " + 
								"studybuffalo@studybuffalo.com";
					
					alert(error);
				}
			});
		}, 00);
	} else {
		$searchResults.empty();
	}
}

/****************************************************************************
 *	chooseResult()	Function handling the AJAX call to the database	to 		*
 *					retrieve the selected product information				*
 *																			*
 *	selection:	the search result that was clicked							*
 *																			*
 *	Returns a JSON array with the selected database entries					*
 ****************************************************************************/
function chooseResult(selection) {
	// Extract indices for MySQL query
	var query = $(selection).attr("data-url");
	showSearchResults("");
	
	$.ajax({
		url: "add-item/",
		data: {q: query},
		type: "GET",
		dataType: "json",
		success: function (results) {
			processResult(results);
			
			// Reset search bar
			$("#Search-Bar").val("");
			$("#Search-Bar").focus();
		},
        error: function (jqXHR, textStatus, errorThrown) {
            console.error(textStatus + ": " + errorThrown)
			var error = "Sorry we have experienced an error with our " +
						"server. Please refresh your page and try " +
						"again. If you continue to run into issues, " +
						"please contact us at " + 
						"studybuffalo@studybuffalo.com";
			
			alert(error);
		}
	});
}

/****************************************************************************
 *	addLCA()	Adds an entry to the JSON array that identifies the LCA		*
 *																			*
 *	result:	the passed JSON array											*
 *																			*
 *	Returns a JSON array with the LCA entry added to the front				*
 ****************************************************************************/
function addLCA(result) {
	var lcaIndex = 0;
	var lcaCost = parseFloat(result[0].unit_price);
	var lcaEntry;
	
	// Identifies the index of the LCA
	for (var i = 0; i < result.length; i++) {
		if (parseFloat(result[i].unit_price) < lcaCost) {
			lcaIndex = i;
			lcaCost = parseFloat(result[i].unit_price);
		}
	}
	
	// Constructs the LCA entry
	lcaEntry = {url: result[lcaIndex].url,
				generic_name: result[lcaIndex].generic_name,
				strength: result[lcaIndex].strength,
				route: result[lcaIndex].route,
				dosage_form: result[lcaIndex].dosage_form,
				brand_name: "LCA",
				unit_price: result[lcaIndex].unit_price,
				lca: result[lcaIndex].lca,
				unit_issue: result[lcaIndex].unit_issue,
				coverage: result[lcaIndex].coverage,
				criteria: result[lcaIndex].criteria,
				criteria_p: result[lcaIndex].criteria_p,
				criteria_sa: result[lcaIndex].criteria_sa,
				group_1: result[lcaIndex].group_1,
				group_66: result[lcaIndex].group_66,
				group_66a: result[lcaIndex].group_66a,
				group_19823: result[lcaIndex].group_19823,
				group_19823a: result[lcaIndex].group_19823a,
				group_19824: result[lcaIndex].group_19824,
				group_20400: result[lcaIndex].group_20400,
				group_20403: result[lcaIndex].group_20403,
				group_20514: result[lcaIndex].group_20514,
				group_22128: result[lcaIndex].group_22128,
				group_23609: result[lcaIndex].group_23609,
				special_auth: result[lcaIndex].special_auth};
	
	// Adds LCA entry to front of array
	result.unshift(lcaEntry);
	
	return result;
}

/****************************************************************************
 *	processResult()	Takes the passed JSON array and formats all the data to	*
 *					insert into Price-Table									*
 *																			*
 *	array:	the JSON array containing the data to insert					*
 ****************************************************************************/
function processResult(results) {
	var $tbody = $("#Price-Table tbody:first");
	var $row = $("<tr></tr>");
	var $medicationCell = $("<td></td>");
	var $brandCell = $("<td></td>");
	var $brandSelect = $("<select></select>");
	var $costCell = $("<td></td>");
	var $costSpan = $("<span></span>");
	var $dosesCell = $("<td></td>");
	var dosesInput = document.createElement("input");
	var $supplyCell = $("<td></td>");
	var supplyInput = document.createElement("input");
	var $dayPriceCell = $("<td></td>");
	var $dayPriceSpan = $("<span></span>");
	var $quantityCell = $("<td></td>");
	var quantityInput = document.createElement("input");
	var $quantityPriceCell = $("<td></td>");
	var $quantityPriceSpan = $("<span></span>");
	var $infoCell = $("<td></td>");
	var $infoButton = $("<span></span>");
	var $deleteCell = $("<td></td>");
	var $deleteButton = $("<span></span>");
	var $colDay = $("#Price-Table thead th.cellDay.cellPrice");
	var $colQuantity = $("#Price-Table thead th.cellQuantity.cellPrice");
	var $tempText;
	var $tempOption;
	var attributeName;
	var attributeValue;
	
	// Add an entry to the result array for the LCA
	results = addLCA(results);
	
	// Medication Name
	$medicationCell.append(
		"<strong>" + results[0].generic_name + "</strong>" + "<br>" + 
		"<em>" + results[0].strength + " " + results[0].route + " " + 
		results[0].dosage_form + "</em>");
	$medicationCell.appendTo($row)
	
	// Brand Name
	$brandSelect.addClass("brandName")
				.on("change", function() {brandUpdate(this);});
				
	
	$.each(results, function (index, value) {
		$tempOption = $("<option></option>");
		
		$tempOption.text(value.brand_name)
				   .attr("data-cost", value.unit_price)
				   .attr("data-unit", value.unit_issue)
				   .attr("data-mac", value.lca ? value.lca : value.unit_price)
				   .attr("data-coverage", value.coverage)
				   .attr("data-criteria-p", value.criteria_p)
				   .attr("data-criteria-sa", value.criteria_sa)
				   .attr("data-group-1", value.group_1)
				   .attr("data-group-66", value.group_66)
				   .attr("data-group-66a", value.group_66a)
				   .attr("data-group-19823", value.group_19823)
				   .attr("data-group-19823a", value.group_19823a)
				   .attr("data-group-19824", value.group_19824)
				   .attr("data-group-20400", value.group_20400)
				   .attr("data-group-20403", value.group_20403)
				   .attr("data-group-20514", value.group_20514)
				   .attr("data-group-22128", value.group_22128)
				   .attr("data-group-23609", value.group_23609)
				   .appendTo($brandSelect);
				   
		// Generates format for special auth data objects
		$.each(value.special_auth, function(index, temp) {
			attributeName = "data-special-auth-title-" + (index + 1);
			attributeValue = temp.title;
			$tempOption.attr(attributeName, attributeValue);
			
			attributeName = "data-special-auth-link-" + (index + 1);
			attributeValue = temp.link;
			$tempOption.attr(attributeName, attributeValue);
		});
	});
	
	$brandCell.append($brandSelect);
	$brandCell.appendTo($row);
	
	// Cost
	$costSpan.addClass("cost");
	
	$costCell.append($costSpan);
	$costCell.appendTo($row);
	
	// Doses per day
	dosesInput.type= "text";
	$(dosesInput).addClass("dosesPerDay")
				 .val(1)
				 .on("keyup", function() {priceUpdateDay(this, "#Price-Table");});
			
	// Day Supply
	supplyInput.type = "text";
	$(supplyInput).addClass("daySupply")
				  .val("100")
				  .on("keyup", function() {priceUpdateDay(this, "#Price-Table");});
	// Price
	$dayPriceSpan.addClass("dayPrice");
	
	// Adds the required number of elements
	$colDay.each(function() {
		$dosesCell.addClass("cellDay")
				  .append(dosesInput)
				  .appendTo($row);
		
		$supplyCell.addClass("cellDay")
				   .append(supplyInput)
				   .appendTo($row);
		
		$dayPriceCell.addClass("cellDay cellPrice")
					 .append($dayPriceSpan)
					 .appendTo($row);
	});
	
	// Quantity
	quantityInput.type = "text";
	$(quantityInput).addClass("quantity")
					.val("100")
					.on("keyup", function() {priceUpdateQuantity(this);});
	
	// Price
	$quantityPriceSpan.addClass("quantityPrice")
		
	$colQuantity.each(function() {
		$quantityCell.addClass("cellQuantity")
					 .append(quantityInput)
					 .appendTo($row);
		
		$quantityPriceCell.addClass("cellQuantity cellPrice")
						  .append($quantityPriceSpan)
						  .appendTo($row);
	});
	
	// Info
	$infoButton.addClass("info")
				 .text(" ")
				 .on("click", function() {showInfo(this);});
				 
	$infoCell.append($infoButton)
			 .appendTo($row);
	
	// Delete
	$deleteButton.addClass("delete")
				 .text(" ")
				 .on("click", function() {removeRow(this);});
				 
	$deleteCell.append($deleteButton)
			   .appendTo($row);
	
	//Adds row to table
	$tbody.append($row);
	
	// Calculates table values
	brandUpdate($brandSelect);
}




/****************************************************************************
 *	FUNCTIONS SPECIFIC TO THE DRUG PRICE COMPARISON SEARCH BAR				*
 ****************************************************************************/
/****************************************************************************
 *	showComparisonResults()	Function handling the AJAX call to the database *
 *							to retieve the search results					*
 *																			*
 *	searchString:	Text entered into the search bar						*
 *																			*
 *	Returns MySQL query results, formatted for use in the search result div *
 ****************************************************************************/
function showComparisonResults(searchString) {
	var $searchResults = $("#Comparison-Results");
	var $searchMethod1 = $("#Comparison-Search-Method-1")[0].checked ? 
						 true : false;
	var $searchMethod2 = $("#Comparison-Search-Method-2")[0].checked ? 
						 true : false;
	
	if (searchString.length > 0) {
		// 300 ms Timeout applied to prevent firing during typing
		clearTimeout(ajaxTimer);
		
		ajaxTimer = setTimeout(function() {
			$.ajax({
				url: "comparison-search/",
				data: {search: searchString,
					   methodATC: $searchMethod1,
					   methodPTC: $searchMethod2},
				type: "GET",
				dataType: "html",
				beforeSend: function() {
					$searchResults.html("<ul><li><a>" + 
										loadingBar() + 
										"</a></li></ul>");
				},
				success: function (results) {
					// Only updates if search string hasn't changed
					if ($("#Comparison-Search").val() == searchString) {
						$searchResults.html(results);
					}
				},
				error: function () {
					$searchResults.empty();
				}
			});
		}, 300);
	} else {
		$searchResults.empty();
	}
}

/****************************************************************************
 *	chooseComparison()	Function handling the AJAX call to the database	to 	*
 *						retrieve the selected product information			*
 *																			*
 *	selection:	the search result that was clicked							*
 *																			*
 *	Returns a JSON array with the selected database entries					*
 ****************************************************************************/
function chooseComparison(selection) {
	// Extract indices for MySQL query
	var query = $(selection).attr("data-url");
	showComparisonResults("");
	
	$.ajax({
		url: "generate_comparison.php",
		data: {q: query},
		type: "GET",
		dataType: "json",
		success: function (results) {
			processComparison(results);
			// Reset search bar
			$("#Comparison-Search").val("");
		},
		error: function () {
			var error = "Sorry we have experienced an error with our " +
						"server. Please refresh your page and try " +
						"again. If you continue to run into issues, " +
						"please contact us at " + 
						"studybuffalo@studybuffalo.com";
			
			alert(error);
		}
	});
}

/****************************************************************************
 *	processComparison()		Takes the passed JSON array and formats all the	*
 *							data to	insert into Comparison-Table			*
 *																			*
 *	results:	the JSON array containing the data to insert				*
 ****************************************************************************/
function processComparison(results) {
	var $tbody = $("#Comparison-Table tbody:first");
	var $row;
	var $medicationCell;
	var $strengthCell;
	var $strengthSelect;
	var $costCell;
	var $costSpan;
	var $dosesCell;
	var dosesInput;
	var $supplyCell;
	var supplyInput;
	var $dayPriceCell;
	var $dayPriceSpan;
	var $quantityCell;
	var quantityInput;
	var $quantityPriceCell;
	var $quantityPriceSpan;
	var $infoCell;
	var $infoButton;
	var $tempText;
	var $tempOption;
	var attributeName;
	var attributeValue;
	
	// Reset the table
	$tbody.empty();
	
	// Cycles through the JSON array to generate an entry for each generic name
	$.each(results, function(index, value) {
		$row = $("<tr></tr>");
		$row.appendTo($tbody);
		
		// Medication Name
		$medicationCell = $("<td></td>");
		$medicationCell.html($("<strong></strong>").text(value.generic_name))
					   .appendTo($row);
		
		// Strength
		$strengthCell = $("<td></td>");
		$strengthCell.appendTo($row);
		$strengthSelect = $("<select></select>");
		$strengthSelect.on("change", function(){comparisonStrength(this);})
					   .addClass("strength")
					   .appendTo($strengthCell);
		
		$.each(value.strength, function(index, temp) {
			// Adds each strength as an option to the select
			$tempOption = $("<option></option>");
			$tempOption.text(temp.strength)
					   .attr("data-cost", temp.unit_price)
					   .attr("data-mac", temp.lca ? temp.lca : temp.unit_price)
					   .attr("data-coverage", temp.coverage)
					   .attr("data-criteria", temp.criteria)
					   .attr("data-criteria-p", temp.criteria_p)
					   .attr("data-criteria-sa", temp.criteria_sa)
					   .attr("data-group-1", temp.group_1)
					   .attr("data-group-66", temp.group_66)
					   .attr("data-group-66a", temp.group_66a)
					   .attr("data-group-19823", temp.group_19823)
					   .attr("data-group-19823a", temp.group_19823a)
					   .attr("data-group-19824", temp.group_19824)
					   .attr("data-group-20400", temp.group_20400)
					   .attr("data-group-20403", temp.group_20403)
					   .attr("data-group-20514", temp.group_20514)
					   .attr("data-group-22128", temp.group_22128)
					   .attr("data-group-23609", temp.group_23609)
					   .appendTo($strengthSelect);
					   
			// Generates format for special auth data objects
			$.each(temp.special_auth, function(index, temp2) {
				attributeName = "data-special-auth-title-" + (index + 1);
				attributeValue = temp2.title;
				$tempOption.attr(attributeName, attributeValue);
				
				attributeName = "data-special-auth-link-" + (index + 1);
				attributeValue = temp2.link;
				$tempOption.attr(attributeName, attributeValue);
			});
		});
		
		// LCA Cost
		$costCell = $("<td></td>");
		$costCell.appendTo($row);
		
		$costSpan = $("<span></span>");
		$costSpan.addClass("cost")
				 .appendTo($costCell);
		
		// Doses per Day
		$dosesCell = $("<td></td>");
		$dosesCell.addClass("cellDay")
				  .appendTo($row)
		
		dosesInput = document.createElement("input");
		dosesInput.type= "text";
		$(dosesInput).addClass("dosesPerDay")
					 .val(1)
					 .on("keyup", function(){priceUpdateDay(this);})
					 .appendTo($dosesCell);
					 
		// Day Supply
		$supplyCell = $("<td></td>");
		$supplyCell.addClass("cellDay")
				   .appendTo($row);
		
		supplyInput = document.createElement("input");
		supplyInput.type = "text";
		$(supplyInput).addClass("daySupply")
					  .val("100")
					  .on("keyup", function(){priceUpdateDay(this);})
					  .appendTo($supplyCell);
					  
		// Day Price
		$dayPriceCell = $("<td></td>");
		$dayPriceCell.addClass("cellDay")
					 .addClass("cellPrice")
					 .appendTo($row);
		
		$dayPriceSpan = $("<span></span>");
		$dayPriceSpan.addClass("dayPrice")
					 .appendTo($dayPriceCell);
		
		// Quantity
		$quantityCell = $("<td></td>");
		$quantityCell.addClass("cellQuantity")
					 .appendTo($row);
		
		quantityInput = document.createElement("input");
		quantityInput.type = "text";
		$(quantityInput).addClass("quantity")
						.val("100")
						.on("keyup", function(){priceUpdateQuantity(this);})
						.appendTo($quantityCell);
		
		// Quantity Price
		$quantityPriceCell = $("<td></td>");
		$quantityPriceCell.addClass("cellQuantity")
						  .addClass("cellPrice")
						  .appendTo($row);
		
		$quantityPriceSpan = $("<span></span>");
		$quantityPriceSpan.addClass("quantityPrice")
						  .appendTo($quantityPriceCell);
		
		// Info
		$infoCell = $("<td></td>");
		$infoCell.appendTo($row);
				 
		$infoButton = $("<span></span>");
		$infoButton.addClass("info")
				   .text(" ")
				   .on("click", function() {showInfo(this);})
				   .appendTo($infoCell);
		
		// Calls functions to update data
		comparisonStrength($strengthSelect);
	});
}


/****************************************************************************
 *	FUNCTIONS SPECIFIC TO PRINTING											*
 ****************************************************************************/
/****************************************************************************
 *	printPrices()	Takes the data from Price-Table and formats it into a	*
 *					new print page											*
 *																			*
 *	Returns a new window.document formatted for printing					*
 ****************************************************************************/
function printPrices() {
	var printPage = window.open().document;
	var html = "";
	
	var method = $("#Price-Table-Method").prop("selectedIndex");
	var pageNum = method === 0 ? 
	  $("#Price-Table thead th.cellDay.cellPrice").length :
	  $("#Price-Table thead th.cellQuantity.cellPrice").length;
	
	var patientName = $("#Patient-Name").val();
	
	var $table;
	var $thead;
	var $headRow;
	var headMedication = "Medication";
	var headQuantity = method === 0 ? "Day Supply" : "Quantity";
	var headPrice = "Price";
	
	var $tbody
	var $bodyRow;
	var $bodyMedication;
	var $bodyNumber;
	var $bodyPrice;
	var $rows = $("#Price-Table tbody:first").children();
	var $medicationData;
	var $quantityData;
	var $priceData;
	
	var $tfoot;
	var $footRow;
	var $footTotal;
	var $totalData;
	
	var $disclaimer = $("<p></p>");
	var lastUpdate = document.getElementById("Last-Update").innerHTML;
	var today = getTodaysDate();
	
	var tempArray;
	
	html = "<head>" +
				"<link rel='stylesheet' type='text/css', href='http://www.studybuffalo.com/practicetools/include/abc_print_style.css?version=1.0'></link>" +
				"<title>Medications Prices</title>" +
		   "</head>";
	
	// Cycle through the table rows and enter them into the print table
	html += "<body>";
	
	for (var page = 0; page < pageNum; page++) {
		// Header
		html += "<h1>";
		
		html += patientName === "" ? 
				"Medication Price List" : 
				"Medication Price List for " + patientName;
		
		html += "</h1>";
		
		// Medication Table
		
		html += "<table>" +
					"<thead>" +
						"<tr>" +
							"<th>" + headMedication + "</th>" +
							"<th>" + headQuantity + "</th>" +
							"<th>" + headPrice + "</th>" +
						"</tr>" +
					"</thead>";
		
		html += "<tbody>";
					
		$rows.each(function(index, row) {
			$row = $(row);
			
			html += "<tr>";
			
			// Medication Name
			$medicationData = $row.children().first();
			
			tempArray = [];
			
			if ($medicationData.find("input").length === 0) {
				tempArray.push($medicationData.children().eq(0).text());
				tempArray.push($medicationData.children().eq(2).text());
			} else {
				tempArray.push($medicationData.children().eq(0).val());
				tempArray.push("");
			}
			
			html += "<td>" + 
						"<strong>" + tempArray[0] + "</strong>" +
						"<br>" +
						"<em>" + tempArray[1] + "</em>" +
					"</td>";
						   
			// Day supply/Quantity
			$quantityData = method === 0 ? 
							$row.children().find("input.daySupply") :
							$row.children().find("input.quantity");
			$quantityData = $quantityData.eq(page).val();
			
			html += "<td>" + $quantityData + "</td>";
			
			// Price
			$priceData = method === 0 ?
						 $row.find(".cellDay.cellPrice span:first").text() :
						 $row.find(".cellQuantity.cellPrice span:first").text();
			
			html += "<td>" + $priceData + "</td>";
			
			html += "</tr>";
		});
		
		html += "</tbody>";
	
	
		// Footer
		$totalData = method === 0 ? 
			$("#Price-Table tfoot .cellDay span.total").eq(page).text() :
			$("#Price-Table tfoot .cellQuantity span.total").eq(page).text();
		
		html += "<tfoot>" +
					"<tr>" +
						"<th></th>" +
						"<th>TOTAL</th>" + 
						"<th>" + $totalData + "</th>" +
					"</tr>" +
				"</tfoot>";
		
		html += "</table>";
		
		// Disclaimer text
		html += "These medications costs are estimates based " +
				"on the best available information. Actual " +
				"costs may vary depending on your pharmacy " +
				"and third-party drug coverage.<br><br>" +
				"<i>Printed on: " + today + "</i>";
	}
	
	html += "</body>";
	
	// Writes HTML to document window
	printPage.write(html);
	
	// Close document
	printPage.close();
}




 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/ 
//Adds event listeners
$(document).ready(function() {
	var searchSupport = eventSupported("onsearch");
	var trigger = searchSupport === true ? "search" : "keyup";
	
	$("#Search-Bar").on(
		trigger,
		function(){showSearchResults(this.value);});
	
	$("#Price-Table-Third-Party").on(
		"change",
		function(){changeThirdParty("Price-Table");});
	
	$("#Price-Table-Method").on(
		"change",
		function(){changePriceTableCols("Price-Table");});

	$("input.changeSupply").on(
		"click",
		function(){changeQuantityPopup(this, "supply");});

	$("input.changeQuantity").on(
		"click",
		function(){changeQuantityPopup(this, "quantity");});

	$("#Add-Freeform").on(
		"click",
		function(){addFreeformEntry();});
	
	$("#Comparison-Search").on(
		trigger,
		function(){showComparisonResults(this.value);});
	
	$("#Comparison-Table-Third-Party").on(
		"change",
		function(){changeThirdParty("Comparison-Table");});
	
	$("#Comparison-Table-Method").on(
		"change",
		function(){changePriceTableCols("Comparison-Table");});
	
	$("#Print-Medication-Prices").on(
		"click",
		function(){printPrices();});

	$("#Search-Bar").focus();
	
	changePriceTableCols("Price-Table");
	changePriceTableCols("Comparison-Table");
	
	//Left aligns the MathJax output
	MathJax.Hub.Config({
		jax: ["input/TeX","output/HTML-CSS"],
		displayAlign: "left",
		messageStyle: "none",
		tex2jax: {preview: "none"}
	});
});

var ajaxTimer;