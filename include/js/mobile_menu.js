function openMenu() {
	var $menu = $("#Menu-List");
	$menu.css("display", "block");
}

function closeMenu(event) {
	var $menu = $("#Menu-List");
	var width = $(document).width();
	
	if (width <= 1000) {
		$menu.css("display", "none");
	}
}

function updateMenu() {
	var width = $(document).width();
	var $menu = $("#Menu");
	
	if (width > 1000) {
		$menu.attr("class", "expanded");
		$("#Menu-List").css("display", "inline-block");
	} else {
		$menu.attr("class", "collapsed");
		$("#Menu-List").css("display", "none");
	}
}

$(document).ready(function() {
	$("#Menu-Icon").on(
		"click",
		function(){openMenu();});
	
	$(window).on(
		"mouseup",
		function(event){closeMenu(event);});
		
	$(window).on(
		"resize",
		function(event){updateMenu();});
	
	updateMenu();
});