function initialize() {
//  var latlng = new google.maps.LatLng(19.333500,-99.184141);
// zoom: 16,
  var latlng = new google.maps.LatLng(19.331500,-99.182141);
  var myOptions = {
    zoom: 17,
    center: latlng,
    streetViewControl: true,
    mapTypeId: google.maps.MapTypeId.HYBRID
  }; 
  
  var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  if (current_alarms.length > 0) {
    setMarkers(map, current_alarms);
  } 
  else {
    setFlag(map, current_alarms);
  }
}

function setFlag(map, locations) {
  var myLatLng = new google.maps.LatLng(19.330000, -99.180641);

  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      icon: '/site_media/img/flag-icon2.png',
      title: 'IIMAS'
  });
  var infowindow = new google.maps.InfoWindow({
      content: '<a href="activities">Instituto de Investigaciones en Matematicas Aplicadas y en Sistemas</a> <p>' +
      '<img src="/site_media/img/info-iimas.png" alt="IIMAS"/> </p>',
  	  maxWidth: 260
  });
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
  }); 
}

function setMarkers(map, locations) {
  
  for (var i = 0; i < locations.length; i++) {
    var evento = locations[i];
    if (evento[0] != '') {
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