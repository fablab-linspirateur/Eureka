import machine
import neopixel
import utime
import network
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
    for i, color in enumerate(led_colors):
        leds[i] = color
    utime.sleep_ms(100)
    leds.write()


def get_config(config_file="config.yaml"):
    # get the configuration dictionary from yaml file
    f = open(config_file)
    content = f.read()
    f.close()
    choix = content.split("\n")
    config = {}
    for kv in choix:
        if kv != '':
            key, val = kv.split(":")
            key = key.strip()
            config[key] = val.strip()
    return config


def connection(sta_if, network, password):
    # connect to Wifi
    sta_if.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = sta_if.scan()
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
            while not sta_if.isconnected():
                sta_if.connect(network, password)
                utime.sleep_ms(1000)
                infoleds()
                print(".")
            print("ready: ", sta_if.ifconfig())
            break


configuration = get_config()

# define leds configuration
NB_LEDS = 150
leds = neopixel.NeoPixel(machine.Pin(2), NB_LEDS)
disp = displayer(nb_leds=NB_LEDS)

# define wifi configuration
sta_if = network.WLAN(network.STA_IF)
connection(sta_if, config["network"], config["password"])

# define MQTT configuration
client = init_mqtt(configuration["name"], configuration["broker"])
