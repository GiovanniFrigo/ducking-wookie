/*
 *   View array
 */
var screens = ["location", "date", "people", "menu", "email", "address"];
var lastLocation;

/*
 *  Utilities variables
 */
var monthNames = ["jan", "feb", "mar", "apr", "may", "jun",
  "jul", "aug", "sep", "oct", "nov", "dec"
];

/*
 *  Handle UI views dynamic displaying on screen  
 */
function checkoutEvent() {

    for (var property in booking) {
        if (booking.hasOwnProperty(property)) {
            var input = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", property).val(booking[property]);
            $('#checkout').append($(input));
        }
    }
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
            available_days.length = 0;
            $('#menu-container .menu-row').html("");
        }
        // get menu availabilities from server using the location
        $.getJSON( "http://gourmate.herokuapp.com/protoapi/menu/" + value + "/", function( data ) {
            $.each( data.menus, function( i, item ) {
                // save menus into a variable
                available_menus.push(item);

                // update the ui
                $('#menu-container .menu-row').append("<div class=\"menu-column\"><a class=\"menu-tile-link\" data-menu-id=" + item.id + " id=\"menu-" + item.id + "\"><div><h4>" + item.name + "<\/h4><p>" + item.price_per_person + " €<\/p><\/div><\/div>")
                $('.menu-tile-link').click(function() {
                    setEntry($this.attr("data-menu-id"), "menu")
                });
            });
        });
        // get menu time availabilities from server
        var d = new Date();
        $.getJSON( "http://gourmate.herokuapp.com/protoapi/menu/" + value + "/" + d.getFullYear() + "/" + monthNames[d.getMonth()] + "/", function ( time_data ) {
            // each object represent
            $.each( time_data.calendar, function( i, item ) {
                available_days.push(item);
                // check if menus are available for that day
                var available = false;
                console.log(i);
                console.log(item);
                for (var key in item) {
                    if (item[key] > 0) {
                        available = true;
                        break;
                    }
                }
                if (!available) {
                    $('li.'+i).addClass('disabled');
                }
            });
        });

        // listener to set disabled dates
        $.each(available_days, function(i, item) {
            
        });
    }
    else if (elOriginal == 'people') {
        if (booking.amount != null) {
            booking.amount = parseInt(booking.n_people==""?"2":booking.n_people) * parseInt($(".card.selected").attr("data-menu-price"));
            $("#pay-button").val("Pay " + booking.amount + " $");
        }
    }
    else if (elOriginal == 'date') {
        // clear menu list
        $('#menu-container .menu-row').html("");
        // check if menu is available that day
        $.each(available_menus, function(i, item) {
            var day = booking.day;
            var id = item.id;
            var json = available_days[day - 1];
            console.log(json);
            for (var key in json) {
                if (json[key] > 0 && key == id) {
                    // update the ui
                    $('#menu-container .menu-row').append("<div class=\"menu-column\"><a class=\"menu-tile-link\" id=\"menu-" + key + "\"><div class=\"card\" data-menu-id="+key+" data-menu-price="+item.price_per_person+"><h4>" + item.name + "<\/h4><p>" + item.price_per_person + " €<\/p><\/div><\/div>");
                    $('#menu-'+ key +' :first').css({"background-image": "url("+item.photo+")", "background-size": "100%", "height" : "100%", "background-repeat" : "no-repeat"});  
                    $('.menu-tile-link').click(function() {
                        $('.card').removeClass("selected");
                        $(this).children(":first").addClass("selected");
                        setEntry( $(this).children(":first").attr("data-menu-id"), "menu");
                        booking.amount = parseInt(booking.n_people==""?"2":booking.n_people) * parseInt($(this).children(":first").attr("data-menu-price"));
                        $("#pay-button").val("Pay " + booking.amount + " $");
                    });
                }
            }
        });
    } else if( elOriginal == 'email') {
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        if( re.test(value)==false )
            return;
    }

    // display next step
    if (next_step == screens.length) {
        checkoutEvent();
        $('html, body').scrollTop( $(document).height());
    }
    else {
        $('#' + screens[next_step] + '-container').show();
        $('html, body').scrollTop( $(document).height());
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
        if (booking.place != null) {
            lastLocation = booking.place;
        }
    });
    // hide checkout
    $('#checkout').hide();

});