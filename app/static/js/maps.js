function initMap(init_lat, init_lng) {
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: init_lat, lng: init_lng},
      zoom: 7,
      mapTypeId: 'roadmap',
      mapTypeControl: false,
    });

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
    return map;
}

function setEarthEngineImage(map, mapid, token) {
    const eeMapOptions = {
        getTileUrl: (tile, zoom) => {
            const baseUrl = 'https://earthengine.googleapis.com/map';
            const url = [baseUrl, mapid, zoom, tile.x, tile.y].join('/');
            return `${url}?token=${token}`;
        },
        tileSize: new google.maps.Size(256, 256)
    };
    const mapType = new google.maps.ImageMapType(eeMapOptions);
    map.overlayMapTypes.push(mapType);
}


function heatmapOnDragend(map) {
    map.addListener('dragend', function() {
      (function($) {
          $.getJSON("/simple_riskmap/heatmap", function(data){
            setEarthEngineImage(map, data["mapid"], data["tokenid"])
          })
      })(jQuery);
  });
}