function processLogEntries(results) {
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
            .on("click", function () { viewDetails(this); })
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
            processLogEntries(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving updated log entries");
            console.error(textStatus + ": " + errorThrown);
        }
    });
}

/****************************************************************************
 *	closeInfoPopup()	Closes the popup window generated to dispaly drug 	*
 *						info												*
 ****************************************************************************/
function closePopup(e) {
    let info_popup = $("#log_entry_info")[0]
    
    if (e !== info_popup) {
        $("#popup").remove();
    }
}

function displayDetails(entry) {
    // Collect page, viewport, and element dimensions/coordinates
    const pageHt = $(document).height();
    const pageWid = $(document).width();
    const screenWid = $(window).width();
    const scrollHt = document.body.scrollTop ||
        document.documentElement.scrollTop;

    // Create a div that covers the page to catch all outside clicks
    let $coverDiv = $("<div></div>");
    $coverDiv
        .attr("id", "popup")
        .height(pageHt)
        .width(pageWid)
        .on("click", function (e) { closePopup(this); })
        .prependTo("body");
    
    // Calculate pop-up width (90% of the window)
    let popupWid = screenWid * 0.9;

    // Give the popup a 5% margin on both sides
    let popupLeft = screenWid * 0.05;

    // Place the popup at the top of the viewport
    let popupTop = scrollHt + 10;

    // Popup div positions to left of trigger button
    let $infoDiv = $("<div></div>");
    $infoDiv
        .attr("id", "log_entry_info")
        .css({
            "left": popupLeft + "px",
            "top": popupTop  + "px",
            "width": popupWid + "px"
        })
        .appendTo($coverDiv);

    // The Pop-Up Div Title
    let $titleDiv = $("<div></div>");
    $titleDiv
        .appendTo($infoDiv);

    let $title = $("<h2></h2>");
    $title
        .text("Log Entry Details")
        .appendTo($titleDiv);

    // The app_name div
    let $appNameDiv = $("<div></div>");
    $appNameDiv
        .appendTo($infoDiv);

    let $appNameStrong = $("<strong></strong>");
    $appNameStrong
        .text("Application Name: ")
        .appendTo($appNameDiv);

    let $appNameSpan = $("<span></span>");
    $appNameSpan
        .text(entry.app_name)
        .appendTo($appNameDiv);

    // The asc_time and msec div
    let $timeDiv = $("<div></div>");
    $timeDiv
        .appendTo($infoDiv);

    let $timeStrong = $("<strong></strong>");
    $timeStrong
        .text("Log Entry Time: ")
        .appendTo($timeDiv);

    let $timeSpan = $("<span></span>");
    $timeSpan
        .text(entry.asc_time + "." + entry.msec + " " + entry.timezone)
        .appendTo($timeDiv);

    // The created div
    let createdText = entry.created + " seconds";
    createdText += entry.relative_created ? " (" + entry.relative_created
        + " milliseconds since logging module loaded)" : "";

    let $createdDiv = $("<div></div>");
    $createdDiv
        .appendTo($infoDiv);

    let $createdStrong = $("<strong></strong>");
    $createdStrong
        .text("Entry Created: ")
        .appendTo($createdDiv);
    
    let $createdSpan = $("<span></span>");
    $createdSpan
        .text(createdText)
        .appendTo($createdDiv);

    // The level_name and level_no div
    const logLevelText = entry.level_no + " (" + entry.level_name + ")";

    let $logLevelDiv = $("<div></div>");
    $logLevelDiv
        .appendTo($infoDiv);

    let $logLevelStrong = $("<strong></strong>");
    $logLevelStrong
        .text("Log Level: ")
        .appendTo($logLevelDiv);

    let $logLevelSpan = $("<span></span>");
    $logLevelSpan
        .text(logLevelText)
        .appendTo($logLevelDiv);

    // The message div
    let $messageDiv = $("<div></div>");
    $messageDiv
        .appendTo($infoDiv);

    let $messageStrong = $("<strong></strong>");
    $messageStrong
        .text("Message: ")
        .appendTo($messageDiv);

    let $messageSpan = $("<span></span>");
    $messageSpan
        .text(entry.message)
        .appendTo($messageDiv);

    // The path_name, file_name, name, module, func_name, and line_no div
    const logPathText = entry.path_name + " > " + entry.file_name
        + " > " + entry.name + " > " + entry.module + " > " + entry.func_name
        + " > line " + entry.line_no;

    let $logPathDiv = $("<div></div>");
    $logPathDiv
        .appendTo($infoDiv);

    let $logPathStrong = $("<strong></strong>");
    $logPathStrong
        .text("Log Path: ")
        .appendTo($logPathDiv);
    
    let $logPathSpan = $("<span></span>");
    $logPathSpan
        .text(logPathText)
        .appendTo($logPathDiv);

    // The exc_info div
    let excInfoText = entry.exc_info;

    let $excInfoDiv = $("<div></div>");
    $excInfoDiv
        .appendTo($infoDiv);

    let $excInfoStrong = $("<strong></strong>");
    $excInfoStrong
        .html("Exception Info: ")
        .appendTo($excInfoDiv);

    let $excInfoPre = $("<pre></pre>");
    $excInfoPre
        .text(entry.exc_info)
        .appendTo($excInfoDiv);

    // The process and process_name div
    const processText = entry.process + " (" + entry.process_name + ")";

    let $processDiv = $("<div></div>");
    $processDiv
        .appendTo($infoDiv);

    let $processStrong = $("<strong></strong>");
    $processStrong
        .text("Process: ")
        .appendTo($processDiv);

    let $processSpan = $("<span></span>");
    $processSpan
        .text(processText)
        .appendTo($processDiv);

    // The thread and thread_name div
    const threadText = entry.thread + " (" + entry.thread_name + ")";

    let $threadDiv = $("<div></div>");
    $threadDiv
        .appendTo($infoDiv);

    let $threadStrong = $("<strong></strong>");
    $threadStrong
        .text("Thread: ")
        .appendTo($threadDiv);

    let $threadSpan = $("<span></span>");
    $threadSpan
        .text(threadText)
        .appendTo($threadDiv);

    // The stack_info div
    let $stackDiv = $("<div></div>");
    $stackDiv
        .appendTo($infoDiv);

    let $stackStrong = $("<strong></strong>");
    $stackStrong
        .text("Stack Info: ")
        .appendTo($stackDiv);

    let $stackSpan = $("<span></span>");
    $stackSpan
        .text(entry.stack_info)
        .appendTo($stackDiv);

    // Close Button
    let $closeDiv = $("<div></div>");
    $closeDiv
        .attr("class", "close")
        .appendTo($infoDiv);

    let $closeButton = $("<input type='button'>")
    $closeButton
        .val("Close")
        .on("click", function () { closePopup(); })
        .appendTo($closeDiv);
}

function viewDetails(a) {
    entry_id = $(a).attr("data-id");
    
    $.ajax({
        url: "retrieve-entry/",
        data: {entry_id: entry_id},
        type: "GET",
        dataType: "json",
        success: function (results) {
            displayDetails(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving desired log entry");
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