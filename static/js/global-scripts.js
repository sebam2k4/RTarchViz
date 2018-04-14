(function(){

///////////////////////////////////////
// Display server messages in front-end

if (document.querySelector('.auth-messages')) {
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
})();