function ShowResult(str)
{
	//Set a timer so that an AJAX request only fires if user is done typing
	// Using a 200 ms delay to detect typing stopping
	clearTimeout(AJAXtimer);
	AJAXtimer = setTimeout(function() {
		if (str.length == 0)
		{
			document.getElementById("ResponseNames").innerHTML="";
			return;
		}
		
		if (window.XMLHttpRequest)
		{
			// code for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
		}
		else
		{
			// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
		
		xmlhttp.onreadystatechange=function()
		{
			if (xmlhttp.readyState==4 && xmlhttp.status==200)
			{
				document.getElementById("ResponseNames").innerHTML=xmlhttp.responseText;
			}
		}
		xmlhttp.open("GET","live_search.php?q=" + str, true);
		xmlhttp.send();
	}, 200)
}

function ChooseResult(id)
{
	id = id.replace("_", " ");
	document.getElementById("SearchBar").value = "";
	ShowResult("");
	
	if (window.XMLHttpRequest)
	{
		// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			
			json = JSON.parse(xmlhttp.responseText);
			ProcessResult(json)
		}
	}
		xmlhttp.open("GET","add_item.php?q=" + id, true);
		xmlhttp.send();
}

function ProcessResult(array)
{
	//Build structure of templist
	TempList =
	[
		{
			GenericName: "",
			NextLevel:
			[
				{
					Form: "",
					NextLevel:
					[
						{
							BrandName: "",
							UnitPrice: "",
							LCA: "",
							LCAText: "",
							Coverage: "",
							CoverageCriteria: "",
							CoverageCriteriaSA: "",
							CoverageCriteriaP: "",
							SpecialAuth: "",
							SpecialAuthLink: "",
							Clients1: "",
							Clients66: "",
							Clients66A: "",
							Clients19823: "",
							Clients19823A: "",
							Clients19824: "",
							Clients20400: "",
							Clients20403: "",
							Clients20514: "",
							Clients22128: "",
							Clients23609: ""
						}
					]
				}
			]
		}
	];

	//Converting all JSON entries into the TempArray
	var first = true;
	
	//Processing the JSON list into the appropriate TempArray categories
	for (var i = 0; i < array.length; i++)
	{
		if (first == true) //Generates the first entry into the array
		{
			first = false;
			TempList[0].GenericName = array[0]['GenericName'];
			TempList[0].NextLevel[0].Form = array[0]['Strength'] + " " + array[0]['DosageForm'];
			TempList[0].NextLevel[0].NextLevel[0].BrandName = array[0]['BrandName'] + " (" + array[0]['Manufacturer'] + ")";
			TempList[0].NextLevel[0].NextLevel[0].UnitPrice = array[0]['UnitPrice'];
			TempList[0].NextLevel[0].NextLevel[0].LCA = array[0]['LCA'];
			TempList[0].NextLevel[0].NextLevel[0].LCAText = array[0]['LCAText'];
			TempList[0].NextLevel[0].NextLevel[0].Coverage = array[0]['Coverage'];
			TempList[0].NextLevel[0].NextLevel[0].CoverageCriteria = array[0]['CoverageCriteria'];
			TempList[0].NextLevel[0].NextLevel[0].CoverageCriteriaSA = array[0]['CoverageCriteriaSA'];
			TempList[0].NextLevel[0].NextLevel[0].CoverageCriteriaP = array[0]['CoverageCriteriaP'];
			TempList[0].NextLevel[0].NextLevel[0].SpecialAuth = array[0]['SpecialAuth'];
			TempList[0].NextLevel[0].NextLevel[0].SpecialAuthLink = array[0]['SpecialAuthLink'];
			TempList[0].NextLevel[0].NextLevel[0].Clients1 = array[0]['Clients1'];
			TempList[0].NextLevel[0].NextLevel[0].Clients66 = array[0]['Clients66'];
			TempList[0].NextLevel[0].NextLevel[0].Clients66A = array[0]['Clients66A'];
			TempList[0].NextLevel[0].NextLevel[0].Clients19823 = array[0]['Clients19823'];
			TempList[0].NextLevel[0].NextLevel[0].Clients19823A = array[0]['Clients19823A'];
			TempList[0].NextLevel[0].NextLevel[0].Clients19824 = array[0]['Clients19824'];
			TempList[0].NextLevel[0].NextLevel[0].Clients20400 = array[0]['Clients20400'];
			TempList[0].NextLevel[0].NextLevel[0].Clients20403 = array[0]['Clients20403'];
			TempList[0].NextLevel[0].NextLevel[0].Clients20514 = array[0]['Clients20514'];
			TempList[0].NextLevel[0].NextLevel[0].Clients22128 = array[0]['Clients22128'];
			TempList[0].NextLevel[0].NextLevel[0].Clients23609 = array[0]['Clients23609'];
		}
		else //All subsequent entries into list
		{
			//Checking for a matching generic name (should be all entries...)
			for (var ii = 0; ii < TempList.length; ii++)
			{
				if (array[i]['GenericName'] == TempList[ii].GenericName) //Has found a matching generic name
				{
					//Checking for a matching dosage form & strength
					var match = false;
					
					for (var iii = 0; iii < TempList[ii].NextLevel.length; iii++)
					{
						if ((array[i]['Strength'] + " " + array[i]['DosageForm']) == TempList[ii].NextLevel[iii].Form) //Has found a matching form
						{
							//Assign the new brand name and unit price to this form
							TempList[ii].NextLevel[iii].NextLevel.push({
								BrandName: array[i]['BrandName'] + " (" + array[i]['Manufacturer'] + ")",
								UnitPrice: array[i]['UnitPrice'],
								LCA: array[i]['LCA'],
								LCAText: array[i]['LCAText'],
								Coverage: array[i]['Coverage'],
								CoverageCriteria: array[i]['CoverageCriteria'],
								CoverageCriteriaSA: array[i]['CoverageCriteriaSA'],
								CoverageCriteriaP: array[i]['CoverageCriteriaP'],
								SpecialAuth: array[i]['SpecialAuth'],
								SpecialAuthLink: array[i]['SpecialAuthLink'],
								Clients1: array[i]['Clients1'],
								Clients66: array[i]['Clients66'],
								Clients66A: array[i]['Clients66A'],
								Clients19823: array[i]['Clients19823'],
								Clients19823A: array[i]['Clients19823A'],
								Clients19824: array[i]['Clients19824'],
								Clients20400: array[i]['Clients20400'],
								Clients20403: array[i]['Clients20403'],
								Clients20514: array[i]['Clients20514'],
								Clients22128: array[i]['Clients22128'],
								Clients23609: array[i]['Clients23609']
							})
							match = true;
							break;
						}
					}
					
					//Append a new form to the list and then add the brand name and unit price to this form
					if (match == false)
					{
						TempList[ii].NextLevel.push({
							Form: array[i]['Strength'] + " " + array[i]['DosageForm'],
							NextLevel: [{
								BrandName: array[i]['BrandName'] + " (" + array[i]['Manufacturer'] + ")",
								UnitPrice: array[i]['UnitPrice'],
								LCA: array[i]['LCA'],
								LCAText: array[i]['LCAText'],
								Coverage: array[i]['Coverage'],
								CoverageCriteria: array[i]['CoverageCriteria'],
								CoverageCriteriaSA: array[i]['CoverageCriteriaSA'],
								CoverageCriteriaP: array[i]['CoverageCriteriaP'],
								SpecialAuth: array[i]['SpecialAuth'],
								SpecialAuthLink: array[i]['SpecialAuthLink'],
								Clients1: array[i]['Clients1'],
								Clients66: array[i]['Clients66'],
								Clients66A: array[i]['Clients66A'],
								Clients19823: array[i]['Clients19823'],
								Clients19823A: array[i]['Clients19823A'],
								Clients19824: array[i]['Clients19824'],
								Clients20400: array[i]['Clients20400'],
								Clients20403: array[i]['Clients20403'],
								Clients20514: array[i]['Clients20514'],
								Clients22128: array[i]['Clients22128'],
								Clients23609: array[i]['Clients23609']
							}]
						})
					}
				}
				else //This result *should* never happen...
				{
					//Append new item to the list
					TempList[TempList.length].GenericName = array[i]['GenericName'];
					TempList[TempList.length].NextLevel[0].Form = array[i]['Strength'] + " " + array[i]['DosageForm'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].BrandName = array[i]['BrandName'] + " (" + array[i]['Manufacturer'] + ")";
					TempList[TempList.length].NextLevel[0].NextLevel[0].UnitPrice = array[i]['UnitPrice'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].LCA = array[i]['LCA'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].LCAText = array[i]['LCAText'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Coverage = array[i]['Coverage'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].CoverageCriteria = array[i]['CoverageCriteria'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].CoverageCriteriaSA = array[i]['CoverageCriteriaSA'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].CoverageCriteriaP = array[i]['CoverageCriteriaP'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].SpecialAuth = array[i]['SpecialAuth'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].SpecialAuthLink = array[i]['SpecialAuthLink'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients1 = array[i]['Clients1'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients66 = array[i]['Clients66'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients66A = array[i]['Clients66A'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients19823 = array[i]['Clients19823'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients19823A = array[i]['Clients19823A'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients19824 = array[i]['Clients19824'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients20400 = array[i]['Clients20400'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients20403 = array[i]['Clients20403'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients20514 = array[i]['Clients20514'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients22128 = array[i]['Clients22128'];
					TempList[TempList.length].NextLevel[0].NextLevel[0].Clients23609 = array[i]['Clients23609'];
				}
			}
		}
	}
	
	//Append the TempList to the main DrugItemsList
	DrugItemsList.push(TempList[0]);
	
	//Takes the global list and places an LCA entry as the first entry under each Strength & Dosage Form
	FindLCA();
	
	//Prints result into table
	PrintResult();
	
	//Print results into comparison table
	PrintComparison();
	
	//Generates coverage info table
	PrintCoverage();
	
	//Returns focus to the textbox for next entry
	document.getElementById("SearchBar").focus();
}

function FindLCA()
{
	var x = DrugItemsList.length-1 //Update the last entry to include an LCA

	for (var i = 0; i < DrugItemsList[x].NextLevel.length; i++)
	{
		//TempArray to screen for lowest LCA and save results
		var TempArray = {
			BrandName: "",
			UnitPrice: 100000,
			LCA: "",
			LCAText: "",
			Coverage: "",
			CoverageCriteria: "",
			CoverageCriteriaSA: "",
			CoverageCriteriaP: "",
			SpecialAuth: "",
			SpecialAuthLink: "",
			Clients1: "",
			Clients66: "",
			Clients66A: "",
			Clients19823: "",
			Clients19823A: "",
			Clients19824: "",
			Clients20400: "",
			Clients20403: "",
			Clients20514: "",
			Clients22128: "",
			Clients23609: ""
		}
		
		for (var ii = 0; ii < DrugItemsList[x].NextLevel[i].NextLevel.length; ii++)
		{
			//If this LCA is lower then previous, replace TempArray contents
			if (DrugItemsList[x].NextLevel[i].NextLevel[ii].UnitPrice < TempArray.UnitPrice && DrugItemsList[x].NextLevel[i].NextLevel[ii].UnitPrice > 0)
			{
				var CompList = DrugItemsList[x].NextLevel[i].NextLevel[ii];
			
				TempArray.BrandName = "LCA";
				TempArray.UnitPrice = CompList.UnitPrice;
				TempArray.LCA = CompList.LCA;
				TempArray.LCAText = CompList.LCAText;
				TempArray.Coverage = CompList.Coverage;
				TempArray.CoverageCriteria = CompList.CoverageCriteria;
				TempArray.CoverageCriteriaSA = CompList.CoverageCriteriaSA;
				TempArray.CoverageCriteriaP = CompList.CoverageCriteriaP;
				TempArray.SpecialAuth = CompList.SpecialAuth;
				TempArray.SpecialAuthLink = CompList.SpecialAuthLink;
				TempArray.Clients1 = CompList.Clients1;
				TempArray.Clients66 = CompList.Clients66;
				TempArray.Clients66A = CompList.Clients66A;
				TempArray.Clients19823 = CompList.Clients19823;
				TempArray.Clients19823A = CompList.Clients19823A;
				TempArray.Clients19824 = CompList.Clients19824;
				TempArray.Clients20400 = CompList.Clients20400;
				TempArray.Clients20403 = CompList.Clients20403;
				TempArray.Clients20514 = CompList.Clients20514;
				TempArray.Clients22128 = CompList.Clients22128;
				TempArray.Clients23609 = CompList.Clients23609;
			}
			else	//If not entry was found, assumed to be no covered medication and LCA will default to the first entry
			{
				var CompList = DrugItemsList[x].NextLevel[i].NextLevel[0];
			
				TempArray.BrandName = "LCA";
				TempArray.UnitPrice = CompList.UnitPrice;
				TempArray.LCA = CompList.LCA;
				TempArray.LCAText = CompList.LCAText;
				TempArray.Coverage = CompList.Coverage;
				TempArray.CoverageCriteria = CompList.CoverageCriteria;
				TempArray.CoverageCriteriaSA = CompList.CoverageCriteriaSA;
				TempArray.CoverageCriteriaP = CompList.CoverageCriteriaP;
				TempArray.SpecialAuth = CompList.SpecialAuth;
				TempArray.SpecialAuthLink = CompList.SpecialAuthLink;
				TempArray.Clients1 = CompList.Clients1;
				TempArray.Clients66 = CompList.Clients66;
				TempArray.Clients66A = CompList.Clients66A;
				TempArray.Clients19823 = CompList.Clients19823;
				TempArray.Clients19823A = CompList.Clients19823A;
				TempArray.Clients19824 = CompList.Clients19824;
				TempArray.Clients20400 = CompList.Clients20400;
				TempArray.Clients20403 = CompList.Clients20403;
				TempArray.Clients20514 = CompList.Clients20514;
				TempArray.Clients22128 = CompList.Clients22128;
				TempArray.Clients23609 = CompList.Clients23609;
			}
		}
		
		//TempArray should now have LCA contents
		//Place LCA as first entry
		DrugItemsList[x].NextLevel[i].NextLevel.unshift(TempArray);
	}
}

function PrintResult()
{
	var x = DrugItemsList.length-1;	//Grabs index for the last entry of the global list

	//Gets appropriate entry from global lists
	var TempList = DrugItemsList[x];
		
	//Generate text for Generic Name
		//Visible span
		var spanGenericName = document.createElement("span");
		spanGenericName.innerHTML = TempList.GenericName;
		spanGenericName.setAttribute("name", "GNText");
		
		//Hidden value
		var hiddenGenericName = document.createElement("input");
		hiddenGenericName.type = "hidden";
		hiddenGenericName.name = "GNValue";
		hiddenGenericName.value = TempList.GenericName;
	
	
	//Generate Select box for Strength + Dosage Form
		//Create select element and name it & add listener
		var selectForm = document.createElement("select");
		selectForm.name = "SD";
		selectForm.className = "strengthdosageselect";
		selectForm.addEventListener("change", function(){ProcessSDUpdate(this);});
		
		//Create and add the items to the select box
		for (var i = 0; i < TempList.NextLevel.length; i++)
		{
			var option = document.createElement("option");
			option.value = TempList.NextLevel[i].Form;
			option.innerHTML = TempList.NextLevel[i].Form;
			selectForm.appendChild(option);
		}
	
	//Generate select box for Brand Name
		//Create select element and name it & add listener
		var selectBrandName = document.createElement("select");
		selectBrandName.name = "BN";
		selectBrandName.className = "brandnameselect";
		selectBrandName.addEventListener("change", function(){ProcessBNUpdate(this);});
		
		//Create and add the items to the select box
		for (var i = 0; i < TempList.NextLevel[0].NextLevel.length; i++)
		{
			var option = document.createElement("option");
			option.value = TempList.NextLevel[0].NextLevel[i].BrandName;
			option.innerHTML = TempList.NextLevel[0].NextLevel[i].BrandName;
			selectBrandName.appendChild(option);
		}
	
	//Generate unit price
		//Visible span
		var spanUnitPrice = document.createElement("span");
		spanUnitPrice.setAttribute("name", "UPText");
		spanUnitPrice.innerHTML = "$" + TempList.NextLevel[0].NextLevel[0].UnitPrice;
		
		//Hidden value
		var hiddenUnitPrice = document.createElement("input");
		hiddenUnitPrice.type = "hidden";
		hiddenUnitPrice.name = "UPValue";
		hiddenUnitPrice.value = TempList.NextLevel[0].NextLevel[0].UnitPrice;
	
	//Generate quantity
		//Create element and add listener
		var inputQuantity = document.createElement("input")
		inputQuantity.type = "number";
		inputQuantity.name = "Q";
		inputQuantity.value = 30;
		inputQuantity.className = "quantityinput"
		inputQuantity.min = 0;
		inputQuantity.step = 1;
		inputQuantity.addEventListener("change", function(){ProcessPriceUpdate(this);});
		inputQuantity.addEventListener("keyup", function(){ProcessPriceUpdate(this);});
		
	//Generate drug price
		//Visible span
		var spanDrugPrice = document.createElement("span");
		spanDrugPrice.setAttribute("name", "DPText");
		spanDrugPrice.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenDrugPrice = document.createElement("input");
		hiddenDrugPrice.type = "hidden";
		hiddenDrugPrice.name = "DPValue";
		hiddenDrugPrice.value = 0;
		
	//Generate fees
		//Visible span
		var spanFee = document.createElement("span");
		spanFee.setAttribute("name", "FText");
		spanFee.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenFee = document.createElement("input");
		hiddenFee.type = "hidden";
		hiddenFee.name = "FValue";
		hiddenFee.value = 0;
		
	//Generate total price
		//Visible span
		var spanTotalPrice = document.createElement("span");
		spanTotalPrice.setAttribute("name", "TPText");
		spanTotalPrice.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenTotalPrice = document.createElement("input");
		hiddenTotalPrice.type = "hidden";
		hiddenTotalPrice.name = "TPValue";
		hiddenTotalPrice.value = 0;
	
	//Add the "x" for deleting a row
		//Create anchor link
		aIcon = document.createElement("a");
		aIcon.title = "Remove Drug";
		aIcon.className = "removeX";
		aIcon.addEventListener("click", function(){ProcessRemoveDrug(this);});
		
		//Create parent div
		divIcon = document.createElement("div");
		divIcon.className = "icon";
		
		//Create child div
		divCross = document.createElement("div");
		divCross.className = "cross";
		
		//Append children to parent
		divIcon.appendChild(divCross);
		aIcon.appendChild(divIcon);
		
	//Get the number of rows in table and add a new one at the end
	var table = document.getElementById("DrugListTableBody");
	var numRow = table.rows.length;
	var newRow = table.insertRow(numRow);
	
	//Create new cells in table
	var newGN = newRow.insertCell(0);
	var newDF = newRow.insertCell(1);
	var newBN = newRow.insertCell(2);
	var newUP = newRow.insertCell(3);
	var newQ = newRow.insertCell(4);
	var newDP = newRow.insertCell(5);
	var newF = newRow.insertCell(6);
	var newTP = newRow.insertCell(7);
	var newX = newRow.insertCell(8);
	
	//Assign classes for alignment
	
	newGN.className = "LA";
	newDF.className = "CA";
	newBN.className = "CA";
	newUP.className = "CA";
	newQ.className = "CA";
	newDP.className = "RA";
	newF.className = "RA";
	newTP.className = "RA";
	newX.className = "CA";
	
	//Appends elements into the new cells
	newGN.appendChild(spanGenericName);
	newGN.appendChild(hiddenGenericName);
	newDF.appendChild(selectForm);
	newBN.appendChild(selectBrandName);
	newUP.appendChild(spanUnitPrice);
	newUP.appendChild(hiddenUnitPrice);
	newQ.appendChild(inputQuantity);
	newDP.appendChild(spanDrugPrice);
	newDP.appendChild(hiddenDrugPrice);
	newF.appendChild(spanFee);
	newF.appendChild(hiddenFee);
	newTP.appendChild(spanTotalPrice);
	newTP.appendChild(hiddenTotalPrice);
	newX.appendChild(aIcon);
	
	UpdatePrice(numRow)
}

function PrintComparison()
{
	var x = DrugItemsList.length-1;		//Grabs index for the last entry of the global list
	
	//Gets appropriate entry from global lists
	var TempList = DrugItemsList[x];

	//Generate medication name
		var spanCompName = document.createElement("span");
		spanCompName.setAttribute("name", "CompName");
		spanCompName.innerHTML = TempList.GenericName + " " + TempList.NextLevel[0].Form;
	
	//Generate unit price
		//Visible span
		var spanUnitPrice = document.createElement("span");
		spanUnitPrice.setAttribute("name", "CompUPText");
		spanUnitPrice.innerHTML = "$" + TempList.NextLevel[0].NextLevel[0].UnitPrice;
		
		//Hidden value
		var hiddenUnitPrice = document.createElement("input");
		hiddenUnitPrice.type = "hidden";
		hiddenUnitPrice.name = "CompUPValue";
		hiddenUnitPrice.value = TempList.NextLevel[0].NextLevel[0].UnitPrice;
	
	//Generate doses per day input
		var inputDosesPerDay = document.createElement("input")
		inputDosesPerDay.type = "number";
		inputDosesPerDay.name = "CompDPD";
		inputDosesPerDay.value = 1;
		inputDosesPerDay.className = "quantityinput"
		inputDosesPerDay.min = 0;
		inputDosesPerDay.step = 1;
		inputDosesPerDay.addEventListener("change", function(){ProcessComparePriceUpdate(this);});
		inputDosesPerDay.addEventListener("keyup", function(){ProcessComparePriceUpdate(this);});
		
	//Generate drug price #1
		//Visible span
		var spanDrugPrice1 = document.createElement("span");
		spanDrugPrice1.setAttribute("name", "CompDP1Text");
		spanDrugPrice1.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenDrugPrice1 = document.createElement("input");
		hiddenDrugPrice1.type = "hidden";
		hiddenDrugPrice1.name = "CompDP1Value";
		hiddenDrugPrice1.value = 0;
		
	//Generate fees #1
		//Visible span
		var spanFee1 = document.createElement("span");
		spanFee1.setAttribute("name", "CompF1Text");
		spanFee1.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenFee1 = document.createElement("input");
		hiddenFee1.type = "hidden";
		hiddenFee1.name = "CompF1Value";
		hiddenFee1.value = 0;
		
	//Generate total price #1
		//Visible span
		var spanTotalPrice1 = document.createElement("span");
		spanTotalPrice1.setAttribute("name", "CompTP1Text");
		spanTotalPrice1.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenTotalPrice1 = document.createElement("input");
		hiddenTotalPrice1.type = "hidden";
		hiddenTotalPrice1.name = "CompTP1Value";
		hiddenTotalPrice1.value = 0;

	//Generate drug price #2
		//Visible span
		var spanDrugPrice2 = document.createElement("span");
		spanDrugPrice2.setAttribute("name", "CompDP2Text");
		spanDrugPrice2.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenDrugPrice2 = document.createElement("input");
		hiddenDrugPrice2.type = "hidden";
		hiddenDrugPrice2.name = "CompDP2Value";
		hiddenDrugPrice2.value = 0;
		
	//Generate fees #2
		//Visible span
		var spanFee2 = document.createElement("span");
		spanFee2.setAttribute("name", "CompF2Text");
		spanFee2.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenFee2 = document.createElement("input");
		hiddenFee2.type = "hidden";
		hiddenFee2.name = "CompF2Value";
		hiddenFee2.value = 0;
		
	//Generate total price #2
		//Visible span
		var spanTotalPrice2 = document.createElement("span");
		spanTotalPrice2.setAttribute("name", "CompTP2Text");
		spanTotalPrice2.innerHTML = "$0.00";
		
		//Hidden value
		var hiddenTotalPrice2 = document.createElement("input");
		hiddenTotalPrice2.type = "hidden";
		hiddenTotalPrice2.name = "CompTP2Value";
		hiddenTotalPrice2.value = 0;
	
	//Get the number of rows in table and add a new one at the end
	var table = document.getElementById("CompareTableBody");
	var numRow = table.rows.length;
	var newRow = table.insertRow(numRow);
	
	//Create new cells in table
	var newCompName = newRow.insertCell(0);
	var newUP = newRow.insertCell(1);
	var newDPD = newRow.insertCell(2);
	var newDP1 = newRow.insertCell(3);
	var newF1 = newRow.insertCell(4);
	var newTP1 = newRow.insertCell(5);
	var newDP2 = newRow.insertCell(6);
	var newF2 = newRow.insertCell(7);
	var newTP2 = newRow.insertCell(8);
	
	//Assign classes for alignment
	newCompName.className = "LA";
	newUP.className = "CA";
	newDPD.className = "CA";
	newDP1.className = "RA";
	newF1.className = "RA";
	newTP1.className = "RA";
	newDP2.className = "RA";
	newF2.className = "RA";
	newTP2.className = "RA";
	
	//Appends elements into the new cells
	newCompName.appendChild(spanCompName)
	newUP.appendChild(spanUnitPrice);
	newUP.appendChild(hiddenUnitPrice);
	newDPD.appendChild(inputDosesPerDay);
	newDP1.appendChild(spanDrugPrice1);
	newDP1.appendChild(hiddenDrugPrice1);
	newF1.appendChild(spanFee1);
	newF1.appendChild(hiddenFee1);
	newTP1.appendChild(spanTotalPrice1);
	newTP1.appendChild(hiddenTotalPrice1);
	newDP2.appendChild(spanDrugPrice2);
	newDP2.appendChild(hiddenDrugPrice2);
	newF2.appendChild(spanFee2);
	newF2.appendChild(hiddenFee2);
	newTP2.appendChild(spanTotalPrice2);
	newTP2.appendChild(hiddenTotalPrice2);
	
	//Calculates prices for defaults
	ComparePriceUpdate(numRow)
}

function PrintCoverage()
{
	var x = DrugItemsList.length-1;		//Grabs index for the last entry of the global list
	
	//Gets appropriate entry from global lists
	var TempList = DrugItemsList[x];

	//Generate medication name
	var spanMed = document.createElement("span");
	spanMed.setAttribute("name", "BenefitName");
	spanMed.innerHTML = TempList.GenericName + " " + TempList.NextLevel[0].Form;
	
	//Generate Coverage Status & link info
	var CoverageText = GenerateCoverageText(x,0,0);
	var spanCoverage = document.createElement("span");
	spanCoverage.setAttribute("name", "BenefitCoverage");
	spanCoverage.innerHTML = CoverageText;
	
	var spanClients1 = document.createElement("span");
	spanClients1.setAttribute("name", "BenefitClients1");
	var spanClients66 = document.createElement("span");
	spanClients66.setAttribute("name", "BenefitClients66");
	var spanClients66A = document.createElement("span");
	spanClients66A.setAttribute("name", "BenefitClients66A");
	var spanClients19823 = document.createElement("span");
	spanClients19823.setAttribute("name", "BenefitClients19823");
	var spanClients19823A = document.createElement("span");
	spanClients19823A.setAttribute("name", "BenefitClients19823A");
	var spanClients19824 = document.createElement("span");
	spanClients19824.setAttribute("name", "BenefitClients19824");
	var spanClients20400 = document.createElement("span");
	spanClients20400.setAttribute("name", "BenefitClients20400");
	var spanClients20403 = document.createElement("span");
	spanClients20403.setAttribute("name", "BenefitClients20403");
	var spanClients20514 = document.createElement("span");
	spanClients20514.setAttribute("name", "BenefitClients20514");
	var spanClients22128 = document.createElement("span");
	spanClients22128.setAttribute("name", "BenefitClients22128");
	var spanClients23609 = document.createElement("span");
	spanClients23609.setAttribute("name", "BenefitClients23609");
	
	spanClients1.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients1 == true ? "&#10003;" : "");
	spanClients66.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients66 == true ? "&#10003;" : "");
	spanClients66A.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients66A == true ? "&#10003;" : "");
	spanClients19823.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients19823 == true ? "&#10003;" : "");
	spanClients19823A.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients19823A == true ? "&#10003;" : "");
	spanClients19824.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients19824 == true ? "&#10003;" : "");
	spanClients20400.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients20400 == true ? "&#10003;" : "");
	spanClients20403.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients20403 == true ? "&#10003;" : "");
	spanClients20514.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients20514 == true ? "&#10003;" : "");
	spanClients22128.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients22128 == true ? "&#10003;" : "");
	spanClients23609.innerHTML = (TempList.NextLevel[0].NextLevel[0].Clients23609 == true ? "&#10003;" : "");
	
	//Get the number of rows in table and add a new one at the end
	var table = document.getElementById("BenefitTableBody");
	var numRow = table.rows.length;
	var newRow = table.insertRow(numRow);
	
	//Create new cells in table
	var newMed = newRow.insertCell(0);
	var newCoverage = newRow.insertCell(1);
	var new1 = newRow.insertCell(2);
	var new66 = newRow.insertCell(3);
	var new66A = newRow.insertCell(4);
	var new19823 = newRow.insertCell(5);
	var new19823A = newRow.insertCell(6);
	var new19824 = newRow.insertCell(7);
	var new20400 = newRow.insertCell(8);
	var new20403 = newRow.insertCell(9);
	var new20514 = newRow.insertCell(10);
	var new22128 = newRow.insertCell(11);
	var new23609 = newRow.insertCell(12);
	
	//Appends elements into the new cells
	newMed.appendChild(spanMed);
	newCoverage.appendChild(spanCoverage);
	new1.appendChild(spanClients1);
	new66.appendChild(spanClients66);
	new66A.appendChild(spanClients66A);
	new19823.appendChild(spanClients19823);
	new19823A.appendChild(spanClients19823A);
	new19824.appendChild(spanClients19824);
	new20400.appendChild(spanClients20400);
	new20403.appendChild(spanClients20403);
	new20514.appendChild(spanClients20514);
	new22128.appendChild(spanClients22128);
	new23609.appendChild(spanClients23609);
}

function GenerateCoverageText(x, y, z)
{
	TempList = DrugItemsList[x].NextLevel[y].NextLevel[z];
	var CoverageText = "";
	
	CoverageText += "<b>" + TempList.Coverage + "</b>";

	//Determines if there is any coverage criteria and adds appropriate link
	if (TempList.CoverageCriteria == true)	
	{
		if (TempList.CoverageCriteriaSA != "N/A")
		{
			CoverageText += '<br><a href="' + TempList.CoverageCriteriaSA + '" target="_blank">Click Here For Special Authorization Criteria</a>';
		}
		
		if (TempList.CoverageCriteriaP != "N/A")
		{
			CoverageText += '<br><a href="' + TempList.CoverageCriteriaP + '" target="_blank">Click Here For Paliative Coverage Criteria</a>';
		}
	}
	
	//Determines if there are links to any special authorization forms
	if (TempList.SpecialAuth != "N/A")
	{
		CoverageText += '<br>Special Authorization Forms:'
		if (TempList.SpecialAuth.search(",") != -1) //Comma = multiple entries
		{
			TempSpecialAuth = TempList.SpecialAuth.split(",")
			TempSpecialAuthLink = TempList.SpecialAuthLink.split(",")
			
			for (var i = 0; i < TempSpecialAuth.length; i++)
			{
				CoverageText += '<br><a href="' + TempSpecialAuthLink[i] + '" title="' + TempSpecialAuth[i] + '" target="_blank">Link ' + (i+1) + '</a>'
			}
		}
		else //No comma = 1 entry
		{
			CoverageText += '<br><a href="' + TempList.SpecialAuthLink + '" title="' + TempList.SpecialAuth + '" target="_blank">Link 1</a>'
		}
	}
	
	return CoverageText;
}

function ReturnIndex(e)
{
	//Finds parent <tr> element
	//Then finds which rowIndex it is
	//Then subtracts 1 to account for the header row
	
	return e.parentNode.parentNode.rowIndex-1;
}

function ProcessPriceUpdate(e)
{
	//Find the proper row index for this grouping
	var rowIndex = ReturnIndex(e);
	
	UpdatePrice(rowIndex);
}

function UpdatePrice(rowIndex)
{
	var UnitPriceValue = document.getElementsByName("UPValue")[rowIndex].value;
	var Quantity = document.getElementsByName("Q")[rowIndex].value;
	
	//Calculates the fees
	var Upcharge1 = 0.03;
	var Upcharge2 = 0
		//Determine fees for Upcharge #2
			//Will be 5.5% until 2015-04-01 (1427868000000 in Unix Timestamp)
			//Then increases to 6% until 2016-04-01 (1459490400000 in Unix Timestamp)
			//Then increases to 6.5% until 2017-04-01 (1491026400000 in Unix Timestamp)
			//Then increases to 7% thereafter
			if (Date.now() < 1427868000000)
			{
				Upcharge2 = 0.055;
			}
			else if (Date.now() < 1459490400000)
			{
				Upcharge2 = 0.06;
			}
			else if (Date.now() < 1491026400000)
			{
				Upcharge2 = 0.065;
			}
			else
			{
				Upcharge2 = 0.07;
			}

	var DrugPrice = UnitPriceValue * Quantity;
	var Fees = CalculateFee(DrugPrice);
	var TotalPrice = DrugPrice + Fees;
	
	//Updates the table entry for the selected rowIndex
	document.getElementsByName("DPValue")[rowIndex].value = DrugPrice;
	document.getElementsByName("DPText")[rowIndex].innerHTML = "$" + DrugPrice.toFixed(2);
	document.getElementsByName("FValue")[rowIndex].value = Fees;
	document.getElementsByName("FText")[rowIndex].innerHTML = "$" + Fees.toFixed(2);
	document.getElementsByName("TPValue")[rowIndex].value = TotalPrice;
	document.getElementsByName("TPText")[rowIndex].innerHTML = "$" + TotalPrice.toFixed(2);
	
	//Calculates the total price
	CalculateTotal();
}

function ProcessComparePriceUpdate(e)
{
	//Find the proper row index for this grouping
	var rowIndex = ReturnIndex(e);
	
	ComparePriceUpdate(rowIndex-1);
}

function ComparePriceUpdate(rowIndex)
{
	var UnitPriceValue = document.getElementsByName("CompUPValue")[rowIndex].value;
	var DosesPerDay = document.getElementsByName("CompDPD")[rowIndex].value;
	var DaySupply1 = document.getElementById("CompDaySupply1").value;
	var DaySupply2 = document.getElementById("CompDaySupply2").value;

	var DrugPrice1 = UnitPriceValue * DosesPerDay * DaySupply1;
	var Fees1 = CalculateFee(DrugPrice1);
	var TotalPrice1 = DrugPrice1 + Fees1;
	
	var DrugPrice2 = UnitPriceValue * DosesPerDay * DaySupply2;
	var Fees2 = CalculateFee(DrugPrice2);
	var TotalPrice2 = DrugPrice2 + Fees2;
	
	//Updates the table entry for the selected rowIndex
	document.getElementsByName("CompDP1Value")[rowIndex].value = DrugPrice1;
	document.getElementsByName("CompDP1Text")[rowIndex].innerHTML = "$" + DrugPrice1.toFixed(2);
	document.getElementsByName("CompF1Value")[rowIndex].value = Fees1;
	document.getElementsByName("CompF1Text")[rowIndex].innerHTML = "$" + Fees1.toFixed(2);
	document.getElementsByName("CompTP1Value")[rowIndex].value = TotalPrice1;
	document.getElementsByName("CompTP1Text")[rowIndex].innerHTML = "$" + TotalPrice1.toFixed(2);
	
	document.getElementsByName("CompDP2Value")[rowIndex].value = DrugPrice2;
	document.getElementsByName("CompDP2Text")[rowIndex].innerHTML = "$" + DrugPrice2.toFixed(2);
	document.getElementsByName("CompF2Value")[rowIndex].value = Fees2;
	document.getElementsByName("CompF2Text")[rowIndex].innerHTML = "$" + Fees2.toFixed(2);
	document.getElementsByName("CompTP2Value")[rowIndex].value = TotalPrice2;
	document.getElementsByName("CompTP2Text")[rowIndex].innerHTML = "$" + TotalPrice2.toFixed(2);
	
	//Calculates the total price
	CalculateComparisonTotal();
}

function ComparePriceUpdateAll()
{
	var DaySupply1 = document.getElementById("CompDaySupply1").value;
	var DaySupply2 = document.getElementById("CompDaySupply2").value;
	var rows = document.getElementById("CompareTableBody").getElementsByTagName("tr").length;

//Cycles through each table row and updates the prices
	for (var i = 0; i < rows; i++)
	{
		var UnitPriceValue = document.getElementsByName("CompUPValue")[i].value;
		var DosesPerDay = document.getElementsByName("CompDPD")[i].value;

		var DrugPrice1 = UnitPriceValue * DosesPerDay * DaySupply1;
		var Fees1 = CalculateFee(DrugPrice1);
		var TotalPrice1 = DrugPrice1 + Fees1;

		var DrugPrice2 = UnitPriceValue * DosesPerDay * DaySupply2;
		var Fees2 = CalculateFee(DrugPrice2);
		var TotalPrice2 = DrugPrice2 + Fees2;

		//Updates the table entry for the selected rowIndex
		document.getElementsByName("CompDP1Value")[i].value = DrugPrice1;
		document.getElementsByName("CompDP1Text")[i].innerHTML = "$" + DrugPrice1.toFixed(2);
		document.getElementsByName("CompF1Value")[i].value = Fees1;
		document.getElementsByName("CompF1Text")[i].innerHTML = "$" + Fees1.toFixed(2);
		document.getElementsByName("CompTP1Value")[i].value = TotalPrice1;
		document.getElementsByName("CompTP1Text")[i].innerHTML = "$" + TotalPrice1.toFixed(2);

		document.getElementsByName("CompDP2Value")[i].value = DrugPrice2;
		document.getElementsByName("CompDP2Text")[i].innerHTML = "$" + DrugPrice2.toFixed(2);
		document.getElementsByName("CompF2Value")[i].value = Fees2;
		document.getElementsByName("CompF2Text")[i].innerHTML = "$" + Fees2.toFixed(2);
		document.getElementsByName("CompTP2Value")[i].value = TotalPrice2;
		document.getElementsByName("CompTP2Text")[i].innerHTML = "$" + TotalPrice2.toFixed(2);
	}
	
	//Updates table header with new day supply
	document.getElementById("DaySupplyHeader1").innerHTML = DaySupply1 == 1 ? DaySupply1 + " day" : DaySupply1 + " days";
	document.getElementById("DaySupplyHeader2").innerHTML = DaySupply2 == 1 ? DaySupply2 + " day" : DaySupply2 + " days";
	
	//Calculates the total price
	CalculateComparisonTotal();
}

function CalculateFee(DrugPrice)
{
	//Calculates the fees
	var Upcharge1 = 0.03;
	var Upcharge2 = 0;
	
	//Determine fees for Upcharge #2
		//Will be 5.5% until 2015-04-01 (1427868000000 in Unix Timestamp)
		//Then increases to 6% until 2016-04-01 (1459490400000 in Unix Timestamp)
		//Then increases to 6.5% until 2017-04-01 (1491026400000 in Unix Timestamp)
		//Then increases to 7% thereafter
		if (Date.now() < 1427868000000)
		{
			Upcharge2 = 0.055;
		}
		else if (Date.now() < 1459490400000)
		{
			Upcharge2 = 0.06;
		}
		else if (Date.now() < 1491026400000)
		{
			Upcharge2 = 0.065;
		}
		else
		{
			Upcharge2 = 0.07;
		}
		
	var Fee1 = (DrugPrice * Upcharge1); //Upcharge #1 fee is 0.03% * drug cost
	var FeeTemp = (DrugPrice + Fee1) * Upcharge2; //Upcharge #2 fee (see above) * (drug cost + upcharge #1 fee)
	var Fee2 = FeeTemp > 100 ? 100 : FeeTemp; //Upcharge #2 is limited to a maximum of $100.00
	var Fees = Fee1 + Fee2 + 12.3; //Finally, dispensing fee of $12.30 is added
	
	return Fees
}

function ProcessSDUpdate(e)
{
	//Find the proper row index for this grouping
	var rowIndex = ReturnIndex(e);

	//Gets the selected index and passes it on
	var selIndex = document.getElementsByName("SD")[rowIndex].selectedIndex;
	
	UpdateSD(rowIndex, selIndex);
	UpdateSDComparison(rowIndex, selIndex);
	UpdateSDBenefits(rowIndex, selIndex);
}

function UpdateSD(rowIndex, selIndex)
{
	//Copy the appropriate brand name list from the global list
	var templist = DrugItemsList[rowIndex].NextLevel[selIndex].NextLevel;
	
	//remove all the options from the brand name select
	var bnselect = document.getElementsByName("BN")[rowIndex];
	bnselect.options.length = 0;
	
	//Cycle through the templist and add each item to the select object
	for (i = 0; i < templist.length; i++)
	{
		var opt = document.createElement('option');
		opt.value = templist[i].BrandName;
		opt.innerHTML = templist[i].BrandName;
		bnselect.appendChild(opt);;
	}
	
	//Update the UnitPrice
	var UnitPrice = templist[0].UnitPrice;
	document.getElementsByName("UPText")[rowIndex].innerHTML = "$" + UnitPrice;
	document.getElementsByName("UPValue")[rowIndex].value = UnitPrice;
	UpdatePrice(rowIndex);
}

function UpdateSDComparison(rowIndex, selIndex)
{
	//Copy the appropriate brand name list from the global list
	var templist = DrugItemsList[rowIndex].NextLevel[selIndex].NextLevel;
	
	//Get the updated unit price
	var UnitPrice = templist[0].UnitPrice
	
	//Update the unit price in the table
	document.getElementsByName("CompUPText")[rowIndex].innerHTML = "$" + UnitPrice;
	document.getElementsByName("CompUPValue")[rowIndex].value = UnitPrice;
	
	//Update the prices in the table
	ComparePriceUpdate(rowIndex);
}

function UpdateSDBenefits(rowIndex, selIndex)
{
	//Copy the appropriate brand name list from the global list
	var templist = DrugItemsList[rowIndex].NextLevel[selIndex].NextLevel[0];
	
	//Get the updated entries
	var Med = DrugItemsList[rowIndex].GenericName + " " + DrugItemsList[rowIndex].NextLevel[selIndex].Form;
	var Coverage = GenerateCoverageText(rowIndex, selIndex, 0);
	var Clients1 = (templist.Clients1 == true ? "&#10003;" : "");
	var Clients66 = (templist.Clients66 == true ? "&#10003;" : "");
	var Clients66A = (templist.Clients66A == true ? "&#10003;" : "");
	var Clients19823 = (templist.Clients19823 == true ? "&#10003;" : "");
	var Clients19823A = (templist.Clients19823A == true ? "&#10003;" : "");
	var Clients19824 = (templist.Clients19824 == true ? "&#10003;" : "");
	var Clients20400 = (templist.Clients20400 == true ? "&#10003;" : "");
	var Clients20403 = (templist.Clients20403 == true ? "&#10003;" : "");
	var Clients20514 = (templist.Clients20514 == true ? "&#10003;" : "");
	var Clients22128 = (templist.Clients22128 == true ? "&#10003;" : "");
	var Clients23609 = (templist.Clients23609 == true ? "&#10003;" : "");
	
	//Update the table
	document.getElementsByName("BenefitName")[rowIndex].innerHTML = Med;
	document.getElementsByName("BenefitCoverage")[rowIndex].innerHTML = Coverage;
	document.getElementsByName("BenefitClients1")[rowIndex].innerHTML = Clients1;
	document.getElementsByName("BenefitClients66")[rowIndex].innerHTML = Clients66;
	document.getElementsByName("BenefitClients66A")[rowIndex].innerHTML = Clients66A;
	document.getElementsByName("BenefitClients19823")[rowIndex].innerHTML = Clients19823;
	document.getElementsByName("BenefitClients19823A")[rowIndex].innerHTML = Clients19823A;
	document.getElementsByName("BenefitClients19824")[rowIndex].innerHTML = Clients19824;
	document.getElementsByName("BenefitClients20400")[rowIndex].innerHTML = Clients20400;
	document.getElementsByName("BenefitClients20403")[rowIndex].innerHTML = Clients20403;
	document.getElementsByName("BenefitClients20514")[rowIndex].innerHTML = Clients20514;
	document.getElementsByName("BenefitClients22128")[rowIndex].innerHTML = Clients22128;
	document.getElementsByName("BenefitClients23609")[rowIndex].innerHTML = Clients23609;
}

function ProcessBNUpdate(e)
{
	//Find the proper row index for this grouping
	var rowIndex = ReturnIndex(e);
	
	//Gets the selected index and passes it on
	var selIndex = document.getElementsByName("BN")[rowIndex].selectedIndex;
	
	UpdateBN(rowIndex, selIndex);
	UpdateBNComparison(rowIndex, selIndex);
	UpdateBNBenefits(rowIndex, selIndex);
}

function UpdateBN(rowIndex, selBNIndex)
{
	//Find the index from Strength and Dosage Form
	var selSDIndex = document.getElementsByName("SD")[rowIndex].selectedIndex
		
	//Copy the UnitPrice from the appropriate item
	var UnitPrice = DrugItemsList[rowIndex].NextLevel[selSDIndex].NextLevel[selBNIndex].UnitPrice;
	
	//Update the UnitPrice
	document.getElementsByName("UPText")[rowIndex].innerHTML = "$" + UnitPrice;
	document.getElementsByName("UPValue")[rowIndex].value = UnitPrice;
	UpdatePrice(rowIndex);
}

function UpdateBNComparison(rowIndex, selBNIndex)
{
	//Find the index from Strength and Dosage Form
	var selSDIndex = document.getElementsByName("SD")[rowIndex].selectedIndex
		
	//Copy the UnitPrice from the appropriate item
	var UnitPrice = DrugItemsList[rowIndex].NextLevel[selSDIndex].NextLevel[selBNIndex].UnitPrice;
	
	//Update the unit price in the table
	document.getElementsByName("CompUPText")[rowIndex].innerHTML = "$" + UnitPrice;
	document.getElementsByName("CompUPValue")[rowIndex].value = UnitPrice;
	
	//Update the prices in the table
	ComparePriceUpdate(rowIndex);
}

function UpdateBNBenefits(rowIndex, selBNIndex)
{
	//Find the index from Strength and Dosage Form
	var selSDIndex = document.getElementsByName("SD")[rowIndex].selectedIndex
	
	//Copy the appropriate brand name list from the global list
	var templist = DrugItemsList[rowIndex].NextLevel[selSDIndex].NextLevel[selBNIndex];
	
	//Get the updated entries
	var Coverage = GenerateCoverageText(rowIndex, selSDIndex, selBNIndex);
	var Clients1 = (templist.Clients1 == true ? "&#10003;" : "");
	var Clients66 = (templist.Clients66 == true ? "&#10003;" : "");
	var Clients66A = (templist.Clients66A == true ? "&#10003;" : "");
	var Clients19823 = (templist.Clients19823 == true ? "&#10003;" : "");
	var Clients19823A = (templist.Clients19823A == true ? "&#10003;" : "");
	var Clients19824 = (templist.Clients19824 == true ? "&#10003;" : "");
	var Clients20400 = (templist.Clients20400 == true ? "&#10003;" : "");
	var Clients20403 = (templist.Clients20403 == true ? "&#10003;" : "");
	var Clients20514 = (templist.Clients20514 == true ? "&#10003;" : "");
	var Clients22128 = (templist.Clients22128 == true ? "&#10003;" : "");
	var Clients23609 = (templist.Clients23609 == true ? "&#10003;" : "");
	
	//Update the table
	document.getElementsByName("BenefitCoverage")[rowIndex].innerHTML = Coverage;
	document.getElementsByName("BenefitClients1")[rowIndex].innerHTML = Clients1;
	document.getElementsByName("BenefitClients66")[rowIndex].innerHTML = Clients66;
	document.getElementsByName("BenefitClients66A")[rowIndex].innerHTML = Clients66A;
	document.getElementsByName("BenefitClients19823")[rowIndex].innerHTML = Clients19823;
	document.getElementsByName("BenefitClients19823A")[rowIndex].innerHTML = Clients19823A;
	document.getElementsByName("BenefitClients19824")[rowIndex].innerHTML = Clients19824;
	document.getElementsByName("BenefitClients20400")[rowIndex].innerHTML = Clients20400;
	document.getElementsByName("BenefitClients20403")[rowIndex].innerHTML = Clients20403;
	document.getElementsByName("BenefitClients20514")[rowIndex].innerHTML = Clients20514;
	document.getElementsByName("BenefitClients22128")[rowIndex].innerHTML = Clients22128;
	document.getElementsByName("BenefitClients23609")[rowIndex].innerHTML = Clients23609;
}

function CalculateTotal()
{
	//Get all value elements
	var DPs = document.getElementsByName("DPValue");
	var Fs = document.getElementsByName("FValue");
	var TPs = document.getElementsByName("TPValue");
	
	//Determine total drug prices
	var TotalDP = 0;
	
	for (var i = 0; i < DPs.length; i++)
	{
		TotalDP = (parseFloat(TotalDP) + parseFloat(DPs[i].value)).toFixed(2);
	}
	
	//Determine total fees
	var TotalF = 0;
	
	for (var i = 0; i < Fs.length; i++)
	{
		TotalF = (parseFloat(TotalF) + parseFloat(Fs[i].value)).toFixed(2);
	}
	
	//Determine total drug prices
	var TotalTP = 0;
	
	for (var i = 0; i < TPs.length; i++)
	{
		TotalTP = (parseFloat(TotalTP) + parseFloat(TPs[i].value)).toFixed(2);
	}
	
	//Update spans and inputs
	document.getElementById("TotalDPText").innerHTML = "$" + TotalDP;
	document.getElementById("TotalDPValue").value = TotalDP;
	document.getElementById("TotalFText").innerHTML = "$" + TotalF;
	document.getElementById("TotalFValue").value = TotalF;
	document.getElementById("TotalTPText").innerHTML = "$" + TotalTP;
	document.getElementById("TotalTPValue").value = TotalTP;
}

function CalculateComparisonTotal()
{
	//Get all value elements
	var DP1 = document.getElementsByName("CompDP1Value");
	var F1 = document.getElementsByName("CompF1Value");
	var TP1 = document.getElementsByName("CompTP1Value");
	var DP2 = document.getElementsByName("CompDP2Value");
	var F2 = document.getElementsByName("CompF2Value");
	var TP2 = document.getElementsByName("CompTP2Value");
	
	//Determine total drug prices
	var TotalDP1 = 0;
	var TotalDP2 = 0;
	
	for (var i = 0; i < DP1.length; i++)
	{
		TotalDP1 = (parseFloat(TotalDP1) + parseFloat(DP1[i].value)).toFixed(2);
		TotalDP2 = (parseFloat(TotalDP2) + parseFloat(DP2[i].value)).toFixed(2);
	}
	
	//Determine total fees
	var TotalF1 = 0;
	var TotalF2 = 0;
	
	for (var i = 0; i < F1.length; i++)
	{
		TotalF1 = (parseFloat(TotalF1) + parseFloat(F1[i].value)).toFixed(2);
		TotalF2 = (parseFloat(TotalF2) + parseFloat(F2[i].value)).toFixed(2);
	}
	
	//Determine total drug prices
	var TotalTP1 = 0;
	var TotalTP2 = 0;
	
	for (var i = 0; i < TP1.length; i++)
	{
		TotalTP1 = (parseFloat(TotalTP1) + parseFloat(TP1[i].value)).toFixed(2);
		TotalTP2 = (parseFloat(TotalTP2) + parseFloat(TP2[i].value)).toFixed(2);
	}
	
	//Update spans and inputs
	document.getElementById("TotalDP1Text").innerHTML = "$" + TotalDP1;
	document.getElementById("TotalDP1Value").value = TotalDP1;
	document.getElementById("TotalF1Text").innerHTML = "$" + TotalF1;
	document.getElementById("TotalF1Value").value = TotalF1;
	document.getElementById("TotalTP1Text").innerHTML = "$" + TotalTP1;
	document.getElementById("TotalTP1Value").value = TotalTP1;
	
	document.getElementById("TotalDP2Text").innerHTML = "$" + TotalDP2;
	document.getElementById("TotalDP2Value").value = TotalDP2;
	document.getElementById("TotalF2Text").innerHTML = "$" + TotalF2;
	document.getElementById("TotalF2Value").value = TotalF2;
	document.getElementById("TotalTP2Text").innerHTML = "$" + TotalTP2;
	document.getElementById("TotalTP2Value").value = TotalTP2;
}

function ProcessRemoveDrug(e)
{
	//Find the proper row index for this grouping
	var rowIndex = ReturnIndex(e);
	RemoveDrug(rowIndex);
}

function RemoveDrug(rowIndex)
{
	//Get the global list and remove the selected item
	var tempDrugList = DrugItemsList;
	tempDrugList.splice(rowIndex, 1)
	
	//Get the DrugListTable and delete the selected row
	//Adds +1 to rowIndex to account for header
	var table = document.getElementById("DrugListTable");
	table.deleteRow(rowIndex + 1);
	
	//Get the CompareTable and delete the selected row
	//Adds +2 to rowIndex to account for header
	var table = document.getElementById("CompareTable");
	table.deleteRow(rowIndex + 2);
	
	//Get the BenefitTable and delete the selected row
	//Adds +2 to rowIndex to account for header
	var table = document.getElementById("BenefitTable");
	table.deleteRow(rowIndex + 2);
}

function expandDiv(e)
{
	if (e.id == "CompareDivCheck")
	{
		if (e.checked)
		{
			document.getElementById("CompareImg").className = "imgFlip";
		}
		else
		{
			document.getElementById("CompareImg").className = "imgReg";
		}
	}
	else if (e.id == "BenefitDivCheck")
	{
		if (e.checked)
		{
			document.getElementById("BenefitImg").className = "imgFlip";
		}
		else
		{
			document.getElementById("BenefitImg").className = "imgReg";
		}
	}
	else if (e.id == "AboutDivCheck")
	{
		if (e.checked)
		{
			document.getElementById("AboutImg").className = "imgFlip";
		}
		else
		{
			document.getElementById("AboutImg").className = "imgReg";
		}
	}
}

function Print()
{
	//Determines which type of table to build
	//Collects variables for table and places them in array
	//Places them in order they will be assigned to table
	//Goes through the additional options and inserts them as needed
	var tableArray = [];
	var tableClassArray = [];
	var tableColArray = [];
	var tableFooterArray = [];
	var footerColSpan = 0;
	var colNum = 0;
	var options = document.getElementsByName("AdditionalPrint")
	var priceSelect = document.getElementById("PrintSelectPrice");
	
	if (priceSelect.selectedIndex == 0)
	{
		var tableHeaderArray = [];
		
		//Generic Name + Strength and Dosage Form
			var tempArray = [];
			var GN = document.getElementsByName("GNValue");
			var SD = document.getElementsByName("SD");
			
			for (var i = 0; i < GN.length; i++)
			{
				tempArray.push(GN[i].value + " " + SD[i].value);
			}
			
			tableArray.push(tempArray);
			tableHeaderArray.push("Medication");
			tableClassArray.push("LA");
			tableColArray.push("colMed");
			
			colNum++;
			footerColSpan++;
		
		//Brand name
			if (options[0].checked){
				var tempArray = [];
				var BN = document.getElementsByName("BN");
				
				for (var i = 0; i < BN.length; i++)
				{
					tempArray.push(BN[i].value);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray.push("Brand Name");
				tableClassArray.push("LA");
				tableColArray.push("colBN");
				
				colNum++;
				footerColSpan++;
			};
		
		//Unit price
			if (options[1].checked){
				var tempArray = [];
				var UP = document.getElementsByName("UPText");
				
				for (var i = 0; i < UP.length; i++)
				{
					tempArray.push(UP[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray.push("Unit Price");
				tableClassArray.push("CA");
				tableColArray.push("colUP");
				
				colNum++;
				footerColSpan++;
			};
			
		//Quantity
			var tempArray = [];
			var Q = document.getElementsByName("Q");
				
			for (var i = 0; i < Q.length; i++)
			{
				tempArray.push(Q[i].value);
			}
				
			tableArray.push(tempArray);
			tableHeaderArray.push("Quantity");
			tableClassArray.push("CA");
			tableColArray.push("colQty");
			
			colNum++;
			footerColSpan++;
		
		//Drug Price
			if (options[2].checked){
				var tempArray = [];
				var DP = document.getElementsByName("DPText");
				
				for (var i = 0; i < DP.length; i++)
				{
					tempArray.push(DP[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray.push("Drug Price");
				tableClassArray.push("RA");
				tableColArray.push("colDP");
				tableFooterArray.push(document.getElementById("TotalDPText").innerHTML);
				
				colNum++;
			};
		
		//Fees
			if (options[3].checked){
				var tempArray = [];
				var F = document.getElementsByName("FText");
				
				for (var i = 0; i < F.length; i++)
				{
					tempArray.push(F[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray.push("Fees");
				tableClassArray.push("RA");
				tableColArray.push("colF");
				tableFooterArray.push(document.getElementById("TotalFText").innerHTML);
				
				colNum++;
			};
			
		//Total price
			var tempArray = [];
			var TP = document.getElementsByName("TPText");
			
			for (var i = 0; i < TP.length; i++)
			{
				tempArray.push(TP[i].innerHTML);
			}
			
			tableArray.push(tempArray);
			tableHeaderArray.push("Total Price");
			tableClassArray.push("RA");
			tableColArray.push("colTP");
			tableFooterArray.push(document.getElementById("TotalTPText").innerHTML);
			
			colNum++;
	}
	else
	{
		var tableHeaderArray1 = [];
		var tableHeaderArray2 = [];
		var headerColSpan = 0;
		var headerRowSpanArray = [];
		var headerColSpanArray = []
		
		//Generic Name + Strength and Dosage Form
			var tempArray = [];
			var GN = document.getElementsByName("GNValue");
			var SD = document.getElementsByName("SD");
			
			for (var i = 0; i < GN.length; i++)
			{
				tempArray.push(GN[i].value + " " + SD[i].value);
			}
			
			//Adds to main array
			tableArray.push(tempArray);
			
			//Creates header array entry
			tableHeaderArray1.push("Medication");
			tableClassArray.push("LA");
			tableColArray.push("colMed");
			
			headerRowSpanArray.push(2);
			headerColSpanArray.push(1);
			
			colNum++;
			footerColSpan++;
		
		//Brand name
			if (options[0].checked){
				var tempArray = [];
				var BN = document.getElementsByName("BN");
				
				for (var i = 0; i < BN.length; i++)
				{
					tempArray.push(BN[i].value);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray1.push("Brand Name");
				tableClassArray.push("LA");
				tableColArray.push("colBN");
				
				headerRowSpanArray.push(2);
				headerColSpanArray.push(1);
				
				colNum++;
				footerColSpan++;
			};
		
		//Unit price
			if (options[1].checked){
				var tempArray = [];
				var UP = document.getElementsByName("UPText");
				
				for (var i = 0; i < UP.length; i++)
				{
					tempArray.push(UP[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray1.push("Unit Price");
				tableClassArray.push("CA");
				tableColArray.push("colUP");
				
				headerRowSpanArray.push(2);
				headerColSpanArray.push(1);
				
				colNum++;
				footerColSpan++;
			};
		
		//Drug Price #1
			if (options[2].checked){
				var tempArray = [];
				var DP = document.getElementsByName("CompDP1Text");
				
				for (var i = 0; i < DP.length; i++)
				{
					tempArray.push(DP[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray2.push("Drug Price");
				tableClassArray.push("RA");
				tableColArray.push("colDP1");
				tableFooterArray.push(document.getElementById("TotalDP1Text").innerHTML);
				
				headerRowSpanArray.push(1);
				
				colNum++;
				headerColSpan++;
			};
		
		//Fees #1
			if (options[3].checked){
				var tempArray = [];
				var F = document.getElementsByName("CompF1Text");
				
				for (var i = 0; i < F.length; i++)
				{
					tempArray.push(F[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray2.push("Fees");
				tableClassArray.push("RA");
				tableColArray.push("colF1");
				tableFooterArray.push(document.getElementById("TotalF1Text").innerHTML);
				
				headerRowSpanArray.push(1);
				
				colNum++;
				headerColSpan++;
			};
			
		//Total price #1
			var tempArray = [];
			var TP = document.getElementsByName("CompTP1Text");
			
			for (var i = 0; i < TP.length; i++)
			{
				tempArray.push(TP[i].innerHTML);
			}
			
			tableArray.push(tempArray);
			tableHeaderArray2.push("Total Price");
			tableClassArray.push("RA");
			tableColArray.push("colTP1");
			tableFooterArray.push(document.getElementById("TotalTP1Text").innerHTML);
			
			headerRowSpanArray.push(1);
			
			colNum++;
			headerColSpan++;
			
		//Drug Price #2
			if (options[2].checked){
				var tempArray = [];
				var DP = document.getElementsByName("CompDP2Text");
				
				for (var i = 0; i < DP.length; i++)
				{
					tempArray.push(DP[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray2.push("Drug Price");
				tableClassArray.push("RA");
				tableColArray.push("colDP1");
				tableFooterArray.push(document.getElementById("TotalDP2Text").innerHTML);
				
				headerRowSpanArray.push(1);
				
				colNum++;
			};
		
		//Fees #2
			if (options[3].checked){
				var tempArray = [];
				var F = document.getElementsByName("CompF2Text");
				
				for (var i = 0; i < F.length; i++)
				{
					tempArray.push(F[i].innerHTML);
				}
				
				tableArray.push(tempArray);
				tableHeaderArray2.push("Fees");
				tableClassArray.push("RA");
				tableColArray.push("colF1");
				tableFooterArray.push(document.getElementById("TotalF2Text").innerHTML);
				
				headerRowSpanArray.push(1);
				
				colNum++;
			};
			
		//Total price #2
			var tempArray = [];
			var TP = document.getElementsByName("CompTP2Text");
			
			for (var i = 0; i < TP.length; i++)
			{
				tempArray.push(TP[i].innerHTML);
			}
			
			tableArray.push(tempArray);
			tableHeaderArray2.push("Total Price");
			tableClassArray.push("RA");
			tableColArray.push("colTP1");
			tableFooterArray.push(document.getElementById("TotalTP2Text").innerHTML);
			
			headerRowSpanArray.push(1);
			
			colNum++;
			
		//Adds the day supplies to the header
		tableHeaderArray1.push("Supply: " + document.getElementById("CompDaySupply1").value + " days");
		headerColSpanArray.push(headerColSpan);
		tableHeaderArray1.push("Supply: " + document.getElementById("CompDaySupply2").value + " days");
		headerColSpanArray.push(headerColSpan);
	}
	
	//Get table and reset
	var table = document.getElementById("PriceTable");
	table.innerHTML = "";
	
	//Variables to build table
	rowNum = 0;
	
	//Cycle through the header array and insert into table
	if (priceSelect.selectedIndex == 0)
	{
		var tr = table.insertRow(rowNum);
		
		for (var i = 0; i < colNum; i++)
		{
			var col = document.createElement("col");
			col.className = tableColArray[i];
			table.appendChild(col);
			
			var th = document.createElement("th");
			th.innerHTML = tableHeaderArray[i];
			tr.appendChild(th);
		};
		
		rowNum++;
	}
	else
	{
		//Appends columns to table
		for (var i = 0; i < colNum; i++)
		{
			var col = document.createElement("col");
			col.className = tableColArray[i];
			table.appendChild(col);
		}
		
		//First header row
		var tr = table.insertRow(rowNum);
		
		for (var i = 0; i < tableHeaderArray1.length; i++)
		{
			//Cycles through the first header array
			var th = document.createElement("th");
		
			th.innerHTML = tableHeaderArray1[i];
			th.rowSpan = headerRowSpanArray[i];
			th.colSpan = headerColSpanArray[i];
			tr.appendChild(th);
		};
		
		rowNum++;
		
		var tr = table.insertRow(rowNum);
		
		for (var i = 0; i < tableHeaderArray2.length; i++)
		{	
			var th = document.createElement("th");
			
			th.innerHTML = tableHeaderArray2[i];
			tr.appendChild(th);
		};
		
		rowNum++;
	}
	
	//Create the rows in the table
	for (var i = 0; i < tableArray[0].length; i++)
	{
		var tr = table.insertRow(rowNum);
		
		for (var ii = 0; ii < colNum; ii++)
		{
			var cell = tr.insertCell(ii);
			cell.innerHTML = tableArray[ii][i];
			cell.className = tableClassArray[ii];
		}
		
		rowNum++;
	}
	
	//Cycle through the footer array and insert into the table
	var tr = table.insertRow(rowNum);
	var x = colNum-(footerColSpan-1);	//Corrects for colSpan;
	
	for (var i = 0; i < x; i++)
	{
		var th = document.createElement("th");
		
		if (i == 0)
		{
			th.innerHTML = "TOTAL";
			th.colSpan = footerColSpan;
		}
		else
		{
			th.innerHTML = tableFooterArray[i-1];
		}

		th.className = "RA";
		tr.appendChild(th);
	};
	
	window.print();
}