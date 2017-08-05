/**
 * Created by Dmytro on 7/18/2017.
 */

$(document).ready( function () {
    var page = new Page();
    page.update();
});

$(window).resize(function() {
    var page = new Page();
    page.update();
});

function Page() {
    var body = new Body();
    var footer = new Footer();


    function updatePage() {
        body.update();
        footer.update();
    }

    return {
        update: updatePage
    };
}

function Body() {
    var FOOTER_HEIGHT = 100, MIN_PAGE_HEIGHT = 600;
    var PAGE_HEIGHT = Math.max(MIN_PAGE_HEIGHT, $(document).height()) - FOOTER_HEIGHT;

    function updateBodyHeight() {
        $('.container').css('height', PAGE_HEIGHT);
    }

    function updateFooterHeight() {
        // NOTE: -1px required to remove unnecessary scroll-bar on the page.
        $('.footer').css('height', FOOTER_HEIGHT - 1);
    }

    function updateHeight() {
        updateBodyHeight();
        updateFooterHeight();
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


$(function () {
    $('#btn').click(function () {
            var stock = $('#stock_name').val(),
                start_date = $('#start_date').val(),
                end_date = $('#end_date').val(),
                short_ma = $('#short_ma').val(),
                long_ma = $('#long_ma').val(),
                range = $('#range').val();

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
                    var response_object = JSON.parse(response);
                    var message = response_object["message"];
                    var messages = message.split("\n");

                    eraseTitle();
                    eraseMessages();

                    var title = messages[0];
                    drawTitle(title);
                    drawMessages(messages);
                },
                error: function (response) {
                    eraseTitle();
                    eraseMessages();
                    console.error(response);
                }
            });
        }
    );
});


function eraseTitle() {
    $('#stock-title').empty()
}

function eraseMessages() {
    $('#stock-calculation').empty()
}

function drawTitle(title) {
    var div = document.createElement('div');
    div.className = 'text-field';
    div.innerText = title;
    $('#stock-title').append(div);
}

function drawMessages(messages) {
    for (var index in messages) {
        if (Number(index) === 0) continue;
        var div = document.createElement('div');
        div.className = 'text-field';
        div.innerText = messages[index];
        $('#stock-calculation').append(div);
    }
}
