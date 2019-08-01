  (function ($) {
 	"use strict";
 	/*----------------------------------------
 	        Slider Plugin about
 	  ----------------------------------------*/

 	$('.about-slider ').owlCarousel({
 		loop: true,
 		margin: 20,
 		nav: true,
 		navText: ["<i class='fas fa-angle-left'></i>", "<i class='fas fa-angle-right'></i>"],
 		responsive: {
 			0: {
 				items: 1
 			},
 			600: {
 				items: 2
 			},
 			1000: {
 				items: 3
 			}
 		}
 	});

 	/*----------------------------------------
 	       Video Plugin
 	   ----------------------------------------*/

 	var $iframe = $('iframe'),
 		$videoLink = $('.video-link'),
 		playerTemplate =
 		'<div class="player"><div class="player__video"><div class="video-filler"></div><button class="video-close">&times;</button><iframe class="video-iframe" src="{{iframevideo}}" frameborder="0" allowfullscreen></iframe></div><div/>';

 	$videoLink.on('click', function (e) {
 		var localTemplate = '',
 			videoWidth = parseInt($(this).data('width')),
 			videoHeight = parseInt($(this).data('height')),
 			videoAspect = (videoHeight / videoWidth) * 100,
 			// elements
 			$player = null,
 			$video = null,
 			$close = null,
 			$iframe = null;

 		e.preventDefault();

 		localTemplate = playerTemplate.replace(
 			'{{iframevideo}}',
 			$(this).prop('href')
 		);

 		$player = $(localTemplate);

 		$player.find('.video-filler').css('padding-top', videoAspect + '%');

 		$close = $player.find('.video-close').on('click', function () {
 			$(this)
 				.off()
 				.closest('.player')
 				.hide()
 				.remove();
 		});

 		$player.appendTo('body').addClass('js--show-video');
 	});


 	/*----------------------------------------
 	          Slider Plugin our work
 	  ----------------------------------------*/
	  	$('.port').owlCarousel({
 		loop: true,
 		margin: 10,
 		nav: true,
 		navText: ["<i class='fas fa-angle-left'></i>", "<i class='fas fa-angle-right'></i>"],
 		responsive: {
 			0: {
 				items: 2
 			},
 			600: {
 				items: 2
 			},
 			992: {
 				items: 3
 			}
 		}
 	});
 	/*-------------------------------------
 			Navbar scrool
 	----------------------------------------*/

 	$(function () {
 		$(window).on('scroll', function () {
 			if ($(this).scrollTop() < 50) {
 				$('.navbar').removeClass('norma-nav');
 			} else {
 				$('.navbar').addClass('norma-nav');
				
 			}
 		});
 	});


 	/*-----------------------------------------
 				wow active
 	------------------------------------------*/

 	$(function () {
 		new WOW().init();
 	});

 	/*===========================================
			MAGNIFIC POPUP
=============================================*/	 
	 $(function () {
	$(".port").magnificPopup({
		delegate: 'a',
		type: 'image',
		gallery: {
			enabled: true
		}
	});

});

 	/*----------------------------------------
 	          Preloader
 	 ----------------------------------------*/

 	$(window).on('load', function () {
 		$('#status').fadeOut();
 		$('#preloader').delay(350).fadeOut('slow');
 	});
	 
	 
	  /*----------------------------------------
            CONTACT FORM
        ----------------------------------------*/

    //cut


 })(jQuery);
