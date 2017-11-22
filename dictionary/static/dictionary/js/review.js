function check_notification_permission() {
    let permission = false;

    // Check for notification support
    if (!("Notification" in window)) {
        console.warn("Notifications not supported");

        // Notification privileges granted
    } else if (Notification.permission === "granted") {
        permission = true;

        // Request notification privileges
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission(function (permission) {
            if (permission === "granted") {
                permission = true;
            }
        });
        // Otherwise, notification permissions denied
    } else {
        console.log("Notifications denied by user")
    }

    return permission
}

function send_message(msg, tag) {
    let permission = check_notification_permission
    
    if (permission) {
        // Get details of the message
        let title = "Study Buffalo Substitutions App"
        let options = {
            body: msg,
            icon: "/static/images/android-chrome-192x192.png",
            tag: tag
        }

        var notification = new Notification(title, options);
    }
}

function remove_pending_word(pendingID) {
    // Setup CSRF token for POST
    let CSRF = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF);
            }
        }
    });

    $.ajax({
        url: "delete-pending-word/",
        data: {
            pending_id: pendingID
        },
        type: "POST",
        success: function (results) {
            if (results.success) {
                // Remove this entry form the page
                $("#pending-" + results.id).remove();

                // Request to display additional entries
                retrieve_entries();
            }

            send_message(results.message, "delete-pending");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error deleting entry");
            console.error(textStatus + ": " + errorThrown);
        }
    });
}

function add_word(button) {
    let $entry = $(button).parents(".entry");
    
    // Get the ID of the entry in the pending model
    let pendingID = $entry.attr("data-id");

    // Get the word to add to the dictionary
    // SOMETHING HERE
    word = ""
    // Setup CSRF token for POST
    let CSRF = $("[name=csrfmiddlewaretoken]").val();
    
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF);
            }
        }
    });

    $.ajax({
        url: "verify-entry/",
        data: {
            pending_id: pendID,
            word: word
        },
        type: "POST",
        success: function (results) {
            if (results.success) {
                remove_pending_word(results.id);
            }

            send_message(results.message, "new-word");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error verifying entries");
            console.error(textStatus + ": " + errorThrown);
        }
    });
}

function exclude_word(button) {
    console.log("Excluding word stuff goes here")
}

function delete_word(button) {
    let pendingID = $(button).parents(".entry").attr("data-id");
    
    remove_pending_word(pendingID);
}

function search_text(button) {
    // Get the editable div to retrieve the search query
    let $button = $(button);
    let $parentDiv = $button.parent();
    let $content = $parentDiv.children(".word");

    // Open a new window with the search
    window.open("https://google.com/search?q=" + $content.text());
}

function create_word_inputs(data) {
    let $div = $("<div></div>");

    // Create an editable div to hold the word
    let $input = $("<div></div>");
    $input
        .attr("contenteditable", "true")
        .addClass("word")
        .text(data.word)
        .appendTo($div);

    // Create a search button
    let $googleButton = $("<button></button>");
    $googleButton
        .addClass("google")
        .on("click", function () {
            search_text(this);
        })
        .appendTo($div);

    let $googleSpan = $("<span></span>");
    $googleSpan
        .text("Search")
        .appendTo($googleButton);

    return $div;
}

function create_entry_dom(entry) {
    let $entryDiv = $("<div></div>");
    $entryDiv
        .addClass("entry")
        .attr("id", "pending-" + entry.id)
        .attr("data-id", entry.id)
        .appendTo($("#entries"));

    // Create the word div
    $wordDiv = $("<div></div>");
    $wordDiv
        .addClass("word-div")
        .append(create_word_inputs(entry))
        .appendTo($entryDiv);
        
    // Create the other options
    let $otherDiv = $("<div></div>");
    $otherDiv
        .addClass("other")
        .appendTo($entryDiv);

    // Create button to add word to dictionary
    let $addButton = $("<button></button>");
    $addButton
        .addClass("add")
        .on("click", function () { add_word(this); })
        .appendTo($otherDiv);

    let $addSpan = $("<span></span>");
    $addSpan
        .text("Add")
        .appendTo($addButton);

    // Create a button to exclude entries from the dictionary
    let $excludeButton = $("<button></button>");
    $excludeButton
        .addClass("exclude")
        .on("click", function () { exclude_word(this); })
        .appendTo($otherDiv);

    let $excludeSpan = $("<span></span>");
    $excludeSpan
        .text("Exclude")
        .appendTo($excludeButton);

    // Create button to delete pending word
    let $deleteButton = $("<button></button>");
    $deleteButton
        .addClass("delete")
        .on("click", function () { delete_word(this); })
        .appendTo($otherDiv);

    let $deleteSpan = $("<span></span>");
    $deleteSpan
        .text("Delete")
        .appendTo($deleteButton);
}

function update_entries(results) {
    $.each(results, function (id, entry) {
        create_entry_dom(entry);
    });
}

function retrieve_entries() {
    let $entries = $(".entry");
    
    // Calculate how many entries to retrieve
    let maxEntries = Number($("#entries-to-display").val());
    let currentNum = $entries.length;
    let requestNum = maxEntries > currentNum ? maxEntries - currentNum : 0;

    // Calculate the last ID retrieved
    let lastNum = 0

    if ($entries.length) {
        lastNum = $entries.last().attr("data-id");
    }

    // Setup CSRF token for POST
    let CSRF = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF);
            }
        }
    });

    $.ajax({
        url: "retrieve-entries/",
        data: {
            last_id: lastNum,
            request_num: requestNum
        },
        type: "POST",
        success: function (results) {
            update_entries(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving entries");
            console.error(textStatus + ": " + errorThrown);
        }
    })
}

function clear_displayed_entries() {
    $("#entries").empty();
}

$(document).ready(function () {
    // Load initial items
    retrieve_entries();

    // Add event listener to update nubmer of queries
    $("#options").on("change", function () {
        clear_displayed_entries();
        retrieve_entries();
    });

    
})