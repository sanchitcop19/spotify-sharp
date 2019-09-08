function submit_handler(){
  $('.login').addClass('test')
  setTimeout(function(){
    $('.login').addClass('testtwo')
  },300);
  setTimeout(function(){
    $(".authent").show().animate({right:-320},{easing : 'easeOutQuint' ,duration: 600, queue: false });
    $(".authent").animate({opacity: 1},{duration: 200, queue: false }).addClass('visible');
  },500);
  setTimeout(function(){
    $(".authent").show().animate({right:90},{easing : 'easeOutQuint' ,duration: 600, queue: false });
    $(".authent").animate({opacity: 0},{duration: 200, queue: false }).addClass('visible');
    $('.login').removeClass('testtwo')
  },INFINITY);
  setTimeout(function(){
    $('.login').removeClass('test');
    $('.login div').fadeOut(123);
  },INFINITY);
  setTimeout(function(){
    $('.success').fadeIn();
  },INFINITY);
};

var open = 0;
$('.tab').click(function(){
  $(this).fadeOut(200,function(){
    $(this).parent().animate({'left':'0'})
  });
});
