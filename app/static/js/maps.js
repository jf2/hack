function initMap(country, zoom_level) {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom_level,
        mapTypeId: 'roadmap',
        mapTypeControl: false,
        mapTypeControlOptions: {
            mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain', 'mundo_style']
        }
    });
    var geocod = new google.maps.Geocoder();
    geocod.geocode({"address": country}, function(results, status) {
      console.log(status);
      map.setCenter(results[0].geometry.location);
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

    return {'map': map, 'geocoder': geocod}
}

function addEarthEngineOverlay(map, mapid, token, opacity) {
    var overlay = new ee.MapLayerOverlay('https://earthengine.googleapis.com/map', mapid, token, {});
    overlay.setOpacity(opacity);
    map.overlayMapTypes.push(overlay);
}


function addEarthEngineImage(map, mapid, token, opacity) {
    const eeMapOptions = {
        getTileUrl: (tile, zoom) => {
            const baseUrl = 'https://earthengine.googleapis.com/map';
            const url = [baseUrl, mapid, zoom, tile.x, tile.y].join('/');
            return `${url}?token=${token}`;
        },
        tileSize: new google.maps.Size(256, 256)
    };
    var mapType = new google.maps.ImageMapType(eeMapOptions);
    mapType.setOpacity(opacity);
    map.overlayMapTypes.push(mapType);
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