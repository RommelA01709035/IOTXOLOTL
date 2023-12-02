// JavaScript para crear gráficos con Chart.js
// Agrega los datos y opciones de los gráficos según sea necesario

// Ejemplo de gráfico de temperatura

// Llama a la función controlarColores con los valores adecuados
var pHActual = 7.2; // Cambia esto con el valor real
var temperaturaActual = 26; // Cambia esto con el valor real
controlarColores(pHActual, temperaturaActual);

function mostrarAjolote(ajoloteId) {
    // Obtén el nombre del ajolote a partir del ID
    const ajoloteName = ajoloteId.replace("ajolote", "");

    // Redirecciona a la página del ajolote seleccionado
    window.location.href = `ajolote${ajoloteName}.html`;
}

// Espera a que la página se cargue completamente
document.addEventListener('DOMContentLoaded', function () {
    // Realiza una solicitud al servidor cada X segundos (por ejemplo, cada 5 segundos)
    setInterval(actualizarDatos, 5000);
});

function actualizarDatos() {
    // Realiza una solicitud al servidor (ESP8266)
    fetch('/lectura')  // Debes definir una ruta en tu servidor para manejar esta solicitud
        .then(response => response.json())
        .then(data => {
            // Actualiza los valores en la página
            document.getElementById('temperatura').textContent = data.temperatura + ' °C';
            document.getElementById('ph').textContent = data.ph;
        })
        .catch(error => {
            console.error('Error al obtener datos:', error);
        });
}

function agregarDispositivo() {
    // Recopila los datos del formulario
    var nombre = document.getElementById('deviceName').value;
    // Recopila más datos según sea necesario

    // Crea elementos HTML para el nuevo dispositivo
    var nuevoDispositivo = document.createElement('a');
    nuevoDispositivo.className = 'buttonAjolote';
    nuevoDispositivo.href = '#' + nombre.toLowerCase();  // Crea un identificador único para el dispositivo

    var nombreElemento = document.createElement('p');
    nombreElemento.className = 'ajoloteName';
    nombreElemento.textContent = nombre;

    var imagenElemento = document.createElement('img');
    imagenElemento.src = 'imagen_por_defecto.jpg';  
    imagenElemento.alt = nombre;
    imagenElemento.onclick = function () {
        mostrarAjolote(nombre.toLowerCase());
    };

    nuevoDispositivo.appendChild(nombreElemento);
    nuevoDispositivo.appendChild(imagenElemento);
    // Obtén la imagen cargada
    var imageInput = document.getElementById('deviceImage');
    var imageFile = imageInput.files[0];

    // Verifica si se cargó una imagen
    if (imageFile) {
      mostrarVistaPrevia(imageFile, nombre.toLowerCase());
      // Realiza acciones con la imagen 
      console.log('Imagen cargada:', imageFile);
  }
     // Muestra la vista previa de la imagen
     mostrarVistaPrevia(imageFile);
     // Realiza acciones con la imagen 
     console.log('Imagen cargada:', imageFile);


    // Agrega el nuevo dispositivo al menú
    document.querySelector('.menu').appendChild(nuevoDispositivo);
}

function actualizarToken() {
  // Obtén el nuevo token del formulario
  var nuevoToken = document.getElementById('updateToken').value;

  // Actualiza el token utilizado por la función getDataFromVariable
  TOKEN = nuevoToken;

  // Vuelve a obtener datos y actualizar la gráfica con el nuevo token
  getDataFromVariable(VARIABLE, TOKEN, function (values) {
      var data = values.map(function (value) {
          return [value.timestamp, value.value];
      });

      chart.series[0].setData(data);
  });
}


function mostrarVistaPrevia(imageFile) {
  var reader = new FileReader();

  reader.onload = function (e) {
      // Crea un elemento de imagen para mostrar la vista previa
      var previewElement = document.createElement('img');
      previewElement.src = e.target.result;
      previewElement.alt = 'Vista previa de la imagen';

      // Muestra la vista previa en el contenedor designado
      var previewContainer = document.getElementById('previewImage');
      previewContainer.innerHTML = ''; // Limpia cualquier vista previa anterior
      previewContainer.appendChild(previewElement);
  };

  // Lee el contenido de la imagen como una URL de datos (data URL)
  reader.readAsDataURL(imageFile);
}


var TOKEN = 'BBUS-MlBkOE4HhxVCePRaQlQd1Lc2p50ukK';
var VARIABLE = '654fc7fa07b504000dfcd5b9';

function getDataFromVariable(variable, token, callback) {
  var url = 'https://industrial.api.ubidots.com/api/v1.6/variables/' + variable + '/values';
  var headers = {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
  };
  
  $.ajax({
    url: url,
    method: 'GET',
    headers: headers,
    success: function (res) {
      callback(res.results);
    }
  });
}

var chart = Highcharts.chart('container', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Bring data from Ubidots'
    },
    xAxis: {
        type: 'datetime',
    },
    credits: {
        enabled: false
    },
    series: [{
    	data: []
    }]
});

getDataFromVariable(VARIABLE, TOKEN, function (values) {
  var data = values.map(function (value) {
    return [value.timestamp, value.value];
  });
  
  chart.series[0].setData(data);
});

