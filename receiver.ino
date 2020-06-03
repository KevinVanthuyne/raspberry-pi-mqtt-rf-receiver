#include <RCSwitch.h>

const int ledPin = 6; 
const RCSwitch mySwitch = RCSwitch();

void setup() {
  Serial.begin(9600);
  mySwitch.enableReceive(0);  // Receiver on interrupt 0 => pin #2
  Serial.println("Setup complete. Ready to receive.");
}

void loop() {
  if (mySwitch.available()) {
    int value = mySwitch.getReceivedValue();
    
    if (value == 2301) {
      Serial.println((String) "Message received: " + value);
      digitalWrite(ledPin, HIGH);
      delay(1000);
      digitalWrite(ledPin, LOW);
    }

    mySwitch.resetAvailable();
  }
}