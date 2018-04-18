$(document).ready(function() {

  ///////////////////////////////////////
  // Display server messages in front-end

  if ($('.auth-messages')) {
    /* Clear Error Message after delay
      note: 3rd parameter of the setTimeout function is
      sent as parameter to the internal function at
      end of the timer */
    setTimeout(clearMessage, 3000, '.auth-messages');
  }
    
  // Clear Messages reusable method
  function clearMessage(message){
    document.querySelector(message).remove();
  }

  // Disables form buttons on submit and shows a loading spinner
  $('form').submit(function() {
    $("form button").addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter('form button')
    // $("form button").append('<i></i>').addClass('fas fa-circle-notch fa-spin')
  })

  // Disables button and shows a loading spinner on button click
  // Used for some non-form buttons throughout the site, like 'Cancel' and 'Delete'
  $('.btn-spinner').click(function() {
    $(this).addClass("disabled");
    $("<span class='ml-1 spinner'><i class='fas fa-circle-notch fa-spin'</span></i>").insertAfter(this)
    // $("form button").append('<i></i>').addClass('fas fa-circle-notch fa-spin')
  })

});
