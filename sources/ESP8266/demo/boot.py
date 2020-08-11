import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient

# Just turn the leds on in the Fablab
Idents=[b"564990",b"559849",b"566970",
           b"419743",b"551776",b"563582",
           b"567368",b"419607",b"567367",
           b"439893",b"805788",b"569558",
           b"559992",b"418991",b"557031"]

def init_mqtt(name, broker):
    # initialize mqtt subscriptions
    print("connect mqtt...")
    client = MQTTClient(
        name, broker, port=1883)
    res = client.connect()
    if not res:
        client.set_callback(sub_cb)
        client.subscribe(b"end")
        client.subscribe(b"search/#")
        return client
    return None

def calculerEmplacement(recherche):
    tailleDunePosition=10
    debut=(Idents.index(recherche)*tailleDunePosition)
    a_piloter = [i for i in range(debut,debut+tailleDunePosition)]
    return a_piloter

def effacer():
    for i in range(NB_LEDS):
        Leds[i]=(0,0,0)
    Leds.write()
    
def piloter(recherche=b"",couleur=b""):
    print("topic:",recherche," payload:",couleur)
    if recherche == b"end":
        effacer()
        return
    id = recherche.strip(b"search/")
    if ( id not in Idents):
        return
    for i in calculerEmplacement(id):
        Leds[i]=(100,100,100)
    Leds.write()

def sub_cb(topic, payload):
    # mqtt callback
    piloter(topic,payload)


def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Fablab-inspirateur', 'Choiseul.67220')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

# define leds configuration
NB_LEDS = 150
Leds = neopixel.NeoPixel(machine.Pin(2), NB_LEDS)

# define wifi configuration
do_connect()

# define MQTT configuration
client = init_mqtt("demo logistique", "192.168.1.2")

