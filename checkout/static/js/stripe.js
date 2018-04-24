// required by Stripe
// links up django forms to Stripe API

$(document).ready(function() {

  $('#paymentForm').submit(function(event){
    // get user's payment details
    var card = {
      number: $("#id_credit_card_number").val(),
      expMonth: $("#id_expiry_month").val(),
      expYear: $("#id_expiry_year").val(),
      cvc: $("#id_cvv").val()
      }

    // Request a token from Stripe:
    Stripe.card.createToken(card, stripeResponseHandler);

    // Prevent form from being submitted:
    return false;
  });

  function stripeResponseHandler(status, response){
    var form = $('#paymentForm');
    if (response.error){
      // Show the errors on the form
      form.find('#credit-card-errors').show();
      form.find('#stripe-error-message').text(response.error.message);
      // Re-enable submission and remove loader and disabled class
      form.find('button').attr('disabled', false).removeClass('disabled').next('span').remove();
    } 
    else { 
      // Token was created!
      // Get the token ID:
      var token = response.id;
      // Insert the token into the stripe_id field so it can get submitted to the server:
      $("#id_stripe_id").val(token);
      // Prevent the Credit Card Details from being submitted to our server
      $("#id_credit_card_number").removeAttr('name');
      $("#id_cvv").removeAttr('name');
      $("#id_expiry_month").removeAttr('name');
      $("#id_expiry_year").removeAttr('name');
      // Submit the form (use form[0] to avoid re-triggering
      // the initial submit listener and getting into infinite loop):
      form[0].submit();
    }
  }
});
