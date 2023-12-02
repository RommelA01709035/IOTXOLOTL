# IOTXOLOTL
Este es mi proyecto de la materia "Internet de las cosas"  con código TC1004B en este proyecto se toman temas de IOT, IA y Desarrollo Web.


## Componentes HARDWARE
- 1 ESP8266
- 1 Sensor ph4502c entrada bnc
- 1 Sensor DHT11
- 1 Buzzer
- 1 LED verde
- 2 LEDs rojos

## Explicación de donde usamos los siguientes temas de software:
- Almacenar datos de Ubidots: En el archivo "IOTxolotl.ino" usamos la librería de Ubidots para mandar los datos al servicio de ubidots con los comandos "add", "wifiConnect" y "send"
- Desarrollo web: a partir de los IDs de las variables generadas y el default token usamos, usamos AJAX para que se actualizarán nuestros graficos y usamos el protocolo GET para extraer la información guardada en las variables.
- Interfaz de usuario DW y AE: En el desarrollo web usamos HTML y CSS básico para hacer la interfaz mientras que en la aplicación de escritorio usamos la librería TKINTER para el desarrollo total del software (Archivos .html, style.css y Analisis.py).
- IA: se importo a través de tensorflow un modelo para que reconociera objeto, esto simulando un modelo que puedo saber cuantos especimenes hay en el habitat (Analisis.py).

## Problemas que tuvimos
-Al usar un ESP8266 en la interfaz de arduino no se desplegaba en pantalla el compuerto habilitado para poder conectar el ESP por lo que buscamos y encontramos el driver que nos funcionó en el manual del ESP32 (Si en el manual del ESP32) en el siguiente link podrás encontrarlo:
https://randomnerdtutorials.com/download/ 

-Al conectar la base de datos desde arduino lo que hicimos nfue no crear un servicio en la plataforma ubidots sino solamente poner los tokens en arduino y se genraba automaticamente el servicio e igual al añadir variables solamente las mandabamos a través del codigo arduino.

-EL DIAGRAMA DEL SENSOR DE PH NO ES COMO PARECE EN INTERNET  DEBES CALIBRARLO CON LOS TORNILLOS DE LA CAJA AZUL QUE NO ESTA A LADO DEL CONECTOR BNC. EN nuestro caso el pin de salida de datos fue el Do, nuestro pin de tierra fue el que esta a lado de del pin Po (debes verficiar que tierra usar dependiendo de tu slida de datos si es analogica o digital, nosotros usamos analogica) y el pin de voltaje fue V+.

-Recuerda totalmente que si vas a usar más compuertos Dn debes poner su configuración en el codigo arduino en la seccion setup para que esten disponibles sino no harán nada.

-Recuerda que mis archivos son solo codigo tu debes de cambiar de acuerdo a tus datos y también instalar las librerías necesarias
 
## Videos que sirvieron:
- Buzzer: https://youtu.be/WA-G_Pg0yas?si=CEqg0hMW61ye9o5g
- ESP8266 DHT11: https://youtu.be/orxxKfL64bA?si=7EdxUve43bunvXj0
- Sensor de pH: https://youtu.be/zUEl3Y3yKL4?si=-8l7TLPtSFB6U1fl
 
- 
