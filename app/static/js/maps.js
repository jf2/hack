function initMap(zoom_level) {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom_level,
        mapTypeId: 'roadmap',
        mapTypeControl: false,
        mapTypeControlOptions: {
            mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain', 'mundo_style']
        }
    });

    var style = new google.maps.StyledMapType([
        {
            featureType: 'poi',
            elementType: 'labels',
            stylers: [{visibility: 'off'}]
        },
        {
            featureType: 'road',
            elementType: 'labels',
            stylers: [{visibility: 'off'}]
        },
        {
            featureType: 'landscape',
            elementType: 'labels',
            stylers: [{visibility: 'off'}]
        },
        {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [{saturation: -90}]
        },
        {
            featureType: 'landscape',
            elementType: 'geometry',
            stylers: [{saturation: -90}]
        },
        {
            featureType: 'landscape.natural.terrain',
            stylers: [{visibility: 'off'}]
        }
    ], {name: "Mundo Style"});
    map.mapTypes.set('mundo_style', style);
    map.setMapTypeId('mundo_style');


    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    // map.addListener('bounds_changed', function() {
    //   searchBox.setBounds(map.getBounds());
    // });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function(marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

    return {'map': map}
}

function setEarthEngineOverlay(map, mapid, token, opacity) {
    var overlay = new ee.MapLayerOverlay('https://earthengine.googleapis.com/map', mapid, token, {});
    l = map.overlayMapTypes.push(overlay);
    map.overlayMapTypes.getAt(l - 1).setOpacity(opacity)
}


function setEarthEngineImage(map, mapid, token, opacity) {
    const eeMapOptions = {
        getTileUrl: (tile, zoom) => {
            const baseUrl = 'https://earthengine.googleapis.com/map';
            const url = [baseUrl, mapid, zoom, tile.x, tile.y].join('/');
            return `${url}?token=${token}`;
        },
        tileSize: new google.maps.Size(256, 256)
    };
    const mapType = new google.maps.ImageMapType(eeMapOptions);
    l = map.overlayMapTypes.push(mapType);
    map.overlayMapTypes.getAt(l - 1).setOpacity(opacity);
}


function heatmapOnDragend(map) {
    map.addListener('dragend', function() {
        (function($) {
            $.getJSON("/simple_riskmap/heatmap", function(data){
                setEarthEngineImage(map, data["mapid"], data["token"], 0.25)
            })
        })(jQuery);
    });
}