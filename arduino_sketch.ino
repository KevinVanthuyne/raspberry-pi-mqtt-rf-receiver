#include "LowPower.h" // https://github.com/rocketscream/Low-Power
#include <RCSwitch.h>

#define BUTTON_PIN 2
#define RF_PIN 10

RCSwitch mySwitch = RCSwitch();

void buttonPressed() {
  // Empty handler
}

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  mySwitch.enableTransmit(RF_PIN);
  Serial.println("Setup complete");
  delay(200); // necessary to do setup before going to sleep
}

void loop() {
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonPressed, LOW);
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF); 
  detachInterrupt(digitalPinToInterrupt(BUTTON_PIN)); 

  mySwitch.send(2201, 24);
  Serial.println("RF message sent");
  delay(200); // delay necessary to prevent Arduino from going to sleep before finishing print
}