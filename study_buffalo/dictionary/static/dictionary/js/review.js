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

                // Reduce the pending count by 1
                let $count = $("#word_count");
                $count.text(Number($count.text()) - 1);
                
                // Request to display additional entries
                retrieve_entries();
            }

            send_message(results.message, "delete-pending");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            send_message(
                `Error deleting entry - ${textStatus}: ${errorThrown}`,
                "error"
            )
        }
    });
}

function add_word(button, e) {
    modelName = e.modelName

    messageTag = modelName === "word" ? "new-word" : "new-excluded-word";

    let $entry = $(button).parents(".entry");
    
    // Get the ID of the entry in the pending model
    let pendingID = $entry.attr("data-id");

    // Get the word element
    $word = $entry.find(".word");

    // Get the word text
    word = $word.text();

    // Get the language of the word
    language = $entry.find(".language").val();

    // Get the dictionary type of the word
    dictionaryType = $entry.find(".dictionary-type").val();

    // Get the dictionary class of the word
    dictionaryClass = $entry.find(".dictionary-class").val();

    // Get the add and exclude buttons
    let addButton = $entry.find(".add")[0];
    let excludeButton = $entry.find(".exclude")[0]

    $.ajax({
        url: "add-new-word/",
        data: {
            pending_id: pendingID,
            model_name: modelName,
            word: word,
            language: language,
            dictionary_type: dictionaryType,
            dictionary_class: dictionaryClass,
        },
        type: "POST",
        beforeSend: function (jqXHR, settings) {
            // Setup the CSRF token for the POST request
            if (!this.crossDomain) {
                const CSRF = $("[name=csrfmiddlewaretoken]").val();

                jqXHR.setRequestHeader("X-CSRFToken", CSRF);
            }

            // Disable add/exclude buttons to prevent duplicate POSTs
            addButton.disabled = true
            excludeButton.disabled = true
        },
        success: function (results) {
            if (results.success) {
                remove_pending_word(results.id);
            }

            send_message(results.message, messageTag);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            send_message(
                `Error adding entry - ${textStatus}: ${errorThrown}`,
                "error"
            )

            // Re-enable buttons to allow re-send
            addButton.disabled = false
            excludeButton.disabled = false
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

function show_source(button) {
    // Get the editable div to retrieve the source text
    let $button = $(button);
    let $parentDiv = $button.parent();
    let $content = $parentDiv.children(".word");

    // Open a new window with the search
    alert($content.attr("data-original"));
}

function create_word_inputs(data) {
    let $div = $("<div></div>");

    // Create the Language select
    let $languageSelect = $(sessionStorage.getItem("language_select"));
    $languageSelect
        .val(data.language)
        .appendTo($div);

    // Create the Dictionary Type select
    let $dictionaryTypeSelect = $(
        sessionStorage.getItem("dictionary_type_select")
    );
    $dictionaryTypeSelect
        .val(data.dictionary_type)
        .appendTo($div);

    // Create the Dictionary Class select
    let $dictionaryClassSelect = $(
        sessionStorage.getItem("dictionary_class_select")
    );

    $dictionaryClassSelect
        .val(data.dictionary_class)
        .appendTo($div);

    // Create an editable div to hold the word
    let $input = $("<div></div>");
    $input
        .attr("contenteditable", "true")
        .attr("data-original", data.original)
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

    // Create a show original button
    let $originalButton = $("<button></button>");
    $originalButton
        .addClass("source")
        .on("click", function () {
            show_source(this);
        })
        .appendTo($div);

    let $originalSpan = $("<span></span>");
    $originalSpan
        .text("Source")
        .appendTo($originalButton);


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
    let $wordDiv = create_word_inputs(entry)
    $wordDiv
        .addClass("word-div")
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
        .on("click", function () {
            add_word(this, { modelName: "word" });
        })
        .appendTo($otherDiv);

    let $addSpan = $("<span></span>");
    $addSpan
        .text("Add")
        .appendTo($addButton);

    // Create a button to exclude entries from the dictionary
    let $excludeButton = $("<button></button>");
    $excludeButton
        .addClass("exclude")
        .on("click", function () {
            add_word(this, { modelName: "excluded" });
        })
        .appendTo($otherDiv);

    let $excludeSpan = $("<span></span>");
    $excludeSpan
        .text("Exclude")
        .appendTo($excludeButton);

    // Create button to delete pending word
    let $deleteButton = $("<button></button>");
    $deleteButton
        .addClass("delete")
        .on("click", function () { delete_word(this) })
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

function save_select_data(selectData) {
    sessionStorage.setItem("language_select", selectData.language);
    sessionStorage.setItem("dictionary_type_select", selectData.dict_type);
    sessionStorage.setItem("dictionary_class_select", selectData.dict_class);
}

function initiate_initial_load() {
    $.ajax({
        url: "retrieve-select-data/",
        data: {},
        type: "GET",
        success: function (results) {
            // Save the data for the select inputs
            save_select_data(results);

            // Retrieve the initial pending entries
            retrieve_entries()
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving entries");
            console.error(textStatus + ": " + errorThrown);
        }
    })

}


$(document).ready(function () {
    // Store database input data and fetch initial query results
    initiate_initial_load();
    
    // Add event listener to update nubmer of queries
    $("#options").on("change", function () {
        clear_displayed_entries();
        retrieve_entries();
    });

})