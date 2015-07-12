/*
 *   View array
 */
var screens = ["location", "time", "people", "menu"];//"allergies", "menu"]; 
var lastLocation;

/*
 *  Handle UI views dynamic displaying on screen  
 */
function checkoutEvent() {
    $('#checkout').show();
}

/*
 *  Set booking entry
 */
function setEntry(value, elOriginal) {
    // set the params
    addParamToBooking(value, elOriginal);
    // set next step index
    var next_step = screens.indexOf(elOriginal) + 1;

    if (elOriginal == 'location') {
        // check if the user has set a different during the form input location from the previous one -> restart the form
        if (lastLocation != value && lastLocation != null) {
            hideAllViewsFromIndex(next_step);
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
                $('#menu-container .menu-row').append("<div class=\"menu-column\"><a class=\"menu-tile-link\" id=\"menu-" + item.id + "\"><div><h4>" + item.name + "<\/h4><p>" + item.price_per_person + " €<\/p><\/div><\/div>")
                $('.menu-tile-link').click(function() {
                    booking.menu_id = this.id;
                    checkoutEvent();
                    self.location = "#checkout";
                });
            });

        });
    }

    // display next step
    if (next_step == screens.length) {
        checkoutEvent();
    }
    else {
        $('#' + screens[next_step] + '-container').show();
    }
}

function hideAllViewsFromIndex(idx) {
    // hide all the screens from idx on
    for (var i = screens.length - 1; i >= idx; i--) {
        $('#' + screens[i] + '-container').hide();
    };
    // also hide the checkout
    $('#checkout').hide();
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
    // hide checkout
    $('#checkout').hide();
});