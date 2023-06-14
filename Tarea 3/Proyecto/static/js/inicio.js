let mapContainer = document.getElementById('map');
let map = L.map(mapContainer)

map.setView([-33.457, -70.6], 3.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

const redMarker = L.icon({
  iconUrl: '/static/media/red_marker.png', 
  iconSize: [30, 41], 
  iconAnchor: [12, 41], 
});

const blueMarker = L.icon({
  iconUrl: '/static/media/blue_marker.png', 
  iconSize: [30, 41], 
  iconAnchor: [12, 41], 
});

fetch("/get-markers")
    .then((response) => response.json())
    .then((data) => {
      listaDonaciones = data[0];
      listaPedidos = data[1];
      listaRepeticiones = data[2];

    for(let i=0; i<listaDonaciones.length; i++) {
      if(listaRepeticiones.length == 0) {
        let marker = L.marker([listaDonaciones[i].latitud, listaDonaciones[i].longitud], {icon: redMarker});
        let message = "";
        console.log(listaDonaciones[i].id);
        for(let llave in listaDonaciones[i]) {
          if (listaDonaciones[i].hasOwnProperty(llave)) {
            let valor = listaDonaciones[i][llave];
            if(llave == "id") {
              message += "<h1>" + valor + "</h1>";
            }
            else if(llave != "latitud" && llave != "longitud") {
              message += "<br>" + valor;
            }          
          }
        }
        marker.bindPopup(message);
        marker.addTo(map);
      }
      else if(listaRepeticiones != 0){
        for(let j=0; j<listaRepeticiones.length; j++) {
          if(listaDonaciones[i].comuna != listaRepeticiones[j]) {
            let marker = L.marker([listaDonaciones[i].latitud, listaDonaciones[i].longitud], {icon: redMarker});
            let message = "";
            for(let llave in listaDonaciones[i]) {
              if (listaDonaciones[i].hasOwnProperty(llave)) {
                let valor = listaDonaciones[i][llave];
                if(llave == "id") {
                  message += "<h1>" + valor + "</h1>";
                }
                else if(llave != "latitud" && llave != "longitud") {
                  message += "<br>" + valor;
                }          
              }
            }
            marker.bindPopup(message);
            marker.addTo(map);
          }
        }
      }
    }
    
    for(let i=0; i<listaPedidos.length; i++) {
      if (listaRepeticiones.length == 0) {
        let marker = L.marker([listaPedidos[i].latitud, listaPedidos[i].longitud], {icon: blueMarker});
        let message = "";
        for(let llave in listaPedidos[i]) {
          if (listaPedidos[i].hasOwnProperty(llave)) {
            let valor = listaPedidos[i][llave];
            if(llave == "id") {
              message += "<h1>" + valor + "</h1>";
            }
            else if(llave != "latitud" && llave != "longitud") {
              message += "<br>" + valor;
            }          
          }
        }
        marker.bindPopup(message);
        marker.addTo(map); 
      }
      if (listaRepeticiones != 0) {
        for(let j=0; j<listaRepeticiones.length; j++) {
          if(listaPedidos[i].comuna != listaRepeticiones[j]) {
            let marker = L.marker([listaPedidos[i].latitud, listaPedidos[i].longitud], {icon: blueMarker});
            let message = "";
            for(let llave in listaPedidos[i]) {
              if (listaPedidos[i].hasOwnProperty(llave)) {
                let valor = listaPedidos[i][llave];
                if(llave == "id") {
                  message += "<h1>" + valor + "</h1>";
                }
                else if(llave != "latitud" && llave != "longitud") {
                  message += "<br>" + valor;
                }          
              }
            }
            marker.bindPopup(message);
            marker.addTo(map);
          }
        }
      }
    }
    
    if(listaRepeticiones.length > 0) {
      for(let i=0; i<listaRepeticiones.length; i++) {
      let markers = L.markerClusterGroup();
      for(let j=0; j<listaDonaciones.length; j++) {
        if(listaRepeticiones[i] == listaDonaciones[j].comuna) {
          let marker = L.marker([listaDonaciones[i].latitud, listaDonaciones[i].longitud], {icon: redMarker});
          let message = "";
          for(let llave in listaDonaciones[i]) {
            if (listaDonaciones[i].hasOwnProperty(llave)) {
              let valor = listaDonaciones[j][llave];
              if(llave == "id") {
                message += "<h1>" + valor + "</h1>";
              }
              else if(llave != "latitud" && llave != "longitud") {
                message += "<br>" + valor;
              }          
            }
          }
          marker.bindPopup(message);
          markers.addLayer(marker);
        }
      }
      for(let j=0; j<listaPedidos.length; j++) {
        if(listaRepeticiones[i] == listaPedidos[j].comuna) {
          let marker = L.marker([listaPedidos[i].latitud, listaPedidos[i].longitud], {icon: blueMarker});
          let message = "";
          for(let llave in listaPedidos[i]) {
            if (listaPedidos[i].hasOwnProperty(llave)) {
              let valor = listaPedidos[j][llave];
              if(llave == "id") {
                message += "<h1>" + valor + "</h1>";
              }
              else if(llave != "latitud" && llave != "longitud") {
                message += "<br>" + valor;
              }          
            }
          }
          marker.bindPopup(message);
          markers.addLayer(marker);
        }
      }
      map.addLayer(markers);
      }
    }      
  })
.catch((error) => console.error("Error", error))


