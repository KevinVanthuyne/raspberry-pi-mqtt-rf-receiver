#include "LowPower.h" // https://github.com/rocketscream/Low-Power
#include <RCSwitch.h>
#include <VoltageReference.h>

#define BUTTON_1_PIN 2 // INT0
#define BUTTON_2_PIN 3 // INT1
#define RF_PIN 10

RCSwitch mySwitch = RCSwitch();
VoltageReference voltRef;
volatile int buttonPressed = 1; // which button was pressed

void button1Pressed() {
  buttonPressed = 1;
}

void button2Pressed() {
  buttonPressed = 2;
}

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_1_PIN, INPUT_PULLUP);
  pinMode(BUTTON_2_PIN, INPUT_PULLUP);
  mySwitch.enableTransmit(RF_PIN);
  voltRef.begin();
  Serial.println("Setup complete");
  delay(5000); // necessary to do setup before going to sleep and to be able to upload new sketch on reset
}

void loop() {
  attachInterrupt(digitalPinToInterrupt(BUTTON_1_PIN), button1Pressed, LOW);
  attachInterrupt(digitalPinToInterrupt(BUTTON_2_PIN), button2Pressed, LOW);
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF); 

  // interrupt wakes from sleep and continues loop from here
  detachInterrupt(digitalPinToInterrupt(BUTTON_1_PIN));
  detachInterrupt(digitalPinToInterrupt(BUTTON_2_PIN)); 

  int vcc = voltRef.readVcc(); // battery voltage in mV

  if (buttonPressed == 1) {
    mySwitch.send(22010000 + vcc, 32); // 2201 (message code) + vcc value 
    Serial.println("Button 1 RF message sent");
  }
  else if (buttonPressed = 2) {
    mySwitch.send(22020000 + vcc, 32); // 2202 (message code) + vcc value 
    Serial.println("Button 2 RF message sent");
  }
  delay(200); // delay necessary to prevent Arduino from going to sleep before finishing print
}