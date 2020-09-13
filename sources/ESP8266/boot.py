from configuration import get_config
from leds import init_component_leds, init_nb_leds, turn_all, flash, to_color, neo_write
from network_cnx import do_connect, wlan_init
from mqtt_cnx import init_mqtt
import network
from utime import sleep_ms
from umqtt.robust import MQTTClient

# define configuration
NB_LEDS = 150
init_nb_leds(NB_LEDS)
config = get_config()
client = MQTTClient(config["name"], config["broker"], port=config["port"])

# display all red = waiting for wifi connection
color = 0x640000
flash(color, sleep_ms)

# define wifi configuration
i = 1
wlan = None
while True:
    neo_write([to_color(color)]*i, sleep_ms)
    i = (i+1) % NB_LEDS
    if wlan == None:
        wlan = wlan_init(config["network"], network, sleep_ms)
    if wlan != None:
        do_connect(wlan, config["network"], config["password"], sleep_ms)
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
