/*
 *   View array
 */
var screens = ["location", "time", "people", "menu"];//"allergies", "menu"]; 
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
        if (lastLocation != value && lastLocation != null) {
            hideAllViewsFromIndex(screens.indexOf(elOriginal) + 1);
            // clear menu list
            available_menus.length = 0;
            $('#menu-container .menu-row').html("");
        }
        // get availabilities from server using the location
        $.getJSON( "http://gourmate.herokuapp.com/protoapi/menu/" + value + "/", function( data ) {
            $.each( data.menus, function( i, item ) {
                // save menus into a variable
                available_menus.push(item);
                // update the ui
                $('#menu-container .menu-row').append("<div class=\"menu-column\"><a class=\"menu-tile\" id=\"menu-" + item.id + "\"><div><h4>" + item.name + "<\/h4><p>" + item.price_per_person + " €<\/p><\/div><\/div>")
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