$(document).ready(function() {

  // AJAX ADD TO CART

  // get add to cart form
  var addToCartform = $('.add-to-cart-ajax')
  // initialize timer for clearing messages with timeout
  var timer 

  addToCartform.submit(function(event) {
    event.preventDefault()
    var thisForm = $(this) // hold on to reference of 'this' for ajax
    var actionEndpoint = thisForm.attr('action');
    var httpMethod = thisForm.attr('method');
    var formData = thisForm.serialize();
    var ajaxRequest = $.ajax({
      url: actionEndpoint,
      type: httpMethod,
      dataType: 'json',
      data: formData,
    })

    ajaxRequest.always(function(data) {
      // clear any ajax messages
      clearTimeout(timer)
      var ajaxMessage = $('.ajax-messages');
      ajaxMessage.hide()
    })

    ajaxRequest.done(function(data) {
      var formSubmitButton = thisForm.find('.submit-button');

      if (data.added) {  // successfully added item to cart
        
        // change submit button
        formSubmitButton.html("<a href='#' class='btn btn-primary btn-lg btn-block disabled'>Already in Cart</a>");
        // update navbar and sticky cart items count
        var navbarCartCount = $('.navbar-cart-count');
        navbarCartCount.text(data.cartItemsCount);
        var stickyCartCount = $('.sticky-cart-count');
        stickyCartCount.text(data.cartItemsCount);
        // display success messages from view's response
        var ajaxMessage = $('.ajax-messages');
        ajaxMessage.html(
          "<ul class='list-unstyled alert-link'>"
          + "<li class='alert alert-success py-4'>"
          + data.message
          + "</li>"
          + "</ul>"
        ).fadeIn();
        // set timer to clear message
        timer = setTimeout(function() {
          ajaxMessage.fadeOut()}, 3500);

      } else {  // did not add item to cart
        // display error message from view's response
        var ajaxMessage = $('.ajax-messages');
        ajaxMessage.hide();
        ajaxMessage.html(
          "<ul class='list-unstyled alert-link'>"
          + "<li class='alert alert-danger py-4'>"
          + data.message
          + "</li>"
          + "</ul>"
        ).fadeIn();
        // set timer to clear message
        timer = setTimeout(function() {
          ajaxMessage.fadeOut()}, 3500);
      }
    })

    ajaxRequest.fail(function(jqHR, textStatus) {
      // display request error
      ajaxMessage.html(
        "<ul class='list-unstyled alert-link'>"
        + "<li class='alert alert-danger py-4'>"
        + "Error occured"
        + textStatus
        + "</li>"
        + "</ul>"
      ).fadeIn();
    })
  })

});
