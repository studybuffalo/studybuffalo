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
 *	calculatePrice()	Calculates the total price of a medication			*
 *																			*
 *	drugPrice:	The cost of the medication (excluding any fees)				*
 *																			*
 *	Returns the price as a float number										*
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
function calculatePrice(drugPrice) {
	var today = new Date();
	
	if (isNaN(drugPrice) || drugPrice === 0) {
		return 0;
	} else {
		var upcharge1 = 0.03;
		var upcharge2 = today < 1427868000000 ? 0.055 :
						today < 1459490400000 ? 0.06 :
						today < 1491026400000 ? 0.065 :
						0.07;
		var fee1 = drugPrice * upcharge1;
		var tempFee2 = (drugPrice + fee1) * upcharge2;
		var fee2 = tempFee2 > 100 ? 100 : tempFee2;
		var totalPrice = drugPrice + fee1 + fee2 + 12.3;

		return totalPrice;
	}
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
 *	FUNCTIONS SPECIFIC TO PRICE-TABLE										*
 ****************************************************************************/
/****************************************************************************
 *	changePriceTable()	Updates column display properites depending on the 	*
 *						calcultaion method selected							*
 ****************************************************************************/
function changePriceTableCols() {
	var index = $("#Price-Table-Method")[0].selectedIndex;
	var $table = $("#Price-Table");
	
	if (index === 0) {
		$table.attr("class", "methodDay");
	} else if (index === 1) {
		$table.attr("class", "methodQuantity");
	}
}

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
	var $deleteCell = $("<td></td>");
	var $deleteButton = $("<span></span>");
	var $colDay = $("thead th.cellDay.cellPrice");
	var $colQuantity = $("thead th.cellQuantity.cellPrice");
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
				.on("keyup", function() {costUpdate(this);});

	$costCell.append(costInput);
	$costCell.appendTo($row);
	
	// Doses per day
	dosesInput.type= "text";
	$(dosesInput).addClass("dosesPerDay")
				 .val(1)
				 .on("keyup", function() {priceUpdateDay(this);});
			
	// Day Supply
	supplyInput.type = "text";
	$(supplyInput).addClass("daySupply")
				  .val("100")
				  .on("keyup", function() {priceUpdateDay(this);});
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
 *	closeQuantity()		Closes the popup window that was generated to take	*
 *						the users input to update a column's quantities		*
 *																			*
 *	coverDiv:	The transparent div that triggers closure					*
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
		$popupDiv.remove();
	}
}

/****************************************************************************
 *	changeQuantity()	Updates the quantities in an entire column			*
 *																			*
 *	amount:			The input element containing the new quantity to apply	*
 *	buttonInput:	The button that generated the popup window				*
 *	name:			Name dictating if this is a day supply or quantity 		*
 *					column													*
 ****************************************************************************/
function changeQuantity(amount, colIndex, type) {
	var $rows = $("#Price-Table tbody tr");
	
	$rows.each(function(index, row) {
		$input = $(row).children("td").eq(colIndex).children("input:first");
		$input.val(amount.value);
		
		if (type === "supply") {
			priceUpdateDay($input);
		} else {
			priceUpdateQuantity($input);
		}
	});
	
	// Closes Popup
	$(amount).parent().parent().remove();
}

/****************************************************************************
 *	changeQuantityKeypress()	Adds keyboard functionality to popup		*
 *																			*
 *	e:				The triggering event									*
 *	amount:			The text input with the quantity						*
 *	buttonInput:	The submit button										*
 *	name:			The name of the column (days supply or quantity)		*
 ****************************************************************************/
function changeQuantityKeypress(amount, colIndex, type, e) {
	if (e.which == 13 || e.keycode == 13) {
		changeQuantity(amount, colIndex, type);
	} else if (e.which == 27 || e.keycode == 27) {
		closeQuantityPopup(undefined);
	} else {
		false;
	}
}

/****************************************************************************
 *	changeQuantity()	Updates all of a columns quantities/day supplies	*
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
	var colIndex = getElementIndex($cell, $cells);
	
	// Position cover div to fill entire page
	$coverDiv.attr("id", "Popup-Veil")
			 .height(pageHt)
			 .width(pageWid)
			 .on("click", function(e){closeQuantityPopup(e);})
			 .on("keydown", function(e) {changeQuantityKeypress(
				 inputText, colIndex, type, e);});
	
	// Popup div positions to left of trigger button
	$inputDiv.attr("id","Popup-Div")
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
					  inputText, colIndex, type);});
	
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
 *	brandUpdate()	Updates the Cost per Unit after a new brand is selected *
 *																			*
 *	brandSelect:	The select object that was changed.						*
 ****************************************************************************/
function brandUpdate(brandSelect) {
	var $row = $(brandSelect).closest("tr");
	var $costSpan = $row.find(".cost");
	var $brandOption = $(brandSelect).children("option:selected");
	var cost = $brandOption.attr("data-cost");
	var unit = $brandOption.attr("data-unit");
	var $daySupply = $row.find(".daySupply");
	var $quantity = $row.find(".quantity");
	var tempText;
	
	// Updates the cost/unit span
	tempText = "$" + cost + "<br>(per " + unit + ")";
	$costSpan.html(tempText)
			 .attr("data-cost", cost);
	
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
	var $row = $(input).closest("tr");
	var inputArray = $row.find("." + $(input).attr("class"));
	var index = getElementIndex(input, inputArray);
	var cost = Number($row.find(".cost").attr("data-cost")) ||
			   Number($row.find(".cost").val());
	var dosesPerDay = Number($row.find(".dosesPerDay").eq(index).val());
	var daySupply = Number($row.find(".daySupply").eq(index).val());
	var $priceSpan = $row.find(".dayPrice").eq(index);
	var price;
	
	// Determines cost
	 cost

	// Uses the determined index to calculate the price and update the span
	price = calculatePrice(dosesPerDay * daySupply * cost);
	price = Math.round(price * 100) / 100;
	
	$priceSpan.text("$" + price.toFixed(2))
			  .attr("data-price", price);
	
	// Updates the total price
	totalUpdate($priceSpan);
}

/****************************************************************************
 *	priceUpdateQuantity()	Updates the price for a "quantity" price span	*
 *																			*
 *	quantityInput:	the input that changed									*
 *	elemIndex:	the index of the trigger input (optional)					*
 *	cost:		the cost per unit for the applicable medication (optional)	*
 ****************************************************************************/
function priceUpdateQuantity(input) {
	var $row = $(input).closest("tr");
	var inputArray = $row.find("." + $(input).attr("class"));
	var index = getElementIndex(input, inputArray);
	var cost = Number($row.find(".cost").attr("data-cost")) ||
			   Number($row.find(".cost").val());
	var quantity = Number($row.find(".quantity").eq(index).val());
	var $priceSpan = $row.find(".quantityPrice").eq(index);
	var price;
	
	// Uses the determined index to calculate the price and update the span
	price = calculatePrice(quantity * cost);
	price = Math.round(price * 100) / 100;
	
	$priceSpan.text("$" + price.toFixed(2))
			  .attr("data-price", price);
	
	// Updates the total price
	totalUpdate($priceSpan);
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
							  .find("span").attr("data-price"));
		
		if (!isNaN(tempPrice) && tempPrice > 0) {
			finalTotal += tempPrice;
		}
	});
	
	$totalSpan.text("$" + finalTotal.toFixed(2));
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
	if (searchString.length > 0) {
		// 200 ms Timeout applied to prevent firing during typing
		clearTimeout(ajaxTimer);
		
		ajaxTimer = setTimeout(function() {
			$.ajax({
				url: "live_search.php",
				data: {q: searchString},
				type: "GET",
				dataType: "html",
				success: function (results) {
					$("#Search-Results").html(results);
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
		}, 200);
	} else {
		$("#Search-Results").empty();
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
	var query = $(selection).attr("data-id");
	showSearchResults("");
	
	$.ajax({
		url: "add_item.php",
		data: {q: query},
		type: "GET",
		dataType: "json",
		success: function (results) {
			processResult(results);
			
			// Reset search bar
			$("#Search-Bar").val("");
			$("#Search-Bar").focus();
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
 *	addLCA()	Adds an entry to the JSON array that identifies the LCA		*
 *																			*
 *	result:	the passed JSON array											*
 *																			*
 *	Returns a JSON array with the LCA entry added to the front				*
 ****************************************************************************/
function addLCA(result) {
	temp = {generic_name: result[0].generic_name,
			strength: result[0].strength,
			route: result[0].route,
			dosage_form: result[0].dosage_form,
			brand_name: "LCA",
			unit_price: result[0].unit_price,
			unit_issue: result[0].unit_issue};
	
	for (var i = 0; i < result.length; i++) {
		if (result[i].unit_price < temp.unit_price) {
			temp = {generic_name: result[i].generic_name,
					strength: result[i].strength,
					route: result[i].route,
					dosage_form: result[i].dosage_form,
					brand_name: "LCA",
					unit_price: result[i].unit_price,
					unit_issue: result[i].unit_issue};
		}
	}
	
	temp.brand_name = "LCA";
	result.unshift(temp);
	
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
	var $deleteCell = $("<td></td>");
	var $deleteButton = $("<span></span>");
	var $colDay = $("thead th.cellDay.cellPrice");
	var $colQuantity = $("thead th.cellQuantity.cellPrice");
	var $tempText;
	var $tempOption;
	
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
				
	
	$.each(results, function(index, value) {
		$tempOption = $("<option></option>");
		$tempOption.text(value.brand_name)
				   .attr("data-cost", value.unit_price)
				   .attr("data-unit", value.unit_issue)
				   .appendTo($brandSelect);
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
				 .on("keyup", function() {priceUpdateDay(this);});
			
	// Day Supply
	supplyInput.type = "text";
	$(supplyInput).addClass("daySupply")
				  .val("100")
				  .on("keyup", function() {priceUpdateDay(this);});
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
	
	// Delete
	$deleteButton.addClass("delete")
				 .html(" ")
				 .on("click", function() {removeRow(this);});
				 
	$deleteCell.append($deleteButton)
			   .appendTo($row);
			   
	//Adds row to table
	$tbody.append($row);
	
	// Calculates table values
	brandUpdate($brandSelect);
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
	var $printContent = $(printPage.body);
	var $css = $("<link></link>");
	
	var method = $("#Price-Table-Method").prop("selectedIndex");
	var pageNum = method === 0 ? 
	  $("#Price-Table thead th.cellDay.cellPrice").length :
	  $("#Price-Table thead th.cellQuantity.cellPrice").length;
	
	var h1;
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
	
	// Window Details
	$css.attr("rel", "stylesheet")
		.attr("type", "text/css")
		.attr("href", "http://www.studybuffalo.com/practicetools/include/abc_print.css?version=1.0")
		.appendTo($(printPage).find("head:first"));
		
	$(printPage).find("head:first").append($("<title>Medications Prices</title>"));
	
	// Cycle through the table rows and enter them into the print table
	for (var page = 0; page < pageNum; page++) {
		// Header
		$h1 = $("<h1></h1>");
		$h1.text(patientName === "" ? 
				 "Medication Price List" : 
				 "Medication Price List for " + patientName)
		   .appendTo($printContent);
		
		// Table Header
		$table = $("<table></table>");
		$table.appendTo($printContent);
		
		$thead = $("<thead></thead>");
		$thead.appendTo($table);
		
		$headRow = $("<tr></tr>");
		$headRow.html("<th>" + headMedication + "</th>" +
					  "<th>" + headQuantity + "</th>" +
					  "<th>" + headPrice + "</th>")
				.appendTo($thead);
		
		// Tabey Body
		$tbody = $("<tbody></tbody>");
		$tbody.appendTo($table);
		
		$rows.each(function(index, row) {
			$bodyRow = $("<tr></tr>");
			$bodyRow.appendTo($tbody);
			
			$row = $(row);
			
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
			
			$bodyMedication = $("<td></td>");
			$bodyMedication.append($("<strong></strong>").text(tempArray[0]))
						   .append($("<br>"))
						   .append($("<em></em>").text(tempArray[1]))
						   .appendTo($bodyRow);
						   
			// Day supply/Quantity
			$quantityData = method === 0 ? 
							$row.children().find("input.daySupply") :
							$row.children().find("input.quantity");
			$quantityData = $quantityData.eq(page).val();
			
			$bodyQuantity = $("<td></td>");
			$bodyQuantity.text($quantityData)
						 .appendTo($bodyRow);
						 
			// Price
			$priceData = method === 0 ?
						 $row.find(".cellDay.cellPrice span:first").text() :
						 $row.find(".cellQuantity.cellPrice span:first").text();
			
			$bodyPrice = $("<td></td>");
			$bodyPrice.text($priceData)
					  .appendTo($bodyRow);
		});
		
		// Footer
		$totalData = method === 0 ? 
			$("#Price-Table tfoot .cellDay span.total").eq(page).text() :
			$("#Price-Table tfoot .cellQuantity span.total").eq(page).text();
		
		$footTotal = $("<th></th>");
		$footTotal.text($totalData);
		
		$tfoot = $("<tfoot></tfoot>");
		$tfoot.append($("<th></th>"))
			  .append($("<th>TOTAL</th>"))
			  .append($footTotal)
			  .appendTo($table);
		
		// Disclaimer text
		$disclaimer.html("These medications costs are estimates based " +
						 "on the best available information. Actual " +
						 "costs may vary depending on your pharmacy " +
						 "and third-party drug coverage.<br><br>" +
						 "<i>Printed on: " + today + "</i>")
				   .appendTo($printContent);
		
		if (pageNum > 0) {
			$disclaimer.css("pageBreakAfter", "always");
		}
	}
	
	// Close document
	printPage.close()
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

	$("#Price-Table-Method").on(
		"change",
		function(){changePriceTableCols();});

	$("input.changeSupply").on(
		"click",
		function(){changeQuantityPopup(this, "supply");});

	$("input.changeQuantity").on(
		"click",
		function(){changeQuantityPopup(this, "quantity");});

	$("#Add-Freeform").on(
		"click",
		function(){addFreeformEntry();});
		
	$("#Print-Medication-Prices").on(
		"click",
		function(){printPrices();});

	$("#Search-Bar").focus();
	changePriceTableCols();
	});
	
var ajaxTimer;