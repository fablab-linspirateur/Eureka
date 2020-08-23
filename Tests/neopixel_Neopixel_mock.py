class NeoPixel(list):
    def __init__(self, pin, nb_leds):
        for i in range(nb_leds):
            self.append(None)
        self.pin = pin
        self.nb_leds = nb_leds
        self.nb_write = 0

    def write(self):
        self.nb_write = self.nb_write + 1
