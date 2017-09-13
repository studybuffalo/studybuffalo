function open_menu($menu) {
    $menu.toggleClass("open");
}

$(document).ready(function () {
    $("#menu-icon").on("click", function () {
        open_menu($(this));
    });
});