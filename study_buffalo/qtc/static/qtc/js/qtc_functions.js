function calculateQTRisk($riskFactors) {
    let score = 0;

    $riskFactors.each(function(index, element) {
        score = score + Number($(element).attr('data-qt-risk'));
    });

    // Determine the percentage
    let percentage = '';

    if (score < 7) {
        percentage = '15%';
    } else if (score < 11) {
        percentage = '37%';
    } else {
        percentage = '73%';
    }
    "";

    // Update displays
    $('#qt-risk-score').text(score);
    $('#qt-risk-percentage').text(percentage);
}

function calculateProQTc($riskFactors) {
    let score = 0;

    $riskFactors.each(function(index, element) {
        score = score + Number($(element).attr('data-pro-qtc'));
    });

    // Determine the percentages
    let percentageLow = '';
    let percentageHigh = '';

    if (score === 0 || score === 1) {
        percentageLow = '11.6%';
        percentageHigh = '11.6%'
    } else if (score === 2) {
        percentageLow = '13.9%';
        percentageHigh = '16.6%';
    } else if (score === 3) {
        percentageLow = '14.2%';
        percentageHigh = '23.8%';
    } else {
        percentageLow = '27.5%';
        percentageHigh = '39.5%';
    }

    $('#pro-qtc-score').text(score);
    $('#pro-qtc-percentage').text(`${percentageLow} to ${percentageHigh}`);
}

function limitToOneSelection(elements, clickedElement) {
    // Limits user to one selection of the elements in the group

    // If new element is clicked, remove any other checked boxes
    if ($(clickedElement).prop('checked')) {
        $.each(elements, function(index, element) {
            if (element !== clickedElement) {
                $(element).prop('checked', false);
            }
        });
    }
}

$(document).ready(function () {
    $('#risk-factors').on('change', function() {
        const $riskFactors = $('#risk-factors :checkbox:checked');
        calculateQTRisk($riskFactors);
        calculateProQTc($riskFactors);
    });

    $('#rf-1, #rf-2').on('change', function() {
        limitToOneSelection(
            [document.getElementById('rf-1'), document.getElementById('rf-2')],
            this
        );
    });
});
