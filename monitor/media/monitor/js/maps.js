function initialize() {

//  var latlng = new google.maps.LatLng(19.333500,-99.184141);
// zoom: 16,

  var latlng = new google.maps.LatLng(19.331500,-99.182141);
  var myOptions = {
    zoom: 17,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.HYBRID
  }; 
  
  var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  var latlng = new google.maps.LatLng(19.330000,-99.180641);
  var marker = new google.maps.Marker({
      position: latlng, 
      map: map, 
      title:"IIMAS"
  });

  var infowindow = new google.maps.InfoWindow({
      content: contentString,
  	maxWidth: 260
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
  });

}