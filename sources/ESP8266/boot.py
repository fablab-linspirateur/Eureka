import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


def update(component):
    # update color table
    start = component[0x000000][0]
    end = component[0x000000][1]
    nbcolor = len(component.keys())-1
    try:
        pas = int((end-start)/nbcolor)
    except:
        pas = int(end-start)

    prev = start
    for i, c in enumerate(component.keys()):
        if c == 0:
            # keep color 0 (off)
            continue
        component[c] = [prev, (i*pas)+start]
        prev = component[c][1]+1
    component[c][1] = end


def add(component, color):
    # add a color to a component
    component[color] = []
    print(component)
    update(component)


def remove(component, color):
    # remove a color from a component
    try:
        del(component[color])
    except:
        return
    update(component)


def to_color(n24):
    # convert color to neopixel color
    r = n24 >> 16
    v = (0x00ff00 & n24) >> 8
    b = (0x0000ff & n24)
    return (r, v, b)


def get_config():
    # get the configuration dictionary from yaml file
    f = open("config.yaml")
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


def get_components():
    # get the list of components stored in the configuration file
    f = open("components.txt")
    content = f.read()
    f.close()
    clist = content.split("\n")
    components = []
    for kv in clist:
        components.append(kv.strip())
    return components


def sub_cb(topic, payload):
    # mqtt callback
    print(topic)
    if topic == TOPIC_BLINK:
        blink_active_leds()
    if topic == TOPIC_OFF:
        for i in range(nbleds):
            leds[i] = LED_OFF
        Activeleds.clear()
    else:
        for pos in range(nbleds):
            if topic == ilot+"/"+components[pos]:
                Activeleds.add(pos)
                leds[pos] = LED_WHITE
    utime.sleep_ms(100)
    leds.write()


def init_mqtt(client, components, ilot):
    # initialize mqtt subscriptions
    print("connect mqtt...")
    res = client.connect()
    if not res:
        client.subscribe(ilot+TOPIC_OFF)
        client.subscribe(ilot+TOPIC_BLINK)
        for _id in components:
            _nom = ilot+"/"+str(_id)
            client.subscribe(_nom)
        client.set_callback(sub_cb)


def infoleds():
    # make the first LED blink red
    utime.sleep_ms(500)
    leds[0] = LED_RED
    leds.write()
    print(".")
    utime.sleep_ms(500)
    leds[0] = LED_OFF
    leds.write()


def connection(sta_if, leds):
    # connect to Wifi
    sta_if.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = sta_if.scan()
        utime.sleep_ms(2000)
        print("found: %s" % _reseaux)
        trouve = False
        for n in _reseaux:
            if b"raspi-poste1" in n[0]:
                print("trouvé")
                trouve = True
                break
            else:
                print("Pas de RPi !!")
        if trouve:
            print("connection to raspi-poste1")
            while not sta_if.isconnected():
                sta_if.connect("raspi-poste1", "Burkert67")
                utime.sleep_ms(1000)
                infoleds()
                print(".")
            print("Ready: ", sta_if.ifconfig())
            break


# constants
configuration = get_config()
chariot = configuration["chariot"]
ilot = configuration["ilot"]
TOPIC_OFF = ilot+"/off"
TOPIC_BLINK = ilot+"/blink"
LED_OFF = (0, 0, 0, 0)
LED_WHITE = (0, 0, 0, 100)
LED_RED = (100, 0, 0, 0)

# deende components configuration
components = get_components()
print("components :", components)

# deende leds configuration
nbleds = 150
leds = neopixel.NeoPixel(machine.Pin(2), nbleds)

# deende wifi configuration
sta_if = network.WLAN(network.STA_IF)

# deende MQTT configuration
client = MQTTClient(b"esp8266_01", configuration["broker"], port=1883)
connection(sta_if, leds)
init_mqtt(client, components, ilot)
client.publish(ilot+chariot, b"ok")
