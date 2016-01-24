/********************************************************************************
 *	STUDY BUFFALO AMINOGLYCOSIDE BUGS & DRUGS DOSING CALCULATOR					*
 *																				*
 *	Last Update: 2016-Jan-24													*
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
 *	round()		Rounds a digit to the specific number of digits					*
 ********************************************************************************
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
 *	calculateBMI()		Returns the BMI of the patient							*
 ********************************************************************************
 *	height:	Height of patient (in cm)											*
 *	weight:	Weight of the patient (in kg)										*
 *																				*
 *	Returns the BMI (in kg/m^2) as a number										*
 ********************************************************************************/
function calculateBMI(height, weight) {
	var bmi;
	
	if (height > 0 && weight > 0) {
		// Convert height to meters
		height = height / 100;
		
		bmi = weight / Math.pow(height, 2);
		bmi = round(bmi, 1);
	}
	
	return bmi;
}

 
/********************************************************************************
 *	calculateIBW()		Returns the IBW of the patient							*
 ********************************************************************************
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
 *	calculateDW()		Returns the dosing weight of the patient				*
 ********************************************************************************
 *	weight:	Weight of the patient (in kg)										*
 *	ibw:	IBW of the patient (in kg)											*
 *																				*
 *	DW = ((weight - IBW) * 0.4) + IBW
 *																				*
 *	Returns the DW (in kg) as a number											*
 ********************************************************************************/
function calculateDW(weight, ibw, bmi) {
	var dw;
	
	if (ibw > 0 && weight > 0) {
		if (weight > (1.2 * ibw) || bmi >= 30) {
			dw = ((weight - ibw) * 0.4) + ibw;
		}
		
		dw = round(dw, 1);
	}
	
	return dw;
}


/********************************************************************************
 *	calculateCrCl()		Returns CrCl and CrCl weight for the patient			*
 ********************************************************************************
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
 *	roundDose()			Rounds vancomcyin dose to nearest 250/500 mg			*
 ********************************************************************************
 *	dose:		Dose of vancomycin in mg										*
 *	nearest:	Nearest number to round dose to									*
 *																				*
 *	Returns the dose (in mg) as a number										*
 ********************************************************************************/
function roundDose(dose, nearest) {
	roundedDose = Math.round(dose / nearest) * nearest;
	
	return roundedDose;
}


/********************************************************************************
 *	calculateHdeiInterval()		Determines the maintenance dosing interval		*
 ********************************************************************************
 *	crcl:	The calculated creatinine clearance for the patient (in mL/min)		*
 *																				*
 *	≥ 60 mL/min: 	Q24H														*
 *	40-59 mL/min: 	Q36H														*
 *	20-39 mL/min: 	Q48H														*
 *	< 20 mL/min: 	Obtain PK consult											*
 *																				*
 *	Returns the both text and number of the calculate interval					*
 ********************************************************************************/
function calculateHdeiInterval(crcl) {
	var intervalText;
	var intervalNumber;
	
	if (crcl > 0) {
		if (crcl < 20) {
			intervalText = "Consider PK consult";
			intervalNumber = 0;
		} else if (crcl < 40) {
			intervalText = "Q48H";
			intervalNumber = 48;
		} else if (crcl < 60) {
			intervalText = "Q36H";
			intervalNumber = 36;
		} else {
			intervalText = "Q24H";
			intervalNumber = 24;
		}
	}
	
	return {text: intervalText, number: intervalNumber};
}


/********************************************************************************
 *	calculateConvInterval()		Determines the maintenance dosing interval		*
 ********************************************************************************
 *	crcl:	The calculated creatinine clearance for the patient (in mL/min)		*
 *																				*
 *	≥ 80 mL/min: 	Q8H															*
 *	50-79 mL/min: 	Q12H														*
 *	20-49 mL/min: 	Q24H														*
 *	< 20 mL/min: 	Obtain PK consult											*
 *																				*
 *	Returns the both text and number of the calculate interval					*
 ********************************************************************************/
function calculateConvInterval(crcl) {
	var intervalText;
	var intervalNumber;
	
	if (crcl > 0) {
		if (crcl < 20) {
			intervalText = "Consider PK consult";
			intervalNumber = 0;
		} else if (crcl < 50) {
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
	
	return {text: intervalText, number: intervalNumber};
}


/********************************************************************************
 *	calculateKe()		Returns the Ke of the patient							*
 ********************************************************************************
 *	crcl:	The calculated creatinine clearance for the patient (in mL/min)		*
 *																				*
 *	ke = (0.00293 * CrCl) + 0.014												*
 *																				*
 *	Returns the calculated ke (in h^-1) as a number								*
 ********************************************************************************/
function calculateKe(crcl) {
	var ke;

	ke	= crcl > 0 ? (0.00293 * crcl) + 0.014 : undefined;
	ke = round(ke, 4);
	
	return ke;
}


/********************************************************************************
 *	calculateT12()		Returns the half-life of the patient					*
 ********************************************************************************
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
 *	calculateTss()		Returns the time-to-steady state for the patient		*
 ********************************************************************************
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
 *	calculateCmax()		Returns the Cmax for the provided data					*
 ********************************************************************************
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
 *	calculateCmin()		Returns the Cmin for the provided data					*
 ********************************************************************************
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
 *	updateDivDisplay()	Controls div display settings based on dosing method	*
 ********************************************************************************/
 function updateDivDisplay() {
	var index = $("#Dosing-Method").prop('selectedIndex');
	var $patientData = $("#Patient-Data-Div");
	var $hdeiInitial = $("#Hdei-Init-Div");
	var $hdeiMonitoring = $("#Hdei-Hartford-Div");
	var $convLoading = $("#Conv-Load-Div");
	var $convMaint = $("#Conv-Maint-Div");
	var $syn = $("#Syn-Dose-Div");
	var $mathAll = $("#Math-Divs");
	var $mathLoading = $("#Math-Loading");
	
	if (index === 0) {
		$patientData.removeClass("hide");
		$hdeiInitial.removeClass("hide");
		$hdeiMonitoring.addClass("hide");
		$convLoading.addClass("hide");
		$convMaint.addClass("hide");
		$syn.addClass("hide");
		$mathAll.removeClass("hide");
		$mathLoading.addClass("hide");
		
		updateData();
		updateHdeiInitial();
	} else if (index === 1) {
		$patientData.addClass("hide");
		$hdeiInitial.addClass("hide");
		$hdeiMonitoring.removeClass("hide");
		$convLoading.addClass("hide");
		$convMaint.addClass("hide");
		$syn.addClass("hide");
		$mathAll.addClass("hide");
		
		updateHdeiHartford();
	} else if (index === 2) {
		$patientData.removeClass("hide");
		$hdeiInitial.addClass("hide");
		$hdeiMonitoring.addClass("hide");
		$convLoading.removeClass("hide");
		$convMaint.removeClass("hide");
		$syn.addClass("hide");
		$mathAll.removeClass("hide");
		$mathLoading.removeClass("hide");
		
		updateData();
		updateConvLoad();
	} else if (index === 3) {
		$patientData.removeClass("hide");
		$hdeiInitial.addClass("hide");
		$hdeiMonitoring.addClass("hide");
		$convLoading.addClass("hide");
		$convMaint.removeClass("hide");
		$syn.addClass("hide");
		$mathAll.removeClass("hide");
		$mathLoading.addClass("hide");
		
		updateData();
		updateConvMaint();
	} else if (index === 4) {
		$patientData.removeClass("hide");
		$hdeiInitial.addClass("hide");
		$hdeiMonitoring.addClass("hide");
		$convLoading.addClass("hide");
		$convMaint.addClass("hide");
		$syn.removeClass("hide");
		$mathAll.removeClass("hide");
		$mathLoading.addClass("hide");
		
		updateData();
		updateSyn();
	}
}


/********************************************************************************
 *	updateDivDisplay()	Controls div display settings based on aminoglcyoside	*
 ********************************************************************************/
function updateAminoglycoside() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var $hdeiInitialDose = $("#Hdei-Init-Per-Weight");
	var $hdeiHartfordDoseDiv = $("#Hdei-Hartford-Dose").closest(".Hdei-Hartford");
	var $hdeiHartfordDose = $("#Hdei-Hartford-Dose");
	var $convLoadDose = $("#Conv-Loading-Dose-Per-Weight");
	var $convMaintDose = $("#Conv-Maint-Dose-Per-Weight");
	var $synDose = $("#Syn-Dose-Per-Weight");
	var $synDivGentamicin = $("#Syn-Dose-Gentamicin");
	var $synDivAmikacin = $("#Syn-Dose-Amikacin");
	
	if (aminoglycoside === 0) {
		$hdeiInitialDose.val("7");
		$hdeiHartfordDose.val("7");
		$hdeiHartfordDoseDiv.removeClass("hide");
		$convLoadDose.val("2");
		$convMaintDose.val("2");
		$synDose.val("1");
		$synDivGentamicin.removeClass("hide");
		$synDivAmikacin.addClass("hide");
	} else if (aminoglycoside === 1) {
		$hdeiInitialDose.val("7");
		$hdeiHartfordDose.val("7");
		$hdeiHartfordDoseDiv.removeClass("hide");
		$convLoadDose.val("2");
		$convMaintDose.val("2");
		$synDose.val("1");
		$synDivGentamicin.removeClass("hide");
		$synDivAmikacin.addClass("hide");
	} else if (aminoglycoside === 2) {
		$hdeiInitialDose.val("15");
		$hdeiHartfordDoseDiv.addClass("hide");
		$convLoadDose.val("7.5");
		$convMaintDose.val("7.5");
		$synDivGentamicin.addClass("hide");
		$synDivAmikacin.removeClass("hide");
	}
	
	// Update form fields
	updateData();
	updateHdeiInitial();
	updateHdeiHartford();
	updateConvLoad();
	updateConvMaint();
	updateSyn();
}


/********************************************************************************
 *	hartfordCoord()	Calculates value for hartford nomogram lines				*
 ********************************************************************************
 * val:			The provided variable (x or y)									*
 * find:		Whether to look for the x or y value							*
 * interval:	Interval equation to use										*
 *																				*
 * Q24H Line: y = -1.0846x + 19.509												*
 * Q36H Line: y = -1.0558x + 17.335												*
 * Q48H Line: y = -0.7175x + 11.887												*
 ********************************************************************************/
function hartfordCoord(val, find, interval) {
	var m;
	var b;
	
	if (interval === "Q24H") {
		m = -0.7175;
		b = 11.887;
	} else if (interval === "Q36H") {
		m = -1.0558;
		b = 17.335;
	} else if (interval === "Q48H") {
		m = -1.0846;
		b = 19.509;
	}
	
	if (find === "y") {
		return (m * val) + b;
	} else if (find === "x") {
		return (val - b) / m;
	}
}


/********************************************************************************
 *	updateHartfordNomogram()	Updates the hartford nomogram					*
 ********************************************************************************/
function updateHartfordNomogram() {
	var time = parseFloat($("#Hdei-Hartford-Time").val());
	var level = parseFloat($("#Hdei-Hartford-Level").val());
	var dose = parseFloat($("#Hdei-Hartford-Dose").val());
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var canvas = document.getElementById("Hdei-Hartford-Graph");
	var context = canvas.getContext("2d");
	var canvasHeight = canvas.height;
	var canvasWidth = canvas.width;
	var lbPadding = 40;
	var trPadding = 10;
	var xMin = 6;
	var xMax = 14;
	var yMin = 2;
	var yMax = 14;
	var xScale;	//Scale to fit coordinates on graph
	var yScale;	//Scale to fit coordinates on graph
	var tempX;	//Temp variables to graph coordinates
	var tempY;	//Temp variables to graph coordinates
	var xAxis;
	var yAxis;
	
	function plotX(x) {
		return lbPadding + ((x - 6) / xScale);
	}
	
	function plotY(y) {
		return canvasHeight - lbPadding - ((y - 2) / yScale);
	}
		
		
	//Determine axis scales
	xScale = (xMax - xMin) / (canvasWidth - lbPadding - trPadding);
	yScale = (yMax - yMin) / (canvasHeight - lbPadding - trPadding);
	
	// Resets the canvas to draw the graph
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.moveTo(0, canvasHeight);
	context.strokeStyle = "rgb(0, 0, 0)";
	
	// Draw background of graph
	context.fillStyle = "rgb(255, 255, 255)";
	context.fillRect(lbPadding, 0, canvasWidth - lbPadding, 
					canvasHeight - lbPadding);
	
	// Create x-axis line
	context.lineWidth = 2;
	context.beginPath();
	tempX = lbPadding - 1;
	tempY = canvasHeight - lbPadding;
	context.moveTo(tempX, tempY);
	tempX = canvasWidth;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	// Label x-axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "12px Arial";
	context.textAlign = "center";
	context.textBaseline = "top";
	
	for (var i = xMin; i <= xMax; i++) {
		xAxis = i - 6;
		tempX = lbPadding + (xAxis / xScale);
		tempY = canvasHeight - lbPadding + 4;
		context.fillText(i, tempX, tempY);
	}
	
	// Title the x-axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "bold 14px Arial";
	context.textAlign = "center";
	context.textBaseline = "alphabetic";
	tempX = ((canvasWidth - lbPadding - trPadding) / 2) + 15;
	tempY = canvasHeight - 2;
	context.fillText("Time between start of infusion and sample draw (h)", tempX, tempY);
	
	// Create y-axis
	context.beginPath();
	tempX = lbPadding;
	tempY = 0;
	context.moveTo(tempX, tempY);
	tempY = canvasHeight - lbPadding;
	context.lineTo(tempX, tempY);
	context.stroke();
	
	// Label the y-axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "12px Arial";
	context.textAlign = "center";
	context.textBaseline = "top";
	
	for (var i = yMin; i <= yMax; i++) {
		yAxis = i - 2;
		tempY = 2 + canvasHeight - lbPadding - trPadding - (yAxis / yScale);
		tempX = lbPadding - 8;
		context.fillText(i, tempX, tempY);
	}
	
	// title the y-axis
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "bold 14px Arial";
	context.textAlign = "center";
	context.textBaseline = "top";
	context.save();
	tempX = 5;
	tempY = ((canvasHeight - lbPadding - trPadding) / 2);
	context.translate(tempX, tempY);
	context.rotate(-Math.PI/2);
	context.fillText("Concentration (mg/L)", 0, 0);
	context.restore();
	
	// Draw the Q24H Threshold Lines
	context.beginPath();
	tempX = plotX(6);
	tempY = plotY(hartfordCoord(6, "y", "Q24H"));
	context.moveTo(tempX, tempY);
	
	tempX = plotX(13.75);
	tempY = plotY(hartfordCoord(13.75, "y", "Q24H"));
	context.lineTo(tempX, tempY);
	
	context.stroke();
	
	// Draw the Q36H Threshold Lines
	context.beginPath();
	tempX = plotX(6);
	tempY = plotY(hartfordCoord(6, "y", "Q36H"));
	context.moveTo(tempX, tempY);
	
	tempX = plotX(14);
	tempY = plotY(hartfordCoord(14, "y", "Q36H"));
	context.lineTo(tempX, tempY);
	
	context.stroke();
	
	// Draw the Q48H Threshold Lines
	context.beginPath();
	tempX = plotX(6);
	tempY = plotY(hartfordCoord(6, "y", "Q48H"));
	context.moveTo(tempX, tempY);
	
	tempX = plotX(14);
	tempY = plotY(hartfordCoord(14, "y", "Q48H"));
	context.lineTo(tempX, tempY);
	
	tempY = plotY(2);
	context.lineTo(tempX, tempY);
	
	context.stroke();
	
	// Label the areas
	context.fillStyle = "rgb(0, 0, 0)";
	context.font = "bold 16px Arial";
	context.textAlign = "left";
	context.textBaseline = "middle";
	context.fillText("Q24H", 50, 280);
	context.fillText("Q36H", 50, 160);
	context.fillText("Q48H", 50, 90);
	
	// Draw the patient level
	if (level > 0 && aminoglycoside >= 0) {
		// Corrects level as appropriate
		if (aminoglycoside === 0 || aminoglycoside === 1) {
			level = dose > 0 ? (level / 7) * dose : "";
		} else if (aminoglycoside === 2) {
			level = level / 2;
		}
	} else {
		level = "";
	}
	
	if (level > 0 && time > 0) {
		level = level > 14 ? 14.3 : level;
		time = plotX(time);
		level = plotY(level);
		tempX = time - 7;
		tempY = level - 7;
		
		context.beginPath();
		context.strokeStyle = "rgb(41, 138, 0)";
		context.lineWidth = 3;
		context.moveTo(tempX, tempY);
		
		tempX = time + 7;
		tempY = level + 7;
		context.lineTo(tempX, tempY);
		context.stroke();
		
		context.beginPath();
		tempX = time - 7;
		tempY = level + 7;
		context.moveTo(tempX, tempY);
		
		tempX = time + 7;
		tempY = level - 7;
		context.lineTo(tempX, tempY);
		context.stroke();
	}
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
	var $bmi = $("#Patient-Bmi");
	var bmi;
	var $ibw = $("#Patient-Ibw");
	var ibw;
	var $dw = $("#Patient-Dw");
	var dw;
	var $crcl = $("#Patient-Crcl");
	var crcl;
	var dosingMethod = $("#Dosing-Method").prop('selectedIndex');
	
	//Converts height and weight to metric (if required)
	if (heightUnit === "in") {
		height = height * 2.54;
	}
	
	if (weightUnit === "lb") {
		weight = weight / 2.2;
	}
	
	//Calculate IBW, DW, and CrCl
	ibw = calculateIBW(sex, height);
	bmi = calculateBMI(height, weight);
	dw = calculateDW(weight, ibw, bmi);
	crcl = calculateCrCl(age, sex, scr, weight, ibw, dw);
	
	//Updates HTML Elements
	$bmi.html(bmi ? bmi + " kg/m<sup>2</sup>" : "");
	$ibw.text(ibw ? ibw + " kg" : "")
		.attr("data-ibw", ibw);
	$dw.text(dw ? dw + " kg" : "N/A");
	$crcl.text(crcl.value ? crcl.value + " mL/min (" + crcl.source + ")" : "")
		 .attr("data-crcl", crcl.value)
		 .attr("data-weight-value", crcl.weight)
		 .attr("data-weight-source", crcl.source);
	
	// Trigger Follow-Up Function
	if (dosingMethod === 0) {
		updateHdeiInitial();
	} else if (dosingMethod === 2) {
		updateConvLoad();
	} else if (dosingMethod === 3) {
		updateConvMaint();
	} else if (dosingMethod === 4) {
		updateSyn();
	}
	
	mathData(sex, height, age, weight, ibw, dw, scr, crcl.value, crcl.source, crcl.weight);
}


/********************************************************************************
 *	updateHdeiInitial()		Updates the HDEI initial dosing section				*
 ********************************************************************************/
function updateHdeiInitial() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var weight = $("#Patient-Crcl").attr("data-weight-value");
	var source = $("#Patient-Crcl").attr("data-weight-source");
	var dosePerWeight = $("#Hdei-Init-Per-Weight").val();
	var $dose = $("#Hdei-Init-Per-Mg");
	var dose;
	var $doseRounded = $("#Hdei-Init-Rounded-Dose");
	var roundTo = aminoglycoside === 2 ? 50 : 20;
	var doseRounded;
	var crcl = $("#Patient-Crcl").attr("data-crcl");
	var $interval = $("#Hdei-Init-Interval");
	var interval;
	
	// Calculate Values
	dose = round(weight * dosePerWeight, 0);
	doseRounded = roundDose(dose, roundTo);
	interval = calculateHdeiInterval(crcl);
	
	// Update HTML elements
	$dose.text(dose ? dose + " mg" : "")
	$doseRounded.text(doseRounded ? doseRounded + " mg" : "");
	$interval.text(interval.text);
	
	// Trigger follow-up functions
	updatePkData(crcl, interval.number, doseRounded);
	mathHdeiMaintenance(weight, dosePerWeight, dose, doseRounded, crcl, source);
}
 
 
/********************************************************************************
 *	updateHdeiHartford()		Updates the HDEI Hartford nomogram section		*
 ********************************************************************************/
function updateHdeiHartford() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var time = $("#Hdei-Hartford-Time").val();
	var level = $("#Hdei-Hartford-Level").val();
	var dose = $("#Hdei-Hartford-Dose").val();
	var y24;
	var y36;
	var y48;
	var $recommendation = $("#Hdei-Hartford-Recom");
	var recommendation;
	
	
	if (level > 0 && aminoglycoside >= 0) {
		// Corrects level as appropriate
		if (aminoglycoside === 0 || aminoglycoside === 1) {
			level = dose > 0 ? (level / 7) * dose : "";
		} else if (aminoglycoside === 2) {
			level = level / 2;
		}
	} else {
		level = undefined;
	}
	
	if (level > 0 && time > 0) {
		y24 = hartfordCoord(time, "y", "Q24H");
		y36 = hartfordCoord(time, "y", "Q36H");
		y48 = hartfordCoord(time, "y", "Q48H");
		
		if (level < y24) {
			recommendation = "Q24H";
		} else if (level < y36) {
			recommendation = "Q36H";
		} else if (level < y48) {
			recommendation = "Q48H";
		} else {
			recommendation = "Discontinued extended interval dosing and switch to conventional dosing";
		}
	} else {
		recommendation = "";
	}
	
	// Update HTML elements
	$recommendation.text(recommendation);
	
	// Trigger follow-up functions
	updateHartfordNomogram();
}


/********************************************************************************
 *	updateConvLoad()		Updates the conventional loading dose section		*
 ********************************************************************************/
function updateConvLoad() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var weight = $("#Patient-Ibw").attr("data-ibw");
	var dosePerWeight = $("#Conv-Loading-Dose-Per-Weight").val();
	var $dose = $("#Conv-Loading-Dose");
	var dose;
	var $doseRound = $("#Conv-Loading-Dose-Round");
	var doseRound;
	var nearest;
	
	// Calculate loading dose
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearest = 25;
	}
	
	dose = round(weight * dosePerWeight, 1);
	doseRound = roundDose(dose, nearest);
	
	// Update HTML Elements
	$dose.text(dose ? dose + " mg" : "");
	$doseRound.text(doseRound ? doseRound + " mg" : "")
			  .attr("data-dose", doseRound);
	
	// Trigger Follow-Up Function
	updateConvMaint();
}


/********************************************************************************
 *	updateConvMaint()		Updates the conventional maintenance dose section	*
 ********************************************************************************/
function updateConvMaint() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var crcl = $("#Patient-Crcl").attr("data-crcl");
	var weight = $("#Patient-Ibw").attr("data-ibw");
	var source = $("#Patient-Crcl").attr("data-weight-source");
	var dosePerWeight = $("#Conv-Maint-Dose-Per-Weight").val();
	var $dose = $("#Conv-Maint-Dose");
	var dose;
	var $doseRounded = $("#Conv-Maint-Dose-Round");
	var doseRounded;
	var nearest;
	var $interval = $("#Conv-Maint-Interval");
	var interval;
	
	// Calculate loading dose
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearest = 25;
	}
	
	dose = round(weight * dosePerWeight, 1);
	doseRounded = roundDose(dose, nearest);
	
	// Determine Interval
	interval = calculateConvInterval(crcl);
	
	// Update HTML Elements
	$dose.text(dose ? dose + " mg" : "");
	$doseRounded.text(doseRounded ? doseRounded + " mg" : "");
	$interval.text(interval ? interval.text : "");
	
	// Trigger Follow-Up Function
	updatePkData(crcl, interval.number, dose);
	mathConvMaintenance(weight, dosePerWeight, dose, doseRounded, crcl);
}


/********************************************************************************
 *	updateSyn()				Updates the synergy dosing section					*
 ********************************************************************************/
function updateSyn() {
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var crcl = $("#Patient-Crcl").attr("data-crcl");
	var weight = $("#Patient-Ibw").attr("data-ibw");
	var dosePerWeight = $("#Syn-Dose-Per-Weight").val();
	var $dose = $("#Syn-Dose");
	var dose;
	var $doseRounded = $("#Syn-Dose-Rounded");
	var doseRounded;
	var nearest;
	var $interval = $("#Syn-Interval");
	var interval;
	
	// Calculate loading dose
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearest = 25;
	}
	
	dose = round(weight * dosePerWeight, 1);
	doseRounded = roundDose(dose, nearest);
	
	// Determine Interval
	interval = calculateConvInterval(crcl);
	
	// Update HTML Elements
	$dose.text(dose ? dose + " mg" : "");
	$doseRounded.text(doseRounded ? doseRounded + " mg" : "");
	$interval.text(interval ? interval.text : "");
	
	// Trigger Follow-Up Function
	updatePkData(crcl, interval.number, dose);
	mathConvMaintenance(weight, dosePerWeight, dose, doseRounded, crcl);
}


/********************************************************************************
 *	updatePkData()		Updates the Pharmacokinetic Data section				*
 ********************************************************************************/
function updatePkData(crcl, interval, dose) {
	var method = $("#Dosing-Method").prop('selectedIndex');
	var loadingDose;
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
	
	// Determines loading dose (if applicable)
	if (method === 2) {
		loadingDose = $("#Conv-Loading-Dose-Round").attr("data-dose");
		loadingDose = Number(loadingDose);
	}
	
	//Calculates the pharmacokinetic parameters
	ke = calculateKe(crcl);
	t12 = calculateT12(ke);
	tss = calculateTss(t12);
	vd = round(0.3 * weight, 1);
	cmax = calculateCmax(dose, vd, ke, interval);
	cmin = calculateCmin(cmax, ke, interval);
	
	//Updates HTML spans
	$ke.html(ke ? ke + " h<sup>-1</sup>" : "");
	$t12.text(t12 ? t12 + " h" : "");
	$tss.text(tss.lower && tss.upper ? tss.lower + " to " + tss.upper + " h" : "");
	$vd.text(vd ? vd + " L (0.3 L/kg)" : "0.3 L/kg");
	$cmax.text(cmax ? cmax + " mg/L" : "");
	$cmin.text(cmin ? cmin + " mg/L" : "");
	
	// Trigger Follow-up Functions
	generateGraph(dose, interval, ke, vd, loadingDose);
	mathPk(crcl, ke, t12, tss, weight, crclWeight, dose, vd, interval, cmax, cmin);
}


/********************************************************************************
 *	generateGraph()		Generates graph based on the level verification data	*
 ********************************************************************************
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
function generateGraph(dose, tau, ke, vd, loadingDose) {
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
	
	function plotX(x) {
		return lbPadding + (x / xScale);
	}
	
	function plotY(y) {
		return canvasHeight - lbPadding - (y / yScale);
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
	
	var canvas = document.getElementById("Pk-Graph");
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
	
	//Resets the canvas to draw the graph
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.moveTo(0, canvasHeight);
	
	//Draw background of graph
	context.fillStyle = "rgb(255, 255, 255)";
	context.fillRect(lbPadding, 0, canvasWidth - lbPadding, 
					canvasHeight - lbPadding);
	
	if (dose > 0 && tau > 0 && ke > 0 && vd > 0) {
		// Calculates how many 30 minute intervals are required to reach end point
		tss = calculateT12(ke) * 5;
		end = (Math.ceil(tss / tau) + 1) * tau * 2;
		
		// Calculates the concentration at each time point (30 minute intervals)
		coordinates[0] = new Coordinates(0, 0);
		
		// Adds initial dose (either loading dose or a maintenance dose)
		loadingBolus = loadingDose > 0 ? loadingDose / vd : undefined;
		maintenanceBolus = dose / vd;
		
		if (loadingBolus) {
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
		
		//Labels the y-axis & add horizontal lines as needed
		context.textAlign = "right";
		context.textBaseline = "middle";
		context.strokeStyle = "rgb(200, 200, 200)";
		context.lineWidth = 1;
		
		context.beginPath();
		tempX = plotX(0);
		tempY = plotY(1);
		context.moveTo(tempX, tempY);
		tempX = canvasWidth;
		context.lineTo(tempX, tempY);
		context.stroke();
		
		for (i = 1; i * 2 <= yMax; i++)
		{
			yAxis = i * 2;
			tempY = 2 + canvasHeight - lbPadding - (yAxis / yScale);
			tempX = lbPadding - 4;
			context.fillText(yAxis, tempX, tempY);
			
			context.beginPath();
			tempX = plotX(0);
			tempY = plotY(yAxis);
			context.moveTo(tempX, tempY);
			tempX = canvasWidth;
			context.lineTo(tempX, tempY);
			context.stroke();
			
			context.beginPath();
			tempX = plotX(0);
			tempY = plotY(yAxis + 1);
			context.moveTo(tempX, tempY);
			tempX = canvasWidth;
			context.lineTo(tempX, tempY);
			context.stroke();
		}
		
		//Draws coordinates
		context.lineWidth = 2;
		context.strokeStyle = "rgb(0, 0, 0)";
		context.beginPath();
		
		for (i = 0; i < coordinates.length; i++) {
			tempX = plotX(coordinates[i].x);
			tempY = plotY(coordinates[i].y);
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
}





/********************************************************************************
 *	MATHJAX FUNCTIONS															*
 ********************************************************************************/

/********************************************************************************
 *	mathData()			Math used for calculating the patient data				*
 ********************************************************************************/
function mathData(sex, height, age, abw, ibw, dw, scr, crcl, cwSource, cwValue) {
	var $weight = $("#Math-Weight");
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
	
	$weight.html(equation);
	
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
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var nearest;
	var equation
	
	// Determine rounding number
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearst = 25;
	}
	
	equation = "\\begin{align}";
	
	equation += "Loading\\ Dose & = \\frac{" + doseWeight + "\\ mg}{kg} * " + 
				"ideal\\ body\\ weight &\\\\[5pt]";
				
	if (weight > 0 && doseWeight > 0) {
		equation += " & = \\frac{" + doseWeight + "\\ mg}{kg} * " + 
					weight + "\\ kg &\\\\[5pt]";
		equation += " & = " + dose + "\\ mg &\\\\[5pt]";
		equation += "Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ " + nearest + "\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	$loading.html(equation);
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathHdeiMaintenance()	Math used for calculating HDEI maintenance doses	*
 ********************************************************************************/
function mathHdeiMaintenance(weight, doseWeight, dose, doseRounded, crcl, source) {
	var $maintenance = $("#Math-Maintenance-Dose");
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var nearest;
	var $interval = $("#Math-Interval-Table").find("tbody");
	var cells;
	var $cells;
	var equation;
	
	// Determine rounding number
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearst = 50;
	}
	
	//Maintenance Dose
	equation = "\\begin{align}";
	equation += "Maintenance\\ Dose & = dose\\ per\\ weight\\ " + 
				"* " + source + " &\\\\[5pt]";
	
	if (weight > 0 && doseWeight > 0) {
		equation += " & = \\frac{" + doseWeight + "\\ mg}{kg} * " + weight +
					"\\ kg &\\\\[5pt]";
		equation += " & = " + dose + "\\ mg &\\\\[5pt]";
		equation += "Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ " + nearest + "\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	$maintenance.html(equation);
	
	//Interval Calculations
	//Reset table
	$interval.empty();
	cells = "<tr><td>&#8805; 60 mL/min</td><td>Q24H</td></tr>" +
			"<tr><td>40-59 mL/min</td><td>Q36H</td></tr>" + 
			"<tr><td>20-39 mL/min</td><td>Q48H</td></tr>" + 
			"<tr><td>&#60; 20 mL/min</td><td>Obtain PK consult</td>";
	$interval.html(cells);
	$cells = $interval.find("td");

	if (crcl < 20) {
		$cells.eq(7).attr("class", "intervalSelected");
	} else if (crcl < 40) {
		$cells.eq(5).attr("class", "intervalSelected");
	} else if (crcl < 60) {
		$cells.eq(3).attr("class", "intervalSelected");
	} else if (crcl > 0) {
		$cells.eq(1).attr("class", "intervalSelected");
	}
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathConvMaintenance()	Math used for calculating HDEI maintenance doses	*
 ********************************************************************************/
function mathConvMaintenance(weight, doseWeight, dose, doseRounded, crcl) {
	var $maintenance = $("#Math-Maintenance-Dose");
	var aminoglycoside = $("#Aminoglycoside").prop("selectedIndex");
	var nearest;
	var $interval = $("#Math-Interval-Table").find("tbody");
	var cells;
	var $cells;
	var equation;
	
	// Determine rounding number
	if (aminoglycoside === 0 || aminoglycoside === 1) {
		nearest = 20;
	} else if (aminoglycoside === 2) {
		nearst = 25;
	}
	
	//Maintenance Dose
	equation = "\\begin{align}";
	equation += "Maintenance\\ Dose & = dose\\ per\\ weight\\ " + 
				"* ideal\\ body\\ weight &\\\\[5pt]";
	
	if (weight > 0 && doseWeight > 0) {
		equation += " & = \\frac{" + doseWeight + "\\ mg}{kg} * " + weight +
					"\\ kg &\\\\[5pt]";
		equation += " & = " + dose + "\\ mg &\\\\[5pt]";
		equation += "Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ " + nearest + "\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	$maintenance.html(equation);
	
	//Interval Calculations
	//Reset table
	$interval.empty();
	cells = "<tr><td>&#8805; 80 mL/min</td><td>Q8H</td></tr>" +
			"<tr><td>50-79 mL/min</td><td>Q12H</td></tr>" + 
			"<tr><td>20-49 mL/min</td><td>Q24H</td></tr>" + 
			"<tr><td>&#60; 20 mL/min</td><td>Obtain PK consult</td>";
	$interval.html(cells);
	$cells = $interval.find("td");
	
	if (crcl < 20) {
		$cells.eq(7).attr("class", "intervalSelected");
	} else if (crcl < 50) {
		$cells.eq(5).attr("class", "intervalSelected");
	} else if (crcl < 80) {
		$cells.eq(3).attr("class", "intervalSelected");
	} else if (crcl > 0) {
		$cells.eq(1).attr("class", "intervalSelected");
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
	equation += "k_e & = \\left(0.00293 * CrCl\\right) + 0.014 &\\\\[5pt]";
	
	if (crcl > 0 && ke > 0) {
		equation += " & = \\left(0.00293 * " + crcl + 
					"\\ mL/min\\right) + 0.014 &\\\\[5pt]";
		
		tempNum = round(crcl * 0.00293, 4);
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



	

/********************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/
//Adds event listeners
$(document).ready(function() {
	$dosingMethod = $("#Dosing-Method")
	$dosingMethod.on(
		"change",
		function() {updateDivDisplay();}
	);
	
	$aminoglycoside = $("#Aminoglycoside")
	$aminoglycoside.on(
		"change",
		function() {updateAminoglycoside();}
	);
	
	$patientData = $(".Patient-Data");
	$patientData.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateData();});
	});
	
	$hdeiInitial = $(".Hdei-Init");
	$hdeiInitial.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateHdeiInitial();});
	});
	
	$hdeiHartford = $(".Hdei-Hartford");
	$hdeiHartford.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateHdeiHartford();});
	});
	
	$convLoad = $(".Conv-Load");
	$convLoad.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateConvLoad();});
	});
	
	$convMaint = $(".Conv-Maint");
	$convMaint.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateConvMaint();});
	});
	
	$synDose = $(".Syn-Dose");
	$synDose.each(function(index, element) {
		$(this).on(
			"change",
			function() {updateSyn();});
	});
	
	// Start up functions
	updateDivDisplay();
	updateAminoglycoside();
	updateHartfordNomogram();
	generateGraph();
	
	//Left aligns the MathJax output
	MathJax.Hub.Config({
		jax: ["input/TeX","output/HTML-CSS"],
		displayAlign: "left",
		messageStyle: "none",
		tex2jax: {preview: "none"}
	});
});