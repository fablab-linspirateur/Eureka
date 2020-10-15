from configuration import get_config
from leds import init_nb_leds
from umqtt.simple import MQTTClient

# define configuration
NB_LEDS = 150
init_nb_leds(NB_LEDS)
config = get_config()
client = MQTTClient(config["name"], config["broker"], port=config["port"])
wlan = None

