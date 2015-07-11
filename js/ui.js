/*
*   View array
*/
var screens = ["location", "time", "people", "maxprice", "allergies", "menu"]; 

/*
*   Handle UI views dynamic loading on screen  
*/
function load_frame_callback(page, container_id, on_complete) {
    $.get(page, function (data){
          $(container_id).html(data).ready(on_complete());
    });
}

function load_frame(page, container_id) {
    $.get(page, function (data){
          $(container_id).html(data);
    });
}

function replaceScreen(screenName, on_complete) {
    if (arguments.length == 1)
        load_frame( "screens/" + screenName + ".html", "#pageContent" );
    else if (arguments.length == 2)
        load_frame_callback( "screens/" + screenName + ".html", "#pageContent", on_complete );
}

function checkoutEvent() {
    replaceScreen("checkout");
}