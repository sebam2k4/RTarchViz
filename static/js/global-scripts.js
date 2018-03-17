if (document.querySelector('.auth-messages')) {
  // Clear Error Message after delay
  console.log("messages div found")
  // 3rd parameter of the setTimeout function is
  // sent as parameter to the internal function at
  // end of the timer
  setTimeout(clearMessage, 3000, '.auth-messages')
  }
  
// Clear Messages
function clearMessage(message){
  document.querySelector(message).remove();
}// Clear Messages
function clearMessage(message){
  document.querySelector(message).remove();
}