/* globals Sentry */
// Global variables
let ajaxTimer;

/**
 * Takes an event name and tests if it is valid in the users browser.
 *
 * @param {str} eventName the name of the event to be tested (including 'on').
 *
 * @param {bool} Returns true if supported, otherwise false.
 */
function eventSupported(eventName) {
  let testEl = document.createElement('input');
  testEl.type = 'text';

  let isSupported = (eventName in testEl);

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
  let patientPays;

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
  } else if (
    thirdParty === '19824' || thirdParty === '20400' || thirdParty === '20401'
    || thirdParty === '20401' || thirdParty === '20403' || thirdParty === '22128'
  ) {
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

  const thirdPartyPays = Math.round((mac - patientPays) * 100) / 100;

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
  const upcharge1 = 0.03;
  const upcharge2 = 0.07;
  const returnPrice = {
    drugCost: 0,
    upcharge1: 0,
    upcharge2: 0,
    dispensingFee: 0,
    grossPrice: 0,
  };

  // Calculates total gross price
  if (!Number.isNaN(costPerUnit) && costPerUnit > 0 && !Number.isNaN(quantity) && quantity > 0) {
    const drugPrice = costPerUnit * quantity;
    const fee1 = drugPrice * upcharge1;
    let fee2 = (drugPrice + fee1) * upcharge2;
    fee2 = fee2 > 100 ? 100 : fee2;
    const grossPrice = drugPrice + fee1 + fee2 + 12.15;

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
  let coverageMatch = false;
  let fees;
  let thirdPartyPays;
  let benefitResult;
  const returnPrice = {
    drugCost: 0,
    upcharge1: 0,
    upcharge2: 0,
    dispensingFee: 0,
    grossPrice: 0,
    thirdParty: 0,
    netPrice: 0,
    benefit: 'N/A',
  };

  // Calculate total drug price
  const tempPrice = calculateFees(costPerUnit, quantity);
  returnPrice.drugCost = tempPrice.drugCost;
  returnPrice.upcharge1 = tempPrice.upcharge1;
  returnPrice.upcharge2 = tempPrice.upcharge2;
  returnPrice.dispensingFee = tempPrice.dispensingFee;
  returnPrice.grossPrice = tempPrice.grossPrice;

  // Calculates the third party pays amount
  if (thirdParty) {
    // Compares third party coverage against benefits to see if match
    for (let i = 0; i < benefits.length; i += 1) {
      if (thirdParty === benefits[i]) { coverageMatch = true; }
    }

    // Determine maximum the third party will pay
    let thirdPartyUnitPrice = 0;

    if (mac && lca) {
      thirdPartyUnitPrice = mac < lca ? mac : lca;
    } else if (mac) {
      thirdPartyUnitPrice = mac;
    } else if (lca) {
      thirdPartyUnitPrice = lca;
    }

    // Calculates the amount they will pay
    fees = calculateFees(thirdPartyUnitPrice, quantity);

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
  if (thirdParty === '') {
    benefitResult = 'N/A';
  } else if (coverageMatch === false) {
    benefitResult = 'No';
  } else {
    benefitResult = 'Yes';
  }

  returnPrice.benefit = benefitResult;

  // Calculates the net price
  const netPrice = returnPrice.grossPrice - thirdPartyPays;
  returnPrice.netPrice = Math.round(netPrice * 100) / 100;

  return returnPrice;
}

/**
 * Returns today's date in YYYY-MM-DD format.
 *
 * @returns {str} Date in YYYY-MM-DD format.
 */
function getTodaysDate() {
  const today = new Date();

  let day = today.getDate();
  day = day < 10 ? `0${day}` : day;

  let month = today.getMonth() + 1;
  month = month < 10 ? `0${month}` : month;

  const year = today.getFullYear();

  return `${year}-${month}-${day}`;
}

/**
 * Returns html code to generate the loading bar
 */
function loadingBar() {
  const output = (
    '<div id="warningGradientOuterBarG">'
    + '<div id="warningGradientFrontBarG"'
    + 'class="warningGradientAnimationG">'
    + '<div class="warningGradientBarLineG"></div>'
    + '<div class="warningGradientBarLineG"></div>'
    + '<div class="warningGradientBarLineG"></div>'
    + '<div class="warningGradientBarLineG"></div>'
    + '<div class="warningGradientBarLineG"></div>'
    + '<div class="warningGradientBarLineG"></div>'
    + '</div></div>'
  );

  return output;
}

/**
 * Converts doses per day fraction inputs to a number
 *
 * @param {float} value: dosesPerDay input value to be converted.
 *
 * @returns {float} the number of doses per day.
 */
function processDosesPerDay(value) {
  let output;
  let match;
  let tempNums;

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
  const $priceDivs = $table.find('.item-price');
  let finalTotal = 0;

  $priceDivs.each((index, div) => {
    const price = Number($(div).find('div').attr('data-net-price'));

    if (!Number.isNaN(price) && price > 0) {
      finalTotal += price;
    }
  });

  $table.find('.item-total span').text(`TOTAL $${finalTotal.toFixed(2)}`);
}

/**
 * Updates the displayed price of a medication.
 *
 * @param {object} $item JQuery reference to the table row to upate.
 */
function priceUpdate($item) {
  // Get the appropriate brand/strength select
  const $select = $item.find('select').eq(0);
  const $option = $select.children('option:selected');

  // Assemble list of benefits
  const benefits = [];
  if ($option.attr('data-group-1') === 'true') { benefits.push('1'); }
  if ($option.attr('data-group-66') === 'true') { benefits.push('66'); }
  if ($option.attr('data-group-19823') === 'true') { benefits.push('19823'); }
  if ($option.attr('data-group-19823a') === 'true') { benefits.push('19823a'); }
  if ($option.attr('data-group-19824') === 'true') { benefits.push('19824'); }
  if ($option.attr('data-group-20400') === 'true') { benefits.push('20400'); }
  if ($option.attr('data-group-20403') === 'true') { benefits.push('20403'); }
  if ($option.attr('data-group-20514') === 'true') { benefits.push('20514'); }
  if ($option.attr('data-group-22128') === 'true') { benefits.push('22128'); }
  if ($option.attr('data-group-23609') === 'true') { benefits.push('23609'); }

  // Calculate the price of this medication
  const cost = (
    Number($item.find('.item-cost span').attr('data-unit-price'))
    || Number($item.find('.item-cost input').val())
    || Number($item.find('.item-cost div').attr('data-unit-price'))
  );

  const quantity = Number($item.find('.item-quantity input').val());

  const lca = $option.attr('data-lca-price');
  const mac = $option.attr('data-mac-price');

  const $table = $item.parent('.content').parent('div');
  const tableName = $table.attr('id');
  const $thirdParty = $(`#${tableName}-third-party`);
  const thirdParty = $thirdParty.children('option:selected').val();

  const price = calculatePrice(cost, quantity, lca, mac, thirdParty, benefits);

  // Update the Price Div
  const $priceDiv = $item.find('.item-price div');
  $priceDiv
    .text(`$${price.netPrice.toFixed(2)}`)
    .attr('data-drug-cost', price.drugCost)
    .attr('data-upcharge-1', price.upcharge1)
    .attr('data-upcharge-2', price.upcharge2)
    .attr('data-dispensing-fee', price.dispensingFee)
    .attr('data-gross-price', price.grossPrice)
    .attr('data-third-party', price.thirdParty)
    .attr('data-net-price', price.netPrice)
    .attr('data-benefit', price.benefit);

  // Update the total price
  totalUpdate($table);

  // Updates class on the Info button
  const $infoButton = $item.find('.info');

  if (price.benefit === 'No') {
    $infoButton.attr('class', 'info warning');
  } else if (
    $option.attr('data-coverage-criteria')
    || $option.attr('data-special-authorizations')
  ) {
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
  const $brandOption = $(brandSelect).children('option:selected');
  const unitPrice = $brandOption.attr('data-unit-price');
  const unit = $brandOption.attr('data-unit') || 'unit';

  // Updates the cost/unit span
  const $item = $(brandSelect).closest('.item');

  const $costSpan = $item.find('.item-cost span');
  $costSpan
    .attr('data-unit-price', unitPrice)
    .text(`$${unitPrice}`);

  const $costEm = $item.find('.item-cost em');
  $costEm.text(`per ${unit}`);

  // Update the total price
  priceUpdate($item);
}

/**
 * Updates comparison table prices based on selected strength
 *
 * @param {object} brandSelect DOM reference to the strength select to update.
 */
function comparisonStrength(strengthSelect) {
  // Collect the relevant data values
  const $strengthOption = $(strengthSelect).children('option:selected');
  const cost = $strengthOption.attr('data-cost');

  // Updates the cost/unit span
  const $item = $(strengthSelect).closest('.item');

  const $costDiv = $item.find('.item-cost div');
  $costDiv
    .attr('data-cost', cost)
    .text(`$${cost}`);

  // Update the total price
  priceUpdate($item);
}

/**
 * Updates the prices in all columns based on new third party coverage.
 *
 * @param {object} table DOM reference to the table to be updated.
 */
function changeThirdParty(table) {
  // Get all the item divs
  const $table = $(`#${table}`);
  const $itemDivs = $table.find('.item');

  // Cycle through each item div and update the price
  $itemDivs.each((index, item) => {
    if (table === 'price-table') {
      const select = $(item).find('select').first();
      brandUpdate(select);
    } else if (table === 'comparison-table') {
      const select = $(item).find('select').first();
      comparisonStrength(select);
    }
  });
}

/**
 * Closes the popup window used to update column's quantities.
 *
 * @param {object} e Reference to triggering DOM element.
 */
function closeQuantityPopup(e) {
  const popupDiv = $('#Popup-Veil')[0];
  const closeButton = $('#close-change-popup')[0];

  if (
    e === undefined
    || e.target === popupDiv
    || e.target === closeButton
  ) {
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
  const $item = $(input).closest('.item');

  // Calculate a new day quantity
  const doses = processDosesPerDay($item.find('.item-dose input').val());
  const supply = Number($item.find('.item-supply input').val());
  let quantity = 0;

  if (
    doses
    && !Number.isNaN(doses)
    && doses > 0
    && supply && !Number.isNaN(supply)
    && supply > 0
  ) {
    quantity = Math.round(doses * supply * 100) / 100;
  }

  // Update the quantity input
  $item.find('.item-quantity input').val(quantity);

  // Recalculate the total price
  priceUpdate($item);
}

/**
 * Updates all the day supply inputs.
 *
 * @param {object} table DOM reference to the table to update.
 */
function changeSupply(table) {
  const amount = $('#change-amount').val();

  const $items = $(`#${table}`).find('.item');

  $items.each((index, item) => {
    const $item = $(item);
    const $input = $item.find('.item-supply input');
    $input.val(amount);

    // Update the day supplies
    updateQuantity($input[0]);
  });

  // Closes Popup
  $('#Popup-Veil').remove();
}

/**
 * Updates the day supply input.
 *
 * @param {object} input DOM reference to the day supply to update.
 */
function updateSupply(input) {
  // Get the containing item div
  const $item = $(input).closest('.item');

  // Calculate a new day supply
  const doses = processDosesPerDay($item.find('.item-dose input').val());
  const quantity = Number($item.find('.item-quantity input').val());
  let supply = 0;

  if (
    doses
    && !Number.isNaN(doses)
    && doses > 0
    && quantity
    && !Number.isNaN(quantity)
    && quantity > 0
  ) {
    supply = Math.round((quantity / doses) * 100) / 100;
  }

  // Update the supply input
  $item.find('.item-supply input').val(supply);

  // Recalculate the total price
  priceUpdate($item);
}

/**
 * Updates the quantities in an entire column.
 *
 * @param {str} table HTML ID of the table containing columns to update.
 */
function changeQuantity(table) {
  const amount = $('#change-amount').val();

  const $items = $(`#${table}`).find('.item');

  $items.each((index, item) => {
    const $item = $(item);
    const $input = $item.find('.item-quantity input');
    $input.val(amount);

    // Update the day supplies
    updateSupply($input[0]);
  });

  // Closes Popup
  $('#Popup-Veil').remove();
}

/**
 * Adds keyboard support for Enter/Esc keys to quantity popup.
 *
 * @param {object} amount:      DOM reference to text input with the quantity.
 * @param {object} buttonInput DOM reference to submit button.
 * @param {str}    name        HTML name of the column (days supply or quantity).
 * @param {str}    table       HTML ID of table containing the columns to update.
 * @param {object} e           Triggering event.
 */
function changeQuantityKeypress(amount, colIndex, type, table, e) {
  if (e.which === 13 || e.keycode === 13) {
    changeQuantity(amount, colIndex, type, table);
  } else if (e.which === 27 || e.keycode === 27) {
    closeQuantityPopup(undefined);
  }
}

/**
 * Updates all of a columns quantities/day supplies.
 *
 * @param {object} buttonInput DOM reference to the button that triggers the change.
 * @param {str}    name        The calculation method this button applies to.
 */
function changeQuantityPopup(buttonInput) {
  // Collect page, viewport, and element dimensions/coordinates
  const pageHt = $(document).height();
  const pageWid = $(document).width();
  const scrollHt = document.body.scrollTop || document.documentElement.scrollTop;
  const viewHt = $(window).height();

  // Position cover div to fill entire page
  const $coverDiv = $('<div></div>');
  $coverDiv
    .attr('id', 'Popup-Veil')
    .on('click', (e) => { closeQuantityPopup(e); })
    .height(pageHt)
    .width(pageWid)
    .prependTo('body');

  // Position the popup in the center of the screen
  const inputHt = 300;
  const inputWid = 300;
  const inputLeft = (pageWid - inputWid) / 2;
  const inputTop = scrollHt + (viewHt / 2) - (inputHt / 2);

  const $popupDiv = $('<div></div>');
  $popupDiv
    .attr('id', 'Change-Popup')
    .css({
      height: `${inputHt}px`,
      width: `${inputWid}px`,
      left: `${inputLeft}px`,
      top: `${inputTop}px`,
    })
    .appendTo($coverDiv);

  // Instruction Text
  const $instruction = $('<div></div>');
  $instruction
    .text('Enter new day supply or quantity')
    .appendTo($popupDiv);

  // Input Amount
  const $input = $('<input type="text"');
  $input.attr('id', 'change-amount');

  const $inputDiv = $('<div></div>');
  $inputDiv
    .append($input)
    .appendTo($popupDiv);

  // Get the table name
  const tableName = $(buttonInput).closest('.footer').parent('div').attr('id');

  // Change Day Supply
  const $buttonSupply = $('<input type="button">');
  $buttonSupply
    .attr('id', 'change-supply')
    .on('click', () => {
      changeSupply(tableName);
    })
    .val('Change Day Supply');

  const $supplyDiv = $('<div></div>');
  $supplyDiv
    .append($buttonSupply)
    .appendTo($popupDiv);

  // Change Quantity
  const $buttonQuantity = $('<input type="button">');
  $buttonQuantity
    .attr('id', 'change-quantity')
    .on('click', () => {
      changeQuantity(tableName);
    })
    .val('Change Quantity');

  const $quantityDiv = $('<div></div>');
  $quantityDiv
    .append($buttonQuantity)
    .appendTo($popupDiv);

  // Close BUtton
  const $buttonClose = $('<input type="button">');
  $buttonClose
    .attr('id', 'close-change-popup')
    .on('click', (e) => { closeQuantityPopup(e); })
    .val('Cancel');

  const $closeDiv = $('<div></div>');
  $closeDiv
    .append($buttonClose)
    .appendTo($popupDiv);

  // Bring focus to popup
  $input.focus();
}

/**
 * Closes the popup window generated to dispaly drug info.
 */
function closeInfoPopup() {
  const $popupDiv = $('#Popup-Veil');

  $popupDiv.remove();
}

/**
 * Generates popup showing additional info on the selected row.
 *
 * @param {object} infoButton DOM reference to the button that was clicked.
 */
function showInfo(infoButton) {
  const $infoButton = $(infoButton);
  const $item = $infoButton.closest('.item');

  // Collect page, viewport, and element dimensions/coordinates
  const pageHt = $(document).height();
  const pageWid = $(document).width();
  const screenWid = $(window).width();
  const buttonTop = $infoButton.offset().top;
  const buttonLeft = $infoButton.offset().left;

  // Calculate pop-up width;
  const popupWid = screenWid < 600 ? screenWid - 20 : 580;

  // Calculate where to place the popup (center it if it can't fit by button)
  let divRight = 0;

  if (buttonLeft < popupWid + 10) {
    divRight = (screenWid - popupWid) / 2;
  } else {
    divRight = (screenWid - buttonLeft) - 10;
  }

  // Popup div positions to left of trigger button
  const $infoDiv = $('<div></div>');
  $infoDiv
    .attr('id', 'Info-Popup')
    .css({
      right: `${divRight}px`,
      top: `${buttonTop}px`,
      width: `${popupWid}px`,
    });

  // The Pop-Up Div Title
  const $title = $('<h3></h3>');
  $title
    .text('Coverage Information')
    .appendTo($infoDiv);

  // Benefit Type
  const $option = $item.find('select').children('option:selected');

  let coverageText = $option.attr('data-coverage-status');
  coverageText = coverageText || 'Not a benefit';

  const $coverage = $('<p></p>');
  $coverage
    .append($('<strong></strong>').text('Benefit Type: '))
    .append($('<span></span>').text(coverageText))
    .appendTo($infoDiv);

  // Check if any third party coverage is applied
  const tableName = $item.parent('.content').parent('div').attr('id');
  const $thirdPartySelect = $(`#${tableName}-third-party`);
  const thirdParty = $thirdPartySelect.val();

  // Add drug cost & MAC if the drug plan was selected
  if (thirdParty) {
    // Collect the relevant data
    const cost = $option.attr('data-unit-price');
    const lca = $option.attr('data-lca-price');
    const mac = $option.attr('data-mac-price');
    let unit = $option.attr('data-unit');

    // Replaces unit with 'unit' if blank
    unit = unit || 'unit';

    // Cost
    const $cost = $('<p></p>');
    $cost
      .append($('<strong></strong>').text('Cost: '))
      .append($('<span></span>').text(`$${cost} per ${unit}`))
      .appendTo($infoDiv);

    // LCA
    if (lca) {
      const $lca = $('<p></p>');
      $lca
        .append($('<strong></strong>').text('LCA: '))
        .append($('<span></span>').text(`$${lca} per ${unit}`))
        .appendTo($infoDiv);
    }

    // MAC
    if (mac) {
      const $mac = $('<p></p>');
      $mac
        .append($('<strong></strong>').text('MAC: '))
        .append($('<span></span>').text(`$${mac} per ${unit}`))
        .appendTo($infoDiv);
    }
  }

  // Add any coverage criteria
  // TODO: create a pop-up window to display criteria
  const criteria = JSON.parse($option.attr('data-coverage-criteria'));

  if (criteria.length) {
    const priceID = $option.attr('data-price-id');

    const $criteria = $('<a></a>');
    $criteria
      .text('Click here for coverage criteria')
      .attr('target', '_blank')
      .attr('rel', 'noopener')
      .attr('href', `/tools/drug-price-calculator/coverage-criteria/${priceID}/`);

    const $criteriaP = $('<p></p>');
    $criteriaP
      .append($criteria)
      .appendTo($infoDiv)
      .css('margin-top: 0.5em;');
  }

  // Price Information
  const $feeTitle = $('<p></p>');
  $feeTitle
    .append($('<strong></strong>').text('Price Breakdown'))
    .addClass('MT1em')
    .appendTo($infoDiv);

  // Drug Costs & Fees Table
  const $feeTable = $('<table></table>');
  $feeTable.appendTo($infoDiv);

  // Drug Costs
  const $price = $item.find('.item-price > div');
  let drugCost = Number($price.attr('data-drug-cost'));
  drugCost = Number.isNaN(drugCost) ? '$0.00' : `${drugCost.toFixed(2)}`;

  const $feeDrug = $('<tr></tr>');
  $feeDrug
    .append($('<td></td>').text('Drug Cost:'))
    .append($('<td></td>'))
    .append($('<td></td>').text(drugCost))
    .appendTo($feeTable);

  // Upcharge #1
  let upcharge1 = Number($price.attr('data-upcharge-1'));
  upcharge1 = Number.isNaN(upcharge1) ? '$0.00' : `$${upcharge1.toFixed(2)}`;

  const $feeUpcharge1 = $('<tr></tr>');
  $feeUpcharge1
    .append($('<td></td>').text('Upcharge #1:'))
    .append($('<td></td>').text('+'))
    .append($('<td></td>').text(upcharge1))
    .appendTo($feeTable);

  // Upcharge #2
  let upcharge2 = Number($price.attr('data-upcharge-2'));
  upcharge2 = Number.isNaN(upcharge2) ? '$0.00' : `$${upcharge2.toFixed(2)}`;

  const $feeUpcharge2 = $('<tr></tr>');
  $feeUpcharge2
    .append($('<td></td>').text('Upcharge #2:'))
    .append($('<td></td>').text('+'))
    .append($('<td></td>').text(upcharge2))
    .appendTo($feeTable);

  // Dispensing Fee
  let dispensingFee = Number($price.attr('data-dispensing-fee'));
  dispensingFee = Number.isNaN(dispensingFee) ? '$0.00' : `$${dispensingFee.toFixed(2)}`;

  const $feeDispensing = $('<tr></tr>');
  $feeDispensing
    .append($('<td></td>').text('Dispensing Fee:'))
    .append($('<td></td>').text('+'))
    .append($('<td></td>').text(dispensingFee))
    .appendTo($feeTable);

  // Gross Price
  let gross = Number($price.attr('data-gross-price'));
  gross = Number.isNaN(gross) ? '$0.00' : `$${gross.toFixed(2)}`;

  const $feeGross = $('<tr></tr>');
  $feeGross
    .append($('<td></td>').text('Sub-Total:'))
    .append($('<td></td>'))
    .append($('<td></td>').text(gross))
    .addClass('totalRow')
    .appendTo($feeTable);

  // Third Party Portion
  let tp = Number($price.attr('data-third-party'));
  tp = Number.isNaN(tp) ? '$0.00' : `$${tp.toFixed(2)}`;

  const $feeTP = $('<tr></tr>');
  $feeTP
    .append($('<td></td>').text('Third Party Portion:'))
    .append($('<td></td>').text('-'))
    .append($('<td></td>').text(tp))
    .appendTo($feeTable);

  // Net Total
  let net = Number($price.attr('data-net-price'));
  net = Number.isNaN(net) ? '$0.00' : `$${net.toFixed(2)}`;

  const $feeNet = $('<tr></tr>');
  $feeNet
    .append($('<td></td>').text('Patient Pays:'))
    .append($('<td></td>'))
    .append($('<td></td>').text(net))
    .addClass('totalRow')
    .appendTo($feeTable);

  // Special Authorization Form Links
  const $saFormTitle = $('<p></p>');
  const $saForm = $('<ul></ul>');

  const specialAuthorizations = JSON.parse($option.attr('data-special-authorizations'));

  // If special authorizations present, add title
  if (specialAuthorizations.length) {
    $saFormTitle
      .append($('<strong></strong>').text('Special Authorization Forms'))
      .addClass('MT1em')
      .appendTo($infoDiv);
    $saForm.appendTo($infoDiv);
  }

  // Add any forms
  specialAuthorizations.forEach((special) => {
    const $saFormA = $('<a></a>');

    $saFormA
      .text(special.pdf_title)
      .attr('href', `https://idbl.ab.bluecross.ca/idbl/DBL/${special.file_name}`)
      .attr('target', '_blank')
      .attr('rel', 'noopner');

    $('<li></li>').append($saFormA).appendTo($saForm);
  });

  // Close Button
  const $close = $('<div></div>');
  $close
    .attr('class', 'close')
    .appendTo($infoDiv);

  const $closeButton = $('<input type="button">');
  $closeButton
    .val('Close')
    .on('click', () => { closeInfoPopup(); })
    .appendTo($close);


  // Position cover div to fill entire page
  const $coverDiv = $('<div></div>');
  $coverDiv
    .attr('id', 'Popup-Veil')
    .height(pageHt)
    .width(pageWid)
    .on('click', (e) => { closeQuantityPopup(e); })
    .on('keydown', (e) => {
      changeQuantityKeypress(null, null, null, e);
    })
    .prependTo('body')
    .append($infoDiv);
}

/**
 * Removes the row containing the clicked button
 *
 * @param {object} deleteButton DOM reference of the button that was clicked.
 */
function removeRow(deleteButton) {
  // Removes row
  const $item = $(deleteButton).closest('.item');
  $item.remove();

  // Updates total prices
  const $table = $item.closest('.content').parent('div');
  totalUpdate($table);
}

/**
 * Adds input elements to allow user to enter freeform medication prices.
 */
function addFreeformEntry() {
  // Generate a unique ID for element IDs
  const id = (new Date()).getTime().toString(36)
    + Math.random().toString(36);

  // Set up containers
  const $content = $('#price-table .content:first');

  const $item = $('<div></div>');
  $item.addClass('item');

  // Medication Name
  const medicationID = `medication-${id}`;

  const $medicationLabel = $('<label></label>');
  $medicationLabel
    .attr('for', medicationID)
    .text('Medication');

  const $medicationInput = $('<input type="text">');
  $medicationInput.attr('id', medicationID);

  const $medication = $('<div></div>');
  $medication
    .addClass('item-medication')
    .append($medicationLabel, $medicationInput)
    .appendTo($item);

  // Brand Name
  const brandID = `brand-${id}`;

  const $brandLabel = $('<label></label>');
  $brandLabel
    .attr('for', brandID)
    .text('Brand');

  const $brandDiv = $('<div></div>');
  $brandDiv
    .attr('id', brandID)
    .text('N/A');

  const $brand = $('<div></div>');
  $brand
    .addClass('item-brand')
    .append($brandLabel, $brandDiv)
    .appendTo($item);

  // Cost Per Unit
  const costID = `cost-${id}`;

  const $costLabel = $('<label></label>');
  $costLabel
    .attr('for', costID)
    .text('Cost Per Unit');

  const $costInput = $('<input type="text">');
  $costInput.attr('id', costID);

  const $cost = $('<div></div>');
  $cost
    .addClass('item-cost')
    .append($costLabel, $costInput)
    .appendTo($item);

  // Does Per Day
  const doseID = `doses-${id}`;

  const $doseLabel = $('<label></label>');
  $doseLabel
    .attr('for', doseID)
    .text('Doses Per Day');

  const $doseInput = $('<input type="text">');
  $doseInput
    .attr('id', doseID)
    .on('keyup', () => { updateQuantity(this); })
    .val(1);

  const $dose = $('<div></div>');
  $dose
    .addClass('item-dose')
    .append($doseLabel, $doseInput)
    .appendTo($item);

  // Day Supply
  const supplyID = `supply-${id}`;

  const $supplyLabel = $('<label></label>');
  $supplyLabel
    .attr('for', supplyID)
    .text('Day Supply');

  const $supplyInput = $('<input type="text">');
  $supplyInput
    .attr('id', supplyID)
    .on('keyup', () => { updateQuantity(this); })
    .val(100);

  const $supply = $('<div></div>');
  $supply
    .addClass('item-supply')
    .append($supplyLabel, $supplyInput)
    .appendTo($item);

  // Quantity
  const quantityID = `quantity-${id}`;

  const $quantityLabel = $('<label></label>');
  $quantityLabel
    .attr('for', quantityID)
    .text('Quantity');

  const $quantityInput = $('<input type="text">');
  $quantityInput
    .attr('id', quantityID)
    .on('keyup', () => { updateSupply(this); })
    .val(100);

  const $quantity = $('<div></div>');
  $quantity
    .addClass('item-quantity')
    .append($quantityLabel, $quantityInput)
    .appendTo($item);

  // Price
  const priceID = `price-${id}`;

  const $priceLabel = $('<label></label>');
  $priceLabel
    .attr('for', priceID)
    .text('Price');

  const $priceDiv = $('<div></div>');
  $priceDiv.attr('id', priceID);

  const $price = $('<div></div>');
  $price
    .addClass('item-price')
    .append($priceLabel, $priceDiv)
    .appendTo($item);

  // Info and Delete Buttons
  const $infoButton = $('<input type="button">');
  $infoButton
    .addClass('info')
    .on('click', () => { showInfo(this); })
    .val('Information');

  const $deleteButton = $('<input type="button">');
  $deleteButton
    .addClass('delete')
    .on('click', () => { removeRow(this); })
    .val('Delete');

  const $buttons = $('<div></div>');
  $buttons
    .addClass('item-buttons')
    .append($infoButton, $deleteButton)
    .appendTo($item);

  // Add the completed $item to the $content container
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
  const lcaEntry = {
    clients: results[0].clients,
    coverage_criteria: results[0].coverage_criteria,
    coverage_status: results[0].coverage_status,
    drug: results[0].drug,
    id: results[0].id,
    lca_price: results[0].lca_price,
    mac_price: results[0].mac_price,
    mac_text: results[0].mac_text,
    special_authorizations: results[0].special_authorizations,
    unit_issue: results[0].unit_issue,
    unit_price: results[0].lca_price,
  };

  // Adds LCA entry to front of array
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
  const results = addLCA(originalResults);

  // Generate a unique ID for element IDs
  const id = (new Date()).getTime().toString(36)
    + Math.random().toString(36);

  // Set up containers
  const $content = $('#price-table .content:first');

  const $item = $('<div></div>');
  $item.addClass('item');

  // Medication Name
  const medicationID = `medication-${id}`;

  const $medicationLabel = $('<label></label>');
  $medicationLabel
    .attr('for', medicationID)
    .text('Medication');

  const $medicationStrong = $('<strong></strong>');
  $medicationStrong.text(results[0].drug.generic_name);

  let medEmText = '';
  medEmText += results[0].strength ? `${results[0].drug.strength} ` : '';
  medEmText += results[0].route ? `${results[0].drug.route} ` : '';
  medEmText += results[0].dosage_form ? `${results[0].drug.dosage_form} ` : '';
  medEmText = medEmText.trim();

  const $medicationEm = $('<em></em>');
  $medicationEm.text(medEmText);

  const $medicationDiv = $('<div></div>');
  $medicationDiv
    .attr('id', medicationID)
    .append($medicationStrong, $medicationEm);

  const $medication = $('<div></div>');
  $medication
    .addClass('item-medication')
    .append($medicationLabel, $medicationDiv)
    .appendTo($item);

  // Brand Name
  const brandID = `brand-${id}`;

  const $brandLabel = $('<label></label>');
  $brandLabel
    .attr('for', brandID)
    .text('Brand');

  const $brandSelect = $('<select></select>');
  $brandSelect
    .attr('id', brandID)
    .on('change', (e) => { brandUpdate(e.currentTarget); });

  $.each(results, (index, value) => {
    const $tempOption = $('<option></option>');

    $tempOption
      .text(value.drug.brand_name)
      .attr('data-price-id', value.id)
      .attr('data-unit-price', value.unit_price)
      .attr('data-unit-issue', value.unit_issue)
      .attr('data-lca-price', value.lca_price)
      .attr('data-mac-price', value.mac_price)
      .attr('data-mac-text', value.mac_text)
      .attr('data-group-1', value.clients.group_1)
      .attr('data-group-66', value.clients.group_66)
      .attr('data-group-66a', value.clients.group_66a)
      .attr('data-group-19823', value.clients.group_19823)
      .attr('data-group-19823a', value.clients.group_19823a)
      .attr('data-group-19824', value.clients.group_19824)
      .attr('data-group-20400', value.clients.group_20400)
      .attr('data-group-20403', value.clients.group_20403)
      .attr('data-group-20514', value.clients.group_20514)
      .attr('data-group-22128', value.clients.group_22128)
      .attr('data-group-23609', value.clients.group_23609)
      .attr('data-coverage-status', value.coverage_status)
      .attr('data-special-authorizations', JSON.stringify(value.special_authorizations))
      .attr('data-coverage-criteria', JSON.stringify(value.coverage_criteria))
      .appendTo($brandSelect);
  });

  const $brand = $('<div></div>');
  $brand
    .addClass('item-brand')
    .append($brandLabel, $brandSelect)
    .appendTo($item);

  // Cost Per Unit
  const costID = `cost-${id}`;

  const $costLabel = $('<label></label>');
  $costLabel
    .attr('for', costID)
    .text('Cost Per Unit');

  const $costSpan = $('<span></span>');

  const $costEm = $('<em></em>');

  const $costDiv = $('<div></div>');
  $costDiv
    .attr('id', costID)
    .append($costSpan, $costEm);

  const $cost = $('<div></div>');
  $cost
    .addClass('item-cost')
    .append($costLabel, $costDiv)
    .appendTo($item);

  // Does Per Day
  const doseID = `doses-${id}`;

  const $doseLabel = $('<label></label>');
  $doseLabel
    .attr('for', doseID)
    .text('Doses Per Day');

  const $doseInput = $('<input type="text">');
  $doseInput
    .attr('id', doseID)
    .on('keyup', () => { updateQuantity(this); })
    .val(1);

  const $dose = $('<div></div>');
  $dose
    .addClass('item-dose')
    .append($doseLabel, $doseInput)
    .appendTo($item);

  // Day Supply
  const supplyID = `supply-${id}`;

  const $supplyLabel = $('<label></label>');
  $supplyLabel
    .attr('for', supplyID)
    .text('Day Supply');

  const $supplyInput = $('<input type="text">');
  $supplyInput
    .attr('id', supplyID)
    .on('keyup', () => { updateQuantity(this); })
    .val(100);

  const $supply = $('<div></div>');
  $supply
    .addClass('item-supply')
    .append($supplyLabel, $supplyInput)
    .appendTo($item);

  // Quantity
  const quantityID = `quantity-${id}`;

  const $quantityLabel = $('<label></label>');
  $quantityLabel
    .attr('for', quantityID)
    .text('Quantity');

  const $quantityInput = $('<input type="text">');
  $quantityInput
    .attr('id', quantityID)
    .on('keyup', () => { updateSupply(this); })
    .val(100);

  const $quantity = $('<div></div>');
  $quantity
    .addClass('item-quantity')
    .append($quantityLabel, $quantityInput)
    .appendTo($item);

  // Price
  const priceID = `price-${id}`;

  const $priceLabel = $('<label></label>');
  $priceLabel
    .attr('for', priceID)
    .text('Price');

  const $priceDiv = $('<div></div>');
  $priceDiv.attr('id', priceID);

  const $price = $('<div></div>');
  $price
    .addClass('item-price')
    .append($priceLabel, $priceDiv)
    .appendTo($item);

  // Info and Delete Buttons
  const $infoButton = $('<input type="button">');
  $infoButton
    .addClass('info')
    .on('click', (e) => { showInfo(e.currentTarget); })
    .val('Information');

  const $deleteButton = $('<input type="button">');
  $deleteButton
    .addClass('delete')
    .on('click', () => { removeRow(this); })
    .val('Delete');

  const $buttons = $('<div></div>');
  $buttons
    .addClass('item-buttons')
    .append($infoButton, $deleteButton)
    .appendTo($item);

  // Add the completed $item to the $content container
  $content.append($item);

  // Calculate the default price values for table
  brandUpdate($brandSelect);
}

/**
 * Function handling the API call retrieve the selected product information.
 *
 * @param {object} selection DOM reference to the search result clicked.
 */
function chooseResult(selection) { // eslint-disable-line no-unused-vars
  // Extract indices for MySQL query
  const queryIDs = $(selection).attr('data-ids');
  showSearchResults(''); // eslint-disable-line no-use-before-define

  $.ajax({
    url: '/api/drug-price-calculator/v1/drugs/prices/',
    data: { ids: queryIDs },
    type: 'GET',
    dataType: 'json',
    success: (results) => {
      processResult(results);

      // Reset search bar
      $('#Search-Bar').val('');
      $('#Search-Bar').focus();
    },
    error: (jqXHR, textStatus, errorThrown) => {
      Sentry.captureException(errorThrown);
      const error = (
        'Sorry we have experienced an error with our server. Please refresh your page and try '
        + 'again. If you continue to run into issues, please contact us at '
        + 'studybuffalo@studybuffalo.com'
      );

      alert(error);
    },
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
  // Group together the common drug names
  const compiledResults = {};

  results.forEach((drug) => {
    // If key not in object, add it
    if (!(drug.generic_product in compiledResults)) {
      compiledResults[drug.generic_product] = {
        ids: [],
        generic_product: drug.generic_product,
        brand_names: new Set(),
      };
    }

    // Add the IDs and brand name to array
    compiledResults[drug.generic_product].ids.push(drug.id);
    compiledResults[drug.generic_product].brand_names.add(drug.brand_name);
  });

  // Generate the HTML search list
  const $list = $('<ul></ul>');

  Object.keys(compiledResults).forEach((key, index) => {
    const $item = $('<li></li>')
      .appendTo($list);

    const $link = $('<a></a>')
      .appendTo($item)
      .attr('id', `Search-Result-${index}`)
      .attr('data-ids', compiledResults[key].ids.join(','))
      .on('click', (e) => { chooseResult(e.currentTarget); });

    $('<strong></strong>')
      .appendTo($link)
      .text(compiledResults[key].generic_product);

    $('<br>').appendTo($link);

    $('<em></em>')
      .appendTo($link)
      .text(`also known as ${Array.from(compiledResults[key].brand_names).join(', ')}`);
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
  const $searchResults = $('#Search-Results');

  if (searchString) {
    // 200 ms Timeout applied to prevent firing during typing
    clearTimeout(ajaxTimer);

    ajaxTimer = setTimeout(() => {
      $.ajax({
        url: '/api/drug-price-calculator/v1/drugs/',
        data: { q: searchString, page: 1 },
        type: 'GET',
        dataType: 'json',
        beforeSend: () => {
          $searchResults.html(`<ul><li><a>${loadingBar}</a></li></ul>`);
        },
        success: (results) => {
          const searchList = formatSearchResults(results.results);
          if ($('#Search-Bar').val() === searchString) {
            $searchResults.html(searchList);
          }
        },
        error: () => {
          $searchResults.empty();
          const error = (
            'Sorry we have experienced an error with our server. Please refresh your page and '
            + 'try again. If you continue to run into issues, please contact us at '
            + 'studybuffalo@studybuffalo.com'
          );

          alert(error);
        },
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
  const $searchResults = $('#Comparison-Results');
  const searchMethod1 = !!$('#Comparison-Search-Method-1')[0].checked;
  const searchMethod2 = !!$('#Comparison-Search-Method-2')[0].checked;

  if (searchString.length > 0) {
    // 300 ms Timeout applied to prevent firing during typing
    clearTimeout(ajaxTimer);

    ajaxTimer = setTimeout(() => {
      $.ajax({
        url: 'comparison-search/',
        data: {
          search: searchString,
          methodATC: searchMethod1,
          methodPTC: searchMethod2,
        },
        type: 'GET',
        dataType: 'html',
        beforeSend: () => {
          $searchResults.html(`<ul><li><a>${loadingBar()}</a></li></ul>`);
        },
        success: (results) => {
          // Only updates if search string hasn't changed
          if ($('#Comparison-Search').val() === searchString) {
            $searchResults.html(results);
          }
        },
        error: () => {
          $searchResults.empty();
        },
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
  // Reset the contents
  const $content = $('#comparison-table .content');
  $content.html('');


  // Cycles through the results to generate the HTML content
  $.each(results, (index, value) => {
    // Generate a unique ID for element IDs
    const id = (new Date()).getTime().toString(36)
      + Math.random().toString(36);

    // Create the item dive to contain the content
    const $item = $('<div></div>');
    $item
      .addClass('item')
      .appendTo($content);

    // Medication Name
    const medicationID = `medication-${id}`;

    const $medicationLabel = $('<label></label>');
    $medicationLabel
      .attr('for', medicationID)
      .text('Medication');

    const $medicationDiv = $('<div></div>');
    $medicationDiv
      .attr('id', medicationID)
      .text(value.generic_name);

    const $medication = $('<div></div>');
    $medication
      .addClass('item-medication')
      .append($medicationLabel, $medicationDiv)
      .appendTo($item);

    // Strength
    const strengthID = `strength-${id}`;

    const $strengthLabel = $('<label></label>');
    $strengthLabel
      .attr('for', strengthID)
      .text('Strength');

    const $strengthSelect = $('<select></select>');
    $strengthSelect
      .attr('id', strengthID)
      .on('change', () => { comparisonStrength(this); });

    const $strength = $('<div></div>');
    $strength
      .addClass('item-strength')
      .append($strengthLabel, $strengthSelect)
      .appendTo($item);

    // Add the various strengths to the select
    $.each(value.strength, (strengthIndex, temp) => {
      const $strengthOption = $('<option></option>');
      $strengthOption
        .text(temp.strength)
        .attr('data-cost', temp.unit_price)
        .attr('data-mac', temp.lca ? temp.lca : temp.unit_price)
        .attr('data-coverage', temp.coverage)
        .attr('data-criteria', temp.criteria)
        .attr('data-criteria-p', temp.criteria_p)
        .attr('data-criteria-sa', temp.criteria_sa)
        .attr('data-group-1', temp.group_1)
        .attr('data-group-66', temp.group_66)
        .attr('data-group-66a', temp.group_66a)
        .attr('data-group-19823', temp.group_19823)
        .attr('data-group-19823a', temp.group_19823a)
        .attr('data-group-19824', temp.group_19824)
        .attr('data-group-20400', temp.group_20400)
        .attr('data-group-20403', temp.group_20403)
        .attr('data-group-20514', temp.group_20514)
        .attr('data-group-22128', temp.group_22128)
        .attr('data-group-23609', temp.group_23609)
        .appendTo($strengthSelect);

      // Generates format for special auth data objects
      $.each(temp.special_auth, (specialIndex, temp2) => {
        // Add the title
        let attributeName = `data-special-auth-title-${(specialIndex + 1)}`;
        let attributeValue = temp2.title;
        $strengthOption.attr(attributeName, attributeValue);

        // Add the link
        attributeName = `data-special-auth-link-${(specialIndex + 1)}`;
        attributeValue = temp2.link;
        $strengthOption.attr(attributeName, attributeValue);
      });
    });

    // LCA Cost
    const lcaID = `lca-${id}`;

    const $lcaLabel = $('<label></label>');
    $lcaLabel
      .attr('for', lcaID)
      .text('LCA');

    const $lcaDiv = $('<div></div>');
    $lcaDiv.attr('id', lcaID);

    const $lca = $('<div></div>');
    $lca
      .addClass('item-cost')
      .append($lcaLabel, $lcaDiv)
      .appendTo($item);

    // Doses per Day
    const doseID = `dose-${id}`;

    const $doseLabel = $('<label></label>');
    $doseLabel
      .attr('for', doseID)
      .text('Doses Per Day');

    const $doseInput = $('<input type="text">');
    $doseInput
      .attr('id', doseID)
      .on('keyup', () => { updateQuantity(this); })
      .val(1);

    const $dose = $('<div></div>');
    $dose
      .addClass('item-dose')
      .append($doseLabel, $doseInput)
      .appendTo($item);

    // Day Supply
    const supplyID = `supply-${id}`;

    const $supplyLabel = $('<label></label>');
    $supplyLabel
      .attr('for', supplyID)
      .text('Day Supply');

    const $supplyInput = $('<input type="text">');
    $supplyInput
      .attr('id', supplyID)
      .on('keyup', () => { updateQuantity(this); })
      .val(100);

    const $supply = $('<div></div>');
    $supply
      .addClass('item-supply')
      .append($supplyLabel, $supplyInput)
      .appendTo($item);

    // Quantity
    const quantityID = `quantity-${id}`;

    const $quantityLabel = $('<label></label>');
    $quantityLabel
      .attr('for', quantityID)
      .text('Quantity');

    const $quantityInput = $('<input type="text">');
    $quantityInput
      .attr('id', quantityID)
      .on('keyup', () => { updateSupply(this); })
      .val(100);

    const $quantity = $('<div></div>');
    $quantity
      .addClass('item-quantity')
      .append($quantityLabel, $quantityInput)
      .appendTo($item);

    // Price
    const priceID = `price-${id}`;

    const $priceLabel = $('<label></label>');
    $priceLabel
      .attr('for', priceID)
      .text('Price');

    const $priceDiv = $('<div></div>');
    $priceDiv.attr('id', priceID);

    const $price = $('<div></div>');
    $price
      .addClass('item-price')
      .append($priceLabel, $priceDiv)
      .appendTo($item);

    // Info
    const $infoButton = $('<input type="button">');
    $infoButton
      .addClass('info')
      .on('click', () => { showInfo(this); })
      .val('Information');

    const $buttons = $('<div></div>');
    $buttons
      .addClass('item-buttons')
      .append($infoButton)
      .appendTo($item);

    // Calls functions to update data
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
function chooseComparison(selection) { // eslint-disable-line no-unused-vars
  // Extract indices for MySQL query
  const query = $(selection).attr('data-url');
  showComparisonResults('');

  $.ajax({
    url: 'generate-comparison/',
    data: { q: query },
    type: 'GET',
    dataType: 'json',
    success: (results) => {
      processComparison(results);
      // Reset search bar
      $('#Comparison-Search').val('');
    },
    error: (jqXHR, textStatus, errorThrown) => {
      Sentry.captureException(errorThrown);

      const error = (
        'Sorry we have experienced an error with our server. Please refresh your page and try '
        + 'again. If you continue to run into issues, please contact us at '
        + 'studybuffalo@studybuffalo.com'
      );

      alert(error);
    },
  });
}

/**
 * Takes the data from Price-Table and formats it into a new print page.
 *
 * @returns {object} A new window.document formatted for printing.
 */
function printPrices() {
  const printPage = window.open().document;
  let html = '';

  const $items = $('#price-table .item');

  const patientName = $('#Patient-Name').val();

  html = (
    '<head>'
    + '<link rel="stylesheet" type="text/css", href="/static/drug_price_calculator/css/print.css"></link>'
    + '<title>Medications Prices</title>'
    + '</head>'
  );

  html += '<body>';

  // Header
  html += '<h1>';

  html += patientName ? 'Medication Price List' : `Medication Price List for ${patientName}`;

  html += '</h1>';

  // Table Header
  html += (
    '<table>'
    + '<thead>'
    + '<tr>'
    + '<th>Medication</th>'
    + '<th>Day Supply</th>'
    + '<th>Quantity</th>'
    + '<th>Price</th>'
    + '</tr>'
    + '</thead>'
  );

  // Cycle through the table rows and enter them into the print table
  html += '<tbody>';

  $items.each((index, item) => {
    const $item = $(item);

    html += '<tr>';

    // Medication Name
    const $medication = $item.find('.item-medication');

    const medicationName = $medication.find('strong').text() || $medication.find('input').val();

    const medicationInfo = $medication.find('em').text();

    html += `<td><strong>${medicationName}</strong><br><em>${medicationInfo}</em></td>`;


    // Day supply
    const supply = $item.find('.item-supply input').val();
    html += `<td>${supply}</td>`;

    // Quantity
    const quantity = $item.find('.item-quantity input').val();
    html += `<td>${quantity}</td>`;

    // Price
    const price = $item.find('.item-price div').text();
    html += `<td>${price}</td>`;

    html += '</tr>';
  });

  html += '</tbody>';

  // Footer
  const total = $('#price-table-total').text();

  html += `<tfoot><tr><th colspan="4">${total}</th></tr></tfoot>`;

  html += '</table>';

  // Disclaimer text
  const today = getTodaysDate();

  html += (
    'These medications costs are estimates based on the best available information. Actual '
    + 'costs may vary depending on your pharmacy and third-party drug coverage.<br><br>'
    + `<i>Printed on: ${today}</i>`
  );

  html += '</body>';

  // Writes HTML to document window
  printPage.write(html);

  // Close document
  printPage.close();
}

$(document).ready(() => {
  const searchSupport = eventSupported('onsearch');
  const trigger = searchSupport === true ? 'search' : 'keyup';

  $('#Search-Bar').on(
    trigger,
    (e) => { showSearchResults(e.target.value); },
  );

  $('#price-table-third-party').on(
    'change',
    () => { changeThirdParty('price-table'); },
  );

  $('input.changeQuantity').on(
    'click',
    (e) => { changeQuantityPopup(e.target); },
  );

  $('#Add-Freeform').on(
    'click',
    () => { addFreeformEntry(); },
  );

  $('#Comparison-Search').on(
    trigger,
    (e) => { showComparisonResults(e.target.value); },
  );

  $('#comparison-table-third-party').on(
    'change',
    () => { changeThirdParty('comparison-table'); },
  );

  $('#Print-Medication-Prices').on(
    'click',
    () => { printPrices(); },
  );

  $('#Search-Bar').focus();
});
