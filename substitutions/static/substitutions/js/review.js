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

function remove_entry(pendID) {
    // Get the application ID
    let appID = $("#app-id").text();

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
        url: "delete-entry/",
        data: {
            app_id: appID,
            pend_id: pendID
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

function verify_entry(button) {
    let $entry = $(button).parents(".entry");

    // Get the application ID
    let appID = $("#app-id").text();

    // Get the ID of the entry in the pending model
    let pendID = $entry.attr("data-id");

    // Get all the original fields
    let $originalFields = $entry.find(".original > div");
    let original = [];

    $originalFields.each(function (key, div) {
        let $div = $(div);

        original.push({
            field_name: $div.find("em").text(),
            field_value: $div.find(".editable-div").text()
        });
    });

    // Get all the substitution fields
    let $subFields = $entry.find(".substitution > div");
    let substitutions = [];

    $subFields.each(function (key, div) {
        let $div = $(div);

        substitutions.push({
            field_name: $div.find("em").text(),
            field_value: $div.find(".editable-div").text()
        });
    });

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
            app_id: appID,
            pend_id: pendID,
            orig: JSON.stringify(original),
            subs: JSON.stringify(substitutions)
        },
        type: "POST",
        success: function (results) {
            if (results.success) {
                remove_entry(results.id);
            }

            send_message(results.message, "new-substitution");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error verifying entries");
            console.error(textStatus + ": " + errorThrown);
        }
    });
}

function delete_entry(button) {
    let pendID = $(button).parents(".entry").attr("data-id");
    
    remove_entry(pendID);
}


function search_text(button) {
    // Get the editable div to retrieve the search query
    const $button = $(button);
    const $parentDiv = $button.parent();
    const $content = $parentDiv.children(".editable-div");

    // Encode the search query for the search string
    let searchText = encodeURIComponent($content.text());
    
    // Open a new window with the search
    window.open("https://google.com/search?q=" + searchText);

}


function create_input_set(data) {
    let $div = $("<div></div>");
        
    let $em = $("<em></em>");
    $em
        .text(data.field_name)
        .appendTo($div);

    let $input = $("<div></div>");
    $input
        .attr("contenteditable", "true")
        .addClass("editable-div")
        .html(data.value)
        .appendTo($div);
    
    if (data.google) {
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
            .appendTo($googleButton)
    }

    return $div;
}

function create_entry_dom(entry) {
    let $entryDiv = $("<div></div>");
    $entryDiv
        .addClass("entry")
        .attr("id", "pending-" + entry.id)
        .attr("data-id", entry.id)
        .appendTo($("#entries"));

    // Create the original inputs
    $origDiv = $("<div></div>");
    $origDiv
        .addClass("original")
        .appendTo($entryDiv);

    $.each(entry.orig, function (key, value) {
        $origDiv.append(create_input_set(value));
    });


    // Create the substitution inputs
    $subDiv = $("<div></div>");
    $subDiv
        .addClass("substitution")
        .appendTo($entryDiv);

    $.each(entry.subs, function (key, value) {
        $subDiv.append(create_input_set(value));
    });

    // Create the other options
    let $otherDiv = $("<div></div>");
    $otherDiv
        .addClass("other")
        .appendTo($entryDiv);

    let $verify = $("<button></button>");
    $verify
        .addClass("upload")
        .on("click", function () { verify_entry(this); })
        .appendTo($otherDiv);

    let $verifySpan = $("<span></span>");
    $verifySpan
        .text("Verify")
        .appendTo($verify);

    // Create the delete button
    let $delete = $("<button></button>");
    $delete
        .addClass("delete")
        .on("click", function () { delete_entry(this); })
        .appendTo($otherDiv);

    let $deleteSpan = $("<span></span>");
    $deleteSpan
        .text("Delete")
        .appendTo($delete);
}

function update_entries(results) {
    $.each(results, function (id, entry) {
        create_entry_dom(entry);
    });
}

function retrieve_entries() {
    let $entries = $(".entry");

    // Get the App ID
    let appID = $("#app-id").text();

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
            app_id: appID,
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