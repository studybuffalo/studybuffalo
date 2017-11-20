function update_entries(results) {
    console.log(results);
}

function retrieve_entries() {
    let $entries = $(".entry");

    // Get the App ID
    let app_id = $("#app-id").text();

    // Calculate how many entries to retrieve
    let max_entries = Number($("#entries-to-display").val());
    let current_num = $entries.length;
    let request_num = max_entries > current_num ? max_entries - current_num : 0;

    // Calculate the last ID retrieved
    let last_num = 0

    if ($entries.length) {
        last_num = $entries.last.attr("data-id");
    }

    $.ajax({
        url: "retrieve-entries/",
        data: {
            app_id: app_id,
            last_id: last_num,
            request_num: request_num
        },
        type: "GET",
        success: function (results) {
            update_entries(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving entries");
            console.error(textStatus + ": " + errorThrown);
        }
    })
}

$(document).ready(function () {
    // Load initial items
    retrieve_entries();

    // Add event listener to update nubmer of queries
    $("#options").on("change", function () {
        retrieve_entries();
    });

    
})