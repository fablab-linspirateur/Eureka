class displayer():
    # displayer class manage calculation of display of information

    def __init__(self, sleep, leds, nb_leds=0, components_file="components.txt", config={}):
        # initialize constants and leds + retrieve file infos and initialize mqtt
        self.LED_OFF = (0, 0, 0)
        self.COLOR_BLACK = 0x000000
        self.MAX_COLOR = 4
        self.TOPIC_END = "end"
        self.TOPIC_SEARCH_BASE = "search"
        self.TOPIC_ERROR_BASE = "error"
        self.NB_LEDS = nb_leds
        self.displayed = {}
        self.components = []
        self.leds = leds
        self.sleep = sleep
        self.components = self.get_components(components_file)
        for component in self.components:
            self.displayed[component] = []
        self.config = config

    def neo_write(self, t_color):
        # write a table of colors to neopixel
        for i, color in enumerate(t_color):
            self.leds[i] = color
        self.sleep(100)
        self.leds.write()

    def init_mqtt(self, client):
        # initialize mqtt subscriptions
        client.set_callback(self.refresh)
        client.subscribe(self.TOPIC_END)
        client.subscribe(self.TOPIC_SEARCH_BASE+"/#")
        client.subscribe(self.TOPIC_ERROR_BASE+"/#")

    def explode_topic(self, topic):
        # retrieve type + info contained in a topic
        ttopic = topic.split("/", 1)
        if len(ttopic) == 1:
            return {"base": ttopic[0], "info": ""}
        else:
            return {"base": ttopic[0], "info": ttopic[1]}

    def to_color(self, hexa_color):
        # convert color to neopixel color
        r = hexa_color >> 16
        v = (0x00ff00 & hexa_color) >> 8
        b = (0x0000ff & hexa_color)
        return (r, v, b)

    def get_components(self, file_path):
        # get the list of components stored in the configuration file
        f = open(file_path)
        content = f.read()
        f.close()
        choix = content.split("\n")
        components = []
        for kv in choix:
            if kv != "":
                components.append(kv.strip())
        return components

    def to_neopixel(self):
        result = []
        for component in self.components:
            blacks = [self.LED_OFF]*(5 - len(self.displayed[component]))
            result += blacks
            for color in self.displayed[component]:
                neocolor = self.to_color(color)
                result += [neocolor]*2
            result += blacks
        return result

    def refresh(self, topic, payload):
        # refresh display on topic action
        etopic = self.explode_topic(topic.decode("utf-8"))
        if etopic["base"] == self.TOPIC_SEARCH_BASE:
            self.display_component(etopic["info"], int(payload))
        elif etopic["base"] == self.TOPIC_END:
            self.turn_off(int(payload))
        elif etopic["base"] == self.TOPIC_ERROR_BASE:
            self.display_error(etopic["info"], int(payload))
        self.neo_write(self.to_neopixel())

    def add(self, disp_comp, color):
        # add a color to a displayed component
        if color == self.COLOR_BLACK:
            return
        if len(disp_comp) == self.MAX_COLOR:
            return
        if color in disp_comp:
            return
        disp_comp.append(color)

    def remove(self, disp_comp, color):
        # remove a color from a displayed component
        try:
            disp_comp.remove(color)
        except:
            return

    def display_component(self, component, color):
        # display a component in a color
        if component in self.displayed:
            self.add(self.displayed[component], color)

    def turn_off(self, color):
        # turn off all LEDs that have been turned on for a specific color
        for component in self.displayed:
            self.remove(self.displayed[component], color)

    def all(self, color=0x000000):
        # turn all LEDs to the color
        result = []
        for i in range(self.NB_LEDS):
            result.append(self.to_color(color))
        self.neo_write(result)

    def display_error(self, message, color):
        # display an error
        return
