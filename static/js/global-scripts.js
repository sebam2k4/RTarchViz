$(document).ready(function() {

  // Add * to required form fields
  $('form input, form select, form textarea').filter('[required]').prev().append('<span> *</span>');
  $('label[for=id_product_file]').after('<span> *</span>');

  // CLear any Django Server Messages after a timeout
  if ($('.flash-messages')) {
    setTimeout(function() {
      $('.flash-messages').fadeOut();
    }, 3500);
  }


  // Disables form buttons on submit and shows a loading spinner
  $('form').not(".add-to-cart-ajax").submit(function() {
    $("form button[type=submit]").attr("disabled", true).addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter('form button[type=submit]');
  })


  // Disables button after clicking it and shows a loading spinner on button click
  // Used for some non-form buttons throughout the site, like 'Cancel' and 'Delete'
  $('.btn-spinner').click(function() {
    $(this).addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter(this);
  })
  

  // Shows sticky cart icon on all pages except 'cart' and 'checkout'
  if (document.location.href.indexOf('cart') === -1 &&
      document.location.href.indexOf('checkout') === -1) {

    $(document).scroll(function () {
      var y = $(this).scrollTop();
      if (y > 500) {
          $('#sticky-cart').fadeIn();
      } else {
          $('#sticky-cart').fadeOut();
      }
    });
  }

});
