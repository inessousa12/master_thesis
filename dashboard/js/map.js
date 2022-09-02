function addMarkerToGroup(group, coordinate, html) {
    var marker = new H.map.Marker(coordinate);

    // add custom data to the marker
    marker.setData(html);
    group.addObject(marker);
}

function addMarkersToMap(map, ui) {

    function ajax_get_all_stations() {
        $.ajax({
            type: "POST",
            url: "../php_includes/get_all_stations.php",
            data: {all: 1,
                res: 1},
            success: function(data) {
                //show success message
                data = $.parseJSON(data);
                var group = new H.map.Group();
    
                map.addObject(group);
                group.addEventListener('tap', function (evt) {
                    // event target is the marker itself, group is a parent event target
                    // for all objects that it contains
                    var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
                        // read custom data
                        content: evt.target.getData()
                    });
        
                    // show info bubble
                    ui.addBubble(bubble);
                }, false);
    
                for (var i = 0; i < data.length; i++) {
                    var network = data[i].name;
                    var latitude = data[i].latitude;
                    var longitude = data[i].longitude;
                    addMarkerToGroup(group, {lat: latitude, lng: longitude},
                        '<div>' + network + '</div>');
                }
            },
            error: function(data) {
                $(".alert-danger").show().delay(2000).fadeOut();
                $(".alert-danger").empty();
                $(".alert-danger").append("<p>Something went wrong, please try again.</p>");
            }
        })
    }

    setInterval(ajax_get_all_stations, 3000);
}

function loadMap() {
    //Step 1: initialize communication with the platform
    var platform = new H.service.Platform({
        apikey: 'LubIVVVaFzHdxeDFZ66yWPxT0gZUpkzMdraQg8LM-AE'
    });

    var defaultLayers = platform.createDefaultLayers();

    //Step 2: initialize a map - this map is centered over Europe
    var map = new H.Map(document.getElementById('map'), defaultLayers.vector.normal.map,{
        center: {lat:38.635643, lng:-9.110037},
        zoom: 14,
    });

    

    // add a resize listener to make sure that the map occupies the whole container
    window.addEventListener('resize', () => map.getViewPort().resize());

    //Step 3: make the map interactive
    // MapEvents enables the event system
    // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
    var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

    // // Create the default UI components
    var ui = H.ui.UI.createDefault(map, defaultLayers);

    addMarkersToMap(map, ui);
}


document.addEventListener('DOMContentLoaded', function() {
    loadMap();
});