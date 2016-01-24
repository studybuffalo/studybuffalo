document.addEventListener("DOMContentLoaded", function() {
	resizeMain();
	window.addEventListener("resize", resizeMain);
	
	//Refires function as images load
	images = document.images;
	for (var i = 0; i < images.length; i++) {
		images[i].onload = function() {resizeMain();}
	}
});

function resizeMain() {
	var div = document.getElementById("Main-Content");
	var divHeight
	var footer = document.querySelector("Footer").scrollHeight;
	var divTop = div.offsetTop;
	var viewportHeight = window.innerHeight;
	var margin = 20;
	var buffer = 30;	//Additional space for unaccounted for toolbars
	
	//Resets the div height to measure the content height
	div.style.height = "100%"
	divHeight = div.scrollHeight;
	
	//Calculates the current height available for the main content div
	var newHeight = viewportHeight - divTop - footer - margin - buffer;
	
	//If available height > current height, expand div to fill
	if (newHeight > divHeight) {div.style.height = newHeight + "px";}
}