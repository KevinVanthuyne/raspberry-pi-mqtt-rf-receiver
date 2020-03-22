#!/usr/bin/env python3

import signal
import time

from rpi_rf import RFDevice

gpio_pin = 26  # RF receiver is connected to pin 37 (GPIO26)

def listen_for_messages():
    timestamp = None
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        print(str(rfdevice.rx_code) +
                " [pulselength " + str(rfdevice.rx_pulselength) +
                ", protocol " + str(rfdevice.rx_proto) + "]")
    time.sleep(0.01)

if __name__ == "__main__":
    try:
        rfdevice = RFDevice(gpio_pin)
        rfdevice.enable_rx()

        print("Listening for codes on GPIO " + str(gpio_pin))
        while True:
            listen_for_messages()


    except KeyboardInterrupt:
        rfdevice.cleanup()