#include <RCSwitch.h>

#define BUTTON_PIN 3
#define RF_PIN 10

RCSwitch mySwitch = RCSwitch();

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  mySwitch.enableTransmit(RF_PIN);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    mySwitch.send(2201, 24);
    Serial.println("button pressed");
    delay(500);  
  }
}