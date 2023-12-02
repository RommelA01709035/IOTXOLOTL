// This example sends data to multiple variables to
// Ubidots through HTTP protocol.

/****************************************
 * Include Libraries
 ****************************************/

#include "Ubidots.h"
#include "DHT.h"

/****************************************
 * Define Instances and Constants
 ****************************************/

const char* UBIDOTS_TOKEN = "BBUS-MlBkOE4HhxVCePRaQlQd1Lc2p50ukK";  // Put here your Ubidots TOKEN
const char* WIFI_SSID = "motorola";      // Put here your Wi-Fi SSID
const char* WIFI_PASS = "AguaUwu2";      // Put here your Wi-Fi password
Ubidots ubidots(UBIDOTS_TOKEN, UBI_HTTP);

const int DHTPIN = 4; //pin dht11
const int DHTTYPE = DHT11;
DHT dht(DHTPIN, DHTTYPE);
const int LED_PIN = 0; //Pin led Wifi
const int LEDT = 16; //Pin led Temperatura mal
const int LEDPH = 5; //Pin led PH
float phFijo = 7.00;
int Buzzer = 2; //Se declara la variable "Buzzer" en el pin 3 de PWM.
bool sonandoBuzzer = false;
int pH;
float Voltaje;

/****************************************
 * Main Functions
 ****************************************/

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LEDT, OUTPUT);
  pinMode(LEDPH, OUTPUT);
  ubidots.wifiConnect(WIFI_SSID, WIFI_PASS);
  digitalWrite(LED_PIN, LOW); // Encender el LED cuando esté conectado a Wi-Fi
  pinMode(Buzzer, OUTPUT); //Se declara el Buzzer como Salida.
  pinMode(pH, INPUT);
}

void loop() {


  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float pHV = analogRead(A0);
  Voltaje =  (5/pHV*1023) - 0.6;
  ubidots.add("humidity1", h);  // Aniadir datos a ubidots
  ubidots.add("temperature1", t);
  ubidots.add("pH", Voltaje);
  bool bufferSent = false;
  bufferSent = ubidots.send();  // Will send data to a device label that matches the device Id
  bool check = false;

  if(t < 17 || t > 20){
    digitalWrite(LEDT, HIGH); // Encender el LED si esta mal la temperatura
    delay(2000); // Ajustar según sea necesario
    digitalWrite(LEDT, LOW); // parpadeo     
    tone(Buzzer, 49, 2000);
  }
  if(Voltaje > 6.5 ){//
    digitalWrite(LEDPH, HIGH); // Encender el LED si esta mal la temperatura
    delay(2000); // Ajustar según sea necesario
    digitalWrite(LEDPH, LOW); // parpadeo
    tone(Buzzer, 100, 2000);   
  }
  if (bufferSent) {
    // Do something if values were sent properly
    Serial.println("Values sent by the device");
    digitalWrite(LED_PIN, HIGH); // Apagar el LED después de enviar datos
    delay(2000); // Ajustar según sea necesario
    digitalWrite(LED_PIN, LOW); // Encender el LED nuevamente antes de la siguiente lectura
    tone(Buzzer, 200, 4000);
  }
  delay(2000);
  
}
