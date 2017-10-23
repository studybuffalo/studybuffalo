function process_log_entries(results) {
    // Remove all the previous entries first
    $(".log_entry").remove();

    // Cycle through each result item and append it the DOM
    let $logDiv = $("#log_entries");

    for (let i = 0; i < results.length; i++) {
        // Create the main anchor element
        let $entryAnchor = $("<a></a>");
        $entryAnchor
            .addClass("level_" + results[i]["level_no"])
            .addClass("log_entry")
            .attr("data-id", results[i]["entry_id"])
            .appendTo($logDiv);

        // Create the elements for asc_time
        let $timeEm = $("<em></em>");
        $timeEm
            .text("Datetime");

        let $timeSpan = $("<span></span>");
        $timeSpan
            .addClass("asc_time")
            .append($timeEm)
            .text(results[i]["asc_time"])
            .appendTo($entryAnchor);

        // Create the elements for app_name
        let $appEm = $("<em></em>");
        $appEm
            .text("Application");

        let $appSpan = $("<span></span>");
        $appSpan
            .addClass("app_name")
            .append($appEm)
            .text(results[i]["app_name"])
            .appendTo($entryAnchor);

        // Create the elements for func_name
        let $funcEm = $("<em></em>");
        $funcEm
            .text("Function");

        let $funcSpan = $("<span></span>");
        $funcSpan
            .addClass("func_name")
            .append($funcEm)
            .text(results[i]["func_name"])
            .appendTo($entryAnchor);

        // Create the elements for message
        let $messageEm = $("<em></em>");
        $messageEm
            .text("Message");

        let $messageSpan = $("<span></span>");
        $messageSpan
            .addClass("message")
            .append($messageEm)
            .text(results[i]["message"])
            .appendTo($entryAnchor);
    }
}

function retrieveEntries() {
    // Collect the filter values to pass to the view
    let $applications = $(".filter_app:checked");
    let $levels = $(".filter_level:checked");
    let start_date = $("#filter_time_start").val();
    let end_date = $("#filter_time_end").val();

    // Assemble array of the selected applications
    app_names = [];

    $applications.each(function () {
        app_names.push(this.value);
    });

    // Assemble array of the log levels
    log_levels = [];

    $levels.each(function () {
        log_levels.push(this.value);
    });

    $.ajax({
        url: "update-entries/",
        data: {
            app_names: app_names.join(","),
            log_levels: log_levels.join(","),
            start_date: start_date,
            end_date: end_date
        },
        type: "GET",
        dataType: "json",
        success: function (results) {
            process_log_entries(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving updated log entries");
            console.error(textStatus + ": " + errorThrown);
        }
    });
}

$(document).ready(function () {
    // Grab default log entries on load
    retrieveEntries();

    // Add the filter event listener
    $("#filter_entries").on("click", function () {
        retrieveEntries();
    });
});