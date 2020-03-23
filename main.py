#!/usr/bin/env python3

import signal
import time
import os
import datetime
import paho.mqtt.client as mqtt
from rpi_rf import RFDevice
from dotenv import load_dotenv

gpio_pin = 26  # RF receiver is connected to pin 37 (GPIO26)

if __name__ == "__main__":
    try:
        # load environment variables
        load_dotenv()

        # setup mqtt
        client = mqtt.Client("rf_client")
        client.connect(os.getenv("MQTT_HOST_ADDRESS"))

        # setup rf
        rfdevice = RFDevice(gpio_pin)
        rfdevice.enable_rx()

        # start listening for rf messages
        print("Listening for codes on GPIO " + str(gpio_pin))
        timestamp = None

        while True:
            if rfdevice.rx_code_timestamp != timestamp:
                timestamp = rfdevice.rx_code_timestamp

                print("[{}] {} (pulselength {}, protocol {})".format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    rfdevice.rx_code,
                    rfdevice.rx_pulselength,
                    rfdevice.rx_proto
                ))

                if str(rfdevice.rx_code) == "2201":
                    client.publish("rf_client", "SIGNAL")
                    time.sleep(1) # debounce/throttle signal
                    timestamp = rfdevice.rx_code_timestamp # update timestamp after wait to prevent looping a second time

            time.sleep(0.01)

    except KeyboardInterrupt:
        rfdevice.cleanup()