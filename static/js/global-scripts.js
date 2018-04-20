$(document).ready(function() {

  // Display Django Messages in front-end
  if ($('.auth-messages')) {
    /* Clear Error Message after delay
      note: 3rd parameter of the setTimeout function is
      sent as parameter to the internal function at
      end of the timer */
    setTimeout(clearMessage, 3000, '.auth-messages');
  }
  // Clear Messages reusable method
  function clearMessage(message){
    $(message).remove();
  }

  // Disables form buttons on submit and shows a loading spinner
  $('form').submit(function() {
    $("form button[type=submit]").attr("disabled", true).addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter('form button')
  })

  // Disables button and shows a loading spinner on button click
  // Used for some non-form buttons throughout the site, like 'Cancel' and 'Delete'
  $('.btn-spinner').click(function() {
    $(this).addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter(this)
  })
  
  // Show sticky cart icon on screens wider than 700
  if (document.location.href.indexOf('cart') === -1
      && document.location.href.indexOf('checkout') === -1){ 
    if ($(window).width() > 700) {
      $(document).scroll(function () {
        var y = $(this).scrollTop();
        if (y > 500) {
            $('#sticky-cart').fadeIn();
        } else {
            $('#sticky-cart').fadeOut();
        }
      });
    }
  }


  



});
