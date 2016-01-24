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
	var elemIndex;
	
	for (var i = 0; i < elemArray.length; i++) {
		if (elem == elemArray[i]) {
			elemIndex = i;
			break;
		}
	}
	
	return elemIndex;
}

/****************************************************************************
 *	getRowIndex()		Finds the table row containg the provided element	*
 *																			*
 *	elemIndex:	The index of the element in element array for which to 		*
 *				determine the row for										*
 *	elemArray:	The array of elements which the elem belongs to.			*
 *																			*
 *	Returns the row index as an integer										*
 ****************************************************************************/
function getRowIndex(elemIndex, numRows) {
	var rowIndex;
	var rowIndex = elemIndex % numRows;
	return rowIndex;
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
	if (isNaN(drugPrice) || drugPrice === 0) {
		return 0;
	} else {
		var upcharge1 = 0.03;
		var upcharge2 = Date.now() < 1427868000000 ? 0.055 :
						Date.now() < 1459490400000 ? 0.06 :
						Date.now() < 1491026400000 ? 0.065 :
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
	var methodSelect = document.getElementById("Price-Table-Method");
	var methodIndex = methodSelect.selectedIndex;
	var table = document.getElementById("Price-Table");
	
	if (methodIndex === 0) {
		table.className = "methodDay";
	} else if (methodIndex === 1) {
		table.className = "methodQuantity";
	}
}

/****************************************************************************
 *	addFreeformEntry()	Adds input elements to allow user to enter freeform *
 *						medication prices.									*
 ****************************************************************************/
function addFreeformEntry() {
	var table = document.getElementById("Price-Table");
	var tbody = table.getElementsByTagName("tbody")[0];
	var row = document.createElement("tr");
	var medicationCell;
	var medicationInput = document.createElement("input");
	var brandCell;
	var brandSpan = document.createElement("span");
	var costCell;
	var costInput = document.createElement("input");
	var dosesCell;
	var dosesInput = document.createElement("input");
	var supplyCell;
	var supplyInput = document.createElement("input");
	var dayPriceCell;
	var dayPriceSpan = document.createElement("span");
	var quantityCell;
	var quantityInput = document.createElement("input");
	var quantityPriceCell;
	var quantityPriceSpan = document.createElement("span");
	var deleteCell;
	var deleteButton = document.createElement("span");
	var colDay = document.getElementsByName("Price-Table-Day-Count").length;
	var colQuantity = document.getElementsByName("Price-Table-Quantity-Count").length;
	var tempText;
	var tempOption;
	
	// Medication Name
	medicationInput.setAttribute("type", "text");
	
	medicationCell = row.insertCell();
	medicationCell.appendChild(medicationInput);
	
	// Brand Name
	brandSpan.setAttribute("name", "Price-Table-Brand");
	brandSpan.innerHTML = "N/A";
	
	brandCell = row.insertCell();
	brandCell.appendChild(brandSpan)
	
	// Cost
	costInput.setAttribute("type", "text");
	costInput.setAttribute("name", "Price-Table-Cost");
	costInput.addEventListener(
		"keyup",
		function() {costUpdate(this);},
		false);
	
	costCell = row.insertCell();
	costCell.appendChild(costInput);
	
	// Doses per day
	dosesInput.type= "text";
	dosesInput.setAttribute("name", "Price-Table-Doses");
	dosesInput.value = "1";
	dosesInput.addEventListener(
		"keyup",
		function() {priceUpdateDay(this);},
		false);
	
	// Day Supply
	supplyInput.type = "text";
	supplyInput.setAttribute("name", "Price-Table-Supply");
	supplyInput.value = "100";
	supplyInput.addEventListener(
		"keyup",
		function() {priceUpdateDay(this);},
		false);
	
	// Price
	dayPriceSpan.setAttribute("name", "Price-Table-Day-Price");
	
	for (var i = 0; i < colDay; i++) {
		dosesCell = row.insertCell();
		dosesCell.appendChild(dosesInput);
		dosesCell.className = "cellDay";
		
		supplyCell = row.insertCell();
		supplyCell.appendChild(supplyInput);
		supplyCell.className = "cellDay";
		
		dayPriceCell = row.insertCell();
		dayPriceCell.appendChild(dayPriceSpan);
		dayPriceCell.className = "cellDay cellPrice";
	}
	
	// Quantity
	quantityInput.type = "text";
	quantityInput.setAttribute("name", "Price-Table-Quantity");
	quantityInput.value = "100";
	quantityInput.addEventListener("keyup", function() {
		priceUpdateQuantity(this);
	});
	
	// Price
	quantityPriceSpan.setAttribute("name", "Price-Table-Quantity-Price");
		
	for (var i = 0; i < colQuantity; i++) {
		quantityCell = row.insertCell();
		quantityCell.appendChild(quantityInput);
		quantityCell.className = "cellQuantity";
		
		quantityPriceCell = row.insertCell();
		quantityPriceCell.appendChild(quantityPriceSpan);
		quantityPriceCell.className = "cellQuantity cellPrice";
	}
	
	// Delete
	deleteButton.className = "delete";
	deleteButton.innerHTML = " ";
	deleteButton.setAttribute("name", "Price-Table-Remove");
	deleteButton.addEventListener("click", function() {
		removeRow(this);
	});
	
	deleteCell = row.insertCell();
	deleteCell.appendChild(deleteButton);
	
	//Adds row to table
	tbody.appendChild(row);
	
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
	var popupDiv = document.getElementById("Popup-Veil");
	var changeButton = document.getElementById("Popup-Change");
	var closeButton = document.getElementById("Popup-Close");
	
	if (e.target === popupDiv || 
		e.target === changeButton ||
		e.target === closeButton ||
		e.target === undefined) {
		popupDiv.parentNode.removeChild(popupDiv);
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
function changeQuantity(amount, buttonInput, name) {
	var buttonArray;
	var inputArray;
	var elemIndex;
	var newValue;
	var table = document.getElementById("Price-Table");
	var numRows = table.getElementsByTagName("tbody")[0].rows.length;
	var index;
	
	if (name === "supply") {
		buttonArray = document.getElementsByName("Change-All-Supply-Button");
		newValue = document.getElementsByName("Change-All-Supply-Input");
		inputArray = document.getElementsByName("Price-Table-Supply");
	} else {
		buttonArray = document.getElementsByName("Change-All-Quantity-Button");
		newValue = document.getElementsByName("Change-All-Quantity-Input");
		inputArray = document.getElementsByName("Price-Table-Quantity");
	}
	
	elemIndex = getElementIndex(buttonInput, buttonArray);
	
	for (var i = 0; i < numRows; i++) {
		index = (elemIndex * numRows) + i;
		inputArray[i].value = amount.value;
		
		if (name === "supply") {
			priceUpdateDay(inputArray[i])
		} else {
			priceUpdateQuantity(inputArray[i])
		}
	}
	
	// Closes Popup
	document.body.removeChild(amount.parentNode.parentNode);
}

/****************************************************************************
 *	changeQuantityKeypress()	Adds keyboard functionality to popup		*
 *																			*
 *	e:				The triggering event									*
 *	amount:			The text input with the quantity						*
 *	buttonInput:	The submit button										*
 *	name:			The name of the column (days supply or quantity)		*
 ****************************************************************************/
function changeQuantityKeypress(e, amount, buttonInput, name) {
	if (e.which == 13 || e.keycode == 13) {
		changeQuantity(amount, buttonInput, name);
	} else if (e.which == 27 || e.keycode == 27) {
		closeQuantityPopup(buttonInput);
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
function changeQuantityPopup(buttonInput, name) {
	// Collect page, viewport, and element dimensions/coordinates
	var pageHt = Math.max(document.body.scrollHeight,
						  document.body.offsetHeight,
						  document.documentElement.clientHeight,
						  document.documentElement.offsetHeight);
	var pageWid = Math.max(document.body.scrollWidth,
						   document.body.offsetWidth,
						   document.documentElement.clientWidth,
						   document.documentElement.offsetWidth);
	var screenWid = window.innerWidth ||
					document.documentElement.clientWidth;
	var scrollHt = document.body.scrollTop ||
				   document.documentElement.scrollTop;
				   
	var buttonTop = buttonInput.getBoundingClientRect().top;
	var buttonLeft = buttonInput.getBoundingClientRect().left;
	
	var inputHt = 200;
	var inputWid = 300;
	var coverDiv = document.createElement("div");
	var inputDiv = document.createElement("div");
	var inputLabel = document.createElement("span");
	var inputText = document.createElement("input");
	var inputButton = document.createElement("input");
	var inputClose = document.createElement("input");
	
	// Position cover div to fill entire page
	coverDiv.id = "Popup-Veil";
	coverDiv.style.height = pageHt + "px";
	coverDiv.style.width = pageWid + "px";
	coverDiv.addEventListener(
		"click",
		function(e){closeQuantityPopup(e);},
		false);
	coverDiv.addEventListener(
		"keydown",
		function(e) {changeQuantityKeypress(e, inputText, inputButton, name);},
		false);
	
	// Popup div positions to left of trigger button
	inputDiv.id = "Popup-Div";
	inputDiv.style.minWidth = inputWid + "px";
	inputDiv.style.right = (screenWid - buttonLeft - 10) + "px";
	inputDiv.style.top = (scrollHt + buttonTop) + "px";
	
	// Creating popup window input elements
	inputLabel.innerHTML = "Enter new amount: ";
	
	inputText.setAttribute("type", "text");
	
	inputButton.setAttribute("type", "button")
	inputButton.id = "Popup-Change";
	inputButton.value = "Change Amounts";
	inputButton.addEventListener(
		"click",
		function(e) {changeQuantity(inputText, inputButton, name);},
		false);
	
	inputClose.setAttribute("type", "button")
	inputClose.id = "Popup-Close";
	inputClose.value = "Cancel";
	inputClose.addEventListener(
		"click",
		function(e){closeQuantityPopup(e);},
		false);
	
	// Assembling popup window
	inputDiv.appendChild(inputLabel);
	inputDiv.appendChild(inputText);
	inputDiv.appendChild(inputButton);
	inputDiv.appendChild(inputClose);
	coverDiv.appendChild(inputDiv);
	document.body.appendChild(coverDiv);
	
	// Bring focus to popup
	inputText.focus();
}

/****************************************************************************
 *	brandUpdate()	Updates the Cost per Unit after a new brand is selected *
 *																			*
 *	brandSelect:	The select object that was changed.						*
 ****************************************************************************/
function brandUpdate(brandSelect) {
	var brandArray = document.getElementsByName("Price-Table-Brand");
	var elemIndex = getElementIndex(brandSelect, brandArray);
	var costSpan = document.getElementsByName("Price-Table-Cost")[elemIndex];
	var selectIndex = brandSelect.selectedIndex;
	var brandOption = brandSelect.options[selectIndex];
	var cost = brandOption.dataset.cost;
	var unit = brandOption.dataset.unit;
	var table = document.getElementById("Price-Table");
	var numRows = table.getElementsByTagName("tbody")[0].rows.length;
	var dayCount = document.getElementsByName("Price-Table-Day-Count").length;
	var quantityCount = document.getElementsByName("Price-Table-Quantity-Count").length;
	var dayInput = document.getElementsByName("Price-Table-Doses");
	var quantityInput = document.getElementsByName("Price-Table-Quantity");
	var index;
	var tempText;
	
	// Updates the cost/unit span
	tempText = "$" + cost + "<br>(per " + unit + ")";
	costSpan.innerHTML = tempText;
	costSpan.dataset.cost = cost;
	
	// Updates day supply pricing
	for (var i = 0; i < dayCount; i++) {
		index = (i * numRows) + elemIndex;
		priceUpdateDay(dayInput[index], index, cost);
	}
	
	// Updates quantity pricing
	for (var i = 0; i < quantityCount; i++) {
		index = (i * numRows) + elemIndex;
		priceUpdateQuantity(quantityInput[index], index, cost);
	}
}

/****************************************************************************
 *	costUpdate()	Updates the price when the Cost per Unit is changed		*
 *																			*
 *	costInput:		The input object that was changed.						*
 ****************************************************************************/
function costUpdate(costInput) {
	var costArray = document.getElementsByName("Price-Table-Cost");
	var elemIndex = getElementIndex(costInput, costArray);
	
	var cost = costInput.value;
	
	var table = document.getElementById("Price-Table");
	var numRows = table.getElementsByTagName("tbody")[0].rows.length;
	var dayCount = document.getElementsByName("Price-Table-Day-Count").length;
	var quantityCount = document.getElementsByName("Price-Table-Quantity-Count").length;
	var dayInput = document.getElementsByName("Price-Table-Doses");
	var quantityInput = document.getElementsByName("Price-Table-Quantity");
	var index;
	var tempText;
	
	// Updates day supply pricing
	for (var i = 0; i < dayCount; i++) {
		index = (i * numRows) + elemIndex;
		priceUpdateDay(dayInput[index], index, cost);
	}
	
	// Updates quantity pricing
	for (var i = 0; i < quantityCount; i++) {
		index = (i * numRows) + elemIndex;
		priceUpdateQuantity(quantityInput[index], index, cost);
	}
}

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
function priceUpdateDay(input, elemIndex, cost) {
	var inputName = input.getAttribute("name");
	var inputArray;
	var dosesPerDay;
	var daySupply;
	var table = document.getElementById("Price-Table");
	var numRows = table.getElementsByTagName("tbody")[0].rows.length;
	var rowIndex;
	var costSpan;
	var price;
	var priceSpan = document.getElementsByName("Price-Table-Day-Price");
	var totalSpan = document.getElementsByName("Price-Table-Day-Total");
	
	// Determines elemIndex if not passed as argument
	if (elemIndex === undefined) {
		inputArray = document.getElementsByName(inputName);
		elemIndex = getElementIndex(input, inputArray);
	}
	
	rowIndex = getRowIndex(elemIndex, numRows);
	
	// Determines cost if not passed as argument
	if (cost === undefined) {
		costElement = document.getElementsByName("Price-Table-Cost")[rowIndex];
		cost = Number(costElement.dataset.cost) || Number(costElement.value);
	}
	
	// Gets input values
	dosesPerDay = document.getElementsByName("Price-Table-Doses");
	dosesPerDay = processDosesPerDay(dosesPerDay[elemIndex].value);
	
	daySupply = document.getElementsByName("Price-Table-Supply");
	daySupply = Number(daySupply[elemIndex].value);
	
	// Calcuates price
	price = calculatePrice(dosesPerDay * daySupply * cost);
	price = Math.round(price * 100) / 100;
	
	// Updates table
	priceSpan[elemIndex].innerHTML = "$" + price.toFixed(2);
	priceSpan[elemIndex].dataset.price = price;
	
	// Updates the total price
	totalUpdate(priceSpan, totalSpan, elemIndex, numRows);
}

/****************************************************************************
 *	priceUpdateQuantity()	Updates the price for a "quantity" price span	*
 *																			*
 *	quantityInput:	the input that changed									*
 *	elemIndex:	the index of the trigger input (optional)					*
 *	cost:		the cost per unit for the applicable medication (optional)	*
 ****************************************************************************/
function priceUpdateQuantity(quantityInput, elemIndex, cost) {
	var quantityArray;
	var quantity = quantityInput.value;
	var table = document.getElementById("Price-Table");
	var numRows = table.getElementsByTagName("tbody")[0].rows.length;
	var rowIndex;
	var costSpan;
	var price;
	var priceSpan = document.getElementsByName("Price-Table-Quantity-Price");
	var totalSpan = document.getElementsByName("Price-Table-Quantity-Total");
	
	// Determines elemIndex if not passed as argument
	if (elemIndex === undefined) {
		quantityArray = document.getElementsByName("Price-Table-Quantity");
		elemIndex = getElementIndex(quantityInput, quantityArray);
	}
	
	rowIndex = getRowIndex(elemIndex, numRows);
	
	// Determines cost if not passed as argument
	if (cost === undefined) {
		costElement = document.getElementsByName("Price-Table-Cost")[rowIndex];
		cost = Number(costElement.dataset.cost) || Number(costElement.value);
	}
	
	// Calcuates price
	price = calculatePrice(quantity * cost);
	price = Math.round(price * 100) / 100;
	
	// Updates table
	priceSpan[elemIndex].innerHTML = "$" + price.toFixed(2);
	priceSpan[elemIndex].dataset.price = price;
	
	// Updates the total price
	totalUpdate(priceSpan, totalSpan, elemIndex, numRows);
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
function totalUpdate(priceArray, totalSpan, elemIndex, numRows) {
	// Determines which column needs to be updated based on elemIndex
	var colIndex = Math.floor(elemIndex / numRows);
	var finalTotal = 0;
	var start = colIndex * numRows;
	var end = start + numRows;
	var tempPrice;
	
	totalSpan = totalSpan[colIndex];
	
	for (var i = start; i < end; i++) {
		tempPrice = priceArray[i].dataset.price;
		
		if (!isNaN(tempPrice) && tempPrice > 0) {
			finalTotal += Number(priceArray[i].dataset.price);
		}
	}
	
	totalSpan.innerHTML = "$" + finalTotal.toFixed(2);
}

/****************************************************************************
 *	removeRow()		Removes the row containing the clicked button	 		*
 *																			*
 *	deleteButton:	the button that was clicked								*
 ****************************************************************************/
function removeRow(deleteButton) {
	var buttonArray = document.getElementsByName("Price-Table-Remove");
	var table = document.getElementById("Price-Table") 
	var rows = table.getElementsByTagName("tbody")[0];
	var numRows;
	var dayPrice = document.getElementsByName("Price-Table-Day-Price");
	var dayTotal = document.getElementsByName("Price-Table-Day-Total");
	var quantityPrice = document.getElementsByName("Price-Table-Quantity-Price");
	var quantityTotal = document.getElementsByName("Price-Table-Quantity-Total");
	
	// Get index of button click
	rowIndex = getElementIndex(deleteButton, buttonArray);
	
	// Removes appropriate row
	rows.deleteRow(rowIndex);
	
	// Update numRows
	numRows = rows.rows.length;
	
	// Updates day supply pricing
	for (var i = 0; i < dayPrice.length; i += numRows) {
		totalUpdate(dayPrice, dayTotal, i, numRows);
	}
	
	// Updates quantity pricing
	for (var i = 0; i < quantityPrice.length; i += numRows) {
		totalUpdate(quantityPrice, quantityTotal, i, numRows);
	}
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
	// 200 ms Timeout applied to prevent firing during typing
	clearTimeout(ajaxTimer);
	
	ajaxTimer = setTimeout(function() {
		var searchResults = document.getElementById("Search-Results");
		
		if (searchString.length == 0)
		{
			searchResults.innerHTML = "";
			return;
		}
		
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
		} else {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
		
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				searchResults.innerHTML = xmlhttp.responseText;
			}
		}
		
		xmlhttp.open("GET","live_search.php?q=" + searchString, true);
		xmlhttp.send();
	}, 200);
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
	// Reset search bar
	var searchBar = document.getElementById("Search-Bar")
	showSearchResults("");
	searchBar.value = "";
	searchBar.focus();
	
	// Extract indices for MySQL query
	var query = selection.dataset.id;
	
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	} else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			// Processes the result and generate table row for insertion
			processResult(xmlhttp.responseText);
		}
	}
	
	xmlhttp.open("GET","add_item.php?q=" + query, true);
	xmlhttp.send();
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
function processResult(array) {
	var result = JSON.parse(array);
	var table = document.getElementById("Price-Table");
	var tbody = table.getElementsByTagName("tbody")[0];
	var row = document.createElement("tr");
	var medicationCell;
	var medicationStrong = document.createElement("strong");
	var medicationBr = document.createElement("br");
	var medicationEm = document.createElement("em");
	var brandCell;
	var brandSelect = document.createElement("select");
	var costCell;
	var costSpan = document.createElement("span");
	var dosesCell;
	var dosesInput = document.createElement("input");
	var supplyCell;
	var supplyInput = document.createElement("input");
	var dayPriceCell;
	var dayPriceSpan = document.createElement("span");
	var quantityCell;
	var quantityInput = document.createElement("input");
	var quantityPriceCell;
	var quantityPriceSpan = document.createElement("span");
	var deleteCell;
	var deleteButton = document.createElement("span");
	var colDay = document.getElementsByName("Price-Table-Day-Count").length;
	var colQuantity = document.getElementsByName("Price-Table-Quantity-Count").length;
	var tempText;
	var tempOption;
	
	// Add an entry to the result array for the LCA
	result = addLCA(result);
	
	// Medication Name
	medicationStrong.innerHTML = result[0].generic_name;
	medicationEm.innerHTML = result[0].strength + " " + result[0].route + 
							 " " + result[0].dosage_form;
	
	medicationCell = row.insertCell();
	medicationCell.appendChild(medicationStrong);
	medicationCell.appendChild(medicationBr);
	medicationCell.appendChild(medicationEm);
	
	// Brand Name
	brandSelect.setAttribute("name", "Price-Table-Brand");
	brandSelect.addEventListener("change", function() {
		brandUpdate(this);
	});
	
	for (var i = 0; i < result.length; i++) {
		tempOption = document.createElement("option");
		tempOption.text = result[i].brand_name;
		tempOption.dataset.cost = result[i].unit_price;
		tempOption.dataset.unit = result[i].unit_issue;
		brandSelect.appendChild(tempOption);
	}
	
	brandCell = row.insertCell();
	brandCell.appendChild(brandSelect);
	
	// Cost
	costSpan.setAttribute("name", "Price-Table-Cost");
	
	costCell = row.insertCell();
	costCell.appendChild(costSpan);
	
	// Doses per day
	dosesInput.type= "text";
	dosesInput.setAttribute("name", "Price-Table-Doses");
	dosesInput.value = "1";
	dosesInput.addEventListener("keyup", function() {
		priceUpdateDay(this);
	});
	
	// Day Supply
	supplyInput.type = "text";
	supplyInput.setAttribute("name", "Price-Table-Supply");
	supplyInput.value = "100";
	supplyInput.addEventListener("keyup", function() {
		priceUpdateDay(this);
	});
	
	// Price
	dayPriceSpan.setAttribute("name", "Price-Table-Day-Price");
	
	for (var i = 0; i < colDay; i++) {
		dosesCell = row.insertCell();
		dosesCell.appendChild(dosesInput);
		dosesCell.className = "cellDay";
		
		supplyCell = row.insertCell();
		supplyCell.appendChild(supplyInput);
		supplyCell.className = "cellDay";
		
		dayPriceCell = row.insertCell();
		dayPriceCell.appendChild(dayPriceSpan);
		dayPriceCell.className = "cellDay cellPrice";
	}
	
	// Quantity
	quantityInput.type = "text";
	quantityInput.setAttribute("name", "Price-Table-Quantity");
	quantityInput.value = "100";
	quantityInput.addEventListener("keyup", function() {
		priceUpdateQuantity(this);
	});
	
	// Price
	quantityPriceSpan.setAttribute("name", "Price-Table-Quantity-Price");
		
	for (var i = 0; i < colQuantity; i++) {
		quantityCell = row.insertCell();
		quantityCell.appendChild(quantityInput);
		quantityCell.className = "cellQuantity";
		
		quantityPriceCell = row.insertCell();
		quantityPriceCell.appendChild(quantityPriceSpan);
		quantityPriceCell.className = "cellQuantity cellPrice";
	}
	
	// Delete
	deleteButton.className = "delete";
	deleteButton.innerHTML = " ";
	deleteButton.setAttribute("name", "Price-Table-Remove");
	deleteButton.addEventListener("click", function() {
		removeRow(this);
	});
	
	deleteCell = row.insertCell();
	deleteCell.appendChild(deleteButton);
	
	//Adds row to table
	tbody.appendChild(row);
	
	// Calculates table values
	brandUpdate(brandSelect);
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
	var printPage = window.open();
	var printContent = printPage.document;
	var css = printContent.createElement("link");
	
	var method = document.getElementById("Price-Table-Method").selectedIndex;
	var pageNum = method === 0 ? 
				  document.getElementsByName("Price-Table-Day-Count").length :
				  document.getElementsByName("Price-Table-Quantity-Count").length;
	
	var h1 = printContent.createElement("h1");
	var patientName = document.getElementById("Patient-Name").value;
	
	var table = printContent.createElement("table");
	var thead = printContent.createElement("thead");
	var headRow = printContent.createElement("tr");
	var headMedication = printContent.createElement("th");
	var headQuantity = printContent.createElement("th");
	var headPrice = printContent.createElement("th");
	var tbody = printContent.createElement("tbody");
	var bodyRow;
	var bodyMedication;
	var bodyMedicationStrong;
	var bodyMedicationBr;
	var bodyMedicationEm;
	var bodyDoses;
	var bodySupply;
	var bodyQuantity;
	var bodyPrice;
	var tfoot = printContent.createElement("tfoot");
	var footRow = printContent.createElement("tr");
	var footTitle = printContent.createElement("th");
	var footPrice = printContent.createElement("th");
	var tableData = document.getElementById("Price-Table");
	var rowData = tableData.getElementsByTagName("tbody")[0].rows;
	var quantityData;
	var priceData;
	var totalData;
	var index;
	var tempData;
	
	var disclaimer = printContent.createElement("p");
	var lastUpdate = document.getElementById("Last-Update").innerHTML;
	var today = getTodaysDate();
	
	var tempText;
	var tempArray;
	
	// Window Details
	printContent.title = "Medications Prices";
	css.setAttribute("rel", "stylesheet");
	css.setAttribute("type", "text/css");
	css.setAttribute("href", "http://www.studybuffalo.com/practicetools/include/printStyle.css")
	printContent.getElementsByTagName("head")[0].appendChild(css);
	
	// Cycle through the table rows and enter them into the print table
	for (var page = 0; page < pageNum; page++) {
		// Header
		tempText = patientName === "" ? 
				   "Medication Price List" : 
				   "Medication Price List for " + patientName;
		h1.appendChild(printContent.createTextNode(tempText));
		printContent.body.appendChild(h1);
		
		// TABLE
		// Header Row
		headMedication.innerHTML = "Medication";
		headQuantity.innerHTML = method === 0 ? "Day Supply" : "Quantity";
		headPrice.innerHTML = "Price";
		
		headRow.appendChild(headMedication);
		headRow.appendChild(headQuantity);
		headRow.appendChild(headPrice);
		
		// Assemble Table Header
		thead.appendChild(headRow);
		table.appendChild(thead);
			
		if (method === 0) {
			quantityData = document.getElementsByName("Price-Table-Supply");
			priceData = document.getElementsByName("Price-Table-Day-Price");
			totalData = document.getElementsByName("Price-Table-Day-Total");
		} else {
			quantityData = document.getElementsByName("Price-Table-Quantity");
			priceData = document.getElementsByName("Price-Table-Quantity-Price");
			totalData = document.getElementsByName("Price-Table-Quantity-Total");
		}
		
		for (var i = 0; i < rowData.length; i++) {
			index = (page * rowData.length) + i;
			
			// Create table row and cells
			bodyRow = printContent.createElement("tr");
			
			// Medication Cell
			bodyMedication = bodyRow.insertCell();
			bodyMedicationStrong = printContent.createElement("strong");
			bodyMedicationBr = printContent.createElement("br");
			bodyMedicationEm = printContent.createElement("em");	
			tempData = rowData[i].cells[0].childNodes;
			tempArray = [];
			
			if (tempData.length === 1) {
				tempArray.push(printContent.createTextNode(tempData[0].value));
				tempArray.push(printContent.createTextNode(""));
			} else {
				tempArray.push(printContent.createTextNode(tempData[0].innerHTML));
				tempArray.push(printContent.createTextNode(tempData[2].innerHTML));
			}
			
			bodyMedicationStrong.appendChild(tempArray[0]);
			bodyMedicationEm.appendChild(tempArray[1]);
			
			bodyMedication.appendChild(bodyMedicationStrong);
			bodyMedication.appendChild(bodyMedicationBr);
			bodyMedication.appendChild(bodyMedicationEm);
			
			// Day Supply
			tempData = quantityData[index].value;
			
			bodySupply = bodyRow.insertCell();
			bodySupply.innerHTML = tempData;
			
			// Price Cell
			tempData = priceData[index].innerHTML;
			
			bodyPrice = bodyRow.insertCell();
			bodyPrice.innerHTML = tempData;
			
			// Append new row to table body
			tbody.appendChild(bodyRow);
		}
		
		// Assemble Table Body
		table.appendChild(tbody);
		
		// Footer
		footTitle.setAttribute("colspan", "2");
		footTitle.innerHTML = "TOTAL";
		footPrice.innerHTML = totalData[page].innerHTML;
		
		footRow.appendChild(footTitle);
		footRow.appendChild(footPrice);
		
		// Assemble Table Footer
		tfoot.appendChild(footRow);
		table.appendChild(tfoot);
		
		// Attach table to new window
		printContent.body.appendChild(table);
		
		// Disclaimer text
		disclaimer.innerHTML = "These medications costs are estimates based " +
							   "on the best available information. Actual " + 
							   "costs may vary depending on your pharmacy " + 
							   "and third-party drug coverage.<br><br>" +
							   "<i>Printed on: " + today + "</i>";
		
		if (pageNum > 0) {
			disclaimer.style.pageBreakAfter = "always";
		}		
		
		printContent.body.appendChild(disclaimer);
	}
	
	// Close document
	printPage.document.close()
}




 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/ 
//Adds event listeners
 document.addEventListener("DOMContentLoaded", function() {
	var searchBar = document.getElementById("Search-Bar")
	var searchSupport = eventSupported("onsearch");
	var trigger = searchSupport === true ? "search" : "keyup";
	
	searchBar.addEventListener(
		trigger,
		function(){showSearchResults(this.value);},
		false);
	
	document.getElementById("Price-Table-Method").addEventListener(
		"change",
		changePriceTableCols,
		false);
	
	document.getElementsByName("Change-All-Supply-Button")[0].addEventListener(
		"click",
		function(){changeQuantityPopup(this, "supply");},
		false);
	
	document.getElementsByName("Change-All-Quantity-Button")[0].addEventListener(
		"click",
		function(){changeQuantityPopup(this, "quantity");},
		false);
	
	document.getElementById("Add-Freeform").addEventListener(
		"click",
		function(){addFreeformEntry();},
		false);
	document.getElementById("Print-Medication-Prices").addEventListener(
		"click",
		printPrices,
		false);
	
	searchBar.focus();
	changePriceTableCols();
 });
var ajaxTimer;