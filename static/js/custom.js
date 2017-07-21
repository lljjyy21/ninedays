/**
 * Created by Dmytro on 7/18/2017.
 */

$(document).ready( function () {
        $('.container').css('height', $(document).height());
        $('.vertical-text').css('margin-left', ($('.logo-field').width()/2 - $('.letter').width()/2) + "px" );
        console.log("width", $(document).width());
        console.log("height", $(document).height());
    }
);

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
