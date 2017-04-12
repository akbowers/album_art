(function($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a:not(.dropdown-toggle)').click(function() {
        $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Initialize and Configure Scroll Reveal Animation
    window.sr = ScrollReveal();
    sr.reveal('.sr-icons', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 200);
    sr.reveal('.sr-button', {
        duration: 1000,
        delay: 200
    });
    sr.reveal('.sr-contact', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 300);

    // Initialize and Configure Magnific Popup Lightbox Plugin
    // $('.popup-gallery').magnificPopup({
    //     delegate: 'a',
    //     type: 'image',
    //     tLoading: 'Loading image #%curr%...',
    //     mainClass: 'mfp-img-mobile',
    //     gallery: {
    //         enabled: true,
    //         navigateByImgClick: true,
    //         preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
    //     },
    //     image: {
    //         tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    //     }
    // });

    //Make Pop-ups separate
    // var groups = {};
    // $('.galleryItem').each(function() {
    //   var id = parseInt($(this).attr('data-group'), 10);
    //
    //   if(!groups[id]) {
    //     groups[id] = [];
    //   }
    //
    //   groups[id].push( this );
    // });
    //
    //
    // $.each(groups, function() {
    //
    //   $(this).magnificPopup({
    //       type: 'image',
    //       tLoading: 'Loading image #%curr%...',
    //       mainClass: 'mfp-img-mobile',
    //       closeOnContentClick: true,
    //       closeBtnInside: false,
    //       gallery: {
    //           enabled: true,
    //           navigateByImgClick: true,
    //           preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
    //       },
    //       image: {
    //           tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    //       }
    //   });


//STRAIGHT FROM WEBSITE!!

    var groups = {};
    $('.galleryItem').each(function() {
      var id = parseInt($(this).attr('data-group'), 10);

      if(!groups[id]) {
        groups[id] = [];
      }

      groups[id].push( this );
    });


    $.each(groups, function() {

      $(this).magnificPopup({
          type: 'image',
          closeOnContentClick: true,
          closeBtnInside: false,
          gallery: { enabled:true }
      })

    });

    $('#open-popup').magnificPopup({
    items: [
      {
        src: '#my-popup', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup2', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup3', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup4', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup5', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup6', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup7', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup8', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup9', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup10', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup11', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      },
      {
        src: '#my-popup12', // CSS selector of an element on page that should be used as a popup
        type: 'inline'
      }
    ],
    gallery: {
      enabled: true
    },
    type: 'image' // this is a default type
});





    //    delegate: 'a',
   //     type: 'image',
   //     tLoading: 'Loading image #%curr%...',
   //     mainClass: 'mfp-img-mobile',
   //     gallery: {
   //         enabled: true,
   //         navigateByImgClick: true,
   //         preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
   //     },
   //     image: {
   //         tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
   //     }
   // });


    //Star rating
    $(document).ready(function(){
    //  Check Radio-box
        $(".rating input:radio").attr("checked", false);
        $('.rating input').click(function () {
            $(".rating span").removeClass('checked');
            $(this).parent().addClass('checked');
        });

        $('input:radio').change(
        function(){
            var userRating = this.value;
        });
    });


})(jQuery); // End of use strict
