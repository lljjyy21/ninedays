/**
 * Created by Dmytro on 7/18/2017.
 */

$ = jQuery;

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
        if (applicationState.stateHasChanged()) {
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
    // 882 is the minimal size of the screen when footer doesn't overlap with progress wheels
    var FOOTER_HEIGHT = 100, MIN_PAGE_HEIGHT = 882;
    var PAGE_HEIGHT = Math.max(MIN_PAGE_HEIGHT, $(window).height()) - FOOTER_HEIGHT;
    var isMobileLayout = $('#mobile').is(':visible');
    calculatePageHeight();

    function calculatePageHeight() {

        var mobileBody = $('#mobile'),
            desktopBody = $('#desktop');
        var classes = ['container-fluid'], hiddenClass = 'hidden';
        if ($(window).height() < MIN_PAGE_HEIGHT) {
            mobileBody.removeClass();
            mobileBody.add(classes);
            desktopBody.addClass(hiddenClass);
            isMobileLayout = true;
        }
        else if ($(window).height() >= MIN_PAGE_HEIGHT && isMobileLayout) {
            desktopBody.removeClass();
            mobileBody.addClass(hiddenClass);
            isMobileLayout = false;
        }

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
    var mobileCenterColumnWidth = $('#mobile').find('.center-column').width()/2,
        desktopCenterColumnWidth = $('#desktop').find('.center-column').width()*2/3,
        mobileInputs = $('.input-mobile'),
        desktopInputs = $('.input-desktop');

    function updateInputFieldWidth() {
        mobileInputs.css({'width': mobileCenterColumnWidth});
        desktopInputs.css({'width': desktopCenterColumnWidth});
    }

    function updateInputField() {
        updateInputFieldWidth();
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
            error: function (error) {
                inputFieldsState.reset();

                for (var index in EVENT_NAMES) {
                    if (EVENT_NAMES.hasOwnProperty(index)) {
                        cleanWheel(EVENT_NAMES[index]);
                    }
                }
            }
        });
    }

    return {
        getAndDrawCalculations: getAndDrawCalculations
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
        stateHasChanged: stateChanged,
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
        var object;
        object = {
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
        var error_message = $('.error-message');
        error_message.css('visibility', 'hidden');
        error_message.flash_message({
            text: 'Input is incorrect.',
            how: 'append'
        });
        error_message.css('visibility', 'visible');
    }

    function resetState() {
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
    var eventWasTriggeredYesterday = eventBody['event-was-triggered'] === undefined ? "Unknown" : eventBody['event-was-triggered'],
        description = eventBody['description'] === undefined ? "": eventBody['description'],
        chanceOfRise = eventBody["chance-of-rise"] === undefined ? 0.0 : parseFloat(eventBody["chance-of-rise"]),
        averageContinuousDays = eventBody["average-continuous-days"] === undefined ? 0.0 : parseFloat(eventBody["average-continuous-days"]);

    var wheelParentDiv = $("#" + eventName),
        wheelMobileParentDiv = $("#mobile-" + eventName),
        classes = ["center-wheels", "progress-circle", (chanceOfRise > 50.0) ? "over50" : "", "p" + Math.round(chanceOfRise)];

    updateWheelParentDiv(wheelParentDiv, classes);
    updateWheelParentDiv(wheelMobileParentDiv, classes);

    var wheelText = $("." + eventName);
    wheelText.text((Math.round(chanceOfRise*10)/10).toFixed(1) + "%");

    var tooltipDesktopDiv = wheelParentDiv.find('.' + eventName),
        tooltipMobileDiv = wheelMobileParentDiv.find('.' + eventName);
    var newLine = '<br>',
        title = 'Description: ' + description + newLine +
                'Event triggered, ' + eventWasTriggeredYesterday + newLine +
                'Chance of rise, ' + chanceOfRise + '%' + newLine +
                'Average continuous days, ' + averageContinuousDays;

    tooltipDesktopDiv.attr('title', title);
    tooltipMobileDiv.attr('title', title);
}

function cleanWheel(eventName) {
    var eventWheelClass = $('.' + eventName),
        eventWheelParentDiv = $('#' + eventName),
        eventWheelMobileParentDiv = $('#mobile-' + eventName),
        classes = ["center-wheels", "progress-circle", "p0"];
    eventWheelClass.attr('title', '');
    eventWheelClass.text('0%');
    updateWheelParentDiv(eventWheelParentDiv, classes);
    updateWheelParentDiv(eventWheelMobileParentDiv, classes);
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


// Tooltip for mobile device
$( function()
{
    var targets = $( '[rel~=tooltip]' ),
        target  = false,
        tooltip = false;

    targets.bind( 'mouseenter', function()
    {
        target  = $( this );
        var tip = target.attr('title');
        tooltip = $( '<div id="tooltip"></div>' );

        if( !tip || tip === '' )
            return false;

        target.removeAttr( 'title' );
        tooltip.css( 'opacity', 0 )
               .html( tip )
               .appendTo( 'body' );

        var init_tooltip = function()
        {
            if( $( window ).width() < tooltip.outerWidth() * 1.5 )
                tooltip.css( 'max-width', $( window ).width() / 2 );
            else
                tooltip.css( 'max-width', 340 );

            var pos_left = target.offset().left + ( target.outerWidth() / 2 ) - ( tooltip.outerWidth() / 2 ),
                pos_top = target.offset().top - tooltip.outerHeight() - 20;

            if( pos_left < 0 )
            {
                pos_left = target.offset().left + target.outerWidth() / 2 - 20;
                tooltip.addClass( 'left' );
            }
            else
                tooltip.removeClass( 'left' );

            if( pos_left + tooltip.outerWidth() > $( window ).width() )
            {
                pos_left = target.offset().left - tooltip.outerWidth() + target.outerWidth() / 2 + 20;
                tooltip.addClass( 'right' );
            }
            else
                tooltip.removeClass( 'right' );

            if( pos_top < 0 || pos_top < $(window).height() )
            {
                pos_top = target.offset().top + target.outerHeight();
                tooltip.addClass( 'top' );
            }
            else
                tooltip.removeClass( 'top' );

            tooltip.css( { left: pos_left, top: pos_top } )
                   .animate( { top: '+=10', opacity: 1 }, 50 );
        };

        init_tooltip();
        $( window ).resize( init_tooltip );

        var remove_tooltip = function()
        {
            tooltip.animate( { top: '-=10', opacity: 0 }, 50, function()
            {
                $( this ).remove();
            });

            target.attr( 'title', tip );
        };

        target.bind( 'mouseleave', remove_tooltip );
        tooltip.bind( 'click', remove_tooltip );
    });
});
