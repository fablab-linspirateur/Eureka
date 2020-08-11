try:
    import utime
except:
    import time as utime

class displayer():
    # displayer class manage calculation of display of information

    def __init__(self, components_file="testComponents.txt"):
        # initialize constants and leds + retrieve file infos and initialize mqtt
        self.LED_OFF = (0, 0, 0, 0)
        self.LED_GREEN = (0, 100, 0, 0)
        self.LED_RED = (100, 0, 0, 0)
        self.TOPIC_END = "end"
        self.TOPIC_SEARCH_BASE = "search"
        self.TOPIC_ERROR_BASE = "error"
        self.components = self.get_components(components_file)
        self.displayed = {}
        for component in self.components:
            self.displayed[component] = {}

    def refresh(self, topic, payload):
        # refresh display on topic action
        etopic = self.explode_topic(topic)
        if etopic["type"] == self.TOPIC_SEARCH_BASE:
            self.display_component(etopic["info"], payload)
        elif etopic["type"] == self.TOPIC_END:
            self.turn_off(payload)
        elif etopic["type"] == self.TOPIC_ERROR_BASE:
            self.display_error(etopic["info"], payload)
    def get_configuration(self, file_path):
        pass
    def get_components(self, file_path):
        # get the list of components stored in the configuration file
        f = open(file_path)
        content = f.read()
        f.close()
        choice = content.split("\n")
        config = {}
        for kv in choice:
            key, val = kv.split(":")
            key = key.strip()
            config[key] = val.strip()[1:-1]
        return config

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
        # TODO move calls to self.leds in boot.py, just keep calculation of color display here
        utime.sleep_ms(500)
        self.leds[0] = self.LED_GREEN
        self.leds.write()
        print(".")
        utime.sleep_ms(500)
        self.leds[0] = self.LED_OFF
        self.leds.write()
