/* TODO:
 *  If QTc not > 500 ms, increase warning size in the pro-qtc section
 */
function updateAssessmentType() {
    const assessmentType = $('.assessment-type:checked').val();

    // Hide all risk factor items flagged as extra
    $('#risk-factors > li').each(function(index, element) {
        const $element = $(element);

        if (assessmentType === 'quick') {

            if ($element.hasClass('extra')) {
                $element.addClass('hide');
            }
        } else {
            $element.removeClass('hide');
        }
    });

    // Update risk scores
    calculateQTRisk();
    calculateProQTc();
}

function calculateQTRisk() {
    const $riskFactors = $('#risk-factors :checkbox:checked');

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

function calculateProQTc() {
    const $riskFactors = $('#risk-factors :checkbox:checked');

    let score = 0;

    $riskFactors.each(function(index, element) {
        score = score + Number($(element).attr('data-pro-qtc'));
    });

    // Determine the percentages
    const assessmentType = $('.assessment-type:checked').val();
    const interpretation = {
        ariLow: '',
        ariHigh: '',
        rriLow: '',
        rriHigh: '',
    }

    if (score === 0 || score === 1) {
        interpretation.ariLow = '6.6%';
        interpretation.ariHigh = '6.6%';
        interpretation.rriLow = '1.32';
        interpretation.rriHigh = '1.32';
    } else if (score === 2) {
        interpretation.ariLow = '8.9%';
        interpretation.ariHigh = '11.6%';
        interpretation.rriLow = '1.78';
        interpretation.rriHigh = '2.32';
    } else if (score === 3) {
        interpretation.ariLow = '9.2%';
        interpretation.ariHigh = '18.8%';
        interpretation.rriLow = '1.84';
        interpretation.rriHigh = '3.76';
    } else {
        interpretation.ariLow = '22.5%';
        interpretation.ariHigh = '34.5%';
        interpretation.rriLow =  '4.50';
        interpretation.rriHigh = '6.90';
    }

    let ariText = '';
    let rriText = '';

    if (assessmentType === 'quick') {
        ariText = interpretation.ariHigh;
        rriText = interpretation.rriHigh;
    } else {
        if (score === 0 || score === 1) {
            ariText = interpretation.ariHigh;
            rriText = interpretation.rriHigh;
        } else {
            ariText = `${interpretation.ariLow} to ${interpretation.ariHigh}`;
            rriText = `${interpretation.rriLow} to ${interpretation.rriHigh}`;
        }
    }

    $('#pro-qtc-score').text(score);
    $('#pro-qtc-ari').text(ariText);
    $('#pro-qtc-rri').text(rriText);
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
    $(".assessment-type").on('change', function() {
        updateAssessmentType();
    });

    $('#risk-factors').on('change', function() {
        calculateQTRisk();
        calculateProQTc();
    });

    $('#rf-1, #rf-2').on('change', function() {
        limitToOneSelection(
            [document.getElementById('rf-1'), document.getElementById('rf-2')],
            this
        );
    });

    // Run initial updates and calculations
    updateAssessmentType();
});
