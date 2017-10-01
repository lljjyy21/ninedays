/**
 * Created by Dmytro on 7/18/2017.
 */

$(window).on("load", function () {
    //console.log("onload");
    var page = new Page();
    page.update();
});

$(window).resize(function () {
    //console.log("resize");
    var page = new Page();
    page.update();
});

$(window).on("orientationchange", function () {
    //console.log("onorientationchange");
    var page = new Page();
    page.update();
});

$(document).bind("ajaxSend", function(){

}).bind("ajaxStop", function(){
    var page = new Page();
    page.update();
});

function Page() {
    var body = new Body();
    var footer = new Footer();
    var inputField = new InputField();
    var scrollArrow = new ScrollArrow();
    var verticalCenterButtonText = new VerticalCenterButtonText();
    var isMobileLayout = $('#mobile').is(':visible');

    function updatePage() {
        body.update();
        if (isMobileLayout) {
            inputField.update();
        }
        else {
            inputField.update();
            scrollArrow.update();
            footer.update();
            verticalCenterButtonText.update();
        }
    }

    return {
        update: updatePage
    };
}

function Body() {
    var FOOTER_HEIGHT = 100, MIN_PAGE_HEIGHT = 650;
    var PAGE_HEIGHT = Math.max(MIN_PAGE_HEIGHT, $(window).height()) - FOOTER_HEIGHT;
    var isMobileLayout = $('#mobile').is(':visible');
    calculatePageHeight();

    function calculatePageHeight() {
        //console.log("Page height", $(window).height(), $(document).height(), MIN_PAGE_HEIGHT);
        //console.log(isMobileLayout);
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
        //console.log(PAGE_HEIGHT, FOOTER_HEIGHT);
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

// Calculate width of text from DOM element or string. By Phil Freo <http://philfreo.com>
$.fn.textWidth = function(text, font) {
    if (!$.fn.textWidth.fakeEl) $.fn.textWidth.fakeEl = $('<span>').hide().appendTo(document.body);
    $.fn.textWidth.fakeEl.text(text || this.val() || this.text()).css('font', font || this.css('font'));
    return $.fn.textWidth.fakeEl.width();
};

function InputField() {
    var centerColumnWidth = $('#mobile').find('.center-column').width()/2,
        inputs = $('.input-mobile');

    function updateInputFieldWidth() {
        inputs.css({'width': centerColumnWidth});
    }

    function updateInputDateAlignment() {
        var inputDate = $('.input-date'),
            isMobileLayout = $('#mobile').is(':visible');

        var span = $("span").val(inputDate.first().val());
        //var textWidth = $.fn.textWidth(inputDate.first().text(), 14);
        console.warn("input date", inputDate.first().outerWidth);
        console.warn("input date text", inputDate.first().val());

        console.warn("Input width", span.width(), span);
        //console.warn("Text width", textWidth);

        if (isMobileLayout) {
            inputDate.css('padding-left', "6%");
        }
        else {
            inputDate.css('text-align', 'left');
            inputDate.css('padding-left', );
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

        //console.log("Before ajax request");


        //TODO: Test
        var inputFieldsValidation = new InputFieldsValidation();
        var isValidInput = inputFieldsValidation.isValid();

        if (isValidInput) {
            state.update();
            var stateObject = state.get();
        }
        else {
            state.reset();
            return;
        }

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
                //console.log("response");
                var response_object = JSON.parse(response);
                var message = response_object["message"];
                var messages = message.split("\n"),
                    title = messages[0];

                var outputDrawer = new OutputDrawer({title: title, messages: messages});
                outputDrawer.erase();
                outputDrawer.draw();
            },
            error: function (response) {
                var outputDrawer = new OutputDrawer({title: "", messages: ""});
                outputDrawer.erase();

                console.error(response);
            }
        });
    }

    return {
        getAndDrawCalculations: getAndDrawCalculations
    };
}


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

    // TODO: Theoretically, this function is redundant
    function rangeIsBiggerOrEqualThanPeriod () {
        return !rangeIsSmallerThanSetPeriod();
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

    function resetState() {
        // Clear output section
        var outputDrawer = new OutputDrawer({});
        outputDrawer.erase();

        // Reset input values
        resetInputFields();

        // Show flush message
        showFlushMessage();
    }

    return {
        update: updateState,
        get: getState,
        reset: resetState
    }
}

var state = new InputState();


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
