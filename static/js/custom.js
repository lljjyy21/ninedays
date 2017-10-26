/**
 * Created by Dmytro on 7/18/2017.
 */

$(window).on("load", function () {
    var page = new Page();
    page.update();
});

$(window).resize(function () {
    var page = new Page();
    page.update();
});

$(window).on("orientationchange", function () {
    var page = new Page();
    page.update();
});

$(document).bind("ajaxSend", function(){

}).bind("ajaxStop", function(){
    var page = new Page();
    page.update();
});

function Page() {
    var body = new BodyStyle();
    var footer = new Footer();
    var inputFieldsStyle = new InputFieldsStyle();
    var scrollArrow = new ScrollArrow();
    var verticalCenterButtonText = new VerticalCenterButtonText();
    var isMobileLayout = $('#mobile').is(':visible');

    function updatePage() {
        // Update values of input fields
        if (applicationState.stateChanged()) {
            if (applicationState.state === applicationState.deviceStatuses.MOBILE) {
                inputFieldsState.updateDesktop();
            }
            else {
                inputFieldsState.updateMobile();
            }
            applicationState.updateCurrentDeviceState();
        }

        body.update();
        if (isMobileLayout) {
            inputFieldsStyle.update();
        }
        else {
            inputFieldsStyle.update();
            scrollArrow.update();
            footer.update();
            verticalCenterButtonText.update();
        }
    }

    return {
        update: updatePage
    };
}

function BodyStyle() {
    var FOOTER_HEIGHT = 100, MIN_PAGE_HEIGHT = 650;
    var PAGE_HEIGHT = Math.max(MIN_PAGE_HEIGHT, $(window).height()) - FOOTER_HEIGHT;
    var isMobileLayout = $('#mobile').is(':visible');
    calculatePageHeight();

    function calculatePageHeight() {
        if (isMobileLayout) {
            PAGE_HEIGHT = $(document).height();
            FOOTER_HEIGHT = 0;
        }
    }

    function updateBodyHeight() {
        $('.container').css('height', PAGE_HEIGHT);
        if (!isMobileLayout) {
            $('.container-start-page').css('height', PAGE_HEIGHT + FOOTER_HEIGHT);
        }
    }

    function updateFooterHeight() {
        // NOTE: -1px required to remove unnecessary scroll-bar on the page.
        $('.footer').css('height', FOOTER_HEIGHT - 1);
    }

    function updateHeight() {
        updateBodyHeight();
        if (!isMobileLayout) {
            updateFooterHeight();
        }
    }

    return {
        update: updateHeight
    };
}

function Footer() {
    function updateLogoImageHeight() {
        $('#logo-block').css({'padding-bottom': $('#logo').height()});
    }

    function updateFooterTextPaddingTop() {
        var LOGO_HEIGHT = $('#logo').height()/2 - $('#logo-text').height()/2;
        $('.logo-text').css({'padding-top': LOGO_HEIGHT});
    }

    function updateFooter() {
        updateLogoImageHeight();
        updateFooterTextPaddingTop();
    }

    return {
        update: updateFooter
    };
}

function ScrollArrow() {
    var rowWidth = $('#textLogo').width()/2,
        scrollArrow = $('#scrollArrow').width()/2,
        bootstrapPadding = 15;

    function updateScrollArrowPosition() {
        $('#scrollArrow').css('margin-left', rowWidth - scrollArrow - bootstrapPadding);
    }

    return {
        update: updateScrollArrowPosition
    }
}

function InputFieldsStyle() {
    var centerColumnWidth = $('#mobile').find('.center-column').width()/2,
        inputs = $('.input-mobile');

    function updateInputFieldWidth() {
        inputs.css({'width': centerColumnWidth});
    }

    function updateInputDateAlignment() {
        var inputDate = $('.input-date'),
            isMobileLayout = $('#mobile').is(':visible');

        var span = $("span").val(inputDate.first().val());
        if (isMobileLayout) {
            inputDate.css('padding-left', "6%");
        }
        else {
            inputDate.css('text-align', 'left');
            inputDate.css('padding-left', '');
        }
    }

    function updateInputField() {
        updateInputFieldWidth();
        updateInputDateAlignment();
    }

    return {
        update: updateInputField
    };
}


function VerticalCenterButtonText() {

    function updateTextMargin() {
        var text = $('#btn-text');
        var verticalTextHeight = text.height(),
            centerColumnHeight = $('#functional-page').height();

        var marginTop = centerColumnHeight/2 - verticalTextHeight/2;
        text.css({'margin-top': marginTop});
    }

    return {
        update: updateTextMargin
    };
}


$('.btn-area').on('click touchstart', function(e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var stockCalculationsDrawer = new StockCalculationsDrawer();
    stockCalculationsDrawer.getAndDrawCalculations();
});


function StockCalculationsDrawer() {
    var stockIdName = undefined,
        startDateIdName = undefined,
        endDateIdName = undefined,
        shortMaIdName = undefined,
        longMaIdName = undefined,
        rangeIdName = undefined;

    function assignHTMLElementIdsDependingOnDeviceLayout() {
        var isMobileLayout = $('#mobile').is(':visible');

        if (isMobileLayout) {
            stockIdName = '#stock-name-mobile';
            startDateIdName = '#start-date-mobile';
            endDateIdName = '#end-date-mobile';
            shortMaIdName = '#short-ma-mobile';
            longMaIdName = '#long-ma-mobile';
            rangeIdName = '#range';
        }
        else {
            stockIdName = '#stock-name';
            startDateIdName = '#start-date';
            endDateIdName = '#end-date';
            shortMaIdName = '#short-ma';
            longMaIdName = '#long-ma';
            rangeIdName = '#range';
        }
    }

    function getAndDrawCalculations() {
        assignHTMLElementIdsDependingOnDeviceLayout();

        var stock = $(stockIdName).val(),
            start_date = $(startDateIdName).val(),
            end_date = $(endDateIdName).val(),
            short_ma = $(shortMaIdName).val(),
            long_ma = $(longMaIdName).val(),
            range = $(rangeIdName).val();


        //TODO: Test
        var inputFieldsValidation = new InputFieldsValidation();
        var isValidInput = inputFieldsValidation.isValid();

        if (isValidInput) {
            inputFieldsState.update();
            var stateObject = inputFieldsState.get();
        }
        else {
            inputFieldsState.reset();
            return;
        }


        var EVENT_NAMES = ["average-event",
                           "moving-average-event",
                           "pass-resistance-line-event",
                           "small-movement-event",
                           "support-line-rebound-event"];

        $.ajax({
            url: '/calculate',
            type: 'GET',
            data: {
                stock: stateObject.stockName,
                start_date: stateObject.startDate,
                end_date: stateObject.endDate,
                short_ma: stateObject.shortMA,
                long_ma: stateObject.longMA,
                range: stateObject.range
            },
            success: function (response) {

                var response_object = JSON.parse(response);

                for (var index in EVENT_NAMES) {
                    if (EVENT_NAMES.hasOwnProperty(index)) {
                        var eventName = EVENT_NAMES[index];
                        if (response_object.hasOwnProperty(eventName)) {
                            drawWheelByEvent(eventName, response_object[eventName])
                        }
                    }
                }
            },
            error: function (response) {
                // TODO: Show error message

                var response_object = JSON.parse(response);

                for (var index in EVENT_NAMES) {
                    if (EVENT_NAMES.hasOwnProperty(index)) {
                        var eventName = EVENT_NAMES[index];
                        if (response_object.hasOwnProperty(eventName)) {
                            drawWheelByEvent(eventName, response_object[eventName])
                        }
                    }
                }
            }
        });
    }

    return {
        getAndDrawCalculations: getAndDrawCalculations
    };
}

// TODO: deprecated, delete
function OutputDrawer(parameters) {
    var title = parameters.title === undefined ? "" : parameters.title,
        messages = parameters.messages === undefined ? "" : parameters.messages,
        stockTitleIdName = undefined,
        stockCalculationsIdName = undefined;

    function assignHTMLElementIdsDependingOnDeviceLayout() {
        if ($('#mobile').is(':visible')) {
            stockTitleIdName = '#stock-title-mobile';
            stockCalculationsIdName = '#stock-calculation-mobile';
        }
        else {
            stockTitleIdName = '#stock-title';
            stockCalculationsIdName = '#stock-calculation';
        }
    }

    function drawTitle() {
        var div = document.createElement('div');
        div.innerText = title;
        $(stockTitleIdName).append(div);
    }

    function drawMessages() {
        for (var index in messages) {
            if (Number(index) === 0) {
                continue;
            }
            var div = document.createElement('div');
            div.className = 'input-field';
            div.innerText = messages[index];
            $(stockCalculationsIdName).append(div);
        }
    }

    function drawContent() {
        assignHTMLElementIdsDependingOnDeviceLayout();
        drawTitle();
        drawMessages();
    }

    function eraseTitle() {
        $(stockTitleIdName).empty()
    }

    function eraseMessages() {
        $(stockCalculationsIdName).empty()
    }

    function eraseContent() {
        assignHTMLElementIdsDependingOnDeviceLayout();
        eraseTitle();
        eraseMessages();
    }

    return {
        draw: drawContent,
        erase: eraseContent
    };
}

function InputFieldsValidation() {

    var stockIdName = undefined,
        startDateIdName = undefined,
        endDateIdName = undefined,
        shortMaIdName = undefined,
        longMaIdName = undefined,
        rangeIdName = undefined;

    function assignHTMLElementIdsDependingOnDeviceLayout() {
        var isMobileLayout = $('#mobile').is(':visible');

        if (isMobileLayout) {
            stockIdName = '#stock-name-mobile';
            startDateIdName = '#start-date-mobile';
            endDateIdName = '#end-date-mobile';
            shortMaIdName = '#short-ma-mobile';
            longMaIdName = '#long-ma-mobile';
            rangeIdName = '#range';
        }
        else {
            stockIdName = '#stock-name';
            startDateIdName = '#start-date';
            endDateIdName = '#end-date';
            shortMaIdName = '#short-ma';
            longMaIdName = '#long-ma';
            rangeIdName = '#range';
        }
    }

    assignHTMLElementIdsDependingOnDeviceLayout();

    var startDate = stringDateToInteger($(startDateIdName).val()),
        endDate = stringDateToInteger($(endDateIdName).val()),
        longMA = stringToInteger($(longMaIdName).val()),
        shortMA = stringToInteger($(shortMaIdName).val()),
        range = stringToInteger($(rangeIdName).val());

    // Converter from anything to integers if values valid, otherwise returns undefined
    function stringToInteger(num) {
        var initialNumber = Number(num);
        var parsedIntegerNumber = Math.floor(initialNumber);
        if (String(parsedIntegerNumber) === num && String(initialNumber) === num) {
            return parsedIntegerNumber;
        }
        return undefined;
    }

    // Convert date represented as a string to a number of days, otherwise return undefined
    function stringDateToInteger(date) {
        var updatedDate = Date.parse(date);
        if (Number(updatedDate) === updatedDate) {
            // Calculate number of days
            updatedDate = Math.ceil(updatedDate / (1000*3600*24));
            return updatedDate;
        }
        return undefined;
    }

    // Range is bigger or equal than maximum MA entry
    function rangeIsBiggerOrEqualThanMA() {
        var MA = Math.max(shortMA, longMA);
        return MA <= range;
    }

    // Short ma is bigger than long ma
    function shortMAIsBiggerThanLongMA () {
        return shortMA > longMA;
    }

    function shortMAIsSmallerOrEqualThanLongMA () {
        return !shortMAIsBiggerThanLongMA();
    }

    // Range is smaller than data set period
    function rangeIsSmallerThanSetPeriod () {
        return range < (endDate - startDate);
    }

    function validateInputFields () {
        if (shortMAIsSmallerOrEqualThanLongMA() &&
            rangeIsBiggerOrEqualThanMA() &&
            rangeIsSmallerThanSetPeriod()) {
            return true;
        }
        return false;
    }

    return {
        isValid: validateInputFields
    }
}

function ApplicationState() {

    var device = Object.freeze({'MOBILE': 0, 'DESKTOP': 1}),
        deviceStateObject = new DeviceStateManager(),
        deviceState = deviceStateObject.getCurrentState();


    function DeviceStateManager() {

        function getCurrentDeviceState() {
            if ($('#mobile').is(':visible')) {
                return device.MOBILE;
            }
            return device.DESKTOP;
        }

        function updateDeviceState() {
            deviceState = getCurrentDeviceState();
        }

        return {
            getCurrentState: getCurrentDeviceState,
            updateCurrentState: updateDeviceState
        }
    }


    function stateChanged() {
        return deviceState !== deviceStateObject.getCurrentState();
    }

    return {
        stateChanged: stateChanged,
        updateCurrentDeviceState: deviceStateObject.updateCurrentState,
        deviceStatuses: device,
        state: deviceState
    }
}


function InputState() {

    var stockName = undefined,
        startDate = undefined,
        endDate = undefined,
        longMA = undefined,
        shortMA = undefined,
        range = undefined;

    updateState();

    var stockIdName = undefined,
        startDateIdName = undefined,
        endDateIdName = undefined,
        shortMaIdName = undefined,
        longMaIdName = undefined,
        rangeIdName = undefined;

    function assignHTMLElementIdsDependingOnDeviceLayout() {
        var isMobileLayout = $('#mobile').is(':visible');

        if (isMobileLayout) {
            stockIdName = '#stock-name-mobile';
            startDateIdName = '#start-date-mobile';
            endDateIdName = '#end-date-mobile';
            shortMaIdName = '#short-ma-mobile';
            longMaIdName = '#long-ma-mobile';
            rangeIdName = '#range-mobile';
        }
        else {
            stockIdName = '#stock-name';
            startDateIdName = '#start-date';
            endDateIdName = '#end-date';
            shortMaIdName = '#short-ma';
            longMaIdName = '#long-ma';
            rangeIdName = '#range';
        }
    }

    function updateState() {
        assignHTMLElementIdsDependingOnDeviceLayout();
        stockName = $(stockIdName).val();
        startDate = $(startDateIdName).val();
        endDate = $(endDateIdName).val();
        longMA = $(longMaIdName).val();
        shortMA = $(shortMaIdName).val();
        range = $(rangeIdName).val();
    }

    function getState() {
        var object = {
            'stockName': stockName,
            'startDate': startDate,
            'endDate': endDate,
            'longMA': longMA,
            'shortMA': shortMA,
            'range': range
        };
        return object;
    }

    function resetInputFields() {
        assignHTMLElementIdsDependingOnDeviceLayout();
        $(stockIdName).val(stockName);
        $(startDateIdName).val(startDate);
        $(endDateIdName).val(endDate);
        $(longMaIdName).val(longMA);
        $(shortMaIdName).val(shortMA);
        $(rangeIdName).val(range);
    }

    function showFlushMessage() {
        $('.error-message').flash_message({
            text: 'Input is incorrect.',
            how: 'append'
        });
    }

    // TODO: Reset wheels
    function resetState() {
        // Clear output section
        // TODO

        // Reset input values
        resetInputFields();

        // Show flush message
        showFlushMessage();
    }


    var mobileIdNames = ['#stock-name-mobile', '#start-date-mobile',
                         '#end-date-mobile', '#short-ma-mobile',
                         '#long-ma-mobile', '#range-mobile'],
        desktopIdNames = ['#stock-name', '#start-date', '#end-date', '#short-ma', '#long-ma', '#range'];

    function updateMobileToDesktop() {
        for (var i in mobileIdNames) {
            if (mobileIdNames.hasOwnProperty(i) && desktopIdNames.hasOwnProperty(i)) {
                var mobileIdName = mobileIdNames[i],
                    desktopIdName = desktopIdNames[i],
                    mobile = $(mobileIdName),
                    desktop = $(desktopIdName);
                desktop.val(mobile.val());
            }
        }
    }

    function updateDesktopToMobile() {
        for (var i in desktopIdNames) {
            if (desktopIdNames.hasOwnProperty(i) && mobileIdNames.hasOwnProperty(i)) {
                var mobileIdName = mobileIdNames[i],
                    desktopIdName = desktopIdNames[i],
                    mobile = $(mobileIdName),
                    desktop = $(desktopIdName);

                mobile.val(desktop.val());
            }
        }
    }

    return {
        update: updateState,
        get: getState,
        reset: resetState,
        updateMobile: updateDesktopToMobile,
        updateDesktop: updateMobileToDesktop
    }
}

var inputFieldsState = new InputState(),
    applicationState = new ApplicationState();






// NOTE: Solution is used from https://jsfiddle.net/BaylorRae/vwvAd/
(function($) {
  $.fn.flash_message = function(options) {

    options = $.extend({
      text: 'Done',
      time: 1000,
      how: 'before',
      class_name: ''
    }, options);

    return $(this).each(function() {
      if ($(this).parent().find('.flash_message').get(0))
        return;

      var message = $('<span />', {
        'class': 'flash_message ' + options.class_name,
        text: options.text
      }).hide().fadeIn('fast');

      $(this)[options.how](message);

      message.delay(options.time).fadeOut('normal', function() {
        $(this).remove();
      });

    });
  };
})(jQuery);



function drawWheelByEvent(eventName, eventBody) {
    var chanceOfRise = eventBody["chance-of-rise"] === undefined ? 0.0 : parseFloat(eventBody["chance-of-rise"]),
        averageRisePercent = eventBody["average-rise-percent"] === undefined ? 0.0 : parseFloat(eventBody["average-rise-percent"]),
        averageContinuousDays = eventBody["average-continuous-days"] === undefined ? 0.0 : parseFloat(eventBody["average-continuous-days"]);

    var wheelParentDiv = $("#" + eventName),
        wheelMobileParentDiv = $("#mobile-" + eventName),
        classes = ["center-wheels", "progress-circle", (chanceOfRise > 50.0) ? "over50" : "", "p" + Math.round(chanceOfRise)];

    updateWheelParentDiv(wheelParentDiv, classes);
    updateWheelParentDiv(wheelMobileParentDiv, classes);

    var wheelText = $("." + eventName);
    wheelText.text((Math.round(chanceOfRise*10)/10).toFixed(1) + "%");

    var title = 'Chance of rise: ' + chanceOfRise + '%\r\n' +
                'Average rise percent: ' + averageRisePercent + '%\r\n' +
                'Average continuous days: ' + averageContinuousDays + '%';

    wheelText.attr('title', title);
}

function updateWheelParentDiv(wheel, classes) {
    wheel.removeClass();

    for (var i in classes) {
        if (classes.hasOwnProperty(i)) {
            var className = classes[i];
            wheel.addClass(className);
        }
    }
}
