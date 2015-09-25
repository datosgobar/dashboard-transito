/*  
 * Map Styles bounds, center and options - V0.1
 * @author: Nicolas Lound 
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://opensource.org/licenses/MIT
 * http://www.gnu.org/licenses/gpl-2.0.html
*/

//edit these for bounding the map.
var centro =  new google.maps.LatLng(-34.604592, -58.375232);	// center of the map
/*
 * DO NOT EDIT BELOW THIS LINE
*/


var settingsItemsMap = {
    zoom: 15, // nivel de zoom inicial
    center: centro,
    streetViewControl: false,
	mapTypeControl: false, // Map type control. Road, satellite, etc.
	mapTypeId: google.maps.MapTypeId.ROADMAP, // Map type 
	maxZoom: 17, //  21+ = sea level
	minZoom: 12, // 0 = globe
	scaleControl: false, 
	panControl:false, 
	zoomControl: true, 
    styles:     // Inicial Styles
// ----------------------------->

[
  {
    "stylers": [
      { "saturation": -100 }
    ]
  },{
    "featureType": "water",
    "stylers": [
      { "visibility": "on" },
      { "hue": "#00ffee" },
      { "saturation": -26 },
      { "color": "#bfd0da" }
    ]
  },{
    "featureType": "administrative.country",
    "elementType": "geometry.fill",
    "stylers": [
      { "hue": "#ff6600" },
      { "lightness": -100 },
      { "color": "#ff3e3c" },
      { "saturation": -63 },
      { "weight": 1.8 },
      { "visibility": "off" }
    ]
  },{
    "featureType": "road",
    "stylers": [
      { "gamma": 4.33 }
    ]
  },{
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" },
      { "gamma": 3.1 },
      { "lightness": 100 }
    ]
  },{
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" }
    ]
  },{
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      { "color": "#ccdac2" },
      { "saturation": -11 },
      { "lightness": 65 },
      { "gamma": 1.07 }
    ]
  },{
    "featureType": "landscape",
    "elementType": "geometry",
    "stylers": [
      { "color": "#ffffff" }
    ]
  },{
    "featureType": "administrative.locality",
    "stylers": [
      { "lightness": 39 },
      { "visibility": "on" }
    ]
  },{
    "featureType": "administrative.neighborhood",
    "elementType": "labels",
    "stylers": [
      { "lightness": 39 },
      { "visibility": "on" }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "geometry",
    "stylers": [
      { "visibility": "on" },
      { "lightness": -5 }
    ]
  },
 { "featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [ { "color": "#999999" } ] },
 { "featureType": "road.arterial", "elementType": "labels.text.fill", "stylers": [ { "color": "#000000" } ] },
 { "featureType": "road.local", "elementType": "geometry.fill", "stylers": [ { "visibility": "simplified" } ] },


  {
    "featureType": "landscape",
    "stylers": [
      { "visibility": "on" },
      { "color": "#808080" },
      { "lightness": 95 }
    ]
  },{
    "featureType": "poi.business",
    "elementType": "geometry",
    "stylers": [
      { "color": "#808080" },
      { "lightness": 95 }
    ]
  }
]
}; 


