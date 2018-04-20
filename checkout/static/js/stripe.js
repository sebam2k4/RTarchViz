// required by Stripe
// links up django forms to Stripe API

$(document).ready(function() {
  $("#paymentForm").submit(function() {
    var form = this;
    var card = {
      number: $("#id_credit_card_number").val(),
      expMonth: $("#id_expiry_month").val(),
      expYear: $("#id_expiry_year").val(),
      cvc: $("#id_cvv").val()
    };

    // disable 'make payment' button to prevent submitng card details again
    // while waiting for Stripe to assign a token/id
    

    Stripe.createToken(card, function(status, response) {
      if (status === 200) {
        console.log(status, response);
        $("#credit-card-errors").hide();
        $("#id_stripe_id").val(response.id);

        //Prevent the Credit Card Details from being submitted to our server
        $("#id_credit_card_number").removeAttr('name');
        $("#id_cvv").removeAttr('name');
        $("#id_expiry_month").removeAttr('name')
        $("#id_expiry_year").removeAttr('name')

        form.submit();

      } else {
        // error message that will come back from Stripe
        // ids are given from Stripe API (required)
        $("#stripe-error-message").text(response.error.message);
        $("#credit-card-error").show();
        $("#validate_card_btn").removeClass("disabled");
      }
    });
    return false;
  });
});
