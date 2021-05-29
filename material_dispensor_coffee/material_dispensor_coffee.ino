#include <ESP8266WiFi.h>

// Replace with your network credentials
const char* ssid     = "Deepblue";
const char* password = "asdfghjkl";
String stat = "free";
// Set web server port number to 80
WiFiServer server(80);


void setup() {
  Serial.begin(115200);
  pinMode(D0,OUTPUT);
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  digitalWrite(D0,HIGH);
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();

}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients
  if (client) {
    while (client.connected()) {
      while (client.available()>0) {
        String c = client.readStringUntil('\r');
        Serial.println(c);
        if(c == "water" or c=="milk" or c == "sugar" or c=="powder"){
            client.println(c);
            digitalWrite(D0,LOW);
            delay(1000);
            if (c=="powder"){
              stat = "free";
            }
            else{
              stat = "busy";  
            }
            
        }
        else if(c == "status"){
          client.println(stat);
          Serial.println(stat);
        }
        else if(c=="comp"){
          stat = "free";
          client.println(stat);
        }
        else{
          client.println("true");
          Serial.println("true");
        }
        //Serial.println(stat);
      } 
      delay(10);
    }

    //client.stop();
    //Serial.println("Client disconnected");
 
  }
}
