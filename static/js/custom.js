/**
 * Created by Dmytro on 7/18/2017.
 */

$(window).on("load", function () {
    console.log("onload");
    var page = new Page();
    page.update();
});

$(window).resize(function () {
    console.log("resize");
    var page = new Page();
    page.update();
});

$(window).on("orientationchange", function () {
    console.log("onorientationchange");
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
    var verticalCenterButtonText = new VerticalCenterButtonText();
    var isMobileLayout = $('#mobile').is(':visible');

    function updatePage() {
        body.update();
        if (isMobileLayout) {
            inputField.update();
        }
        else {
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
        console.log("Page height", $(window).height(), $(document).height(), MIN_PAGE_HEIGHT);
        console.log(isMobileLayout);
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
        console.log(PAGE_HEIGHT, FOOTER_HEIGHT);
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

function InputField() {
    var centerColumnWidth = $('#mobile').find('.center-column').width()/2,
        inputs = $('.input-mobile');

    function updateInputFieldWidth() {
        inputs.css({'width': centerColumnWidth});
    }

    return {
        update: updateInputFieldWidth
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


$('.btn').on('click touchstart', function() {
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

    function strategy() {
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
        strategy();

        var stock = $(stockIdName).val(),
            start_date = $(startDateIdName).val(),
            end_date = $(endDateIdName).val(),
            short_ma = $(shortMaIdName).val(),
            long_ma = $(longMaIdName).val(),
            range = $(rangeIdName).val();

        console.log("Before ajax request");

        $.ajax({
            url: '/calculate',
            type: 'GET',
            data: {
                stock: stock,
                start_date: start_date,
                end_date: end_date,
                short_ma: short_ma,
                long_ma: long_ma,
                range: range
            },
            success: function (response) {
                console.log("response");
                var response_object = JSON.parse(response);
                var message = response_object["message"];
                var messages = message.split("\n"),
                    title = messages[0];

                var outputDrawer = new OutputDrawer({title: title, messages: messages});
                outputDrawer.draw();
            },
            error: function (response) {
                var outputDrawer = new OutputDrawer({title: "", messages: ""});
                outputDrawer.draw();

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

    function strategy() {
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
        div.className = 'text-field';
        div.innerText = title;
        $(stockTitleIdName).append(div);
    }

    function drawMessages() {
        for (var index in messages) {
            if (Number(index) === 0) {
                continue;
            }
            var div = document.createElement('div');
            div.className = 'text-field';
            div.innerText = messages[index];
            $(stockCalculationsIdName).append(div);
        }
    }

    function drawContent() {
        strategy();
        eraseContent();
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
        eraseTitle();
        eraseMessages();
    }

    return {
        draw: drawContent
    };
}
