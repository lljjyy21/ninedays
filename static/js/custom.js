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
