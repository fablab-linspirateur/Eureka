import network
import machine
from neopixel import NeoPixel
from utime import sleep_ms
from umqtt.robust import MQTTClient
from displayer import displayer


def wlan_init(idnet):
    # initialize wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("scanning wifi")
    _reseaux = wlan.scan()
    sleep_ms(2000)
    print("found: %s" % _reseaux)
    for n in _reseaux:
        if idnet in n[0]:
            print("network", idnet, "found")
            return wlan
    return None


def do_connect(wlan, idnet, password):
    # connect to Wifi
    print("connecting to", idnet)
    wlan.connect(idnet, password)
    sleep_ms(5000)


# define leds configuration
NB_LEDS = 150
leds = NeoPixel(machine.Pin(2), NB_LEDS)
disp = displayer(sleep_ms, leds, nb_leds=NB_LEDS)

# display all red = waiting for wifi connection
color = 0x640000
disp.all(color)
sleep_ms(1000)
disp.all()

# define wifi configuration
i = 1
wlan = None
while True:
    print([disp.to_color(color)]*i)
    disp.neo_write([disp.to_color(color)]*i)
    i = (i+1) % NB_LEDS
    if wlan == None:
        wlan = wlan_init(disp.config["network"])
    if wlan != None:
        do_connect(wlan, disp.config["network"], disp.config["password"])
        if wlan.isconnected():
            break

# display all blue = wifi connected
color = 0x000064
disp.all(color)
sleep_ms(1000)
disp.all()

# define MQTT configuration
i = 1
client = MQTTClient(disp.config["name"],
                    disp.config["broker"], port=disp.config["port"])
while not client.connect():
    disp.neo_write([disp.to_color(color)]*i)
    i = (i+1) % NB_LEDS
    break
disp.init_mqtt(client)

# display all green = ready
color = 0x006400
disp.all(color)
sleep_ms(1000)
disp.all()
