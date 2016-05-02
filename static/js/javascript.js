/**
 * Created by olof.olivecrona on 2015-10-28.
 */
$(document).ready(function(){
    var w=$(window).width()-300;
    var s;
    switch (true){
        case $(window).width()<=767-17:
            s="70%";
            break;
        case w>=1090:
            s=1090;
            break;
        case w>=820:
            s=820;
            break;
        case w>=550:
            s=550;
            break;
        case w>=280:
            s=280;
            break;
    }
    $("section").css("width", s);
    $(window).resize(function(){
        var w=$(window).width()-300;
        var s;
        switch (true){
            case $(window).width()<=767-17:
                s="70%";
                break;
            case w>=1090:
                s=1090;
                break;
            case w>=820:
                s=820;
                break;
            case w>=550:
                s=550;
                break;
            case w>=280:
                s=280;
                break;
        }
        $("section").css("width", s);
    });


    //The settings menu button
    var v=$(window).width();
    if(v>767-17){
        var width = 300;
    }
    else if(v<=767-17){
        var width = '70%';
    }
    $(window).resize(function(){
        var v=$(window).width();
        if(v>767-17){
            width = 300;
        }
        else if(v<=767-17){
            width = '70%';
        }
    });


    counter=0;
    $("#h_settings").click(function(){
        console.log("counter = "+counter);
        if (counter<=0){
            $(".settings_menu_ul").toggle();
            $(".settings_menu_li").toggle();
            $(".h_settings_img").toggleClass("rotate");
            $("#settings_menu").animate({width:width},500, function() {
                counter++;
            })
        }
        else if (counter>=1) {
            $(".h_settings_img").toggleClass("rotate");
            $("#settings_menu").animate({width:0},500, function(){
                counter--;
                $(".settings_menu_ul").toggle();
                $(".settings_menu_li").toggle();
            })
        }
    });

    //The change theme button
    $("#change_theme").click(function(){
            $('#theme_form').submit();
    });

    //Logout button
    $("h_logOut").click(function(){
    });

});