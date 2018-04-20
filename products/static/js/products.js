

$(document).ready(function(){

  // PRODUCT STAR RATINGS
  $('.stars-inner').each(function() {

    // get average rating for each product
    var avg_rating = $(this).data("average-rating")

    // get percentage
    var starPercentage = ((avg_rating * 2) / 10) * 100

    // round to nearest 10 (used to define star width)
    var starPercentageRounded = String(Math.round(starPercentage / 10) * 10) + '%'

    // set width of stars
    $(this).css('width', starPercentageRounded)
  })

});
