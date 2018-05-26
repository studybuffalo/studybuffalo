function set_all_values() {
    // Get the new times and durations
    const newStartTime = $("#quick_start_time").val();
    const newDuration = $("#quick_duration").val();

    // Get all the elements to update
    let startTimeInputs = $(".input_table .start_time input");
    let durationInputs = $(".input_table .duration input");

    // Update all elements
    startTimeInputs.val(newStartTime);
    durationInputs.val(newDuration);
}

$(document).ready(function () {
    $("#set_all_values").on("click", function () {
        set_all_values();
    });
});