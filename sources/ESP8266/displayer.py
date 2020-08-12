class displayer():
    # displayer class manage calculation of display of information

    def __init__(self, components_file="components.txt"):
        # initialize constants and leds + retrieve file infos and initialize mqtt
        self.LED_OFF = (0, 0, 0, 0)
        self.LED_GREEN = (0, 100, 0, 0)
        self.LED_RED = (100, 0, 0, 0)
        self.COLOR_BLACK = 0x00000000
        self.MAX_COLOR = 4
        self.TOPIC_END = "end"
        self.TOPIC_SEARCH_BASE = "search"
        self.TOPIC_ERROR_BASE = "error"
        self.displayed = {}
        for component in self.get_components(components_file):
            self.displayed[component] = {0: [1, 8]}

    def explode_topic(self, topic):
        # retrieve type + info contained in a topic
        ttopic = topic.split(sep="/", maxsplit=1)
        if len(ttopic) == 1:
            return {"base": ttopic[0], "info": ""}
        else:
            return {"base": ttopic[0], "info": ttopic[1]}

    def to_color(self, hexa_color):
        # convert color to neopixel color
        r = hexa_color >> 24
        v = (0x00ff0000 & hexa_color) >> 16
        b = (0x0000ff00 & hexa_color) >> 8
        w = (0x000000ff & hexa_color)
        return (r, v, b, w)

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

    def refresh(self, topic, payload):
        # refresh display on topic action
        etopic = self.explode_topic(topic)
        if etopic["type"] == self.TOPIC_SEARCH_BASE:
            self.display_component(etopic["info"], payload)
        elif etopic["type"] == self.TOPIC_END:
            self.turn_off(payload)
        elif etopic["type"] == self.TOPIC_ERROR_BASE:
            self.display_error(etopic["info"], payload)

    def update(self, disp_comp):
        # update color table for a displayed component
        start = disp_comp[0x00000000][0]
        end = disp_comp[0x00000000][1]
        nbcolor = len(disp_comp.keys())-1
        try:
            pas = int((end-start)/nbcolor)
        except:
            pas = int(end-start)

        prev = start
        for i, c in enumerate(disp_comp.keys()):
            if c == 0:
                # ne pas effacer la color 0
                continue
            disp_comp[c] = [prev, (i*pas)+start]
            prev = disp_comp[c][1]+1
        disp_comp[c][1] = end

    def add(self, disp_comp, color):
        # add a color to a displayed component
        if color == self.COLOR_BLACK:
            return
        if len(disp_comp) == self.MAX_COLOR + 1:
            return
        disp_comp[color] = []
        self.update(disp_comp)

    def remove(self, disp_comp, color):
        # remove a color from a displayed component
        if color == self.COLOR_BLACK:
            return
        try:
            del(disp_comp[color])
        except:
            return
        self.update(disp_comp)

    def display_component(self, component, color):
        # display a component in a color
        if component in self.displayed:
            self.add(self.displayed[component], color)

    def turn_off(self, color):
        # turn off all LEDs that have been turned on for a specific color
        for component in self.displayed:
            self.remove(self.displayed[component], color)

    def display_error(self, message, color):
        # display an error
        return null

#    def info_leds(self):
        # make the first LED blink green
        # TODO move calls to self.leds in boot.py, just keep calculation of color display here
        # utime.sleep_ms(500)
        #self.leds[0] = self.LED_GREEN
        # self.leds.write()
        # print(".")
        # utime.sleep_ms(500)
        #self.leds[0] = self.LED_OFF
        # self.leds.write()
