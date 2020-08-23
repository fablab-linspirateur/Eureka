import machine
import neopixel
from utime import sleep_ms
from umqtt.robust import MQTTClient
import displayer


def do_connect(network, password):
    # connect to Wifi
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = wlan.scan()
        sleep_ms(2000)
        print("found: %s" % _reseaux)
        trouve = False
        for n in _reseaux:
            if network in n[0]:
                print("network found")
                trouve = True
                break
            else:
                print("!! No RPi !!")
        if trouve:
            print("connec to", network)
            while not wlan.isconnected():
                wlan.connect(network, password)
                sleep_ms(1000)
                print(".")
            print("ready: ", wlan.ifconfig())
            break


# define leds configuration
NB_LEDS = 150
leds = neopixel.NeoPixel(machine.Pin(2), NB_LEDS)
disp = displayer(sleep_ms, leds, nb_leds=NB_LEDS)

# display all red = waiting for wifi connection
disp.neo_write(disp.all(0x640000))
sleep_ms(1000)

# define wifi configuration
do_connect(disp.config["network"], disp.config["password"])

# display all green = wifi connected
disp.neo_write(disp.all(0x006400))
sleep_ms(1000)

# define MQTT configuration
disp.init_mqtt(MQTTClient(
    disp.config["name"], disp.config["broker"], port=1883))

# turn all off
disp.neo_write(disp.all())
