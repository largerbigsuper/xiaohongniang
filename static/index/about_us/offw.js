/**
 * Created by Administrator on 2016/12/9 0009.
 */
var win_height = $(window).height();
var body_height = $('body').height();
var footer = $('footer').css('height');
$(document).ready(function(){
   var text = $('.yd-offw-join .nav>li.active>a').text();
    $('.yd-offw-navbar-title').html(text);
    $('.yd-offw-join .nav>li').each(function(){
       $(this).on('click',function(){
           $('.yd-offw-navbar-title').html($(this).children().text());
       });
    });

    var win_width = $(window).width();
    var pro_height;
    var myArray = new Array();
    $('.pro .page').each(function(){
        pro_height = parseFloat($(this).children().css('height'));
        myArray.push(pro_height);
    });
    var max = myArray[0];
    var len = myArray.length;
    for (var i = 1; i < len; i++){
        if (myArray[i] > max) {
            max = myArray[i];
        }
    }
    if(win_width>750){
        $('.pro .yd-offw-pro').css({'height':max});
    }else{
        $('.pro .yd-offw-pro').css({'height':''});
    }

    if(body_height<win_height){
        $('footer').css({'position':'fixed','bottom':0});
        $('.yd-offw-main').css({'padding-bottom':footer});
    }else{
        $('footer').css({'position':'','bottom':''});
        $('.yd-offw-main').css({'padding-bottom':''});
    }
    window.onresize = function () {
        var win_height = $(window).height();
        var body_height = $('body').height();
        if(body_height<win_height){
            $('footer').css({'position':'fixed','bottom':0});
            $('.yd-offw-main').css({'padding-bottom':footer});
        }else{
            $('footer').css({'position':'','bottom':''});
            $('.yd-offw-main').css({'padding-bottom':''});
        }

        var win_width = $(window).width();
        var pro_height;
        var youArray = new Array();
        $('.pro .yd-offw-pro').css({'height':''});
        $('.pro .page').each(function(){
            pro_height = parseFloat($(this).children().css('height'));
            youArray.push(pro_height);
        });
        var max = youArray[0];
        var len = youArray.length;
        for (var i = 1; i < len; i++){
            if (youArray[i] > max) {
                max = youArray[i];
            }
        }
        if(win_width>750){
            $('.pro .yd-offw-pro').css({'height':max});
        }else{
            $('.pro .yd-offw-pro').css({'height':''});
        }

    }
});