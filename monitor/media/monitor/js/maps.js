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

  setMarkers(map, eventos);
}

function setMarkers(map, locations) {
  
  for (var i = 0; i < locations.length; i++) {
    if (evento[0] != '') {
      var evento = locations[i];
      var myLatLng = new google.maps.LatLng(evento[1], evento[2]);
      var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: evento[0]
      });

      var contentString = '<div id="content">'+
    	 '<div id="siteNotice">'+
    	 '</div>'+
    	 '<h1 id="firstHeading" class="firstHeading">' + evento[0]  + '</h1>'+
    	 '<div id="bodyContent">'+
    	 '<p><b>'+ evento[0] +'</b>, ' +
    		''+ evento[4] +'</p> ' +
    	 '<p><a href="'+ evento[5] +'">'+
    	 'Detalle</a></p>'+
    	 '</div>'+
    	 '</div>';
  	
      var infowindow = new google.maps.InfoWindow({
          content: contentString,
      	  maxWidth: 260
      });
    
      google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
      }); 
    }
  }
}