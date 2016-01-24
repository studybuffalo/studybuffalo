/********************************************************************************
 *	STUDY BUFFALO VANCOMYCIN BUGS & DRUGS DOSING CALCULATOR						*
 *																				*
 *	Last Update: 2016-Jan-10													*
 *																				*
 *	Copyright(c) Notices														*
 *		2016	Joshua R. Torrance, BSc Pharm	<studybuffalo@studybuffalo.com>	*
 *																				*
 * 	Use, modification and sharing of this software is restricted as per the 	*
 *	Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.	*
 *																				*
 *	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,	EXPRESS		*
 *	OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, *
 *	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL		*
 *	THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER	*
 *	LIABILITY, WHETHER IN AN ACTION	OF CONTRACT, TORT OR OTHERWISE, ARISING		*
 *	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER			*
 *	DEALINGS IN THE SOFTWARE.													*
 ********************************************************************************/


/********************************************************************************
 *	GENERAL FUNCTIONS															*
 ********************************************************************************/
 /********************************************************************************
 *	round()		Rounds a digit to the specific number of digits					*/
/********************************************************************************
 *	number:	The number to round													*
 *	digits:	The number of decimal places to round to							*
 *																				*
 *	Returns the rounded digit													*
 ********************************************************************************/
function round(number, digit) {
	var roundNum = Math.pow(10, digit);
	var output;
	
	if (number) {
		output = Math.round(Number(number.toFixed(8)) * roundNum) / roundNum;
	}
	
	return output;
}
 
 
/********************************************************************************
 *	calculateIBW()		Returns the IBW of the patient							*/
/********************************************************************************
 *	sex:	The sex of the patient (male or female)								*
 *	height:	Height of patient (in cm)											*
 *																				*
 *	Male IBW = 50 kg + (0.92 * cm > 150)										*
 *	Female IBW = 45.5 kg + (0.92 * cm > 150)									*
 *																				*
 *	Returns the IBW (in kg) as a number											*
 ********************************************************************************/
function calculateIBW(sex, height) {
	var ibw;
	
	if (height > 0 && (sex === "Male" || sex === "Female")) {
		if (sex === "Male") {
			ibw = 50 + (0.92 * (height - 150));
		} else if (sex === "Female") {
			ibw = 45.5 + (0.92 * (height - 150));
		}
		
		ibw = round(ibw, 1);
	}
	
	return ibw;
}


/********************************************************************************
 *	calculateDW()		Returns the dosing weight of the patient				*/
/********************************************************************************
 *	weight:	Weight of the patient (in kg)										*
 *	ibw:	IBW of the patient (in kg)											*
 *																				*
 *	DW = ((weight - IBW) * 0.4) + IBW
 *																				*
 *	Returns the DW (in kg) as a number											*
 ********************************************************************************/
function calculateDW(weight, ibw) {
	var dw;
	
	if (ibw > 0 && weight > 0) {
		if (weight > (1.2 * ibw)) {
			dw = ((weight - ibw) * 0.4) + ibw;
		}
		
		dw = round(dw, 1);
	}
	
	return dw;
}


/********************************************************************************
 *	calculateCrCl()		Returns CrCl and CrCl weight for the patient			*/
/********************************************************************************
 *	age:	Age of the patient (years)											*
 *	sex:	Sex of the patient (male or female)									*
 *	scr:	SCr of the patient (in umol/L)										*
 *	weight:	Actual body weight of the patient (in kg)							*
 *	ibw:	IBW of the patient (in kg)											*
 *	dw:		DW of the patient (in kg)											*
 *																				*
 *	Male CrCl = ((140 - age) * weight/IBW/DW * 1.2) / SCr						*
 *	Female CrCl = ((140 - age) * weight/IBW/DW) / SCr							*
 *																				*
 *	Returns the CrCl, name of weight used, value of weight used as an object	*
 ********************************************************************************/
function calculateCrCl(age, sex, scr, weight, ibw, dw) {
	var cwValue;
	var cwSource;
	var crcl;
	var normalized = false;
	
	//Determines the weight to use to calculate CrCl
	if (dw) {
		cwValue = dw;
		cwSource = "DW";
	} else if (weight > 0 && ibw > 0 && weight < ibw) {
		cwValue = weight;
		cwSource= "ABW";
	} else if (weight > 0 && ibw > 0 && weight > ibw) {
		cwValue = ibw;
		cwSource = "IBW";
	} else if (weight > 0) {
		cwValue = weight;
		cwSource = "ABW";
	} else if (ibw > 0) {
		cwValue = ibw;
		cwSource = "IBW";
	} else {
		normalized = true;
		cwValue = 90;
		cwSource = "normalized"
	}
	
	if (normalized === false && age > 0 && cwValue > 0 && scr > 0) {
		if (sex === "Male") {
			crcl = ((140 - age) * 1.2 * cwValue) / scr;
		} else if (sex === "Female") {
			crcl = ((140 - age) * cwValue) / scr;
		}
		
		crcl = round(crcl, 0);
	} else if (normalized === true && age > 0 && scr > 0) {
		if (sex === "Male") {
			crcl = ((140 - age) * 90) / scr;
		} else if (sex === "Female") {
			crcl = ((140 - age) * 90 * 0.85) / scr;
		}
		
		crcl = round(crcl, 0);
	}
	
	return {value: crcl, source: cwSource, weight: cwValue};
}


/********************************************************************************
 *	roundDose()			Rounds vancomcyin dose to nearest 250/500 mg			*/
/********************************************************************************
 *	Dose:	Dose of vancomycin in mg											*
 *																				*
 *	Rounds to nearest 50 mg if dose < 50 mg or nearest 250 mg (all other doses)	*
 *																				*
 *	Returns the dose (in mg) as a number										*
 ********************************************************************************/
function roundDose(dose) {
	dose = dose < 500 ? 
		   Math.round(dose / 50) * 50 : 
		   Math.round(dose / 250) * 250;
	
	return dose;
}


/********************************************************************************
 *	calculateInterval()		Determines the maintenance dosing interval			*/
/********************************************************************************
 *	crcl:	The calculated creatinine clearance for the patient (in mL/min)		*
 *	target:	The target trough level for the patient								*
 *																				*
 *					10-20 mg/L		15-20 mg/L									*
 *	≥ 80 mL/min: 	Q12H			Q8H											*
 *	40-79 mL/min: 	Q24H			Q12H										*
 *	20-39 mL/min: 	Q36H			Q24H										*
 *	10-19 mL/min: 	Q48H			Q48H										*
 *	< 10 mL/min: 	Consider LD and PK consult									*
 *																				*
 *	Returns the both text and number of the calculate interval					*
 ********************************************************************************/
function calculateInterval(crcl, target) {
	var intervalText;
	var intervalNumber;
	if (crcl > 0) {
		if (target === "10-20 mg/L") {
			if (crcl < 10) {
				intervalText = "Consider loading dose &#38; PK consult";
				intervalNumber = 0;
			} else if (crcl < 20) {
				intervalText = "Q48H";
				intervalNumber = 48;
			} else if (crcl < 40) {
				intervalText = "Q36H";
				intervalNumber = 36;
			} else if (crcl < 80) {
				intervalText = "Q24H";
				intervalNumber = 24;
			} else {
				intervalText = "Q12H";
				intervalNumber = 12;
			}
		} else if (target === "15-20 mg/L") {
			if (crcl < 10) {
				intervalText = "Consider loading dose &#38; PK consult";
				intervalNumber = 0;
			} else if (crcl < 20) {
				intervalText = "Q48H";
				intervalNumber = 48;
			} else if (crcl < 40) {
				intervalText = "Q24H";
				intervalNumber = 24;
			} else if (crcl < 80) {
				intervalText = "Q12H";
				intervalNumber = 12;
			} else {
				intervalText = "Q8H";
				intervalNumber = 8;
			}
		}
	}
	
	return {text: intervalText, number: intervalNumber};
}


/********************************************************************************
 *	calculateKe()		Returns the Ke of the patient							*/
/********************************************************************************
 *	crcl:	The calculated creatinine clearance for the patient (in mL/min)		*
 *																				*
 *	ke = (0.00083 * crcl) + 0.0043												*
 *																				*
 *	Returns the calculated ke (in h^-1) as a number								*
 ********************************************************************************/
function calculateKe(crcl) {
	var ke;
	
	if (crcl > 0) {
		ke = round((0.00083 * crcl), 3);
		ke = round(ke + 0.0043, 3);
	}
	
	return ke;
}


/********************************************************************************
 *	calculateT12()		Returns the half-life of the patient					*/
/********************************************************************************
 *	ke:	The rate constant of the patient (in h^-1)								*
 *																				*
 *	t1/2 = 0.693 * ke															*
 *																				*
 *	Returns the calculated t1/2 (in h) as a number								*
 ********************************************************************************/
function calculateT12(ke) {
	var t12;
	
	if (ke > 0) {
		t12 = 0.693 / ke;
		t12 = round(t12, 0);
	}
	
	return t12;
}


/********************************************************************************
 *	calculateTss()		Returns the time-to-steady state for the patient		*/
/********************************************************************************
 *	t12:	The calculated half-life for the patient (in h)						*
 *																				*
 *	tss = 4 to 5 * t12															*
 *																				*
 *	Returns the calculated tss as a range of 4-5 half-lives (as an object)		*
 ********************************************************************************/
function calculateTss(t12) {
	var tssLower;
	var tssUpper;
	
	if (t12 > 0) {
		tssLower = t12 * 4;
		tssUpper = t12 * 5;
	}

	return {lower: tssLower, upper: tssUpper};
}


/********************************************************************************
 *	drawLevel()		Generates text explaining when to draw level				*/
/********************************************************************************
 *	tss:	Object with the the lower and upper bounds of the tss (in h)		*
 *	tau:	Dosing interval (in hours)											*
 *																				*
 *	tss = 4 to 5 * t12															*
 *																				*
 *	Returns text stating when to draw level										*
 ********************************************************************************/
function drawLevel(tss, tau) {
	var drawLower;
	var drawUpper;
	var draw;
	var drawArray = [];
	
	function returnOrdinal(number) {
		number = number === 1 || number === 2 ? "2nd" : 
				 number === 3 ? "3rd" : number + "th";
		
		return number;
	}
	
	if (tss.lower > 0 && tss.upper > 0 && tau > 0) {
		// Calculate the closest dose to tss at each bound (rounded up)
		drawLower = Math.ceil(tss.lower / tau);
		drawUpper = Math.ceil(tss.upper / tau);
		
		if (returnOrdinal(drawLower) === returnOrdinal(drawUpper)) {
			draw = returnOrdinal(drawUpper);
			draw = "Draw trough level 30 minutes before the " + draw + " dose";
		} else {
			// Generate array of integers (of doses to draw levels before)
			for (var i = drawLower; i <= drawUpper; i++) {
				drawArray.push(i);
			}
			
			// Formats the string with all the possible doses
			for (var i = 0; i < drawArray.length; i++) {
				if (i === 0) {
					draw = "Draw trough level 30 minutes before the " + 
						   returnOrdinal(drawArray[i]);
				} else if (i > 0 && i < drawArray.length - 1) {
					draw += ", " + returnOrdinal(drawArray[i]);
				} else {
					draw += " or " + returnOrdinal(drawArray[i]) + " dose";
				}
			}
		}
		
		
	}
	
	return draw;
}


/********************************************************************************
 *	calculateCmax()		Returns the Cmax for the provided data					*/
/********************************************************************************
 *	dose:	Dose of vancomcyin (in mg)											*
 *	vd:		Volume of distribution (in L)										*
 *	ke:		Rate constant of patient (in h^-1)									*
 *	tau:	Dosing interval (in hours)											*
 *																				*
 *	cmax = dose / (vd * (1 - e^(-ke * tau)))									*
 *																				*
 *	Returns the calculated cmax as a number										*
 ********************************************************************************/
function calculateCmax(dose, vd, ke, tau) {
	var cmax;
	
	if (dose > 0 && vd > 0 && ke > 0 && tau > 0) {
		cmax = dose / (vd * (1 - Math.pow(Math.E, -ke * tau)))
		cmax = round(cmax, 1);
	}
	
	return cmax;
}


/********************************************************************************
 *	calculateCmin()		Returns the Cmin for the provided data					*/
/********************************************************************************
 *	Cmax:	The calculated Cmax for the patient (in mg/L)						*
 *	ke:		Rate constant of patient (in h^-1)									*
 *	tau:	Dosing interval (in hours)											*
 *																				*
 *	cmax = dose / (vd * (1 - e^(-ke * tau)))									*
 *																				*
 *	Returns the calculated cmax as a number										*
 ********************************************************************************/
function calculateCmin(cmax, ke, tau) {
	var cmin;
	
	if (cmax > 0 && ke > 0 && tau > 0) {
		cmin = cmax * Math.pow(Math.E, -ke * tau);
		cmin = round(cmin, 1);
	}
	
	return cmin;
}




/********************************************************************************
 *	FORM FUNCTIONS																*
 ********************************************************************************/
/********************************************************************************
 *	includeLoadingDose()	Updates form display to hide or show loading dose	*
 ********************************************************************************/
 function includeLoadingDose() {
	var includeRadio = $(".Loading-Include-Radio:checked").val();
	var $includeDiv = $(".Loading-Include");
	
	$includeDiv.each(function(index, element) {
		if (includeRadio === "Yes") {
			$(this).removeClass("No");
		} else if (includeRadio === "No") {
			$(this).addClass("No");
		}
	});
	
	// Trigger Follow-up Functions
	updateLoadingDose();
}

 
/********************************************************************************
 *	updateData()	Updates the Patient Data Section							*
 ********************************************************************************/
function updateData() {
	var age = $("#Patient-Age").val();
	var sex = $("#Patient-Sex").val();
	var height = $("#Patient-Height").val();
	var heightUnit = $("#Patient-Height-Unit").val();
	var weight = $("#Patient-Weight").val();
	var weightUnit = $("#Patient-Weight-Unit").val();
	var scr = $("#Patient-Scr").val();
	var $ibw = $("#Patient-Ibw");
	var ibw;
	var $dw = $("#Patient-Dw");
	var dw;
	var $crcl = $("#Patient-Crcl");
	var crcl;
	
	//Converts height and weight to metric (if required)
	if (heightUnit === "in") {
		height = height * 2.54;
	}
	
	if (weightUnit === "lb") {
		weight = weight / 2.2;
	}
	
	//Calculate IBW, DW, and CrCl
	ibw = calculateIBW(sex, height);
	dw = calculateDW(weight, ibw);
	crcl = calculateCrCl(age, sex, scr, weight, ibw, dw);
	
	//Updates HTML Elements
	$ibw.text(ibw ? ibw + " kg" : "");
	$dw.text(dw ? dw + " kg" : "N/A");
	$crcl.text(crcl.value ? crcl.value + " mL/min (" + crcl.source + ")" : "")
		 .attr("data-crcl", crcl.value)
		 .attr("data-weight-value", crcl.weight)
		 .attr("data-weight-source", crcl.source);
	
	// Trigger Follow-Up Function
	updateLoadingDose();
	mathData(sex, height, age, weight, ibw, dw, scr, crcl.value, 
			 crcl.source, crcl.weight);
}


/********************************************************************************
 *	updateLoadingDose()		Updates the loading dose section					*
 ********************************************************************************/
function updateLoadingDose() {
	var dosePerWeight = $("#Loading-Weight").val();
	var weight = $("#Patient-Weight").val()
	var weightUnit = $("#Patient-Weight-Unit").val();
	var $ld = $("#Loading-Dose");
	var ld;
	var $ldRounded = $("#Loading-Dose-Rounded");
	var ldRounded;
	
	//Convert weight to metric (if required)
	if (weightUnit === "in") {
		weight = weight * 2.54;
	}
	
	//Calculates the loading dose
	if (weight > 0 && dosePerWeight > 0) {
		ld = weight * dosePerWeight;
		ld = round(ld, 0);
		ldRounded = roundDose(ld);
	}
	
	// Update HTML Elements
	$ld.text(ld ? ld + " mg" : "");
	$ldRounded.text(ldRounded ? ldRounded + " mg" : "")
			  .attr("data-dose", ldRounded);
	
	// Trigger Follow-up Functions
	updateMaintenanceDose();
	mathLoading(weight, dosePerWeight, ld, ldRounded);
}


/********************************************************************************
 *	updateMaintenanceDose()		Updates the maintenance dose section			*
 ********************************************************************************/
function updateMaintenanceDose() {
	var target = $("#Maintenance-Target").val();
	var dosePerWeight = $("#Maintenance-Weight").val();
	var weight = $("#Patient-Weight").val()
	var weightUnit = $("#Patient-Weight-Unit").val();
	var $md = $("#Maintenance-Dose");
	var md;
	var $mdRounded = $("#Maintenance-Dose-Rounded");
	var mdRounded;
	var crcl = $("#Patient-Crcl").attr("data-crcl");
	var $interval = $("#Maintenance-Interval");
	var interval;
	
	//Convert weight to metric (if required)
	if (weightUnit === "in") {
		weight = weight * 2.54;
	}
	
	//Calculates the maintenance dose
	if (weight > 0 && dosePerWeight > 0) {
		md = weight * dosePerWeight;
		md = round(md, 0);
		mdRounded = roundDose(md);
		mdRounded = mdRounded > 2000 ? 2000 : mdRounded;
	}
	
	// Calculates the dosing interval
	interval = calculateInterval(crcl, target);
	
	// Update HTML Elements
	$md.text(md ? md + " mg" : "");
	$mdRounded.text(mdRounded ? mdRounded === 2000 ? 
					mdRounded + " mg (maximum 2 g/dose empirically)" : 
					mdRounded + " mg" : "");
	$interval.html(interval.text)
			 .attr("Data-Interval-Number", interval.number);
	
	// Trigger Follow-up Functions
	updatePkData(crcl, interval.number, mdRounded);
	mathMaintenance(weight, dosePerWeight, md, mdRounded, crcl, target);
}


/********************************************************************************
 *	updatePkData()		Updates the Pharmacokinetic Data section				*
 ********************************************************************************/
function updatePkData(crcl, interval, dose) {
	var $ke = $("#Patient-Ke");
	var ke;
	var $t12 = $("#Patient-T12");
	var t12;
	var $tss = $("#Patient-Tss");
	var tss;
	var $vd = $("#Patient-Vd");
	var vd;
	var weight;
	var crclWeight = $("#Patient-Crcl").attr("data-weight-source");
	var $cmax = $("#Patient-Cmax");
	var cmax;
	var $cmin = $("#Patient-Cmin");
	var cmin;
	var $draw = $("#Maintenance-Draw");
	var draw;
	
	// Determines weight
	weight = crclWeight === "normalized" ? undefined :  
							$("#Patient-Crcl").attr("data-weight-value");
	//Calculates the pharmacokinetic parameters
	ke = calculateKe(crcl);
	t12 = calculateT12(ke);
	tss = calculateTss(t12);
	vd = round(0.7 * weight, 1);
	cmax = calculateCmax(dose, vd, ke, interval);
	cmin = calculateCmin(cmax, ke, interval);
	
	//Determines when to draw the vancomycin level
	draw = drawLevel(tss, interval);
	
	//Updates HTML spans
	$ke.html(ke ? ke + " h<sup>-1</sup>" : "");
	$t12.text(t12 ? t12 + " h" : "");
	$tss.text(tss.lower && tss.upper ? tss.lower + " to " + tss.upper + " h" : "");
	$vd.text(vd ? vd + " L (0.7 L/kg)" : "0.7 L/kg");
	$cmax.text(cmax ? cmax + " mg/L" : "");
	$cmin.text(cmin ? cmin + " mg/L" : "");
	$draw.text(draw ? draw : interval > 0 ? "" : "N/A");
	
	// Trigger Follow-up Functions
	if (dose > 0 && interval > 0 && ke > 0 && vd > 0) {
		generateGraph(dose, interval, ke, vd);
	};
	mathPk(crcl, ke, t12, tss, weight, crclWeight, dose, vd, interval, cmax, cmin);
}


/********************************************************************************
 *	generateGraph()		Generates graph based on the level verification data	*/
/********************************************************************************
 * 		Dose:	Vancomycin dose (in mg)											*
 *		Tau:	Vancomycin dosing interval (in hours)							*
 *		Ke:		Ke of patient (in h^-1)											*
 *		Vd:		Vd of patient (in L)											*
 *																				*
 *		Cp = cp0 * e^(-ke * t)													*
 *																				*
 *		Calculates doses to a minimum of 5 half-lives (finishing at the next 	*
 *		trough)																	*
 ********************************************************************************
 *		Canvas is 500 px tall with variable width								*
 *		Padding is applies to left and bottom borderStyle						*
 ********************************************************************************/
function generateGraph(dose, tau, ke, vd) {
	// Object to hold the x-y coordinates of the graph
	function Coordinates(x, y) {
		this.x = x;
		this.y = y;
	}
	
	// Function to calculate concentration
	function calcConc(cp0, ke, t) {
		var cp;
		
		cp = cp0 * Math.pow(Math.E, -ke * t);
		
		return cp;
	}
	
	var coordinates = [];
	var tss;
	var end;
	var loadingInclude = $(".Loading-Include-Radio:checked").val();
	var loadingDose = $("#Loading-Dose-Rounded").attr("data-dose");
	var loadingBolus;
	var maintenanceBolus;
	var arrayEnd;
	var cp0;
	var cp;
	
	var canvas = document.getElementById("Graph");
	var context = canvas.getContext("2d");
	var canvasHeight = canvas.height;
	var canvasWidth = canvas.width;
	var lbPadding = 40;
	var trPadding = 10;
	var xMax;	//Maximum x value
	var yMax;	//Maximum y value
	var xScale;	//Scale to fit coordinates on graph
	var yScale;	//Scale to fit coordinates on graph
	var tempX;	//Temp variables to graph coordinates
	var tempY;	//Temp variables to graph coordinates
	var xAxis;
	var yAxis;
	
	// Calculates how many 30 minute intervals are required to reach end point
	tss = calculateT12(ke) * 5;
	end = (Math.ceil(tss / tau) + 1) * tau * 2;
	
	// Calculates the concentration at each time point (30 minute intervals)
	coordinates[0] = new Coordinates(0, 0);
	
	// Adds initial dose (either loading dose or a maintenance dose)
	loadingBolus = loadingDose / vd;
	maintenanceBolus = dose / vd;
	
	if (loadingInclude === "Yes" && loadingDose > 0) {
		coordinates[1] = new Coordinates(1 / 60, loadingBolus);
	} else {
		coordinates[1] = new Coordinates(1 / 60, maintenanceBolus);
	}
	
	
	// Apply metabolism to data and adds a new maintenance bolus every tau
	for (var i = 1; i < end; i++) {
		arrayEnd = coordinates.length;
		time = i * 0.5;
		cp0 = coordinates[arrayEnd - 1].y;
		cp = calcConc(cp0, ke, 0.5);
		cp += time % tau === 0 ? maintenanceBolus : 0;
		
		coordinates[arrayEnd] = new Coordinates(time, cp);
	}
	
	//Determine x-axis scale
	xMax = coordinates[coordinates.length - 1].x;
	xScale = xMax / (canvasWidth - lbPadding - trPadding);	
	
	//Largest y value (rounded up to nearest 10)/available canvas space
	yMax = Math.max.apply(Math, coordinates.map(function(o){return o.y;}))
	yScale =  yMax / (canvasHeight - lbPadding - trPadding);	
	
	//Resets the canvas to draw the graph
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.moveTo(0, canvasHeight);
	
	//Draw background of graph
	context.fillStyle = "rgb(255, 255, 255)";
	context.fillRect(lbPadding, 0, canvasWidth - lbPadding, 
					canvasHeight - lbPadding);
	
	//Create x-axis
	context.lineWidth = 2;
	context.beginPath();
	tempX = lbPadding - 1;
	tempY = canvasHeight - lbPadding;
	context.moveTo(tempX, tempY);
	tempX = canvasWidth;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	//Create y-axis
	context.beginPath();
	tempX = lbPadding;
	tempY = 0;
	context.moveTo(tempX, tempY);
	tempY = canvasHeight - lbPadding;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	//Draw lines at 10, 15, and 20 mg/L
	context.lineWidth = 1;
	context.strokeStyle = "rgb(41, 138, 0)";
	context.beginPath();
	tempX = lbPadding;
	tempY = canvasHeight - lbPadding - (10 / yScale);
	context.moveTo(tempX, tempY);
	tempX = canvasWidth;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	context.beginPath();
	tempX = lbPadding;
	tempY = canvasHeight - lbPadding - (15 / yScale);
	context.moveTo(tempX, tempY);
	tempX = canvasWidth;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	context.beginPath();
	tempX = lbPadding;
	tempY = canvasHeight - lbPadding - (20 / yScale);
	context.moveTo(tempX, tempY);
	tempX = canvasWidth;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	//Labels the x-axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "12px Arial";
	context.textAlign = "center";
	context.textBaseline = "top"
	for (i = 1; i * 4 <= xMax; i++)
	{
		xAxis = i * 4;
		tempX = lbPadding + (xAxis / xScale);
		tempY = canvasHeight - lbPadding + 4;
		context.fillText(xAxis, tempX, tempY);
	}
	
	
	//Labels the y-axis
	context.textAlign = "right";
	context.textBaseline = "middle";
	for (i = 1; i * 5 <= end; i++)
	{
		yAxis = i * 5;
		tempY = canvasHeight - lbPadding - (yAxis / yScale);
		tempX = lbPadding - 4;
		context.fillText(yAxis, tempX, tempY);
	}
	
	//Draws coordinates
	context.lineWidth = 2;
	context.strokeStyle = "rgb(0, 0, 0)";
	context.beginPath();
	for (i = 0; i < coordinates.length; i++) {
		tempX = (coordinates[i].x / xScale) + lbPadding;
		tempY = canvasHeight - lbPadding - (coordinates[i].y / yScale);
		context.lineTo(tempX, tempY);
	}
	context.stroke();
	
	//Title the axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "bold 14px Arial";
	context.textAlign = "center";
	context.textBaseline = "alphabetic";
	tempX = ((canvasWidth - lbPadding - trPadding) / 2) + 15;
	tempY = canvasHeight - 2;
	context.fillText("Time (h)", tempX, tempY);
	
	context.textBaseline = "top";
	context.save();
	tempX = 5;
	tempY = ((canvasHeight - lbPadding - trPadding) / 2);
	context.translate(tempX, tempY);
	context.rotate(-Math.PI/2);
	context.fillText("Concentration (mg/L)", 0, 0);
	context.restore();
}





/********************************************************************************
 *	MATHJAX FUNCTIONS															*
 ********************************************************************************/
/********************************************************************************
 *	mathData()			Math used for calculating the patient data				*
 ********************************************************************************/
function mathData(sex, height, age, abw, ibw, dw, scr, crcl, cwSource, cwValue) {
	var $ibw = $("#Math-Ibw");
	var $crcl = $("#Math-Crcl");
	
	var equation;
	var tempNum;
	
	//IBW Calculation
	equation = "\\begin{align}";
	
	if (sex === "Male") {
		equation += "IBW\\ (Male) & = 50\\ kg + \\left(\\frac {0.92\\ kg}{cm}" +
					" * height\\ over\\ 150\\ cm\\right) &\\\\[5pt]";
	} else if (sex === "Female") {
		equation += "IBW\\ (Female) & = 50\\ kg + \\left(\\frac {2.3\\ kg}{cm}" +
					"* height\\ over\\ 150\\ cm\\right) &\\\\[5pt]";
	}
	
	if (height > 0) {
		if (sex === "Male") {
			tempNum = height - 150;
			tempNum = round(tempNum, 1);
			equation += "& = 50\\ kg + \\left(\\frac {0.92\\ kg}{cm} * " + 
						tempNum + "\\ cm\\right) &\\\\[5pt]";
			
			tempNum = tempNum * 0.92;
			tempNum = round(tempNum, 1);
			equation += "& = 50\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
			
			equation += "& = " + ibw + "\\ kg &\\\\[10pt]";
		} else if (sex === "Female") {
			tempNum = height - 150;
			tempNum = round(tempNum, 1);
			equation += "& = 45.5\\ kg + \\left(\\frac {0.92\\ kg}{cm} * " + 
						tempNum + "\\ cm\\right) &\\\\[5pt]";
			
			tempNum = tempNum * 0.92;
			tempNum = round(tempNum, 1);
			equation += "& = 45.5\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
			
			equation += "& = " + ibw + "\\ kg &\\\\";
		}
	}
	
	//Dosing weight calculation (if needed)
	if (cwSource === "DW") {
		equation += "DW & = IBW + ((ABW - IBW) * 0.4) &\\\\[5pt]";
		equation += " & = " + ibw + "\\ kg + ((" + abw + "\\ kg  -" + ibw + 
					"\\ kg) * 0.4) &\\\\[5pt]";
		
		tempNum = (abw - ibw) * 0.4;
		tempNum = round(tempNum, 1);
		equation += " & = " + ibw + "\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
		
		equation += " & = " + dw + "\\ kg &\\\\";
	}
	
	equation += "\\end{align}";
	
	$ibw.html(equation);
	
	//CrCl Calculations
	equation = "\\begin{align}";
	
	if (sex === "Male") {
		equation += "CrCl\\ (Male) & = \\frac{\\left(140 - age\\right) " + 
					"* weight}{SCr} * 1.2 &\\\\[5pt]";
	} else if (sex === "Female") {
		equation += "CrCl\\ (Female) & = \\frac{\\left(140 - age\\right) " + 
					"* weight}{SCr} &\\\\[5pt]";
	}
	
	if (age > 0 & cwValue > 0 && scr > 0) {
		if (sex === "Male") {
			equation += "& = \\frac{\\left(140 - " + age + "\\right) * " + 
						cwValue + "\\ kg\\ (" + cwSource + ")}{" + scr + 
						"\\ \\mu mol/L} * 1.2 &\\\\[5pt]";
			
			tempNum = (140 - age) * cwValue;
			tempNum = round(tempNum, 1);
			equation += "& = \\frac{" + tempNum + "}{" + scr + 
						"\\ \\mu mol/L} * 1.2 &\\\\[5pt]";
			
			equation += "& = " + crcl + "\\ mL/min &\\\\";
		} else if (sex === "Female") {
			equation += "& = \\frac{\\left(140 - " + age + "\\right) * " + 
						cwValue + "\\ kg\\ (" + cwSource + ")}{" + scr + 
						"\\ \\mu mol/L} &\\\\[5pt]";
						
			tempNum = (140 - age) * cwValue;
			tempNum = round(tempNum, 1);
			equation += "& = \\frac{" + tempNum + "}{" + scr + 
						"\\ \\mu mol/L} &\\\\[5pt]";
						
			equation += "& = " + crcl + "\\ mL/min &\\\\";
		}
	}
	
	equation += "\\end{align}"
	
	$crcl.html(equation);
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathLoading()		Math used for calculating the loading dose				*
 ********************************************************************************/
function mathLoading(weight, doseWeight, dose, doseRounded) {
	var $loading = $("#Math-Loading-Dose");
	var equation
	
	equation = "\\begin{align}";
	
	equation += "Loading\\ Dose & = \\frac{" + doseWeight + "\\ mg}{kg} * " + 
				"actual\\ body\\ weight &\\\\[5pt]";
				
	if (weight > 0 && doseWeight > 0) {
		equation += " & = \\frac{" + doseWeight + "\\ mg}{kg} * " + 
					weight + "\\ kg &\\\\[5pt]";
		equation += " & = " + dose + "\\ mg &\\\\[5pt]";
		equation += dose > 500 ? 
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\" :
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	$loading.html(equation);
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathMaintenance()	Math used for calculating maintenance doses			*
 ********************************************************************************/
function mathMaintenance(weight, doseWeight, dose, doseRounded, crcl, target) {
	var $maintenance = $("#Math-Maintenance-Dose");
	var $interval = $("#Math-Interval-Table");
	var $cells = $interval.find("td");
	var equation;
	
	//Maintenance Dose
	equation = "\\begin{align}";
	equation += "Maintenance\\ Dose & = dose\\ per\\ weight\\ " + 
				"* actual\\ body\\ weight &\\\\[5pt]";
					
	if (weight > 0 && doseWeight > 0) {
		equation += " & = \\frac{" + doseWeight + "\\ mg}{kg} * " + weight +
					"\\ kg &\\\\[5pt]";
		equation += " & = " + dose + "\\ mg &\\\\[5pt]";
		equation += dose > 500 ? 
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\" :
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	$maintenance.html(equation);
	
	//Interval Calculations
	//Reset table
	$cells.each(function(index, element) {
		$(element).attr("class", "");
	});
	
	if (crcl < 10) {
		if (target === "10-20 mg/L") {
			$cells.eq(13).attr("class", "intervalSelected");
		} else if (target === "15-20 mg/L") {
			$cells.eq(13).attr("class", "intervalSelected");
		}
	} else if (crcl < 20) {
		if (target === "10-20 mg/L") {
			$cells.eq(10).attr("class", "intervalSelected");
		} else if (target === "15-20 mg/L") {
			$cells.eq(11).attr("class", "intervalSelected");
		}
	} else if (crcl < 40) {
		if (target === "10-20 mg/L") {
			$cells.eq(7).attr("class", "intervalSelected");
		} else if (target === "15-20 mg/L") {
			$cells.eq(8).attr("class", "intervalSelected");
		}
	} else if (crcl < 80) {
		if (target === "10-20 mg/L") {
			$cells.eq(4).attr("class", "intervalSelected");
		} else if (target === "15-20 mg/L") {
			$cells.eq(5).attr("class", "intervalSelected");
		}
	} else if (crcl >= 80) {
		if (target === "10-20 mg/L") {
			$cells.eq(1).attr("class", "intervalSelected");
		} else if (target === "15-20 mg/L") {
			$cells.eq(2).attr("class", "intervalSelected");
		}
	}
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathPk()			Math used for calculating pharmacokinetic parameters	*
 ********************************************************************************/
function mathPk(crcl, ke, t12, tss, weight, wtSource, dose, vd, tau, cmax, cmin) {
	var $ke = $("#Math-Ke");
	var $t12 = $("#Math-T12");
	var $tss = $("#Math-Tss");
	var $vd = $("#Math-Vd");
	var $cmax = $("#Math-Cmax");
	var $cmin = $("#Math-Cmin");
	var tempNum;
	var equation;
	
	//ke calculations
	equation = "\\begin{align}";
	equation += "k_e & = \\left(0.00083 * CrCl\\right) + 0.0044 &\\\\[5pt]";
	
	if (crcl > 0 && ke > 0) {
		equation += " & = \\left(0.00083 * " + crcl + 
					"\\ mL/min\\right) + 0.0044 &\\\\[5pt]";
		
		tempNum = round(crcl * 0.00083, 4);
		equation += " & = " + tempNum + "+ 0.0044 &\\\\[5pt]";
		
		equation += " & = " + ke + "\\ h^{-1} &\\\\";
	}
	
	equation += "\\end{align}";
	
	$ke.html(equation);
	
	//Half-life calculations
	equation = "\\begin{align}";
	equation += "t_{1/2} & = \\frac{0.693}{k_e} &\\\\[5pt]";
	
	if (ke > 0 && t12 > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\";
	}
	
	equation += "\\end{align}";
	
	$t12.html(equation);
	
	//Time to steady-state calculation
	equation = "\\begin{align}";
	equation += "t_{SS} & = t_{1/2} * 4\\ or\\ 5 &\\\\[5pt]";
	
	if (t12 > 0 && tss.lower > 0 & tss.upper) {
		equation += " & = " + t12 + "\\ h * 4\\ or\\ 5 &\\\\[5pt]";
		equation += " & = " + tss.lower + "\\ h\\ to\\ " + tss.upper + "\\ h &\\\\";
	}
	
	equation += "\\end{align}";
	
	$tss.html(equation);
	
	// Volume of Distribution Calculations
	equation = "\\begin{align}";
	equation += "V_{d} & = \\frac{0.7\\ L}{kg} * weight &\\\\[5pt]"
	
	if (vd > 0 && weight > 0 && wtSource) {
		equation += " & = \\frac{0.7\\ L}{kg} * " + weight + "\\  kg\\ (" +
					wtSource + ")\\ &\\\\[5pt]"
		equation += " & = " + vd + "\\ L &\\\\"
	}
	
	equation += "\\end{align}";
	
	$vd.html(equation);
	
	// Cmax Calculations
	equation = "\\begin{align}";
	equation += "C_{max} & = \\frac{Dose\\ (mg)}{V_d\\ (L) * " +
				"\\left(1 - e^{-ke * \\tau}\\right)} &\\\\[5pt]"
	
	if (dose > 0 && vd > 0 && ke > 0 && tau > 0) {
		equation += " & = \\frac{" + dose + "\\ mg}{" + vd + "\\ L " + 
					"* \\left(1 - e^{-" + ke + "\\ h^{-1} " +
					"* " + tau + "\\ h}\\right)} &\\\\[5pt]";
					
		tempNum = round(Math.pow(Math.E, -ke * tau), 3);
		equation += " & = \\frac{" + dose + "\\ mg}{" + vd + "\\ L " + 
					"* \\left(1 - " + tempNum + "\\right)} &\\\\[5pt]";
			
		tempNum = round(vd * (1 - tempNum), 2);
		equation += " & = \\frac{" + dose + "\\ mg}{" + tempNum + "\\ L} &\\\\[5pt]";
		equation += " & = " + cmax + "\\ mg/L &\\\\";
	}
	
	equation += "\\end{align}";
	
	$cmax.html(equation);
	
	// Cmin Calculations
	equation = "\\begin{align}";
	equation += "C_{min} & = C_{max} * e^{-ke * \\tau} &\\\\[5pt]"
	
	if (cmax > 0 && ke > 0 && tau > 0) {
		equation += " & = " + cmax + "\\ mg/L * e^{-" + ke + "\\ h^{-1} * " + 
					tau + "\\ h} &\\\\[5pt]"
					
		tempNum = round(Math.pow(Math.E, -ke * tau), 3);
		equation += " & = " + cmax + "\\ mg/L * " + tempNum + " &\\\\[5pt]"
		
		equation += " & = " + cmin + "\\ mg/L &\\\\"
	}
	
	equation += "\\end{align}";
	
	$cmin.html(equation);
}




 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/
//Adds event listeners
$(document).ready(function() {
	$patientData = $(".Patient-Data");
	$patientData.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateData();});
	});
	
	$loadingDose = $(".Loading-Dose");
	$loadingDose.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateLoadingDose();});
	});
	
	$loadingInclude = $(".Loading-Include-Radio");
	$loadingInclude.each(function(index, element) {
		$(this).on(
			"change",
			function() {includeLoadingDose();});
	});
	$MaintenanceDose = $(".Maintenance-Dose");
	$MaintenanceDose.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateMaintenanceDose();});
	});
	
	//Left aligns the MathJax output
	MathJax.Hub.Config({
		jax: ["input/TeX","output/HTML-CSS"],
		displayAlign: "left",
		messageStyle: "none",
		tex2jax: {preview: "none"}
	});
});

//AUC = dose (per day) / (((CrCl * 0.77) + 15.4) * 0.06))