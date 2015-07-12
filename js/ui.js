/*
 *   View array
 */
var screens = ["location", "time", "people", "allergies", "menu"]; 
var lastLocation;

/*
 *  Handle UI views dynamic displaying on screen  
 */
function checkoutEvent() {
    replaceScreen('checkout');
}

/*
 *  Set booking entry
 */
function setEntry(value, elOriginal) {
    // set the params
    addParamToBooking(value, elOriginal);

    if (elOriginal == 'location') {
        // check if the user has set a different during the form input location from the previous one -> restart the form
        if (lastLocation != value && lastLocation != null)
            hideAllViewsFromIndex(screens.indexOf(elOriginal) + 1);
        // get availabilities from server using the location
        $.getJSON( "http://gourmate.herokuapp.com/protoapi/menu/Treviso/", function( data ) {
          var items = [];
          $.each( data, function( key, val ) {
            //items.push( "<li id='" + key + "'>" + val + "</li>" );
          });
        });
    }

    // display next step
    $('#' + screens[screens.indexOf(elOriginal) + 1] + '-container').show();
}

function hideAllViewsFromIndex(idx) {
    for (var i = screens.length - 1; i >= idx; i--) {
        $('#' + screens[i] + '-container').hide();
    };
}

/*
 *   Handle the routing of views
 */
$(document).ready(function() {
    // hide all forms elements
    $('.form-part').hide();
    // show location form
    $('#location-container').show();
    //put listener to dropdown menus
    $('#location-container').mousedown(function() {
        if (booking.location != null) {
            lastLocation = booking.location;
        }
    });
});