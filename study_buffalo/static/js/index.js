function changeUpdateIcon(update) {
    let $update = $(update);
    console.log($update);
    // Stop the update loop
    $("#updates").attr("data-loop", "");

    // Remove selection from all updates
    $(".update-link").removeClass("selected");

    // Add selected to this icon
    $update.addClass("selected");

    // Change the update display
    const id = $update.attr("data-id");

    changeUpdate(id);
}

function changeUpdate(id) {
    let $updates = $(".update");
    
    $updates.addClass("hide");

    $updates.each(function (index, updateDiv) {
        let $updateDiv = $(updateDiv);

        if ($updateDiv.attr("data-id") === id) {
            $updateDiv.removeClass("hide");
        }
    });
}

function cycleUpdates() {
    // Check if looping cancelled
    const loop = $("#updates").attr("data-loop");

    // Find the currently selected item
    if (loop) {
        // Get the currently selected item
        const $selection = $("#updates .selected");
        const $sibling = $selection.next();

        // Remove the current selection
        $selection.removeClass("selected");

        // Change to the next sibling, or the first item if no sibling 
        // and collect the selected ID
        let id = 0;

        if ($sibling.length) {
            $sibling.addClass("selected");
            id = $sibling.attr("data-id");
        } else {
            const $firstItem = $selection.parent().children().eq(1);
            
            $firstItem.addClass("selected");
            id = $firstItem.attr("data-id");
        }

        // Update the display
        changeUpdate(id);

        // Loop in 5 seconds
        setTimeout(cycleUpdates, 5000);
    }
}

$(document).ready(function () {
    setTimeout(function () {cycleUpdates()}, 7500);
});