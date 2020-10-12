from network_cnx import do_connect, wlan_init
from mqtt_cnx import init_mqtt
from utime import sleep_ms
from leds import init_component_leds, turn_all, flash, to_color, neo_write
import network

while True:

    if wlan == None or not wlan.isconnected():
        # display all red = waiting for wifi connection
        color = 0x640000
        flash(color, sleep_ms)

        i = 1
        while True:
            neo_write([to_color(color)]*i, sleep_ms)
            i = (i+1) % NB_LEDS
            if wlan == None:
                wlan = wlan_init(config["network"], network, sleep_ms)
            if wlan != None:
                do_connect(wlan, config["network"],
                           config["password"], sleep_ms)
                if wlan.isconnected():
                    break

        # display all blue = wifi connected
        color = 0x000064
        flash(color, sleep_ms)

        # define MQTT configuration
        i = 1
        while not client.connect():
            neo_write([to_color(color)]*i, sleep_ms)
            i = (i+1) % NB_LEDS
            break
        init_mqtt(client, sleep_ms)

        # display all green = ready
        flash(0x006400, sleep_ms)

    client.check_msg()
