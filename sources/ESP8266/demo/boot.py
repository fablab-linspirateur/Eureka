import machine
import neopixel
import utime
from umqtt.robust import MQTTClient
import displayer


def init_mqtt(name, broker):
    # initialize mqtt subscriptions
    print("connect mqtt...")
    client = MQTTClient(
        name, broker, port=1883)
    res = client.connect()
    if not res:
        client.subscribe(disp.TOPIC_END)
        client.subscribe(disp.TOPIC_SEARCH_BASE+"/#")
        client.subscribe(disp.TOPIC_ERROR_BASE+"/#")
        client.set_callback(sub_cb)
        return client
    return None


def sub_cb(topic, payload):
    # mqtt callback
    led_colors = disp.refresh(topic, payload)
    neo_write(led_colors)


def neo_write(t_color):
    # write a table of colors to neopixel
    for i, color in enumerate(t_color):
        leds[i] = color
    utime.sleep_ms(100)
    leds.write()


def do_connect(network, password):
    # connect to Wifi
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = wlan.scan()
        utime.sleep_ms(2000)
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
                utime.sleep_ms(1000)
                print(".")
            print("ready: ", wlan.ifconfig())
            break


# define leds configuration
NB_LEDS = 150
leds = neopixel.NeoPixel(machine.Pin(2), NB_LEDS)
disp = displayer(nb_leds=NB_LEDS)
neo_write(disp.all(0x640000))
utime.sleep_ms(1000)

# define wifi configuration
do_connect(disp.config["network"], disp.config["password"])
neo_write(disp.all(0x640000))
utime.sleep_ms(1000)

# define MQTT configuration
client = init_mqtt(disp.config["name"], disp.config["broker"])
neo_write(disp.all())
