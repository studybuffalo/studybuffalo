/********************************************************************************
 *	STUDY BUFFALO VANCOMYCIN PHARMACOKINETICS CALCULATOR						*
 *																				*
 *	Last Update: 2015-Oct-24													*
 *																				*
 *	Copyright(c) Notices														*
 *		2015	Joshua R. Torrance, BSc Pharm	<studybuffalo@studybuffalo.com>	*
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
 *	GENERAL FORM FUNCTIONS														*
 ********************************************************************************/
 /********************************************************************************
 *	processDate()		Converts user inputs into JS date variable				*
 ********************************************************************************
 * 		date:	User-inputed date												*
 ********************************************************************************/
function processDate(date){
	//Functions to convert named months to numerical values
	function convertMonth(month) {
		month = month.toUpperCase()
		
		if (month == "JAN" || month == "JANUARY") {
			return 0;
		} else if (month == "FEB" || month == "FEBRUARY") {
			return 1;
		} else if (month == "MAR" || month == "MARCH") {
			return 2;
		} else if (month == "APR" || month == "APRIL") {
			return 3;
		} else if (month == "MAY") {
			return 4;
		} else if (month == "JUN" || month == "JUNE") {
			return 5;
		} else if (month == "JUL" || month == "JULY") {
			return 6;
		} else if (month == "AUG" || month == "AUGUST") {
			return 7;
		} else if (month == "SEP" || month == "SEPT" || month == "SEPTEMBER") {
			return 8;
		} else if (month == "OCT" || month == "OCTOBER") {
			return 9;
		} else if (month == "NOV" || month == "NOVEMBER") {
			return 10;
		} else if (month == "DEC" || month == "DECEMBER") {
			return 11;
		}
	}
	
	//Determines the format of the date object
	if (/\d{4}[-/]\d{1,2}[-/]\d{1,2}/.test(date) === true) {
		//Matches "YYYY-MM-DD" format
		date = date.split(/[-/]/);
		date = date[0] + "-" + (date[1] - 1) + "-" + date[2];
	} else if (/\d{4}[-/][a-zA-Z]*[-/]\d{1,2}/.test(date) === true) {
		//Matches "YYYY-mmm-DD" or "YYYY-mmmm-DD" format
		date = date.split(/[-/]/);
		date = date[0] + "-" + convertMonth(date[1]) + "-" + date[2];
	} else if (/\d{1,2}[-/]\d{1,2}[-/]\d{4}/.test(date) === true) {
		//Matches "MM-DD-YYYY" format
		date = date.split(/[-/]/);
		date = date[2] + "-" + (date[0] - 1) + "-" + date[1];
	} else if (/[a-zA-Z]*[-/]\d{1,2}[-/]\d{4}/.test(date) === true) {
		//Matches "mmm-DD-YYYY" or "mmmm-DD-YYYY" format
		date = date.split(/[-/]/);
		date = date[2] + "-" + convertMonth(date[0]) + "-" + date[1];
	} else if (/[a-zA-Z]* \d{1,2}, \d{4}/.test(date) === true) {
		//Matches "mmmm DD, YYYY" format
		date = date.split(" ");
		date[1].replace(",", "");
		date = date[2] + "-" + convertMonth(date[0]) + "-" + date[1];
	} else {
		date = "";
	}
	
	return date;
}


/********************************************************************************
 *	processTime()		Converts user inputs into JS time variable				*
 ********************************************************************************
 *		time:	User-inputed time												*
 ********************************************************************************/
function processTime(time){
	time = time.toUpperCase();
	
	if (time.search("PM") === -1) {
		if (time.search("AM") === -1) {
			//24 Hour Time
			if (time.search(":") !== -1) {
				//hh:mm or h:mm
				time = time.split(":");
			} else if (time.length === 3) {
				//hmm
				time = [time.substring(0, 1), time.substring(1)];
			} else if (time.length === 4) {
				//hhmm
				time = [time.substring(0, 2), time.substring(2)];
			}
		} else {
			//AM 12 hour time
			time = time.replace(" AM", "").replace("AM", "");
			
			if (time.search(":") !== -1) {
				//hh:mm or h:mm
				time = time.split(":");
			} else if (time.length === 3) {
				//hmm
				time = [time.substring(0, 1), time.substring(1)];
			} else if (time.length === 4) {
				//hhmm
				time = [time.substring(0, 2), time.substring(2)];
			}
		}
	} else {
		//PM 12 hour time
		time = time.replace(" PM", "").replace("PM", "");
		
		if (time.search(":") !== -1) {
			//hh:mm or h:mm
			time = time.split(":");
		} else if (time.length === 3) {
			//hmm
			time = [time.substring(0, 1), time.substring(1)];
		} else if (time.length === 4) {
			//hhmm
			time = [time.substring(0, 2), time.substring(2)];
		}
		
		time[0] = parseInt(time[0]) + 12;
	}
	
	time = time[0] + ":" + time[1];
	
	return time;
}


/********************************************************************************
 *	processDateTime()	Converts user inputs into JS datetime variable			*
 ********************************************************************************
 * 		date:	Parsed date (to YYYY-MM-DD)										*
 *		time:	Parsed time	(to 24 hour time)									*
 ********************************************************************************/
function processDateTime(date, time){
	var dateTime;
	date = date.split("-");
	time = time.split(":");
	
	if (date[0] && date [1] && date[2] && time[0] && time[1]) {
		dateTime = new Date(date[0], date[1], date[2], time[0], time[1]);
	}
	
	return dateTime;
}


/********************************************************************************
 *	roundDose()			Rounds vancomcyin dose to nearest 250/500 mg			*
 ********************************************************************************
 * 		dose:	Dose of vancomcyin in mg; rounds to nearest 50 if dose is <		*
 *				500 mg or to nearest 250 mg for all other doses					*
 ********************************************************************************/
function roundDose(dose) {
	dose = dose < 500 ? 
		   Math.round(dose / 50) * 50 : 
		   Math.round(dose / 250) * 250;
	
	return dose;
}


/********************************************************************************
 *	roundInterval()		Rounds dosing interval to nearest appropriate interval	*
 ********************************************************************************
 * 		interval:	Interval of dosing in hours; rounds to nearest 8, 12, 24, 	*
 *					36, or 48 hours												*
 ********************************************************************************/
function roundInterval(interval) {
	interval = interval <= 10 ? 8 : 
			   interval <= 18 ? 12 : 
			   interval <= 30 ? 24 : 
			   interval <= 42 ? 36 : 48;
	
	return interval;
}


/********************************************************************************
 *	drawLevel()			Generates the text to explain when to draw level		*
 ********************************************************************************
 * 		tss:	Time to steady state (in hours) of current vancomycin dose		*
 *		tau:	Dosing interval (in hours) of current vancomcyin dose			*
 ********************************************************************************/
function drawLevel(tss, tau) {
	var draw = Math.ceil(tss / tau);
	draw = draw === 1 || draw === 2 ? "2nd" : draw === 3 ? "3rd" : draw + "th";
	draw = "Draw level 30 minutes before the " + draw + " dose";
	
	return draw;
}


/********************************************************************************
 *	extractValue()		Extracts the value from an html span					*
 ********************************************************************************
 * 		string:	The text containing the value to be extracted from the span		*
 ********************************************************************************/
function extractValue(string) {
	if (string.search(" ") !== -1) {
		string = string.split(" ");
		return string[0];
	} else {
		return string;
	}
}

/********************************************************************************
 *	HTML FORM FUNCTIONS															*
 ********************************************************************************/
/********************************************************************************
 *	showDiv()			Updates HTML divs based on user selection				*
 ********************************************************************************/
function showDiv() {
	var radio = document.getElementsByName("Dosing-Radio");
	var div = document.getElementsByName("Dosing-Div");
	var graphDiv = document.getElementById("PK-Graph");
	var mathDiv = document.getElementsByName("Math-Div");
	
	// Radio
	//	0 = Empiric dosing
	//	1 = PK: Empiric
	//	2 = PK: Peak-Trough
	//	3 = PK: C1-C2
	
	// Div & mathDiv
	//	0 = Patient data
	//	1 = Empiric dosing
	//	2 = Pharmacokinetic Parameter Calculations: Peak-Trough
	//	3 = Pharmacokinetic Parameter Calculations: C1-C2
	//	4 = Dose Calculation (Empiric)
	//	5 = Dose Calculation (PK)
	//	6 = Level Verification
	
	// Math div
	//	0 = Empiric: Weight calculations
	//	1 = Empiric: CrCl calculations
	//	2 = Empiric: Dose calculations
	//	3 = Empiric: Interval calculations
	//	4 = draw level calculations
	
	if (radio[0].checked) {
		div[0].style.display = "block";
		div[1].style.display = "block";
		div[2].style.display = "none";
		div[3].style.display = "none";
		div[4].style.display = "none";
		div[5].style.display = "none";
		div[6].style.display = "none";
		
		graphDiv.style.display = "none";
		
		mathDiv[0].className = "Math-Div";
		mathDiv[1].className = "Math-Div";
		mathDiv[2].className = "hide";
		mathDiv[3].className = "hide";
		mathDiv[4].className = "hide";
		mathDiv[5].className = "hide";
		mathDiv[6].className = "hide";
		
		data();
	} else if (radio[1].checked) {
		div[0].style.display = "block";
		div[1].style.display = "none";
		div[2].style.display = "none";
		div[3].style.display = "none";
		div[4].style.display = "block";
		div[5].style.display = "none";
		div[6].style.display = "block";
		
		graphDiv.style.display = "block";
		
		mathDiv[0].className = "Math-Div";
		mathDiv[1].className = "hide";
		mathDiv[2].className = "hide";
		mathDiv[3].className = "hide";
		mathDiv[4].className = "Math-Div";
		mathDiv[5].className = "hide";
		mathDiv[6].className = "Math-Div";
		
		data();
	} else if (radio[2].checked) {
		div[0].style.display = "none";
		div[1].style.display = "none";
		div[2].style.display = "block";
		div[3].style.display = "none";
		div[4].style.display = "none";
		div[5].style.display = "block";
		div[6].style.display = "block";
		
		graphDiv.style.display = "block";
		
		mathDiv[0].className = "hide";
		mathDiv[1].className = "hide";
		mathDiv[2].className = "Math-Div";
		mathDiv[3].className = "hide";
		mathDiv[4].className = "hide";
		mathDiv[5].className = "Math-Div";
		mathDiv[6].className = "Math-Div";
		
		parametersPeakTrough();
	} else if (radio[3].checked) {
		div[0].style.display = "none";
		div[1].style.display = "none";
		div[2].style.display = "none";
		div[3].style.display = "block";
		div[4].style.display = "none";
		div[5].style.display = "block";
		div[6].style.display = "block";
		
		graphDiv.style.display = "block";
		
		mathDiv[0].className = "hide";
		mathDiv[1].className = "hide";
		mathDiv[2].className = "hide";
		mathDiv[3].className = "Math-Div";
		mathDiv[4].className = "hide";
		mathDiv[5].className = "Math-Div";
		mathDiv[6].className = "Math-Div";
		
		parametersC1C2();
	}
}


/********************************************************************************
 *	calculateIBW()		Returns the IBW of the patient							*
 ********************************************************************************
 *		sex:		0 = male, 1 = female										*
 *		height:		height (in cm)												*
 ********************************************************************************/
function calculateIBW(sex, height) {
	//Male: 50 kg +(0.92 * cm over 150 cm)
	//Female: 45.5kg + (0.92 * cm over 150 cm)
	var ibw;
	
	if (height > 0) {
		if (sex == 0) {
			ibw = 50 + (0.9055 * (height-152.4));
		} else {
			ibw = 45.5 + (0.9055 * (height-152.4));
		}
	}
	
	return ibw;
}


/********************************************************************************
 *	calculateDW()		Returns the dosing weight of the patient				*
 ********************************************************************************
 *		height:		height (in cm)												*
 *		weight:		weight (in kg)												*
 *		ibw:		ideal body weight (in kg)									*
 ********************************************************************************/
function calculateDW(height, weight, ibw) {
	var dw;
	
	if (ibw > 0 && weight > 0) {
		if (weight > (1.2 * ibw)) {
			dw = ((weight - ibw) * 0.4) + ibw;
		}
	}
	
	return dw;
}
 
 
/********************************************************************************
 *	CrCl()				Returns CrCl and CrCl weight for the patient			*
 ********************************************************************************
 *		age:		age of the patient (years)									*
 *		sex:		0 = male, 1 = female										*
 *		scr:		Serum creatinine of patient (in umol/L)						*
 *		weight:		actual body weight (in kg)									*
 *		ibw:		ideal body weight (in kg)									*
 *		dw:			dosing weight (in kg)										*
 ********************************************************************************/
function calculateCrCl(age, sex, scr, weight, ibw, dw) {
	//Male: (140-age) * 1.2 * Wt / SCr
	//Female: (140-age) * Wt / SCr
	
	var cwValue;
	var cwSource;
	var crcl;
	
	//Determines the weight to use to calculate CrCl
	if (dw) {
		cwValue = dw;
		cwSource = "DW";
	} else if (weight > 0 && ibw > 0 && weight < ibw) {
		cwValue = weight;
		cwSource= "ABW";
	} else if (weight > 0 && ibw > 0 && ibw > weight) {
		cwValue = ibw;
		cwSource = "IBW";
	} else if (weight > 0) {
		cwValue = weight;
		cwSource = "ABW";
	} else if (ibw > 0) {
		cwValue = ibw;
		cwSource = "IBW";
	}
	
	if (age > 0 && cwValue > 0 && scr > 0) {
		if (sex == 0) {
			crcl = ((140 - age) * 1.2 * cwValue)/scr;
		} else {
			crcl = ((140 - age) * cwValue)/scr;
		}
	}
	
	return {value: crcl, source: cwSource, weight: cwValue};
}


/********************************************************************************
 *	calculateKe()		Returns the Ke of the patient							*
 ********************************************************************************
 *		crcl:		Creatinine clearance of the patient (in mL/min)				*
 ********************************************************************************/
function calculateKe(crcl) {
	var ke;
	
	if (crcl) {ke = (0.00083 * crcl) + 0.0043;}
	
	return ke;
}


/********************************************************************************
 *	calculateT12()		Returns the half-life of the patient					*
 ********************************************************************************
 *		ke:			The rate constant of the patient (in h^-1)					*
 ********************************************************************************/
function calculateT12(ke) {
	var t12;
	
	if (ke) {t12 = Math.log(2) / ke;}
	
	return t12;
}


/********************************************************************************
 *	calculateTss()		Returns the time-to-steady state for the patient		*
 ********************************************************************************
 *		t12:		The half-life of the patient (in h)							*
 ********************************************************************************/
function calculateTss(t12) {
	//t95 = 4.32 half-lives
	var tss;
	
	if (t12) {tss = t12 * 4.32;}

	return tss;
}


/********************************************************************************
 *	calculateVd()		Returns the volume of distribution for the patient		*
 ********************************************************************************
 *		dose:		The vancomycin dose for the patient (in mg)					*
 *		cmax:		The maximum concentraton for the patient (in mg/L)			*
 *		cmin:		The minimum concentraton for the patient (in mg/L)			*
 ********************************************************************************/
function calculateVd(dose, cmax, cmin) {
	var vd;
	
	if (dose && cmax && cmin) {vd = dose / (cmax - cmin)};
	
	return vd;
	
}


/********************************************************************************
 *	data()				Directs	functioning of empiric dosing calculations		*
 ********************************************************************************/
function data() {
	var dosing = document.getElementsByName("Dosing-Radio");
	var age = Number(document.getElementById("Empiric-Age").value);
	var sex = document.getElementById("Empiric-Sex").selectedIndex;
	var height = document.getElementById("Empiric-Height").value;
	var heightUnit = document.getElementById("Empiric-Height-Unit").selectedIndex;
	var weight = document.getElementById("Empiric-Weight").value;
	var weightUnit = document.getElementById("Empiric-Weight-Unit").selectedIndex;
	var scr = Number(document.getElementById("Empiric-SCr").value);
	var ibw;
	var dw;
	var crcl;
	
	//Converts height and weigh to metric (if required)
	if (heightUnit === 1) {
		height = height * 2.54;
	}
	
	if (weightUnit === 1) {
		weight = weight / 2.2;
	}
	
	//Calculate IBW, DW, and CrCl
	ibw = calculateIBW(sex, height);
	dw = calculateDW(height, weight, ibw);
	crcl = calculateCrCl(age, sex, scr, weight, ibw, dw);
	
	//Updates HTML spans
	document.getElementById("Empiric-IBW-Span").innerHTML = 
		ibw ? (Math.round(10 * ibw)/ 10) + " kg" : "";
	document.getElementById("Empiric-DW-Span").innerHTML = 
		dw ? (Math.round(10 * dw)/ 10) + " kg" : "N/A";
	document.getElementById("Empiric-CrCl-Span").innerHTML = 
		crcl.value ? 
		Math.round(crcl.value) + " mL/min (" + crcl.source + ")" : "";
		
	//Calls the appropriate dosing function based on the dosing radio
	dosing[0].checked ? doseEmpiric(weight, crcl.value) : "";
	dosing[1].checked ? doseEmpiricPK(crcl.weight, crcl.source, crcl.value) : "";
	
	//Passes data to generate the math equations
	mathData(sex, height, age, weight, ibw, dw, scr, crcl.value, crcl.source, 
			 crcl.weight);
}


/********************************************************************************
 *	doseEmpiric()		Directs	functioning of the Empiric dosing div			*
 ********************************************************************************
 *		weight:		actual body weight (in kg)									*
 *		crcl:		Creatinine clearance (in mL/min)							*
 ********************************************************************************/
function doseEmpiric(weight, crcl) {
	var loadingDoseWeight = 
		Number(document.getElementById("Empiric-Loading-Weight").value);
	var loadingDose;
	var maintenanceDoseWeight = 
		Number(document.getElementById("Empiric-Maintenance-Weight").value);
	var maintenanceDose;
	var target = 
		document.getElementById("Empiric-Maintenance-Target").selectedIndex;
	var intervalText;
	var intervalNumber;
	var ke;
	var t12;
	var tss;
	var draw;
	
	//Calculates the loading dose
	if (weight > 0 && loadingDoseWeight > 0) {
		loadingDose = weight * loadingDoseWeight;
	}
	
	//Calculates the maintenance dose
	if (weight > 0 && maintenanceDoseWeight > 0) {
		maintenanceDose = weight * maintenanceDoseWeight;
	}
	
	//Calculates the dosing interval
	if (crcl > 0) {
		if (target === 0) {
			//≥ 80 mL/min: Q12H
			//40-79 mL/min: Q24H
			//20-39 mL/min: Q36H
			//10-19 mL/min: Q48H
			//< 10 mL/min: Consider LD and PK consult
			
			if (crcl < 10) {
				intervalText = "Consider loading dose &#38; PK consult";
				intervalNumber = "As required for PK consult";
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
		} else if (target === 1) {
			//≥ 80 mL/min: Q8H
			//40-79 mL/min: Q12H
			//20-39 mL/min: Q24H
			//10-19 mL/min: Q48H
			//< 10 mL/min: Consider LD and PK consult
			
			if (crcl < 10) {
				intervalText = "Consider loading dose &#38; PK consult";
				intervalNumber = "As required for PK consult";
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
	
	//Calculates the pharmacokinetic parameters
	ke = calculateKe(crcl);
	t12 = calculateT12(ke);
	tss = calculateTss(t12);
	
	//Determines when to draw the vancomycin level
	draw = tss > 0 && intervalNumber > 0 ? drawLevel(tss, intervalNumber) : "";
	
	//Updates HTML spans
	document.getElementById("Empiric-Loading-Dose").innerHTML = 
		loadingDose ? Math.round(loadingDose) + " mg" : "";
	document.getElementById("Empiric-Loading-Round-Dose").innerHTML = 
		loadingDose ? roundDose(loadingDose) + " mg": "";
	document.getElementById("Empiric-Maintenance-Dose").innerHTML = 
		maintenanceDose ? Math.round(maintenanceDose) + " mg" : "";
	document.getElementById("Empiric-Maintenance-Round-Dose").innerHTML = 
		maintenanceDose ? roundDose(maintenanceDose) + " mg" : "";
	document.getElementById("Empiric-Maintenance-Interval-Span").innerHTML = 
		intervalText ? intervalText : "";
	document.getElementById("Empiric-Ke").innerHTML = 
		ke ? (Math.round(ke * 10000) / 10000) + " h<sup>-1</sup>" : "";
	document.getElementById("Empiric-T12").innerHTML = 
		t12 ? (Math.round(t12 * 10) / 10) + " h" : "";
	document.getElementById("Empiric-Tss").innerHTML = 
		tss ? (Math.round(tss * 10) / 10) + " h" : "";
	document.getElementById("Empiric-Draw").innerHTML = 
		draw ? draw : "";
	
	//Passes data to generate math equations
	mathEmpiric(
		weight, loadingDoseWeight, loadingDose, roundDose(loadingDose), 
		maintenanceDoseWeight, maintenanceDose, roundDose(maintenanceDose),
		target, crcl, ke, t12, tss);
}


/********************************************************************************
 *	parametersPeakTrough()	Calculates of the Peak-Trough PK parameters			*
 ********************************************************************************/
function parametersPeakTrough() {
	var dose = document.getElementById("PK-PT-Dose").value;
	var interval = document.getElementById("PK-PT-Interval").value;
	var infusionDate = document.getElementById("PK-PT-Infusion-Date").value;
	var infusionTime = document.getElementById("PK-PT-Infusion-Time").value;
	var infusionDuration = document.getElementById("PK-PT-Infusion-Duration").value;
	var infusionDateTime;
	var peak = document.getElementById("PK-PT-Peak").value;
	var peakDate = document.getElementById("PK-PT-Peak-Date").value;
	var peakTime = document.getElementById("PK-PT-Peak-Time").value;
	var peakDateTime;
	var trough = document.getElementById("PK-PT-Trough").value;
	var troughDate = document.getElementById("PK-PT-Trough-Date").value;
	var troughTime = document.getElementById("PK-PT-Trough-Time").value;
	var troughDateTime;
	var t;
	var t1
	var t2
	var ke;
	var t12;
	var cmax;
	var cmin;
	var vd;
	
	//Converts dates and times to proper datetime
	infusionDate = processDate(infusionDate);
	infusionTime = processTime(infusionTime);
	infusionDateTime = processDateTime(infusionDate, infusionTime);
	
	peakDate = processDate(peakDate);
	peakTime = processTime(peakTime);
	peakDateTime = processDateTime(peakDate, peakTime);
	
	troughDate = processDate(troughDate);
	troughTime = processTime(troughTime);
	troughDateTime = processDateTime(troughDate, troughTime);
	
	//Calculate the PK parameters
	t = troughDateTime && peakDateTime ? 
		(troughDateTime.getTime() - peakDateTime.getTime()) / 3600000 : "";
	
	ke = peak && trough && t ? Math.log(peak / trough) / t : "";
	
	t12 = calculateT12(ke);
	
	t1 = peakDateTime && infusionDateTime ?
		(peakDateTime.getTime() - infusionDateTime.getTime() - 
		(infusionDuration * 60000)) / 3600000 : "";
	
	cmax = ke && t1 ? peak / Math.pow((Math.E),(-ke * t1)) : "";
	
	t2 = infusionDateTime && interval && troughDateTime ? 
		(infusionDateTime.getTime() + (interval * 3600000) - 
		 troughDateTime.getTime()) / 3600000 : "";
		 
	cmin = ke && t2 ? trough * Math.pow((Math.E),(-ke * t2)) : "";
	
	vd = calculateVd(dose, cmax, cmin)
	
	//Update HTML spans
	document.getElementById("PK-PT-T").innerHTML = 
		t ? (Math.round(10 * t) / 10) + " h" : "";
	document.getElementById("PK-PT-Ke").innerHTML = 
		ke ? (Math.round(10000 * ke) / 10000) + " h<sup>-1</sup>" : "";
	document.getElementById("PK-PT-Ke-Input").value = 
		ke ? (Math.round(10000 * ke) / 10000) : "";
	document.getElementById("PK-PT-T12").innerHTML = 
		t12 ? (Math.round(10 * t12) / 10) + " h" : "";
	document.getElementById("PK-PT-Cmax").innerHTML = 
		cmax ? (Math.round(10 * cmax) / 10) + " mg/L" : "";
	document.getElementById("PK-PT-Cmin").innerHTML = 
		cmin ? (Math.round(10 * cmin) / 10) + " mg/L" : "";
	document.getElementById("PK-PT-Vd").innerHTML = 
		vd ? (Math.round(10 * vd) / 10) + " L" : "";
	document.getElementById("PK-PT-Vd-Input").value = 
		vd ? (Math.round(10 * vd) / 10) : "";
	
	//Generates math equations
	mathPeakTrough(infusionDateTime, infusionDuration, peakDateTime, peak, 
	troughDateTime, trough, interval, dose, t, t1, t2, ke, t12, cmax, cmin, vd);
}


/********************************************************************************
 *	parametersC1C2()	Calculates of the C1-C2 PK parameters					*
 ********************************************************************************/
function parametersC1C2() {
	var dose = document.getElementById("PK-C1C2-Dose").value;
	var interval = document.getElementById("PK-C1C2-Interval").value;
	var infusionDate = document.getElementById("PK-C1C2-Infusion-Date").value;
	var infusionTime = document.getElementById("PK-C1C2-Infusion-Time").value;
	var infusionDateTime;
	var infusionDuration = document.getElementById("PK-C1C2-Infusion-Duration").value;
	var c1 = document.getElementById("PK-C1C2-C1").value;
	var c1Date = document.getElementById("PK-C1C2-C1-Date").value;
	var c1Time = document.getElementById("PK-C1C2-C1-Time").value;
	var c1DateTime;
	var c2 = document.getElementById("PK-C1C2-C2").value;
	var c2Date = document.getElementById("PK-C1C2-C2-Date").value;
	var c2Time = document.getElementById("PK-C1C2-C2-Time").value;
	var c2DateTime;
	var t;
	var ke;
	var t12;
	var t1;
	var t2;
	var cmax;
	var cmin;
	var vd;
	
	//Converts dates and times to proper datetime
	infusionDate = processDate(infusionDate);
	infusionTime = processTime(infusionTime);
	infusionDateTime = processDateTime(infusionDate, infusionTime);
	
	c1Date = processDate(c1Date);
	c1Time = processTime(c1Time);
	c1DateTime = processDateTime(c1Date, c1Time);
	
	c2Date = processDate(c2Date);
	c2Time = processTime(c2Time);
	c2DateTime = processDateTime(c2Date, c2Time);
	
	//Calculate PK parameters
	t = c2DateTime && c1DateTime ?
		(c2DateTime.getTime() - c1DateTime.getTime()) / 3600000 : "";
	
	ke = c1 && c2 && t ? Math.log(c1 / c2) / t : "";
	
	t12 = calculateT12(ke);
	
	t1 = c1DateTime && infusionDateTime && infusionDuration ?
		(c1DateTime.getTime() - infusionDateTime.getTime() - 
		 (infusionDuration * 60000)) / 3600000 : "";
		 
	cmax = c1 && ke && t1 ? c1 / Math.pow((Math.E),(-ke * t1)) : "";
	
	t2 = interval && infusionDuration ? 
		interval - (infusionDuration / 60) : "";
	
	cmin = cmax && ke && t2 ? cmax * Math.pow((Math.E),(-ke * t2)) : "";
	
	vd = calculateVd(dose, cmax, cmin);
	
	//Updates HTML spans
	document.getElementById("PK-C1C2-Ke").innerHTML = 
		ke ? (Math.round(10000 * ke) / 10000) + " h<sup>-1</sup>" : "";
	document.getElementById("PK-C1C2-T12").innerHTML = 
		t12 ? (Math.round(10 * t12) / 10) + " h" : "";
	document.getElementById("PK-C1C2-Vd").innerHTML = 
		vd ? (Math.round(10 * vd) / 10) + " L" : "";
	
	//Generates math equations
	mathC1C2(infusionDateTime, infusionDuration, interval, c1DateTime, c1, 
			 c2DateTime, c2, t, t1, t2, cmax, cmin, ke, t12, dose, vd);
}


/********************************************************************************
 *	doseEmpiricPK()		Calculates of the empiric PK parameters					*
 ********************************************************************************
 *		weight:		Creatinine clearance weight (in kg)							*
 *		crcl:		Creatinine clearance (in mL/min)							*
 ********************************************************************************/
function doseEmpiricPK(weight, weightSource, crcl) {
	var peak = document.getElementById("PK-Empiric-Peak").value;
	var trough = document.getElementById("PK-Empiric-Trough").value;
	var vdWeight = document.getElementById("PK-Empiric-Vd-Weight").value;
	var vd;
	var dose;
	var doseRounded;
	var interval;
	var intervalRounded;
	var ke;
	var t12;
	
	//Calculations
	vd = vdWeight && weight ? vdWeight * weight : "";
	dose = vd && peak && trough ? vd * (peak - trough) : "";
	doseRounded = roundDose(dose);
	ke = calculateKe(crcl);
	interval = peak > 0 && trough > 0 && ke > 0 ? Math.log(peak / trough) / ke : "";
	intervalRounded = roundInterval(interval);
	t12 = calculateT12(ke);
	
	//Updates HTML spans
	document.getElementById("PK-Empiric-Vd").innerHTML = 
		vd ? (Math.round(10 * vd)/10) + " L (" + weightSource + ")" : "";
	document.getElementById("PK-Empiric-Dose").innerHTML = 
		dose ? Math.round(dose) + " mg" : "";
	document.getElementById("PK-Empiric-Round-Dose").innerHTML = 
		dose ? doseRounded + " mg" : "";
	document.getElementById("PK-Empiric-Interval").innerHTML = 
		interval ? (Math.round(10 * interval)/10) + " h" : "";
	document.getElementById("PK-Empiric-Round-Interval").innerHTML = 
		interval ? intervalRounded + " h" : "";
	document.getElementById("PK-Empiric-Ke").innerHTML = 
		ke ? (Math.round(ke * 10000) / 10000) + " h<sup>-1</sup>" : "";
	document.getElementById("PK-Empiric-T12").innerHTML = 
		t12 ? (Math.round(t12 * 10) / 10) + " h" : "";
	
	//Passes data to generate math equations
	mathEmpiricPK(vdWeight, weight, weightSource, vd, peak, trough, dose, 
				  doseRounded, crcl, ke, t12, interval, intervalRounded);
}


/********************************************************************************
 *	dosePK()			Calculates the dose based on PK parameters				*
 ********************************************************************************/
function dosePK() {
	var peak = document.getElementById("PK-Dose-Calc-Peak").value;
	var trough = document.getElementById("PK-Dose-Calc-Trough").value;
	var vd = document.getElementById("PK-Dose-Calc-Vd").value;
	var ke = document.getElementById("PK-Dose-Calc-Ke").value;
	var dose;
	var doseRounded;
	var t12;
	var interval;
	var intervalRounded;
	
	dose = vd && peak && trough ? vd * (peak - trough) : "";
	doseRounded = dose ? roundDose(dose) : "";
	
	t12 = calculateT12(ke);
	
	//AHS METHOD: interval = t12 ? 2 * t12 : "";
	//APPLIED CLINICAL PHARMACOKINETICS METHOD
	interval = peak && trough && ke ? (Math.log(peak) - Math.log(trough)) / ke : "";
	
	intervalRounded = interval ? roundInterval(interval) : "";
	
	document.getElementById("PK-Dose-Calc-Dose").innerHTML = dose ? Math.round(dose) + " mg" : "";
	document.getElementById("PK-Dose-Calc-Round-Dose").innerHTML = doseRounded ? doseRounded + " mg" : "";
	document.getElementById("PK-Dose-Calc-Round-Dose-Input").value = doseRounded ? doseRounded : "";
	document.getElementById("PK-Dose-Calc-T12").innerHTML = t12 ? (Math.round(10 * t12) / 10) + " h" : "";
	document.getElementById("PK-Dose-Calc-Interval").innerHTML = interval ? (Math.round(10 * interval)/10) + " h" : "";
	document.getElementById("PK-Dose-Calc-Round-Interval").innerHTML = intervalRounded ? intervalRounded + " h" : "";
	document.getElementById("PK-Dose-Calc-Round-Interval-Input").value = intervalRounded ? intervalRounded : "";
	
	//Generates math equations
	mathDosePK(vd, peak, trough, dose, doseRounded, ke, interval, 
			   intervalRounded);
}


/********************************************************************************
 *	levelVerification()		Estimates levels based on dose calculation			*
 ********************************************************************************/
function levelVerification() {
	var dose = document.getElementById("PK-Level-Dose").value;
	var interval = document.getElementById("PK-Level-Interval").value;
	var vd = document.getElementById("PK-Level-Vd").value;
	var ke = document.getElementById("PK-Level-Ke").value;
	var cmax;
	var cmin;
	var t12;
	var tss;
	
	cmax = dose && vd && ke && interval ? dose / (vd * (1 - Math.pow(Math.E, -ke * interval))) : "";
	cmin = cmax && ke && interval ? cmax * Math.pow(Math.E, -ke * interval) : "";
	
	t12 = calculateT12(ke);
	tss = calculateTss(t12);
	
	document.getElementById("PK-Level-Cmax").innerHTML = cmax ? (Math.round(10 * cmax) / 10) + " mg/L" : "";
	document.getElementById("PK-Level-Cmin").innerHTML = cmax ? (Math.round(10 * cmin) / 10) + " mg/L" : "";
	document.getElementById("PK-Level-Tss").innerHTML = tss ? (Math.round(10 * tss) / 10) + " h" : "";
	if (dose > 0 && interval > 0 && ke > 0 && vd > 0) {
		generateGraph(dose, interval, ke, vd);
	}
	
	//Generates math equations
	mathLevel(dose, vd, ke, interval, cmax, cmin, t12, tss);
}


/********************************************************************************
 *	generateGraph()		Generates graph based on the level verification data	*
 ********************************************************************************
 * 		Dose:	Vancomycin dose (in mg)											*
 *		Tau:	Vancomycin dosing interval (in hours)							*
 *		Ke:		Ke of patient (in h^-1)											*
 *		Vd:		Vd of patient (in L)											*
 *																				*
 *		Cp:		Concentration of vancomcyin at time since last dose (t) and		*
 *				number of doses (n)												*
 *		Cp =	(dose / vd) * e^(-ke * t) * 									*
 *				((1 - e^(-n * ke * tau)) / (1 - e^(-ke * tau)))					*
 *																				*
 *		Calculates doses to a minimum of 5 half-lives (finishing at the next 	*
 *		trough)																	*
 ********************************************************************************
 *		Canvas is 500 px tall with variable width								*
 *		Padding is applies to left and bottom borderStyle						*
 ********************************************************************************/
function generateGraph(dose, tau, ke, vd) {
	//Object to hold the x-y coordinates of the graph
	function Coordinates(x, y) {
		this.x = x;
		this.y = y;
	}
	
	//Function to calculate concentration
	function calculateConcentration(dose, vd, n, ke, tau, t) {
		var c = (dose / vd) * ((1 - Math.pow(Math.E, -n * ke * tau)) / 
		        (1 - Math.pow(Math.E, -ke * tau))) * Math.pow(Math.E, -ke * t);
		return c;
	}
	
	var canvas = document.getElementById("Graph");
	var context = canvas.getContext("2d");
	var canvasHeight = canvas.height;
	var canvasWidth = canvas.width;
	var lbPadding = 40;
	var trPadding = 10;
	var coordinates = [];
	var n = 0;
	var t = 0;
	var tTotal = 0;
	var i = 0; //Counter to mark time interval since last dose
	var t12;
	var tss;
	var end;
	var xMax;	//Maximum x value
	var yMax;	//Maximum y value
	var xScale;	//Scale to fit coordinates on graph
	var yScale;	//Scale to fit coordinates on graph
	var tempX;	//Temp variables to graph coordinates
	var tempY;	//Temp variables to graph coordinates
	var xAxis;
	var yAxis;
	
	//Calculating how many data points will need to be calculated
	//	Calculates # of intervals to reach steady state and then adds one more
	//	Then converts that number to 30 minute intervals
	t12 = calculateT12(ke);
	tss = calculateTss(t12);
	end = Math.ceil(tss / tau) + 1;
	end = end * tau * 60;		
	end = end / 30;
	
	//Calculates the concentration at each data point and adds to array
	//	Calculates a data point for every 30 minutes
	for (i = 0; i < end; i++) {
		tTotal = i * 30;
		tTotal = tTotal / 60;
		
		//Number of intervals that have elapsed
		n = Math.floor(tTotal / tau);
		
		//Removes the completed intervals from t to give time since last dose
		t = tTotal - (n * tau);
		
		//Adds data point to array which will generate graph
		coordinates[i] = new Coordinates(
			tTotal, 
			calculateConcentration(dose, vd, n + 1, ke, tau, t)
		);
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
		//console.log("x: " + coordinates[i].x + ", y:" + coordinates[i].y);
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
 *	copyParameters()	Copies PK parameters to the dose calculation div		*
 ********************************************************************************/
function copyParameters() {
	var type = document.getElementsByName("Dosing-Radio");
	var vd;
	var ke;
	
	if (type[2].checked) {
		vd = document.getElementById("PK-PT-Vd").innerHTML;
		ke = document.getElementById("PK-PT-Ke").innerHTML;
		
	}
	else if (type[3].checked) {
		vd = document.getElementById("PK-C1C2-Vd").innerHTML;
		ke = document.getElementById("PK-C1C2-Ke").innerHTML;
	}
	
	//Extracts the first word form the span (i.e. the numerical value)
	vd = vd ? extractValue(vd) : "";
	ke = ke ? extractValue(ke) : "";
	
	document.getElementById("PK-Dose-Calc-Vd").value = vd;
	document.getElementById("PK-Dose-Calc-Ke").value = ke;
	
	dosePK();
}

/********************************************************************************
 *	copyLevel()			Copies estimated dose to the level verification div		*
 ********************************************************************************/
function copyLevel() {
	var type = document.getElementsByName("Dosing-Radio");
	var dose;
	var interval;
	var vd;
	var ke;
	
	if (type[1].checked) {
		dose = document.getElementById("PK-Empiric-Round-Dose").innerHTML;
		interval = document.getElementById("PK-Empiric-Round-Interval").innerHTML;
		vd = document.getElementById("PK-Empiric-Vd").innerHTML;
		ke = document.getElementById("PK-Empiric-Ke").innerHTML;
	} else if (type[2].checked || type[3].checked) {
		dose = document.getElementById("PK-Dose-Calc-Round-Dose").innerHTML;
		interval = document.getElementById("PK-Dose-Calc-Round-Interval").innerHTML;
		vd = document.getElementById("PK-Dose-Calc-Vd").value;
		ke = document.getElementById("PK-Dose-Calc-Ke").value;
	}
	
	//Extracts the first word form the span (i.e. the numerical value)
	dose = dose ? extractValue(dose) : "";
	interval = interval ? extractValue(interval) : "";
	vd = vd ? extractValue(vd) : "";
	ke = ke ? extractValue(ke) : "";
	
	//Copies info to inputs
	document.getElementById("PK-Level-Dose").value = dose;
	document.getElementById("PK-Level-Interval").value = interval;
	document.getElementById("PK-Level-Vd").value = vd;
	document.getElementById("PK-Level-Ke").value = ke;
	
	levelVerification();
}





/********************************************************************************
 *	FUNCTIONS TO GENERATE EQUATIONS USED										*
 ********************************************************************************/
/********************************************************************************
 *	convertDates()		Converts a date-time object to a plaintext date to 		*
 *						insert into TeX code									*
 ********************************************************************************/
 function convertDates(dateTime) {
	var year = dateTime.getFullYear();
	var month = dateTime.getMonth();
	var day = dateTime.getDate();
	var hour = dateTime.getHours();
	var minute = dateTime.getMinutes();
	var text;
	
	//Pad Day with leading 0 if needed
	day = ("0" + day).slice(-2);
	
	//Convert month to text
	month = month === 0 ? "Jan" : 
			month === 1 ? "Feb" : 
			month === 2 ? "Mar" : 
			month === 3 ? "Apr" : 
			month === 4 ? "May" : 
			month === 5 ? "Jun" : 
			month === 6 ? "Jul" : 
			month === 7 ? "Aug" : 
			month === 8 ? "Sep" : 
			month === 9 ? "Oct" : 
			month === 10 ? "Nov" : 
			month === 11 ? "Dec" : 
			"";
	
	//Pad hour with leading 0 if needed
	hour = ("0" + hour).slice(-2);
	
	//Pad minute with leading 0 if needed
	minute = ("0" + minute).slice(-2);
	
	text = "\\text{" + year + "-" + month + "-" + day + 
		   " " + hour + ":" + minute + "}";
	
	return text;
}

/********************************************************************************
 *	mathData()			Math used for calculating the patient data				*
 ********************************************************************************/
function mathData(
	sex, height, age, abw, ibw, dw, scr, crcl, cwSource, cwValue) {
	var mathSection = document.getElementsByName("Math-Section");
	var equation;
	var tempNum;
	
	abw = Math.round(abw * 10) / 10;
	ibw = Math.round(ibw * 10) / 10;
	dw = Math.round(dw * 10) / 10;
	cwValue = Math.round(cwValue * 10) / 10;
	crcl = Math.round(crcl);
	
	//IBW Calculation
	equation = "\\begin{align}";
	
	if (sex === 0) {
		equation += "IBW\\ (Male) & = 50\\ kg + \\left(\\frac {0.9055\\ kg}{cm}" +
					" * height\\ (cm)\\ over\\ 152.4\\ cm\\right) &\\\\[5pt]";
	} else if (sex === 1) {
		equation += "IBW\\ (Female) & = 50\\ kg + \\left(\\frac {0.9055\\ kg}{cm}" +
					"* height\\ (cm)\\ over\\ 152.4\\ cm\\right) &\\\\[5pt]";
	}
	
	if (height > 0) {
		if (sex === 0) {
			tempNum = height - 152.4;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = 50\\ kg + \\left(\\frac {0.9055\\ kg}{cm} * " + 
						tempNum + "\\ cm\\right) &\\\\[5pt]";
			
			tempNum = tempNum * 0.9055;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = 50\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
			
			equation += "& = " + ibw + "\\ kg &\\\\[10pt]";
		} else if (sex === 1) {
			tempNum = height - 152.4;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = 45.5\\ kg + \\left(\\frac {0.9055\\ kg}{cm} * " + 
						tempNum + "\\ cm\\right) &\\\\[5pt]";
			
			tempNum = tempNum * 0.9055;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = 45.5\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
			
			equation += "& = " + ibw + "\\ kg &\\\\[10pt]";
		}
	}
	
	//Dosing weight calculation (if needed)
	if (cwSource === "DW") {
		equation += "DW & = IBW + ((ABW - IBW) * 0.4) &\\\\[5pt]";
		equation += " & = " + ibw + "\\ kg + ((" + abw + "\\ kg  -" + ibw + 
					"\\ kg) * 0.4) &\\\\[5pt]";
		
		tempNum = (abw - ibw) * 0.4;
		tempNum = Math.round(tempNum * 10)/ 10;
		equation += " & = " + ibw + "\\ kg + " + tempNum + "\\ kg &\\\\[5pt]";
		
		equation += " & = " + dw + "\\ kg &\\\\";
	}
	
	equation += "\\end{align}";
	
	mathSection[0].innerHTML = equation;
	
	//CrCl Calculations
	equation = "\\begin{align}";
	
	if (sex === 0) {
		equation += "CrCl\\ (Male) & = \\frac{\\left(140 - age\\right) " + 
					"* weight}{SCr} * 1.2 &\\\\[5pt]";
	} else if (sex === 1) {
		equation += "CrCl\\ (Female) & = \\frac{\\left(140 - age\\right) " + 
					"* weight}{SCr} &\\\\[5pt]";
	}
	
	if (age > 0 & cwValue > 0 && scr > 0) {
		//&
		if (sex === 0) {
			equation += "& = \\frac{\\left(140 - " + age + "\\right) * " + 
						cwValue + "\\ kg\\ (" + cwSource + ")}{" + scr + 
						"\\ \\mu mol/L} * 1.2 &\\\\[5pt]";
			
			tempNum = (140 - age) * cwValue;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = \\frac{" + tempNum + "}{" + scr + 
						"\\ \\mu mol/L} * 1.2 &\\\\[5pt]";
			
			equation += "& = " + crcl + "\\ mL/min &\\\\";
		} else if (sex === 1) {
			equation += "& = \\frac{\\left(140 - " + age + "\\right) * " + 
						cwValue + "\\ kg\\ (" + cwSource + ")}{" + scr + 
						"\\ \\mu mol/L} &\\\\[5pt]";
						
			tempNum = (140 - age) * cwValue;
			tempNum = Math.round(tempNum * 10) / 10;
			equation += "& = \\frac{" + tempNum + "}{" + scr + 
						"\\ \\mu mol/L} &\\\\[5pt]";
						
			equation += "& = " + crcl + "\\ mL/min &\\\\";
		}
	}
	
	equation += "\\end{align}"
	
	mathSection[1].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathEmpiric()		Math used for calculating the empiric doses				*
 ********************************************************************************/
function mathEmpiric(
	abw, loadingWeight, loadingDose, loadingRounded, maintenanceWeight, 
	maintenanceDose, maintenanceRounded, target, crcl, ke, t12, tss) {
	var mathSection = document.getElementsByName("Math-Section");
	var intervalTable = document.getElementById("Math-Interval-Table");
	var intervalCells = intervalTable.getElementsByTagName("td");
	var tempNum;
	var equation;
	
	//Rounding variables
	crcl = Math.round(crcl);
	ke = Math.round(ke * 10000) / 10000;
	t12 = Math.round(t12 * 10) / 10;
	tss = Math.round(tss * 10) / 10;
	
	//Loading Dose
	equation = "\\begin{align}";
	equation += "Loading\\ Dose & = \\frac{" + loadingWeight + "\\ mg}{kg} * " + 
				"actual\\ body\\ weight &\\\\[5pt]";
				
	if (abw > 0 && loadingWeight > 0) {
		equation += " & = \\frac{" + loadingWeight + "\\ mg}{kg} * " + 
					abw + "\\ kg &\\\\[5pt]";
		equation += " & = " + loadingDose + "\\ mg &\\\\[5pt]";
		equation += loadingDose > 500 ? 
					"Rounded\\ Loading\\ Dose & = " + loadingRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\[10pt]" :
					"Rounded\\ Loading\\ Dose & = " + loadingRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//Maintenance Dose
	equation += "\\begin{align}";
	equation += "Maintenance\\ Dose & = \\frac{" + maintenanceWeight + 
				"\\ mg}{kg} * actual\\ body\\ weight &\\\\[5pt]";
					
	if (abw > 0 && maintenanceWeight > 0) {
		equation += " & = \\frac{" + maintenanceWeight + "\\ mg}{kg} * " + abw +
					"\\ kg &\\\\[5pt]";
		equation += " & = " + maintenanceDose + "\\ mg &\\\\[5pt]";
		equation += maintenanceDose > 500 ? 
					"Rounded\\ Loading\\ Dose & = " + maintenanceRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\" :
					"Rounded\\ Loading\\ Dose & = " + maintenanceRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\";
	}
	
	equation += "\\end{align}";
	
	mathSection[2].innerHTML = equation;
	
	//Interval Calculations
	//Reset table
	for (var i = 0; i < intervalCells.length; i++) {
		intervalCells[i].className = "";
	}
			
	if (crcl < 10) {
		if (target === 0) {
			intervalCells[13].className = "intervalSelected";
		} else if (target === 1) {
			intervalCells[13].className = "intervalSelected";
		}
	} else if (crcl < 20) {
		if (target === 0) {
			intervalCells[10].className = "intervalSelected";
		} else if (target === 1) {
			intervalCells[11].className = "intervalSelected";
		}
	} else if (crcl < 40) {
		if (target === 0) {
			intervalCells[7].className = "intervalSelected";
		} else if (target === 1) {
			intervalCells[8].className = "intervalSelected";
		}
	} else if (crcl < 80) {
		if (target === 0) {
			intervalCells[4].className = "intervalSelected";
		} else if (target === 1) {
			intervalCells[5].className = "intervalSelected";
		}
	} else if (crcl >= 80) {
		if (target === 0) {
			intervalCells[1].className = "intervalSelected";
		} else if (target === 1) {
			intervalCells[2].className = "intervalSelected";
		}
	}
	
	//Steady State Calculations
	//ke calculations
	equation = "\\begin{align}";
	equation += "k_e & = \\left(0.00083 * CrCl\\right) + 0.0044 &\\\\[5pt]";
	
	if (crcl > 0 && ke > 0) {
		equation += " & = \\left(0.00083 * " + crcl + 
					"\\ mL/min\\right) + 0.0044 &\\\\[5pt]";
		
		tempNum = crcl * 0.00083;
		equation += " & = " + tempNum + "+ 0.0044 &\\\\[5pt]";
		
		equation += " & = " + ke + "\\ h^{-1} &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//Half-life calculations
	equation += "\\begin{align}";
	equation += "t_{1/2} & = \\frac{ln(2)}{k_e} &\\\\[5pt]";
	
	if (ke > 0 && t12 > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//Time to steady-state calculation
	equation += "\\begin{align}";
	equation += "t_{SS} & = t_{1/2} * 4.32 &\\\\[5pt]";
	
	if (t12 > 0 && tss > 0) {
		equation += " & = " + t12 + "\\ h * 4.32 &\\\\[5pt]";
		equation += " & = " + tss + "\\ h &\\\\";
	}
	
	equation += "\\end{align}";
	
	mathSection[3].innerHTML = equation;
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

/********************************************************************************
 *	mathPeakTrough()	Math used for calculating the Peak-Trough PK data		*
 ********************************************************************************/
function mathPeakTrough(
	infusionStart, infusionDuration, peakDrawTime, peakLevel, troughDrawTime, 
	troughLevel, interval, dose, t, t1, t2, ke, t12, cmax, cmin, vd) {
	var mathSection = document.getElementsByName("Math-Section");
	var tempNum;
	var equation;
	
	//Round numbers
	t = Math.round(t * 10) / 10;
	t1 = Math.round(t1 * 10) / 10;
	t2 = Math.round(t2 * 10) / 10;
	ke = Math.round(ke * 10000) / 10000;
	t12 = Math.round(t12 * 10) / 10;
	cmax = Math.round(cmax * 10) / 10;
	cmin = Math.round(cmin * 10) / 10;
	vd = Math.round(vd * 10) / 10;
	
	//t
	equation = "\\begin{align}";
	equation += "\\Delta t & = Trough\\ Draw\\ Time - " + 
				"Peak\\ Draw\\ Time &\\\\[5pt]";
	
	if 	(peakDrawTime > 0 && troughDrawTime > 0 && t > 0) {
		equation += "& = " + convertDates(troughDrawTime) + " - " + 
					convertDates(peakDrawTime) + " &\\\\[5pt]";
		equation += "& = " + t + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//ke
	equation += "\\begin{align}";
	equation += "k_e & = \\frac{log\\left(Peak\\ Level\\ (mg/L) - " + 
				"Trough\\ Level\\ (mg/L)\\right)}{\\Delta t\\ (h)} &\\\\[5pt]";
	
	if 	(peakLevel > 0 && troughLevel > 0 && t > 0) {
		equation += "& = \\frac{log\\left(" + peakLevel + "\\ mg/L - " + 
				troughLevel + "\\ mg/L\\right)}{" + t + "\\ h} &\\\\[5pt]";
		
		tempNum = Math.log(peakLevel - troughLevel) / Math.LN10;
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + tempNum + "}{" + 
					t + "\\ h} &\\\\[5pt]"
		
		equation += "& = " + ke + "\\ h^{-1} &\\\\[10pt]"
	}
	
	equation += "\\end{align}";
	
	//t12
	equation += "\\begin{align}";
	equation += "t_{1/2} & = \\frac{ln(2)}{k_e} &\\\\[5pt]";
	
	if (ke > 0 && t12 > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[4].innerHTML = equation;
	
	//t1
	equation = "\\begin{align}";
	equation += "\\Delta t & = Peak\\ Draw\\ Time - " + 
				"End\\ of\\ Infusion &\\\\[5pt]";
	equation += "& = \\left(Peak\\ Draw\\ Time - Infusion\\ Start\\ Time" + 
				"\\right) - Infusion\\ Duration\\ (h) &\\\\[5pt]";
	
	if (peakDrawTime > 0 && infusionStart > 0 && infusionDuration > 0) {
		equation += "& = \\left(" + convertDates(peakDrawTime) + " - " + 
					convertDates(infusionStart) + "\\right) - " + 
					infusionDuration + "\\ h &\\\\[5pt]";
					
		tempNum = (peakDrawTime - infusionStart) / 3600000
		tempNum = Math.round(tempNum * 10) / 10;
		equation += "& = " + tempNum + "\\ h - " + 
					(infusionDuration / 60) + "\\ h &\\\\[5pt]";
					
		equation += "& = " + t1 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//Cmax	
	equation += "\\begin{align}";
	equation += "C_{max} & = \\frac{Peak\\ Level\\ (mg/L)}" + 
				"{e^{-k_e * \\Delta t}} &\\\\[5pt]";
	
	if (peakLevel > 0 && ke > 0 && t1 > 0) {
		equation += "& = \\frac{" + peakLevel + "\\ mg/L}" + 
				"{e^{-" + ke + "\\ h^{-1} * " + t1 + "\\ h}} &\\\\[5pt]";
		
		tempNum = Math.pow((Math.E),(-ke * t1));
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + peakLevel + "\\ mg/L}" + 
				"{" + tempNum + "} &\\\\[5pt]";
		
		equation += "& = " + cmax + "\\ mg/L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[5].innerHTML = equation;
	
	//t2
	equation = "\\begin{align}";
	equation += "\\Delta t & = Next\\ Infusion\\ Start\\ Time - " + 
				"Trough\\ Draw\\ Time &\\\\[5pt]";
	equation += "& = \\left(Infusion\\ Start\\ Time + Dosing\\ Interval\\ " + 
				"(h)\\right) - Trough\\ Draw\\ Time &\\\\[5pt]";
	
	if (infusionStart > 0 && interval > 0 && troughDrawTime > 0) {
		equation += "& = \\left(" + convertDates(infusionStart) + " + " +
					interval + "\\ h\\right)" + " - " + 
					convertDates(troughDrawTime) + " &\\\\[5pt]";
		equation += "& = " + t2 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";			
	
	//Cmin
	equation += "\\begin{align}";
	equation +=	"C_{min} & = Trough\\ Level\\ (mg/L) * " + 
				"e^{-k_e * \\Delta t} &\\\\[5pt]";
	
	if (troughLevel > 0 && ke > 0 && t2 > 0) {
		equation +=	"& = " + troughLevel + "\\ mg/L * " + 
					"e^{-" + ke + "\\ h^{-1} * " + t2 + "\\ h} &\\\\[5pt]";
					
		tempNum =  Math.pow((Math.E),(-ke * t2));
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation +=	"& = " + troughLevel + "\\ mg/L * " + 
					tempNum + " &\\\\[5pt]";
					
		equation += "& = " + cmin + "\\ mg/L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[6].innerHTML = equation;
	
	//Vd
	equation = "\\begin{align}";
	equation += "V_d & = \\frac{dose\\ (mg)}" +
				"{C_{max}\\ (mg/L) - C_{min}\\ (mg/L)} &\\\\[5pt]";
	
	if (dose > 0 && cmax > 0 && cmin > 0) {
		equation += "& = \\frac{" + dose + "\\ mg}" + 
					"{" + cmax + "\\ mg/L - " + cmin + "\\ mg/L} &\\\\[5pt]";
		
		tempNum = cmax - cmin;
		tempNum = Math.round(tempNum * 10) / 10;
		equation += "& = \\frac{" + dose + "\\ mg}" +
					"{" + tempNum + "\\ mg/L} &\\\\[5pt]";
		
		equation += "& = " + vd + "\\ L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[7].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathC1C2()			Math used for calculating the C1-C2 PK data				*
 ********************************************************************************/
function mathC1C2(infusionStart, infusionDuration, interval, c1Draw, c1Level, 
				  c2Draw, c2Level, t, t1, t2, cmax, cmin, ke, t12, dose, vd) {
	var mathSection = document.getElementsByName("Math-Section");
	var tempNum;
	var equation;
	
	//Rounding variables
	ke = Math.round(ke * 10000) / 10000;
	t12 = Math.round(t12 * 10) / 10;
	vd = Math.round(vd * 10) / 10;
	cmax = Math.round(cmax * 10) / 10;
	cmin = Math.round(cmin * 10) / 10;
	
	//t
	equation = "\\begin{align}";
	equation += "\\Delta t & = C_2\\ Draw\\ Time - " + 
				"C_1\\ Draw\\ Time &\\\\[5pt]";
	
	if (c1Draw > 0 && c2Draw > 0) {
		equation += "& = " + convertDates(c2Draw) + " - " + 
				convertDates(c1Draw) + " &\\\\[5pt]";
		equation += "& = " + t + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//k3
	equation += "\\begin{align}";
	equation += "k_e & = \\frac{log\\left(C_1\\ Level\\ (mg/L) - " +
				"C_2\\ Level\\ (mg/L)\\right)}{\\Delta t} &\\\\[5pt]";
	
	if (c1Level > 0 && c2Level > 0 && t > 0) {
		equation += "& = \\frac{log\\left(" + c1Level + "\\ mg/L - " +
				c2Level + "\\ mg/L\\right)}{" + t + "\\ h} &\\\\[5pt]";
		
		tempNum = Math.log(c1Level - c2Level) / Math.LN10;
		tempNum = Math.round(tempNum * 10) / 10;
		
		equation += "& = \\frac{" + tempNum + "}{" + t + "\\ h} &\\\\[5pt]";
		
		equation += "& = " + ke + "\\ h^{-1} &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//t12
	equation += "\\begin{align}";
	equation += "t_{1/2} & = \\frac{ln(2)}{k_e} &\\\\[5pt]";
	
	if (ke > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[8].innerHTML = equation;
	
	//Cmax
	equation = "\\begin{align}";
	equation += "\\Delta t & = C_1\\ Draw\\ Time - End\\ of\\ Infusion " + 
				"&\\\\[5pt]";
	equation += "& = C_1\\ Draw\\ Time - Infusion\\ Start\\ Time "+ 
				"- Infusion\\ Duration\\ (h) &\\\\[5pt]";
	
	if (c1Draw > 0 && infusionStart > 0 && infusionDuration > 0) {
		equation += "& = " + convertDates(c1Draw) + " - " +
					convertDates(infusionStart) + " - " + 
					(infusionDuration / 60) + "\\ h &\\\\[5pt]";
					
		tempNum = (c1Draw - infusionStart) / 3600000;
		tempNum = Math.round(tempNum * 10) / 10;
		equation += "& = " + tempNum + "\\ h - " + 
					(infusionDuration / 60) + "\\ h &\\\\[5pt]";
					
		equation += "& = " + t1 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	equation += "\\begin{align}";
	equation += "C_{max} & = \\frac{C_1\\ Level\\ (mg/L)}" +
				"{e^{-k_e * \\Delta t}} &\\\\[5pt]";
	
	if (c1Level, ke, t1) {
		equation += "& = \\frac{" + c1Level + "\\ mg/L}" +
				"{e^{-" + ke + "\\ h^{-1} * " + t1 + "\\ h}} &\\\\[5pt]";
		
		tempNum = Math.pow((Math.E),(-ke * t1));
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + c1Level + "\\ mg/L}" +
				"{" + tempNum + "} &\\\\[5pt]";
				
		equation += "& = " + cmax + "\\ mg/L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[9].innerHTML = equation;
	
	//Cmin
	equation = "\\begin{align}";
	equation += "\\Delta t & = Dosing\\ Interval\\ (h) - " + 
				"Infusion\\ Duration\\ (h) &\\\\[5pt]";
	
	if (interval > 0 && infusionDuration > 0) {
		equation += "& = " + interval + "\\ h - " + 
					(infusionDuration / 60) + "\\ h &\\\\[5pt]";
		equation += "& = " + t2 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	equation += "\\begin{align}";
	equation += "C_{min} & = C_{max} * e^{-k_e * \\Delta t} &\\\\[5pt]";
	
	if (cmax > 0 && ke > 0 && t2 > 0) {
		equation += "& = " + cmax + "\\ mg/L * " +
					"e^{-" + ke + "\\ h^{-1} * " + t2 + "\\ h} &\\\\[5pt]";
					
		tempNum = Math.pow((Math.E),(-ke * t2));
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = " + cmax + "\\ mg/L * " + tempNum + " &\\\\[5pt]";
		
		equation += "& = " + cmin + "\\ mg/L &\\\\[5pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[10].innerHTML = equation;
	
	//Vd
	equation = "\\begin{align}";
	equation += "V_d & = \\frac{dose\\ (mg)}{C_{max} - C_{min}} &\\\\[5pt]";
	
	if (dose > 0 && cmax > 0 && cmin > 0) {
		equation += "& = \\frac{" + dose + "\\ mg}" + 
					"{" + cmax + "\\ mg/L - " + cmin + "\\ mg/L} &\\\\[5pt]";
		
		tempNum = cmax - cmin;
		tempNum = Math.round(tempNum * 10) / 10;
		equation += "& = \\frac{" + dose + "\\ mg}" +
					"{" + tempNum + "\\ mg/L} &\\\\[5pt]";
		
		equation += "& = " + vd + "\\ L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[11].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathEmpiricPK()		Math used for calculating the empiric PK data			*
 ********************************************************************************/
function mathEmpiricPK(vdWeight, weight, weightSource, vd, peak, trough, dose, 
					   doseRounded, crcl, ke, t12, interval, intervalRounded) {
	var mathSection = document.getElementsByName("Math-Section");
	var tempNum;
	var equation;
	
	vdWeight = vdWeight > 0 ? vdWeight : 0;
	weightSource = typeof weightSource === "undefined" ? 
				   "\\ (kg)" : "\\ (" + weightSource + "\\ in\\ kg)";
	
	//Rounding variables
	vd = Math.round(vd * 10) / 10;
	weight = Math.round(weight * 10) / 10;
	dose = Math.round(dose * 10) / 10;
	crcl = Math.round(crcl);
	ke = Math.round(ke * 10000) / 10000;
	t12 = Math.round(ke * 10) / 10;
	interval = Math.round(interval * 10) / 10;
	
	//vd
	equation = "\\begin{align}";
	equation += "V_d & = " + vdWeight + "\\ L/kg * weight" + weightSource + 
				" &\\\\[5pt]";
	
	if (vdWeight > 0 && weight > 0) {
		equation += "& = " + vdWeight + "\\ L/kg * " + 
					weight + "\\ kg &\\\\[5pt]";
		equation += "& = " + vd + "\\ L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[12].innerHTML = equation;
	
	//Dose
	equation = "\\begin{align}";
	equation += "dose & = V_d * \\left(Desired\\ Peak - " + 
				"Desired\\ Trough\\right) &\\\\[5pt]";
	
	if (vd > 0 && peak > 0 && trough > 0) {
		equation += "& = " + vd + "\\ L * \\left(" + peak + "\\ mg/L - " + 
					trough + "\\ mg/L\\right) &\\\\[5pt]";
		
		tempNum = peak - trough;
		equation += "& = " + vd + "\\ L * \\left(" + 
					tempNum + "\\ mg/L\\right) &\\\\[5pt]";
		
		equation += "& = " + dose + "\\ mg &\\\\[10pt]";
		
		equation += "\\end{align}";
		
		equation += "\\begin{align}";
		
		equation += doseRounded > 500 ?
					"Rounded\\  Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\[10pt]" :
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[13].innerHTML = equation;
	
	//PK Parameters
	equation = "\\begin{align}";
	equation += "k_e & = \\left(0.00083 * CrCl\\right) + 0.0044 &\\\\[5pt]";
	
	if (crcl > 0) {
		equation += " & = \\left(0.00083 * " + crcl + 
					"\\ mL/min\\right) + 0.0044 &\\\\[5pt]";
		
		tempNum = crcl * 0.00083;
		equation += " & = " + tempNum + "+ 0.0044 &\\\\[5pt]";
		
		equation += " & = " + ke + "\\ h^{-1} &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	//Half-life calculations
	equation += "\\begin{align}";
	equation += "t_{1/2} & = \\frac{ln(2)}{k_e} &\\\\[5pt]";
	
	if (ke > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[14].innerHTML = equation;
	
	//Interval
	equation = "\\begin{align}";
	equation += "\\tau & = log\\left(\\frac{Desired\\ Peak\\ (mg/L)}" +
				"{Desired\\ Trough\\ (mg/L)}\\right) * " + 
				"\\frac{1}{k_e\\ (h^{-1})} &\\\\[10pt]";
	
	if (peak > 0 && trough > 0 && ke > 0) {
		equation += "& = log\\left(\\frac{" + peak + "\\ mg/L}" + 
					"{" + trough + "\\ mg/L}\\right) * " +
					"\\frac{1}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		
		tempNum = Math.log(peak - trough) / Math.LN10;
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = " + tempNum + " * " +
					"\\frac{1}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
					
		equation += "& = " + interval +"\\ h &\\\\[10pt]";
		
		equation += "\\end{align}";
		
		equation += "\\begin{align}";
		
		equation += "Rounded\\ Interval & = " + intervalRounded + 
					"\\ h &\\\\[10pt]"
	}
	
	equation += "\\end{align}";
	
	mathSection[15].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathDosePK()		Math used for calculating the PK dose					*
 ********************************************************************************/
function mathDosePK(vd, peak, trough, dose, doseRounded, ke, interval,
					intervalRounded) {
	var mathSection = document.getElementsByName("Math-Section");
	var tempNum;
	var equation;
	
	//Rounding variables
	dose = Math.round(dose * 10) / 10;
	interval = Math.round(interval * 10) / 10;
	
	//Dose
	equation = "\\begin{align}";
	equation += "dose & = V_d * " + 
				"(Desired\\ Peak\\ (mg/L) - Desired\\ Trough\\ (mg/L)) &\\\\[5pt]";
	
	if (vd > 0 && peak > 0 && trough > 0) {
		equation += "& = " + vd + "\\ L * " +
					"(" + peak + "\\ mg/L - " + trough + "\\ mg/L) &\\\\[5pt]";
					
		tempNum = peak - trough;
		tempNum = Math.round(tempNum * 10) / 10;
		equation += "& = " + vd + "\\ L * " + tempNum + "\\ mg/L &\\\\[5pt]";
		
		equation += "& = " + dose + "\\ mg &\\\\[10pt]";
		equation += "\\end{align}";
		
		equation += "\\begin{align}";
		equation += doseRounded > 500 ?
					"Rounded\\  Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 250\\ mg) &\\\\[10pt]" :
					"Rounded\\ Loading\\ Dose & = " + doseRounded + 
					"\\ mg\\ (nearest\\ 50\\ mg) &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[16].innerHTML = equation;
	
	//Interval
	equation = "\\begin{align}";
	equation += "\\tau & = \\frac{ln(Desired\\ Peak\\ Level\\ (mg/L)) - " + 
				"ln(Desired\\ Trough\\ Level\\ (mg/L))}{k_e} &\\\\[5pt]";
	
	if (peak > 0 && trough > 0 && ke > 0) {
		equation += "& = \\frac{ln(" + peak + "\\ mg/L) - " + 
					"ln(" + trough + "\\ mg/L)}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		
		tempNum = Math.log(peak) - Math.log(trough);
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + tempNum + "}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		
		equation += "& = " + interval + "\\ h &\\\\[10pt]";
		equation += "\\end{align}";
		
		equation += "\\begin{align}";
		equation += "Rounded\\ Interval & = " + intervalRounded + 
					"\\ h &\\\\[10pt]"
	}
	
	equation += "\\end{align}";
	
	mathSection[17].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


/********************************************************************************
 *	mathLevel()		Math used for calculating the PK level						*
 ********************************************************************************/
function mathLevel(dose, vd, ke, interval, cmax, cmin, t12, tss) {
	var mathSection = document.getElementsByName("Math-Section");
	var tempNum;
	var equation;
	
	//Rounding variables
	cmax = Math.round(cmax * 10) / 10;
	cmin = Math.round(cmin * 10) / 10;
	t12 = Math.round(t12 * 10) / 10;
	tss = Math.round(tss * 10) / 10;
	
	//Cmax
	equation = "\\begin{align}";
	equation += "C_{max} & = \\frac{Dose\\ (mg)}{V_d\\ (L) * " + 
				"\\left(1 - e^{-ke * \\tau}\\right)} &\\\\[5pt]";
	
	if (dose > 0 && vd > 0 && ke > 0 && interval > 0) {
		equation += "& = \\frac{" + dose + "\\ mg}" +
					"{" + vd + "\\ L * \\left(1 - " + 
					"e^{-" + ke + "\\ h^{-1} * " + interval + "\\ h}\\right)}" +
					" &\\\\[5pt]";
		
		tempNum = Math.pow(Math.E, -ke * interval);
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + dose + "\\ mg}" +
					"{" + vd + "\\ L * \\left(1 - " + 
					tempNum + "\\right)} &\\\\[5pt]";
					
		tempNum = vd * (1 - Math.pow(Math.E, -ke * interval));
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = \\frac{" + dose + "\\ mg}" +
					"{" + tempNum + "} &\\\\[5pt]";
					
		equation += "& = " + cmax + "\\ mg/L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[18].innerHTML = equation;
	
	//Cmin
	equation = "\\begin{align}";
	equation += "C_{min} & = C_{max} * e^{-ke * \\tau} &\\\\[10pt]";
	
	if (cmax > 0 && ke > 0 && interval > 0) {
		equation += "& = " + cmax + "\\ mg/L *" + 
					"e^{-" + ke + "\\ h^{-1} * " + interval + "\\ h}" +
					" &\\\\[5pt]";
		
		tempNum = Math.pow(Math.E, -ke * interval);
		tempNum = Math.round(tempNum * 10000) / 10000;
		equation += "& = " + cmax + "\\ mg/L *" + tempNum + " &\\\\[5pt]";
		
		equation += "& = " + cmin + "\\ mg/L &\\\\[10pt]";
	}
	
	equation += "\\end{align}";
	
	mathSection[19].innerHTML = equation;
	
	//Steady State Calculations
	equation = "\\begin{align}";
	equation += "t_{1/2} & = \\frac{ln(2)}{k_e} &\\\\[5pt]";
	
	if (ke > 0 && t12 > 0) {
		equation += " & = \\frac{0.693}{" + ke + "\\ h^{-1}} &\\\\[5pt]";
		equation += " & = " + t12 + "\\ h &\\\\[10pt]";
	}
	
	equation += "\\end{align}";

	equation += "\\begin{align}";
	equation += "t_{SS} & = t_{1/2} * 4.32 &\\\\[5pt]";
	
	if (t12 > 0 && tss > 0) {
		equation += " & = " + t12 + "\\ h * 4.32 &\\\\[5pt]";
		equation += " & = " + tss + "\\ h &\\\\";
	}
	
	equation += "\\end{align}";
	
	mathSection[20].innerHTML = equation;
	
	//Updates math function changes
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}




 /*******************************************************************************
 *	ADDS EVENT LISTENERS TO HTML DOM ELEMENTS									*
 ********************************************************************************/
//Adds event listeners
 document.addEventListener("DOMContentLoaded", function() {
	document.getElementsByName("Dosing-Radio-Div")[0].addEventListener("change", showDiv, false);
	document.getElementsByName("Dosing-Div")[0].addEventListener("change", data, false);
	document.getElementsByName("Dosing-Div")[1].addEventListener("change", data, false);
	document.getElementsByName("Dosing-Div")[2].addEventListener("change", parametersPeakTrough, false);
	document.getElementsByName("Dosing-Div")[3].addEventListener("change", parametersC1C2, false);
	document.getElementsByName("Dosing-Div")[4].addEventListener("change", data, false);
	document.getElementsByName("Dosing-Div")[5].addEventListener("change", dosePK, false);
	document.getElementsByName("Dosing-Div")[6].addEventListener("change", levelVerification, false);
	document.getElementById("PK-Level-Copy").addEventListener("click", copyLevel, false);
	document.getElementById("PK-Dose-Calc-Copy").addEventListener("click", copyParameters, false);
	
	/*
	var test = document.getElementById("Empiric-Age");
	var newTip = new Opentip(test, "Testing", {target: true, tipJoint: "left"});
	newTip.show();
	*/
	
	//Left aligns the MathJax output
	MathJax.Hub.Config({
		jax: ["input/TeX","output/HTML-CSS"],
		displayAlign: "left",
		messageStyle: "none",
		tex2jax: {preview: "none"}
	});
});

//AUC = dose (per day) / (((CrCl * 0.77) + 15.4) * 0.06))