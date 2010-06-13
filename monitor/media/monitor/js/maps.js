function initialize() {

  var latlng = new google.maps.LatLng(19.333500,-99.184141);
  var myOptions = {
    zoom: 16,
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

  var contentString = '<div id="content">'+
    '<div id="siteNotice">'+
    '</div>'+
    '<h1 id="firstHeading" class="firstHeading">IIMAS</h1>'+
    '<div id="bodyContent">'+
    '<p><b>INSTITUTO DE INVESTIGACIONES EN MATEMÁTICAS APLICADAS Y EN SISTEMAS</b>, ' +
	'CIRCUITO ESCOLAR, CIUDAD UNIVERSITARIA, MÉXICO D.F. ' +
	'Apartado Postal 20-726, Admón. No. 20, C.P. 01000, Del. Álvaro Obregón, ' +
    'México, D.F.</p>'+
    '<p><a href="http://127.0.0.1:8000/monitor/activities/">'+
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