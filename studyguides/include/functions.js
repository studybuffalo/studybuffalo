document.addEventListener("DOMContentLoaded", function() {
	attachFunctions();	//Attaches all the appropriate event listeners
});

function tableSort() {
	var id = this.id;
	var table = document.getElementById("Study-Table-List");
	var rows = table.rows;
	var values = [];
	var x
	var row;
	var title;
	var description;
	var update;
	
	//Creates array of indices and values
	for (var i = 1; i < rows.length; i++) {
		values.push([
			rows[i].cells[0],
			rows[i].cells[1],
			rows[i].cells[2]
		]);
	}
	
	//Sorts the entries
	if (id === "Study-Table-Title-D") {
		//Sorts titles in ascending order
		values.sort(function(a, b) {
			if (a[0].childNodes[0].innerHTML > b[0].childNodes[0].innerHTML) {return 1;}
			if (a[0].childNodes[0].innerHTML < b[0].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Study-Table-Title-D").id = "Study-Table-Title-A";
	} else if (id === "Study-Table-Title-A") {
		//Sorts titles in descending order
		values.sort(function(a, b) {
			if (b[0].childNodes[0].innerHTML > a[0].childNodes[0].innerHTML) {return 1;}
			if (b[0].childNodes[0].innerHTML < a[0].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Study-Table-Title-A").id = "Study-Table-Title-D";
	} else if (id === "Study-Table-Update-D") {
		//Sorts updates in ascending order
		values.sort(function(a, b) {
			if (a[2].childNodes[0].innerHTML > b[2].childNodes[0].innerHTML) {return 1;}
			if (a[2].childNodes[0].innerHTML < b[2].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
		
		//Updates the ID
		document.getElementById("Study-Table-Update-D").id = "Study-Table-Update-A";
	} else if (id === "Study-Table-Update-A") {
		//Sorts updates in descending order
		values.sort(function(a, b) {
			if (b[2].childNodes[0].innerHTML > a[2].childNodes[0].innerHTML) {return 1;}
			if (b[2].childNodes[0].innerHTML < a[2].childNodes[0].innerHTML) {return -1;}
			return 0;
		});
			
		//Updates the ID
		document.getElementById("Study-Table-Update-A").id = "Study-Table-Update-D";
	}
	
	//Copies the sorted values into the table
	for (var i = 0; i < values.length; i++) {
		row = table.insertRow(-1);
		title = row.insertCell(0);
		description = row.insertCell(1);
		update = row.insertCell(2);
		
		title.innerHTML = values[i][0].innerHTML;
		description.innerHTML = values[i][1].innerHTML;
		update.innerHTML = values[i][2].innerHTML;
	}

	//Deletes the old rows
	for (var i = values.length; i > 0; i--) {
		table.deleteRow(i);
	}
}

function attachFunctions() {
	document.getElementById("Study-Table-Title-A").addEventListener("click", tableSort);
	document.getElementById("Study-Table-Update-D").addEventListener("click", tableSort);
}