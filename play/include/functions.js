document.addEventListener("DOMContentLoaded", function() {
	attachFunctions();	//Attaches all the appropriate event listeners
});

function tableSort() {
	var id = this.id;
	var table = document.getElementById("Play-Table-List");
	var rows = table.rows;
	var values = [];
	var x
	var row;
	var date;
	var title;
	var category;
	
	//Creates array of indices and values
	for (var i = 1; i < rows.length; i++) {
		values.push([
			rows[i].cells[0],
			rows[i].cells[1],
			rows[i].cells[2],
		]);
	}
	
	//Sorts the entries
	if (id === "Play-Table-Date-D") {
		//Sorts dates in ascending order
		values.sort(function(a, b) {
			if (a[0].childNodes[0].innerHTML > b[0].childNodes[0].innerHTML) {return 1;}
			if (a[0].childNodes[0].innerHTML < b[0].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Date-D").id = "Play-Table-Date-A";
	} else if (id === "Play-Table-Date-A") {
		//Sorts dates in descending order
		values.sort(function(a, b) {
			if (b[0].childNodes[0].innerHTML > a[0].childNodes[0].innerHTML) {return 1;}
			if (b[0].childNodes[0].innerHTML < a[0].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Date-A").id = "Play-Table-Date-D";
	} else if (id === "Play-Table-Title-D") {
		//Sorts titles in ascending order
		values.sort(function(a, b) {
			if (a[1].childNodes[0].innerHTML > b[1].childNodes[0].innerHTML) {return 1;}
			if (a[1].childNodes[0].innerHTML < b[1].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Title-D").id = "Play-Table-Title-A";
	} else if (id === "Play-Table-Title-A") {
		//Sorts titles in descending order
		values.sort(function(a, b) {
			if (b[1].childNodes[0].innerHTML > a[1].childNodes[0].innerHTML) {return 1;}
			if (b[1].childNodes[0].innerHTML < a[1].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Title-A").id = "Play-Table-Title-D";
	} else if (id === "Play-Table-Category-D") {
		console.log("Category Ascending");
		//Sorts category in ascending order
		values.sort(function(a, b) {
			if (a[2].childNodes[0].innerHTML > b[2].childNodes[0].innerHTML) {return 1;}
			if (a[2].childNodes[0].innerHTML < b[2].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Category-D").id = "Play-Table-Category-A";
	} else if (id === "Play-Table-Category-A") {
		console.log("Category Descending");
		//Sorts category in descending order
		values.sort(function(a, b) {
			if (b[2].childNodes[0].innerHTML > a[2].childNodes[0].innerHTML) {return 1;}
			if (b[2].childNodes[0].innerHTML < a[2].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Play-Table-Category-A").id = "Play-Table-Category-D";
	}
	
	//Copies the sorted values into the table
	for (var i = 0; i < values.length; i++) {
		row = table.insertRow(-1);
		date = row.insertCell(0);
		title = row.insertCell(1);
		category = row.insertCell(2);
		
		date.innerHTML = values[i][0].innerHTML;
		title.innerHTML = values[i][1].innerHTML;
		category.innerHTML = values[i][2].innerHTML;
		
	}

	//Deletes the old rows
	for (var i = values.length; i > 0; i--) {
		table.deleteRow(i);
	}
}

function attachFunctions() {
	document.getElementById("Play-Table-Date-A").addEventListener("click", tableSort);
	document.getElementById("Play-Table-Title-D").addEventListener("click", tableSort);
	document.getElementById("Play-Table-Category-D").addEventListener("click", tableSort);
}