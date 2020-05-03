#!/usr/bin/env python3

import signal
import time
import os
import datetime
import paho.mqtt.client as mqtt
import logging
from rpi_rf import RFDevice
from dotenv import load_dotenv

gpio_pin = 26  # RF receiver is connected to pin 37 (GPIO26)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("MQTT CONNECT: Connected with result code %s", str(rc))

def on_log(client, userdata, level, buf):
    logging.info("MQTT LOG: client %s - userdata %s - level %s - bug %s", client, userdata, level, bug)

if __name__ == "__main__":
    try:
        # load environment variables
        load_dotenv()

        # setup logger
        logging.basicConfig(format = "%(asctime)s %(levelname)-10s %(message)s", level = logging.INFO)

        # setup mqtt
        client = mqtt.Client("rf_client")
        client.on_connect = on_connect
        client.on_log = on_log
        client.enable_logger()
        client.connect(os.getenv("MQTT_HOST_ADDRESS"))
        client.loop_start()

        # setup rf
        rfdevice = RFDevice(gpio_pin)
        rfdevice.enable_rx()


        # start listening for rf messages
        logging.info("Listening for codes on GPIO " + str(gpio_pin))
        timestamp = None

        while True:
            if rfdevice.rx_code_timestamp != timestamp:
                timestamp = rfdevice.rx_code_timestamp

                logging.info(
                    "Received message: %s (pulselength %s, protocol %s)", 
                    rfdevice.rx_code,
                    rfdevice.rx_pulselength,
                    rfdevice.rx_proto
                )

                # first 4 numbers contain "id" code, next 4 numbers contain voltage of the sender's battery in mV
                if str(rfdevice.rx_code)[:4] == "2201":
                    client.publish("rf_button_1", str(rfdevice.rx_code)[4:8])
                    logging.info("  Published 'rf_button_1' topic with message '%s'", str(rfdevice.rx_code)[4:8])
                    time.sleep(1) # debounce/throttle signal
                    timestamp = rfdevice.rx_code_timestamp # update timestamp after wait to prevent looping a second time

            time.sleep(0.01)

    except KeyboardInterrupt:
        rfdevice.cleanup()