"use strict";

/* globals Sentry */
// To compile via babel: // ./node_modules/.bin/babel <source file> -o <output file>
// Global variables
var ajaxTimer;
/**
 * Takes an event name and tests if it is valid in the users browser.
 *
 * @param {str} eventName the name of the event to be tested (including 'on').
 *
 * @param {bool} Returns true if supported, otherwise false.
 */

function eventSupported(eventName) {
  var testEl = document.createElement('input');
  testEl.type = 'text';
  var isSupported = eventName in testEl;

  if (!isSupported) {
    testEl.setAttribute(eventName, 'return;');
    isSupported = typeof testEl[eventName] === 'function';
  }

  testEl = null;
  return isSupported;
}
/**
 * Calculates the how much ABC will pay for a medication.
 *
 * @param {float} mac         Maximum allowable cost that will be paid by ABC.
 * @param {string} thirdParty String representing the ABC coverage to apply.
 *
 * @returns {float} Amount paid by the third party coverage.
 */


function calculateThirdParty(mac, thirdParty) {
  var patientPays;

  if (thirdParty === '1') {
    // http://www.health.alberta.ca/services/drugs-non-group.html
    // 70% coverage; $25.00 max per prescription; no annual maximum
    patientPays = mac * 0.30;
    patientPays = patientPays > 25 ? 25.00 : patientPays;
  } else if (thirdParty === '66') {
    // http://www.health.alberta.ca/services/drugs-seniors.html
    // 70% thirdParty; $25.00 max per prescription; no annual maximum
    patientPays = mac * 0.30;
    patientPays = patientPays > 25 ? 25.00 : patientPays;
  } else if (thirdParty === '20514') {
    // http://www.health.alberta.ca/services/drugs-palliative-care.html
    // 70% thirdParty; $25.00 max per prescription; no annual maximum
    patientPays = mac * 0.30;
    patientPays = patientPays > 25 ? 25.00 : patientPays;
  } else if (thirdParty === '19823') {
    // http://humanservices.alberta.ca/financial-support/2085.html
    // 100% thirdParty; no annual maximum
    patientPays = 0;
  } else if (thirdParty === '19823a') {
    // http://humanservices.alberta.ca/disability-services/aish.html
    // 100% thirdParty; no annual maximum
    patientPays = 0;
  } else if (thirdParty === '19824' || thirdParty === '20400' || thirdParty === '20401' || thirdParty === '20401' || thirdParty === '20403' || thirdParty === '22128') {
    // http://humanservices.alberta.ca/financial-support/2073.html
    // 100% thirdParty; no annual maximum
    patientPays = 0;
  } else if (thirdParty === '23609') {
    // http://humanservices.alberta.ca/financial-support/2076.html
    // 100% thirdParty; no annual maximum
    patientPays = 0;
  } else {
    patientPays = mac;
  }

  var thirdPartyPays = Math.round((mac - patientPays) * 100) / 100;
  return thirdPartyPays;
}
/**
 * Calculates the dispensing price of a medication
 *
 * Fee Calculation
 *   Upcharge #1:    3% of the drug cost.
 *   Upcharge #2:    7.0% of drug cost + upcharge #1 (to a maximum of $100.00).
 *   Dispensing Fee: A $12.15 dispensing fee is added on top of the noted upcharges.
 *
 * @param {float} costPerUnit The cost per unit for the medication.
 * @param {float} quantity    The number of units to be dispensed.
 *
 * @return {object} Object of the various fees and prices as float numbers.
 */


function calculateFees(costPerUnit, quantity) {
  var upcharge1 = 0.03;
  var upcharge2 = 0.07;
  var returnPrice = {
    drugCost: 0,
    upcharge1: 0,
    upcharge2: 0,
    dispensingFee: 0,
    grossPrice: 0
  }; // Calculates total gross price

  if (!Number.isNaN(costPerUnit) && costPerUnit > 0 && !Number.isNaN(quantity) && quantity > 0) {
    var drugPrice = costPerUnit * quantity;
    var fee1 = drugPrice * upcharge1;
    var fee2 = (drugPrice + fee1) * upcharge2;
    fee2 = fee2 > 100 ? 100 : fee2;
    var grossPrice = drugPrice + fee1 + fee2 + 12.15;
    returnPrice.drugCost = Math.round(drugPrice * 100) / 100;
    returnPrice.upcharge1 = Math.round(fee1 * 100) / 100;
    returnPrice.upcharge2 = Math.round(fee2 * 100) / 100;
    returnPrice.dispensingFee = Math.round(12.15 * 100) / 100;
    returnPrice.grossPrice = Math.round(grossPrice * 100) / 100;
  }

  return returnPrice;
}
/**
 * Calculates the total price of a medication.
 *
 * Fee Calculation
 *   Upcharge #1:    3% of the drug cost.
 *   Upcharge #2:    7.0% of drug cost + upcharge #1 (to a maximum of $100.00).
 *   Dispensing Fee: A $12.15 dispensing fee is added on top of the noted upcharges.
 *
 * @param {float} costPerUnit unit price of the medication.
 * @param {float} quantity    amount of medication.
 * @param {float} lca         least cost alternative of the medication.
 * @param {float} mac         maximum allowable cost of the medication.
 * @param {str}   thirdParty  third party coverage to apply.
 * @param {array} benefits    Array of strings of the benefits applicable to this drug.
 *
 * @returns {object} object of the various fees and prices as float numbers.
 */


function calculatePrice(costPerUnit, quantity, lca, mac, thirdParty, benefits) {
  var coverageMatch = false;
  var fees;
  var thirdPartyPays;
  var benefitResult;
  var returnPrice = {
    drugCost: 0,
    upcharge1: 0,
    upcharge2: 0,
    dispensingFee: 0,
    grossPrice: 0,
    thirdParty: 0,
    netPrice: 0,
    benefit: 'N/A'
  }; // Calculate total drug price

  var tempPrice = calculateFees(costPerUnit, quantity);
  returnPrice.drugCost = tempPrice.drugCost;
  returnPrice.upcharge1 = tempPrice.upcharge1;
  returnPrice.upcharge2 = tempPrice.upcharge2;
  returnPrice.dispensingFee = tempPrice.dispensingFee;
  returnPrice.grossPrice = tempPrice.grossPrice; // Calculates the third party pays amount

  if (thirdParty) {
    // Compares third party coverage against benefits to see if match
    for (var i = 0; i < benefits.length; i += 1) {
      if (thirdParty === benefits[i]) {
        coverageMatch = true;
      }
    } // Determine maximum the third party will pay


    var thirdPartyUnitPrice = 0;

    if (mac && lca) {
      thirdPartyUnitPrice = mac < lca ? mac : lca;
    } else if (mac) {
      thirdPartyUnitPrice = mac;
    } else if (lca) {
      thirdPartyUnitPrice = lca;
    } // Calculates the amount they will pay


    fees = calculateFees(thirdPartyUnitPrice, quantity); // Calculates net price based on coverage information

    if (coverageMatch === false) {
      thirdPartyPays = 0;
    } else {
      thirdPartyPays = calculateThirdParty(fees.grossPrice, thirdParty);
      returnPrice.thirdParty = thirdPartyPays;
    }
  } else {
    thirdPartyPays = 0;
  } // Determines if drug is a benefit or not


  if (thirdParty === '') {
    benefitResult = 'N/A';
  } else if (coverageMatch === false) {
    benefitResult = 'No';
  } else {
    benefitResult = 'Yes';
  }

  returnPrice.benefit = benefitResult; // Calculates the net price

  var netPrice = returnPrice.grossPrice - thirdPartyPays;
  returnPrice.netPrice = Math.round(netPrice * 100) / 100;
  return returnPrice;
}
/**
 * Returns today's date in YYYY-MM-DD format.
 *
 * @returns {str} Date in YYYY-MM-DD format.
 */


function getTodaysDate() {
  var today = new Date();
  var day = today.getDate();
  day = day < 10 ? "0".concat(day) : day;
  var month = today.getMonth() + 1;
  month = month < 10 ? "0".concat(month) : month;
  var year = today.getFullYear();
  return "".concat(year, "-").concat(month, "-").concat(day);
}
/**
 * Converts doses per day fraction inputs to a number
 *
 * @param {float} value: dosesPerDay input value to be converted.
 *
 * @returns {float} the number of doses per day.
 */


function processDosesPerDay(value) {
  var output;
  var match;
  var tempNums;

  if (Number.isNaN(value)) {
    match = value.match(/^\d+\/\d+$/);

    if (match) {
      tempNums = value.split('/');
      output = Number(tempNums[0]) / Number(tempNums[1]);
    }
  } else {
    output = value;
  }

  return output;
}
/**
 * Updates the relevant total price span.
 *
 * @param {object} $table a JQuery reference to the HTML table.
 */


function totalUpdate($table) {
  // Collect all the price divs and calculate the total price
  var $priceDivs = $table.find('.item-price');
  var finalTotal = 0;
  $priceDivs.each(function (index, div) {
    var price = Number($(div).find('div').attr('data-net-price'));

    if (!Number.isNaN(price) && price > 0) {
      finalTotal += price;
    }
  });
  $table.find('.item-total span').text("TOTAL $".concat(finalTotal.toFixed(2)));
}
/**
 * Updates the displayed price of a medication.
 *
 * @param {object} $item JQuery reference to the table row to upate.
 */


function priceUpdate($item) {
  // Get the appropriate brand/strength select
  var $select = $item.find('select').eq(0);
  var $option = $select.children('option:selected'); // Assemble list of benefits

  var benefits = [];

  if ($option.attr('data-group-1') === 'true') {
    benefits.push('1');
  }

  if ($option.attr('data-group-66') === 'true') {
    benefits.push('66');
  }

  if ($option.attr('data-group-19823') === 'true') {
    benefits.push('19823');
  }

  if ($option.attr('data-group-19823a') === 'true') {
    benefits.push('19823a');
  }

  if ($option.attr('data-group-19824') === 'true') {
    benefits.push('19824');
  }

  if ($option.attr('data-group-20400') === 'true') {
    benefits.push('20400');
  }

  if ($option.attr('data-group-20403') === 'true') {
    benefits.push('20403');
  }

  if ($option.attr('data-group-20514') === 'true') {
    benefits.push('20514');
  }

  if ($option.attr('data-group-22128') === 'true') {
    benefits.push('22128');
  }

  if ($option.attr('data-group-23609') === 'true') {
    benefits.push('23609');
  } // Calculate the price of this medication


  var cost = Number($item.find('.item-cost span').attr('data-unit-price')) || Number($item.find('.item-cost input').val()) || Number($item.find('.item-cost div').attr('data-unit-price'));
  var quantity = Number($item.find('.item-quantity input').val());
  var lca = $option.attr('data-lca-price');
  var mac = $option.attr('data-mac-price');
  var $table = $item.parent('.content').parent('div');
  var tableName = $table.attr('id');
  var $thirdParty = $("#".concat(tableName, "-third-party"));
  var thirdParty = $thirdParty.children('option:selected').val();
  var price = calculatePrice(cost, quantity, lca, mac, thirdParty, benefits); // Update the Price Div

  var $priceDiv = $item.find('.item-price div');
  $priceDiv.text("$".concat(price.netPrice.toFixed(2))).attr('data-drug-cost', price.drugCost).attr('data-upcharge-1', price.upcharge1).attr('data-upcharge-2', price.upcharge2).attr('data-dispensing-fee', price.dispensingFee).attr('data-gross-price', price.grossPrice).attr('data-third-party', price.thirdParty).attr('data-net-price', price.netPrice).attr('data-benefit', price.benefit); // Update the total price

  totalUpdate($table); // Updates class on the Info button

  var $infoButton = $item.find('.info');

  if (price.benefit === 'No') {
    $infoButton.attr('class', 'info warning');
  } else if ($option.attr('data-coverage-criteria') || $option.attr('data-special-authorizations')) {
    $infoButton.attr('class', 'info notice');
  } else {
    $infoButton.attr('class', 'info');
  }
}
/**
 * Updates the Cost per Unit after a new brand is selected.
 *
 * @param {object} brandSelect DOM reference to the select that was changed.
 */


function brandUpdate(brandSelect) {
  // Collect the relevant data values
  var $brandOption = $(brandSelect).children('option:selected');
  var unitPrice = $brandOption.attr('data-unit-price');
  var unit = $brandOption.attr('data-unit-issue') || 'unit'; // Updates the cost/unit span

  var $item = $(brandSelect).closest('.item');
  var $costSpan = $item.find('.item-cost span');
  $costSpan.attr('data-unit-price', unitPrice).text("$".concat(unitPrice));
  var $costEm = $item.find('.item-cost em');
  $costEm.text("per ".concat(unit)); // Update the total price

  priceUpdate($item);
}
/**
 * Updates comparison table prices based on selected strength
 *
 * @param {object} brandSelect DOM reference to the strength select to update.
 */


function comparisonStrength(strengthSelect) {
  // Collect the relevant data values
  var $strengthOption = $(strengthSelect).children('option:selected');
  var cost = $strengthOption.attr('data-cost'); // Updates the cost/unit span

  var $item = $(strengthSelect).closest('.item');
  var $costDiv = $item.find('.item-cost div');
  $costDiv.attr('data-cost', cost).text("$".concat(cost)); // Update the total price

  priceUpdate($item);
}
/**
 * Updates the prices in all columns based on new third party coverage.
 *
 * @param {object} table DOM reference to the table to be updated.
 */


function changeThirdParty(table) {
  // Get all the item divs
  var $table = $("#".concat(table));
  var $itemDivs = $table.find('.item'); // Cycle through each item div and update the price

  $itemDivs.each(function (index, item) {
    if (table === 'price-table') {
      var select = $(item).find('select').first();
      brandUpdate(select);
    } else if (table === 'comparison-table') {
      var _select = $(item).find('select').first();

      comparisonStrength(_select);
    }
  });
}
/**
 * Closes the popup window used to update column's quantities.
 *
 * @param {object} e Reference to triggering DOM element.
 */


function closeQuantityPopup(e) {
  var popupDiv = $('#Popup-Veil')[0];
  var closeButton = $('#close-change-popup')[0];

  if (e === undefined || e.target === popupDiv || e.target === closeButton) {
    $('#Popup-Veil').remove();
  }
}
/**
 * Updates the provided quantity field
 *
 * @param {object} input DOM reference to the input to update.
 */


function updateQuantity(input) {
  // Get the containing item div
  var $item = $(input).closest('.item'); // Calculate a new day quantity

  var doses = processDosesPerDay($item.find('.item-dose input').val());
  var supply = Number($item.find('.item-supply input').val());
  var quantity = 0;

  if (doses && !Number.isNaN(doses) && doses > 0 && supply && !Number.isNaN(supply) && supply > 0) {
    quantity = Math.round(doses * supply * 100) / 100;
  } // Update the quantity input


  $item.find('.item-quantity input').val(quantity); // Recalculate the total price

  priceUpdate($item);
}
/**
 * Updates all the day supply inputs.
 *
 * @param {object} table DOM reference to the table to update.
 */


function changeSupply(table) {
  var amount = $('#change-amount').val();
  var $items = $("#".concat(table)).find('.item');
  $items.each(function (index, item) {
    var $item = $(item);
    var $input = $item.find('.item-supply input');
    $input.val(amount); // Update the day supplies

    updateQuantity($input[0]);
  }); // Closes Popup

  $('#Popup-Veil').remove();
}
/**
 * Updates the day supply input.
 *
 * @param {object} input DOM reference to the day supply to update.
 */


function updateSupply(input) {
  // Get the containing item div
  var $item = $(input).closest('.item'); // Calculate a new day supply

  var doses = processDosesPerDay($item.find('.item-dose input').val());
  var quantity = Number($item.find('.item-quantity input').val());
  var supply = 0;

  if (doses && !Number.isNaN(doses) && doses > 0 && quantity && !Number.isNaN(quantity) && quantity > 0) {
    supply = Math.round(quantity / doses * 100) / 100;
  } // Update the supply input


  $item.find('.item-supply input').val(supply); // Recalculate the total price

  priceUpdate($item);
}
/**
 * Updates the quantities in an entire column.
 *
 * @param {str} table HTML ID of the table containing columns to update.
 */


function changeQuantity(table) {
  var amount = $('#change-amount').val();
  var $items = $("#".concat(table)).find('.item');
  $items.each(function (index, item) {
    var $item = $(item);
    var $input = $item.find('.item-quantity input');
    $input.val(amount); // Update the day supplies

    updateSupply($input[0]);
  }); // Closes Popup

  $('#Popup-Veil').remove();
}
/**
 * Updates all of a columns quantities/day supplies.
 *
 * @param {object} buttonInput DOM reference to the button that triggers the change.
 * @param {str}    name        The calculation method this button applies to.
 */


function changeQuantityPopup(buttonInput) {
  // Collect page, viewport, and element dimensions/coordinates
  var pageHt = $(document).height();
  var pageWid = $(document).width();
  var scrollHt = document.body.scrollTop || document.documentElement.scrollTop;
  var viewHt = $(window).height(); // Position cover div to fill entire page

  var $coverDiv = $('<div></div>');
  $coverDiv.attr('id', 'Popup-Veil').on('click', function (e) {
    closeQuantityPopup(e);
  }).height(pageHt).width(pageWid).prependTo('body'); // Position the popup in the center of the screen

  var inputHt = 300;
  var inputWid = 300;
  var inputLeft = (pageWid - inputWid) / 2;
  var inputTop = scrollHt + viewHt / 2 - inputHt / 2;
  var $popupDiv = $('<div></div>');
  $popupDiv.attr('id', 'Change-Popup').css({
    height: "".concat(inputHt, "px"),
    width: "".concat(inputWid, "px"),
    left: "".concat(inputLeft, "px"),
    top: "".concat(inputTop, "px")
  }).appendTo($coverDiv); // Instruction Text

  var $instruction = $('<div></div>');
  $instruction.text('Enter new day supply or quantity').appendTo($popupDiv); // Input Amount

  var $input = $('<input type="text">');
  $input.attr('id', 'change-amount');
  var $inputDiv = $('<div></div>');
  $inputDiv.append($input).appendTo($popupDiv); // Get the table name

  var tableName = $(buttonInput).closest('.footer').parent('div').attr('id'); // Change Day Supply

  var $buttonSupply = $('<input type="button">');
  $buttonSupply.attr('id', 'change-supply').on('click', function () {
    changeSupply(tableName);
  }).val('Change Day Supply');
  var $supplyDiv = $('<div></div>');
  $supplyDiv.append($buttonSupply).appendTo($popupDiv); // Change Quantity

  var $buttonQuantity = $('<input type="button">');
  $buttonQuantity.attr('id', 'change-quantity').on('click', function () {
    changeQuantity(tableName);
  }).val('Change Quantity');
  var $quantityDiv = $('<div></div>');
  $quantityDiv.append($buttonQuantity).appendTo($popupDiv); // Close Button

  var $buttonClose = $('<input type="button">');
  $buttonClose.attr('id', 'close-change-popup').on('click', function (e) {
    closeQuantityPopup(e);
  }).val('Cancel');
  var $closeDiv = $('<div></div>');
  $closeDiv.append($buttonClose).appendTo($popupDiv); // Bring focus to popup

  $input.focus();
}
/**
 * Closes the popup window generated to dispaly drug info.
 */


function closeInfoPopup() {
  var $popupDiv = $('#Popup-Veil');
  $popupDiv.remove();
}
/**
 * Generates popup showing additional info on the selected row.
 *
 * @param {object} infoButton DOM reference to the button that was clicked.
 */


function showInfo(infoButton) {
  var $infoButton = $(infoButton);
  var $item = $infoButton.closest('.item'); // Collect page, viewport, and element dimensions/coordinates

  var pageHt = $(document).height();
  var pageWid = $(document).width();
  var screenWid = $(window).width();
  var buttonTop = $infoButton.offset().top;
  var buttonLeft = $infoButton.offset().left; // Calculate pop-up width;

  var popupWid = screenWid < 600 ? screenWid - 20 : 580; // Calculate where to place the popup (center it if it can't fit by button)

  var divRight = 0;

  if (buttonLeft < popupWid + 10) {
    divRight = (screenWid - popupWid) / 2;
  } else {
    divRight = screenWid - buttonLeft - 10;
  } // Popup div positions to left of trigger button


  var $infoDiv = $('<div></div>');
  $infoDiv.attr('id', 'Info-Popup').css({
    right: "".concat(divRight, "px"),
    top: "".concat(buttonTop, "px"),
    width: "".concat(popupWid, "px")
  }); // The Pop-Up Div Title

  var $title = $('<h3></h3>');
  $title.text('Coverage Information').appendTo($infoDiv); // Benefit Type

  var $option = $item.find('select').children('option:selected');
  var coverageText = $option.attr('data-coverage-status');
  coverageText = coverageText || 'Not a benefit';
  var $coverage = $('<p></p>');
  $coverage.append($('<strong></strong>').text('Benefit Type: ')).append($('<span></span>').text(coverageText)).appendTo($infoDiv); // Check if any third party coverage is applied

  var tableName = $item.parent('.content').parent('div').attr('id');
  var $thirdPartySelect = $("#".concat(tableName, "-third-party"));
  var thirdParty = $thirdPartySelect.val(); // Add drug cost & MAC if the drug plan was selected

  if (thirdParty) {
    // Collect the relevant data
    var cost = $option.attr('data-unit-price');
    var lca = $option.attr('data-lca-price');
    var mac = $option.attr('data-mac-price');
    var unit = $option.attr('data-unit'); // Replaces unit with 'unit' if blank

    unit = unit || 'unit'; // Cost

    var $cost = $('<p></p>');
    $cost.append($('<strong></strong>').text('Cost: ')).append($('<span></span>').text("$".concat(cost, " per ").concat(unit))).appendTo($infoDiv); // LCA

    if (lca) {
      var $lca = $('<p></p>');
      $lca.append($('<strong></strong>').text('LCA: ')).append($('<span></span>').text("$".concat(lca, " per ").concat(unit))).appendTo($infoDiv);
    } // MAC


    if (mac) {
      var $mac = $('<p></p>');
      $mac.append($('<strong></strong>').text('MAC: ')).append($('<span></span>').text("$".concat(mac, " per ").concat(unit))).appendTo($infoDiv);
    }
  } // Add any coverage criteria
  // TODO: create a pop-up window to display criteria


  var criteria = [];

  if ($option.length) {
    criteria = JSON.parse($option.attr('data-coverage-criteria'));
  }

  if (criteria.length) {
    var priceID = $option.attr('data-price-id');
    var $criteria = $('<a></a>');
    $criteria.text('Click here for coverage criteria').attr('target', '_blank').attr('rel', 'noopener').attr('href', "/tools/drug-price-calculator/coverage-criteria/".concat(priceID, "/"));
    var $criteriaP = $('<p></p>');
    $criteriaP.append($criteria).appendTo($infoDiv).css('margin-top: 0.5em;');
  } // Price Information


  var $feeTitle = $('<p></p>');
  $feeTitle.append($('<strong></strong>').text('Price Breakdown')).addClass('MT1em').appendTo($infoDiv); // Drug Costs & Fees Table

  var $feeTable = $('<table></table>');
  $feeTable.appendTo($infoDiv); // Drug Costs

  var $price = $item.find('.item-price > div');
  var drugCost = Number($price.attr('data-drug-cost'));
  drugCost = Number.isNaN(drugCost) ? '$0.00' : "".concat(drugCost.toFixed(2));
  var $feeDrug = $('<tr></tr>');
  $feeDrug.append($('<td></td>').text('Drug Cost:')).append($('<td></td>')).append($('<td></td>').text(drugCost)).appendTo($feeTable); // Upcharge #1

  var upcharge1 = Number($price.attr('data-upcharge-1'));
  upcharge1 = Number.isNaN(upcharge1) ? '$0.00' : "$".concat(upcharge1.toFixed(2));
  var $feeUpcharge1 = $('<tr></tr>');
  $feeUpcharge1.append($('<td></td>').text('Upcharge #1:')).append($('<td></td>').text('+')).append($('<td></td>').text(upcharge1)).appendTo($feeTable); // Upcharge #2

  var upcharge2 = Number($price.attr('data-upcharge-2'));
  upcharge2 = Number.isNaN(upcharge2) ? '$0.00' : "$".concat(upcharge2.toFixed(2));
  var $feeUpcharge2 = $('<tr></tr>');
  $feeUpcharge2.append($('<td></td>').text('Upcharge #2:')).append($('<td></td>').text('+')).append($('<td></td>').text(upcharge2)).appendTo($feeTable); // Dispensing Fee

  var dispensingFee = Number($price.attr('data-dispensing-fee'));
  dispensingFee = Number.isNaN(dispensingFee) ? '$0.00' : "$".concat(dispensingFee.toFixed(2));
  var $feeDispensing = $('<tr></tr>');
  $feeDispensing.append($('<td></td>').text('Dispensing Fee:')).append($('<td></td>').text('+')).append($('<td></td>').text(dispensingFee)).appendTo($feeTable); // Gross Price

  var gross = Number($price.attr('data-gross-price'));
  gross = Number.isNaN(gross) ? '$0.00' : "$".concat(gross.toFixed(2));
  var $feeGross = $('<tr></tr>');
  $feeGross.append($('<td></td>').text('Sub-Total:')).append($('<td></td>')).append($('<td></td>').text(gross)).addClass('totalRow').appendTo($feeTable); // Third Party Portion

  var tp = Number($price.attr('data-third-party'));
  tp = Number.isNaN(tp) ? '$0.00' : "$".concat(tp.toFixed(2));
  var $feeTP = $('<tr></tr>');
  $feeTP.append($('<td></td>').text('Third Party Portion:')).append($('<td></td>').text('-')).append($('<td></td>').text(tp)).appendTo($feeTable); // Net Total

  var net = Number($price.attr('data-net-price'));
  net = Number.isNaN(net) ? '$0.00' : "$".concat(net.toFixed(2));
  var $feeNet = $('<tr></tr>');
  $feeNet.append($('<td></td>').text('Patient Pays:')).append($('<td></td>')).append($('<td></td>').text(net)).addClass('totalRow').appendTo($feeTable); // Special Authorization Form Links

  var $saFormTitle = $('<p></p>');
  var $saForm = $('<ul></ul>');
  var specialAuthorizations = [];

  if ($option.length) {
    specialAuthorizations = JSON.parse($option.attr('data-special-authorizations'));
  } // If special authorizations present, add title


  if (specialAuthorizations.length) {
    $saFormTitle.append($('<strong></strong>').text('Special Authorization Forms')).addClass('MT1em').appendTo($infoDiv);
    $saForm.appendTo($infoDiv);
  } // Add any forms


  specialAuthorizations.forEach(function (special) {
    var $saFormA = $('<a></a>');
    $saFormA.text(special.pdf_title).attr('href', "https://idbl.ab.bluecross.ca/idbl/DBL/".concat(special.file_name)).attr('target', '_blank').attr('rel', 'noopner');
    $('<li></li>').append($saFormA).appendTo($saForm);
  }); // Close Button

  var $close = $('<div></div>');
  $close.attr('class', 'close').appendTo($infoDiv);
  var $closeButton = $('<input type="button">');
  $closeButton.val('Close').on('click', function () {
    closeInfoPopup();
  }).appendTo($close); // Position cover div to fill entire page

  var $coverDiv = $('<div></div>');
  $coverDiv.attr('id', 'Popup-Veil').height(pageHt).width(pageWid).on('click', function (e) {
    closeQuantityPopup(e);
  }).prependTo('body').append($infoDiv);
}
/**
 * Removes the row containing the clicked button
 *
 * @param {object} deleteButton DOM reference of the button that was clicked.
 */


function removeRow(deleteButton) {
  // Removes row
  var $item = $(deleteButton).closest('.item');
  $item.remove(); // Updates total prices

  var $table = $item.closest('.content').parent('div');
  totalUpdate($table);
}
/**
 * Adds input elements to allow user to enter freeform medication prices.
 */


function addFreeformEntry() {
  // Generate a unique ID for element IDs
  var id = new Date().getTime().toString(36) + Math.random().toString(36); // Set up containers

  var $content = $('#price-table .content:first');
  var $item = $('<div></div>');
  $item.addClass('item'); // Medication Name

  var medicationID = "medication-".concat(id);
  var $medicationLabel = $('<label></label>');
  $medicationLabel.attr('for', medicationID).text('Medication');
  var $medicationInput = $('<input type="text">');
  $medicationInput.attr('id', medicationID);
  var $medication = $('<div></div>');
  $medication.addClass('item-medication').append($medicationLabel, $medicationInput).appendTo($item); // Brand Name

  var brandID = "brand-".concat(id);
  var $brandLabel = $('<label></label>');
  $brandLabel.attr('for', brandID).text('Brand');
  var $brandDiv = $('<div></div>');
  $brandDiv.attr('id', brandID).text('N/A');
  var $brand = $('<div></div>');
  $brand.addClass('item-brand').append($brandLabel, $brandDiv).appendTo($item); // Cost Per Unit

  var costID = "cost-".concat(id);
  var $costLabel = $('<label></label>');
  $costLabel.attr('for', costID).text('Cost Per Unit');
  var $costInput = $('<input type="text">');
  $costInput.attr('id', costID);
  var $cost = $('<div></div>');
  $cost.addClass('item-cost').on('keyup', function (e) {
    updateQuantity(e.target);
  }).append($costLabel, $costInput).appendTo($item); // Does Per Day

  var doseID = "doses-".concat(id);
  var $doseLabel = $('<label></label>');
  $doseLabel.attr('for', doseID).text('Doses Per Day');
  var $doseInput = $('<input type="text">');
  $doseInput.attr('id', doseID).on('keyup', function (e) {
    updateQuantity(e.target);
  }).val(1);
  var $dose = $('<div></div>');
  $dose.addClass('item-dose').append($doseLabel, $doseInput).appendTo($item); // Day Supply

  var supplyID = "supply-".concat(id);
  var $supplyLabel = $('<label></label>');
  $supplyLabel.attr('for', supplyID).text('Day Supply');
  var $supplyInput = $('<input type="text">');
  $supplyInput.attr('id', supplyID).on('keyup', function (e) {
    updateQuantity(e.target);
  }).val(100);
  var $supply = $('<div></div>');
  $supply.addClass('item-supply').append($supplyLabel, $supplyInput).appendTo($item); // Quantity

  var quantityID = "quantity-".concat(id);
  var $quantityLabel = $('<label></label>');
  $quantityLabel.attr('for', quantityID).text('Quantity');
  var $quantityInput = $('<input type="text">');
  $quantityInput.attr('id', quantityID).on('keyup', function (e) {
    updateSupply(e.target);
  }).val(100);
  var $quantity = $('<div></div>');
  $quantity.addClass('item-quantity').append($quantityLabel, $quantityInput).appendTo($item); // Price

  var priceID = "price-".concat(id);
  var $priceLabel = $('<label></label>');
  $priceLabel.attr('for', priceID).text('Price');
  var $priceDiv = $('<div></div>');
  $priceDiv.attr('id', priceID);
  var $price = $('<div></div>');
  $price.addClass('item-price').append($priceLabel, $priceDiv).appendTo($item); // Info and Delete Buttons

  var $infoButton = $('<input type="button">');
  $infoButton.addClass('info').on('click', function (e) {
    showInfo(e.target);
  }).val('Information');
  var $deleteButton = $('<input type="button">');
  $deleteButton.addClass('delete').on('click', function (e) {
    removeRow(e.target);
  }).val('Delete');
  var $buttons = $('<div></div>');
  $buttons.addClass('item-buttons').append($infoButton, $deleteButton).appendTo($item); // Add the completed $item to the $content container

  $content.append($item);
}
/**
 * Adds an entry to the JSON array that identifies the LCA.
 *
 * @param {object} result The passed JSON array.
 *
 * @returns {array} JSON array with the LCA entry added to the front.
 */


function addLCA(results) {
  // Identify the lowest cost drug
  var lowestPrice = results[0].unit_price;
  var lowestIndex = 0;
  results.forEach(function (result, index) {
    if (result.unit_price < lowestPrice) {
      lowestPrice = result.unit_price;
      lowestIndex = index;
    }
  }); // Return the LCA entry and update brand name

  var lcaEntry = JSON.parse(JSON.stringify(results[lowestIndex]));
  lcaEntry.drug.brand_name = 'LCA'; // Adds LCA entry to front of array

  results.unshift(lcaEntry);
  return results;
}
/**
 * Takes passed JSON array and formats all the data to insert into Price-Table.
 *
 * @param {array} array JSON array containing the data to insert.
 */


function processResult(originalResults) {
  // Add an entry to the result array for the LCA
  var results = addLCA(originalResults); // Generate a unique ID for element IDs

  var id = new Date().getTime().toString(36) + Math.random().toString(36); // Set up containers

  var $content = $('#price-table .content:first');
  var $item = $('<div></div>');
  $item.addClass('item'); // Medication Name

  var medicationID = "medication-".concat(id);
  var $medicationLabel = $('<label></label>');
  $medicationLabel.attr('for', medicationID).text('Medication');
  var $medicationStrong = $('<strong></strong>');
  $medicationStrong.text(results[0].drug.generic_name);
  var medEmText = '';
  medEmText += results[0].drug.strength ? "".concat(results[0].drug.strength, " ") : '';
  medEmText += results[0].drug.route ? "".concat(results[0].drug.route, " ") : '';
  medEmText += results[0].drug.dosage_form ? "".concat(results[0].drug.dosage_form, " ") : '';
  medEmText = medEmText.trim();
  var $medicationEm = $('<em></em>');
  $medicationEm.text(medEmText);
  var $medicationDiv = $('<div></div>');
  $medicationDiv.attr('id', medicationID).append($medicationStrong, $medicationEm);
  var $medication = $('<div></div>');
  $medication.addClass('item-medication').append($medicationLabel, $medicationDiv).appendTo($item); // Brand Name

  var brandID = "brand-".concat(id);
  var $brandLabel = $('<label></label>');
  $brandLabel.attr('for', brandID).text('Brand');
  var $brandSelect = $('<select></select>');
  $brandSelect.attr('id', brandID).on('change', function (e) {
    brandUpdate(e.currentTarget);
  });
  $.each(results, function (index, value) {
    var $tempOption = $('<option></option>');
    $tempOption.text(value.drug.brand_name).attr('data-price-id', value.id).attr('data-unit-price', value.unit_price).attr('data-unit-issue', value.unit_issue).attr('data-lca-price', value.lca_price).attr('data-mac-price', value.mac_price).attr('data-mac-text', value.mac_text).attr('data-group-1', value.clients.group_1).attr('data-group-66', value.clients.group_66).attr('data-group-66a', value.clients.group_66a).attr('data-group-19823', value.clients.group_19823).attr('data-group-19823a', value.clients.group_19823a).attr('data-group-19824', value.clients.group_19824).attr('data-group-20400', value.clients.group_20400).attr('data-group-20403', value.clients.group_20403).attr('data-group-20514', value.clients.group_20514).attr('data-group-22128', value.clients.group_22128).attr('data-group-23609', value.clients.group_23609).attr('data-coverage-status', value.coverage_status).attr('data-special-authorizations', JSON.stringify(value.special_authorizations)).attr('data-coverage-criteria', JSON.stringify(value.coverage_criteria)).appendTo($brandSelect);
  });
  var $brand = $('<div></div>');
  $brand.addClass('item-brand').append($brandLabel, $brandSelect).appendTo($item); // Cost Per Unit

  var costID = "cost-".concat(id);
  var $costLabel = $('<label></label>');
  $costLabel.attr('for', costID).text('Cost Per Unit');
  var $costSpan = $('<span></span>');
  var $costEm = $('<em></em>');
  var $costDiv = $('<div></div>');
  $costDiv.attr('id', costID).append($costSpan, $costEm);
  var $cost = $('<div></div>');
  $cost.addClass('item-cost').append($costLabel, $costDiv).appendTo($item); // Does Per Day

  var doseID = "doses-".concat(id);
  var $doseLabel = $('<label></label>');
  $doseLabel.attr('for', doseID).text('Doses Per Day');
  var $doseInput = $('<input type="text">');
  $doseInput.attr('id', doseID).on('keyup', function (e) {
    updateQuantity(e.target);
  }).val(1);
  var $dose = $('<div></div>');
  $dose.addClass('item-dose').append($doseLabel, $doseInput).appendTo($item); // Day Supply

  var supplyID = "supply-".concat(id);
  var $supplyLabel = $('<label></label>');
  $supplyLabel.attr('for', supplyID).text('Day Supply');
  var $supplyInput = $('<input type="text">');
  $supplyInput.attr('id', supplyID).on('keyup', function (e) {
    updateQuantity(e.target);
  }).val(100);
  var $supply = $('<div></div>');
  $supply.addClass('item-supply').append($supplyLabel, $supplyInput).appendTo($item); // Quantity

  var quantityID = "quantity-".concat(id);
  var $quantityLabel = $('<label></label>');
  $quantityLabel.attr('for', quantityID).text('Quantity');
  var $quantityInput = $('<input type="text">');
  $quantityInput.attr('id', quantityID).on('keyup', function (e) {
    updateSupply(e.target);
  }).val(100);
  var $quantity = $('<div></div>');
  $quantity.addClass('item-quantity').append($quantityLabel, $quantityInput).appendTo($item); // Price

  var priceID = "price-".concat(id);
  var $priceLabel = $('<label></label>');
  $priceLabel.attr('for', priceID).text('Price');
  var $priceDiv = $('<div></div>');
  $priceDiv.attr('id', priceID);
  var $price = $('<div></div>');
  $price.addClass('item-price').append($priceLabel, $priceDiv).appendTo($item); // Info and Delete Buttons

  var $infoButton = $('<input type="button">');
  $infoButton.addClass('info').on('click', function (e) {
    showInfo(e.currentTarget);
  }).val('Information');
  var $deleteButton = $('<input type="button">');
  $deleteButton.addClass('delete').on('click', function (e) {
    removeRow(e.target);
  }).val('Delete');
  var $buttons = $('<div></div>');
  $buttons.addClass('item-buttons').append($infoButton, $deleteButton).appendTo($item); // Add the completed $item to the $content container

  $content.append($item); // Calculate the default price values for table

  brandUpdate($brandSelect);
}
/**
 * Function handling the API call retrieve the selected product information.
 *
 * @param {object} selection DOM reference to the search result clicked.
 */


function chooseResult(selection) {
  // eslint-disable-line no-unused-vars
  // Extract indices for MySQL query
  var queryIDs = $(selection).attr('data-ids');
  showSearchResults(''); // eslint-disable-line no-use-before-define

  $.ajax({
    url: '/api/drug-price-calculator/v1/drugs/prices/',
    data: {
      ids: queryIDs
    },
    type: 'GET',
    dataType: 'json',
    success: function success(results) {
      processResult(results); // Reset search bar

      $('#Search-Bar').val('');
      $('#Search-Bar').focus();
    },
    error: function error(jqXHR, textStatus, errorThrown) {
      Sentry.captureException(errorThrown);
      var error = 'Sorry we have experienced an error with our server. Please refresh your page and try ' + 'again. If you continue to run into issues, please contact us at ' + 'studybuffalo@studybuffalo.com';
      var $searchResults = $('#Search-Results');
      $searchResults.html("<span style=\"color: red\">".concat(error, "</span>"));
    }
  });
}
/**
 * Formats the array of search results for search result list.
 *
 * @param {array} results Array of search results.
 *
 * @results {string} The HTML search results
 */


function formatSearchResults(results) {
  if (results.length === 0) {
    return '<span>No results found</span>';
  } // Group together the common drug names


  var compiledResults = {};
  results.forEach(function (drug) {
    // If key not in object, add it
    if (!(drug.generic_product in compiledResults)) {
      compiledResults[drug.generic_product] = {
        ids: [],
        generic_product: drug.generic_product,
        brand_names: new Set()
      };
    } // Add the IDs and brand name to array


    compiledResults[drug.generic_product].ids.push(drug.id);
    compiledResults[drug.generic_product].brand_names.add(drug.brand_name);
  }); // Generate the HTML search list

  var $list = $('<ul></ul>');
  Object.keys(compiledResults).forEach(function (key, index) {
    var $item = $('<li></li>').appendTo($list);
    var $link = $('<a></a>').appendTo($item).attr('id', "Search-Result-".concat(index)).attr('data-ids', compiledResults[key].ids.join(',')).on('click', function (e) {
      chooseResult(e.currentTarget);
    });
    $('<strong></strong>').appendTo($link).text(compiledResults[key].generic_product);
    $('<br>').appendTo($link);
    $('<em></em>').appendTo($link).text("also known as ".concat(Array.from(compiledResults[key].brand_names).join(', ')));
  });
  return $list;
}
/**
 * Function handling API call to retieve search results.
 *
 * @param {object} searchString Search string to query against.
 *
 */


function showSearchResults(searchString) {
  var $searchResults = $('#Search-Results');

  if (searchString) {
    // 200 ms Timeout applied to prevent firing during typing
    clearTimeout(ajaxTimer);
    ajaxTimer = setTimeout(function () {
      $.ajax({
        url: '/api/drug-price-calculator/v1/drugs/',
        data: {
          q: searchString,
          page: 1
        },
        type: 'GET',
        dataType: 'json',
        success: function success(results) {
          var searchList = formatSearchResults(results.results);

          if ($('#Search-Bar').val() === searchString) {
            $searchResults.html(searchList);
          }
        },
        error: function error() {
          var error = 'Sorry we have experienced an error with our server. Please refresh your page and ' + 'try again. If you continue to run into issues, please contact us at ' + 'studybuffalo@studybuffalo.com';
          $searchResults.html("<span style=\"color: red\">".concat(error, "</span>"));
        }
      });
    }, 0);
  } else {
    $searchResults.empty();
  }
}
/**
 * Function handling the API call to the database to retieve the search results.
 *
 * @param {str} searchString Text entered into the search bar.
 */


function showComparisonResults(searchString) {
  var $searchResults = $('#Comparison-Results');
  var searchMethod1 = !!$('#Comparison-Search-Method-1')[0].checked;
  var searchMethod2 = !!$('#Comparison-Search-Method-2')[0].checked;

  if (searchString.length > 0) {
    // 300 ms Timeout applied to prevent firing during typing
    clearTimeout(ajaxTimer);
    ajaxTimer = setTimeout(function () {
      $.ajax({
        url: 'comparison-search/',
        data: {
          search: searchString,
          methodATC: searchMethod1,
          methodPTC: searchMethod2
        },
        type: 'GET',
        dataType: 'html',
        success: function success(results) {
          // Only updates if search string hasn't changed
          if ($('#Comparison-Search').val() === searchString) {
            $searchResults.html(results);
          }
        },
        error: function error() {
          $searchResults.empty();
        }
      });
    }, 300);
  } else {
    $searchResults.empty();
  }
}
/**
 * Takes passed JSON array and formats all the data to insert into Comparison-Table.
 *
 * @param {array} results JSON array containing the data to insert.
 */


function processComparison(results) {
  var _this = this;

  // Reset the contents
  var $content = $('#comparison-table .content');
  $content.html(''); // Cycles through the results to generate the HTML content

  $.each(results, function (index, value) {
    // Generate a unique ID for element IDs
    var id = new Date().getTime().toString(36) + Math.random().toString(36); // Create the item dive to contain the content

    var $item = $('<div></div>');
    $item.addClass('item').appendTo($content); // Medication Name

    var medicationID = "medication-".concat(id);
    var $medicationLabel = $('<label></label>');
    $medicationLabel.attr('for', medicationID).text('Medication');
    var $medicationDiv = $('<div></div>');
    $medicationDiv.attr('id', medicationID).text(value.generic_name);
    var $medication = $('<div></div>');
    $medication.addClass('item-medication').append($medicationLabel, $medicationDiv).appendTo($item); // Strength

    var strengthID = "strength-".concat(id);
    var $strengthLabel = $('<label></label>');
    $strengthLabel.attr('for', strengthID).text('Strength');
    var $strengthSelect = $('<select></select>');
    $strengthSelect.attr('id', strengthID).on('change', function () {
      comparisonStrength(_this);
    });
    var $strength = $('<div></div>');
    $strength.addClass('item-strength').append($strengthLabel, $strengthSelect).appendTo($item); // Add the various strengths to the select

    $.each(value.strength, function (strengthIndex, temp) {
      var $strengthOption = $('<option></option>');
      $strengthOption.text(temp.strength).attr('data-cost', temp.unit_price).attr('data-mac', temp.lca ? temp.lca : temp.unit_price).attr('data-coverage', temp.coverage).attr('data-criteria', temp.criteria).attr('data-criteria-p', temp.criteria_p).attr('data-criteria-sa', temp.criteria_sa).attr('data-group-1', temp.group_1).attr('data-group-66', temp.group_66).attr('data-group-66a', temp.group_66a).attr('data-group-19823', temp.group_19823).attr('data-group-19823a', temp.group_19823a).attr('data-group-19824', temp.group_19824).attr('data-group-20400', temp.group_20400).attr('data-group-20403', temp.group_20403).attr('data-group-20514', temp.group_20514).attr('data-group-22128', temp.group_22128).attr('data-group-23609', temp.group_23609).appendTo($strengthSelect); // Generates format for special auth data objects

      $.each(temp.special_auth, function (specialIndex, temp2) {
        // Add the title
        var attributeName = "data-special-auth-title-".concat(specialIndex + 1);
        var attributeValue = temp2.title;
        $strengthOption.attr(attributeName, attributeValue); // Add the link

        attributeName = "data-special-auth-link-".concat(specialIndex + 1);
        attributeValue = temp2.link;
        $strengthOption.attr(attributeName, attributeValue);
      });
    }); // LCA Cost

    var lcaID = "lca-".concat(id);
    var $lcaLabel = $('<label></label>');
    $lcaLabel.attr('for', lcaID).text('LCA');
    var $lcaDiv = $('<div></div>');
    $lcaDiv.attr('id', lcaID);
    var $lca = $('<div></div>');
    $lca.addClass('item-cost').append($lcaLabel, $lcaDiv).appendTo($item); // Doses per Day

    var doseID = "dose-".concat(id);
    var $doseLabel = $('<label></label>');
    $doseLabel.attr('for', doseID).text('Doses Per Day');
    var $doseInput = $('<input type="text">');
    $doseInput.attr('id', doseID).on('keyup', function () {
      updateQuantity(_this);
    }).val(1);
    var $dose = $('<div></div>');
    $dose.addClass('item-dose').append($doseLabel, $doseInput).appendTo($item); // Day Supply

    var supplyID = "supply-".concat(id);
    var $supplyLabel = $('<label></label>');
    $supplyLabel.attr('for', supplyID).text('Day Supply');
    var $supplyInput = $('<input type="text">');
    $supplyInput.attr('id', supplyID).on('keyup', function () {
      updateQuantity(_this);
    }).val(100);
    var $supply = $('<div></div>');
    $supply.addClass('item-supply').append($supplyLabel, $supplyInput).appendTo($item); // Quantity

    var quantityID = "quantity-".concat(id);
    var $quantityLabel = $('<label></label>');
    $quantityLabel.attr('for', quantityID).text('Quantity');
    var $quantityInput = $('<input type="text">');
    $quantityInput.attr('id', quantityID).on('keyup', function () {
      updateSupply(_this);
    }).val(100);
    var $quantity = $('<div></div>');
    $quantity.addClass('item-quantity').append($quantityLabel, $quantityInput).appendTo($item); // Price

    var priceID = "price-".concat(id);
    var $priceLabel = $('<label></label>');
    $priceLabel.attr('for', priceID).text('Price');
    var $priceDiv = $('<div></div>');
    $priceDiv.attr('id', priceID);
    var $price = $('<div></div>');
    $price.addClass('item-price').append($priceLabel, $priceDiv).appendTo($item); // Info

    var $infoButton = $('<input type="button">');
    $infoButton.addClass('info').on('click', function () {
      showInfo(_this);
    }).val('Information');
    var $buttons = $('<div></div>');
    $buttons.addClass('item-buttons').append($infoButton).appendTo($item); // Calls functions to update data

    comparisonStrength($strengthSelect);
  });
}
/**
 * Function handling API call to retrieve the selected product information.
 *
 * @param {object} selection DOM reference to search result that was clicked.
 *
 * @returns {array} JSON array with the selected database entries.
 */


function chooseComparison(selection) {
  // eslint-disable-line no-unused-vars
  // Extract indices for MySQL query
  var query = $(selection).attr('data-url');
  showComparisonResults('');
  $.ajax({
    url: 'generate-comparison/',
    data: {
      q: query
    },
    type: 'GET',
    dataType: 'json',
    success: function success(results) {
      processComparison(results); // Reset search bar

      $('#Comparison-Search').val('');
    },
    error: function error(jqXHR, textStatus, errorThrown) {
      Sentry.captureException(errorThrown);
      var error = 'Sorry we have experienced an error with our server. Please refresh your page and try ' + 'again. If you continue to run into issues, please contact us at ' + 'studybuffalo@studybuffalo.com';
      var $searchResults = $('#Comparison-Results');
      $searchResults.html("<span style=\"color: red\">".concat(error, "</span>"));
    }
  });
}
/**
 * Takes the data from Price-Table and formats it into a new print page.
 *
 * @returns {object} A new window.document formatted for printing.
 */


function printPrices() {
  var printPage = window.open().document;
  var $items = $('#price-table .item');
  var patientName = $('#Patient-Name').val();
  var html = '<head>' + '<link rel="stylesheet" type="text/css", href="/static/drug_price_calculator/css/print.css"></link>' + '<title>Medications Prices</title>' + '</head>';
  html += '<body>'; // Header

  html += '<h1>';
  html += patientName ? "Medication Price List for ".concat(patientName) : 'Medication Price List';
  html += '</h1>'; // Table Header

  html += '<table>' + '<thead>' + '<tr>' + '<th>Medication</th>' + '<th>Day Supply</th>' + '<th>Quantity</th>' + '<th>Price</th>' + '</tr>' + '</thead>'; // Cycle through the table rows and enter them into the print table

  html += '<tbody>';
  $items.each(function (index, item) {
    var $item = $(item);
    html += '<tr>'; // Medication Name

    var $medication = $item.find('.item-medication');
    var medicationName = $medication.find('strong').text() || $medication.find('input').val();
    var medicationInfo = $medication.find('em').text();
    html += "<td><strong>".concat(medicationName, "</strong><br><em>").concat(medicationInfo, "</em></td>"); // Day supply

    var supply = $item.find('.item-supply input').val();
    html += "<td>".concat(supply, "</td>"); // Quantity

    var quantity = $item.find('.item-quantity input').val();
    html += "<td>".concat(quantity, "</td>"); // Price

    var price = $item.find('.item-price div').text();
    html += "<td>".concat(price, "</td>");
    html += '</tr>';
  });
  html += '</tbody>'; // Footer

  var total = $('#price-table-total').text();
  html += "<tfoot><tr><th colspan=\"4\">".concat(total, "</th></tr></tfoot>");
  html += '</table>'; // Disclaimer text

  var today = getTodaysDate();
  html += 'These medications costs are estimates based on the best available information. Actual ' + 'costs may vary depending on your pharmacy and third-party drug coverage.<br><br>' + "<i>Printed on: ".concat(today, "</i>");
  html += '</body>'; // Writes HTML to document window

  printPage.write(html); // Close document

  printPage.close();
}

$(document).ready(function () {
  var searchSupport = eventSupported('onsearch');
  var trigger = searchSupport === true ? 'search' : 'keyup';
  $('#Search-Bar').on(trigger, function (e) {
    showSearchResults(e.target.value);
  });
  $('#price-table-third-party').on('change', function () {
    changeThirdParty('price-table');
  });
  $('input.changeQuantity').on('click', function (e) {
    changeQuantityPopup(e.target);
  });
  $('#Add-Freeform').on('click', function () {
    addFreeformEntry();
  });
  $('#Comparison-Search').on(trigger, function (e) {
    showComparisonResults(e.target.value);
  });
  $('#comparison-table-third-party').on('change', function () {
    changeThirdParty('comparison-table');
  });
  $('#Print-Medication-Prices').on('click', function () {
    printPrices();
  });
  $('#Search-Bar').focus();
});
