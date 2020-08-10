import machine
import neopixel
import utime


class displayer(self):
    # displayer class manage mqtt connection + display of information using NeoPixel LEDs

    def __init__(self, components_file="components.txt", config_file="config.yaml"):
        # initialize constants and leds + retrieve file infos and initialize mqtt
        self.LED_OFF = (0, 0, 0, 0)
        self.LED_GREEN = (0, 100, 0, 0)
        self.LED_RED = (100, 0, 0, 0)
        self.TOPIC_END = "end"
        self.TOPIC_SEARCH_BASE = "search"
        self.TOPIC_ERROR_BASE = "error"
        self.NB_LEDS = 150
        self.leds = neopixel.NeoPixel(machine.Pin(2), self.NB_LEDS)
        self.components = self.get_components(components_file)
        self.config = self.get_config(config_file)
        self.init_mqtt(self.config["name"], self.config["broker"])
        self.displayed = {}
        for component in self.components:
            self.displayed[component] = {}

    def init_mqtt(self, name, broker):
        # initialize mqtt subscriptions
        print("connect mqtt...")
        self.client = MQTTClient(
            name, broker, port=1883)
        res = self.client.connect()
        if not res:
            self.client.subscribe(self.TOPIC_END)
            self.client.subscribe(self.TOPIC_SEARCH_BASE+"/*")
            self.client.subscribe(self.TOPIC_ERROR_BASE+"/*")
            self.client.set_callback(self.sub_cb)

    def sub_cb(self, topic, payload):
        # mqtt callback
        etopic = self.explode_topic(topic)
        if etopic["type"] == self.TOPIC_SEARCH_BASE:
            self.display_component(etopic["info"], payload)
        elif etopic["type"] == self.TOPIC_END:
            self.turn_off(payload)
        elif etopic["type"] == self.TOPIC_ERROR_BASE:
            self.display_error(etopic["info"], payload)
        utime.sleep_ms(100)
        self.leds.write()

    def get_config(self, config_file):
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

    def get_components(self, file_path):
        # get the list of components stored in the configuration file
        f = open(file_path)
        config = f.read()
        f.close()
        choix = config.split("\n")
        components = []
        for kv in choix:
            components.append(kv.strip())
        return components

    def explode_topic(self, topic):
        # retrieve type + info contained in a topic
        ttopic = topic.split(sep="/", maxsplit=1)
        if len(ttopic) == 1:
            return {"base": ttopic[0], "info": ""}
        else:
            return {"base": ttopic[0], "info": ttopic[1]}

    def update(self, component):
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
                # ne pas effacer la color 0
                continue
            component[c] = [prev, (i*pas)+start]
            prev = component[c][1]+1
        component[c][1] = end

    def add(self, disp_comp, color):
        # add a color to a component
        disp_comp[color] = []
        self.update(disp_comp)

    def remove(self, disp_comp, color):
        # remove a color from a component
        try:
            del(disp_comp[color])
        except:
            return
        self.update(disp_comp)

    def display_component(self, component, color):
        # display a specific component in a specific color
        self.add(self.displayed[component], color)

    def turn_off(self, color):
        # turn off all LEDs that have been turned on for a specific color
        for component in self.components:
            self.remove(self.displayed[component], color)

    def display_error(self, message, color):
        # display an error
        return null

    def to_color(self, n24):
        # convert color to neopixel color
        r = n24 >> 16
        v = (0x00ff00 & n24) >> 8
        b = (0x0000ff & n24)
        return (r, v, b)

    def info_leds(self):
        # make the first LED blink green
        utime.sleep_ms(500)
        self.leds[0] = self.LED_GREEN
        self.leds.write()
        print(".")
        utime.sleep_ms(500)
        self.leds[0] = self.LED_OFF
        self.leds.write()
