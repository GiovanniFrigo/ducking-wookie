/*
*   View array
*/
var screens = ["location", "time", "people", "allergies", "menu"]; 

/*
*   Handle UI views dynamic loading on screen  
*/
function load_frame_callback(screenName, container_id, on_complete) {
    $.get(("screens/" + screenName + ".html"), function (data){
          $(container_id).html(data).ready(on_complete());
    });
}

function load_frame(screenName, container_id) {
    $.get(("screens/" + screenName + ".html"), function (data){
          $(container_id).html(data);
    });
}

function replaceScreen(screenName, on_complete) {
    if (arguments.length == 1)
        load_frame(screenName, "#pageContent" );
    else if (arguments.length == 2)
        load_frame_callback(screenName, "#pageContent", on_complete );
}

function checkoutEvent() {
    replaceScreen("checkout");
}

function setEntry(value, elOriginal) {
    addParamToBooking(value, elOriginal);
}

/**
*   Handle the routing of views
*/
$(document).ready(function() {
    // location listener    
    $(document).on("#locationInput", 'change', function() {
        // attach location dropdown listener
        //addParamToBooking(booking, form_i, $( sender.target ).val());
        //shrink current view
        console.log("roncade");
        // go to next screen
        form_i++;
    });
});