NB_LEDS = 150
LED_OFF = (0, 0, 0)
component_leds = {}
components = []
backgrounds = {}
COLOR_BLACK = 0x000000
MAX_COLOR = 4


def init_component_leds(comps, cleds=component_leds):
    components = comps
    for component in components:
        cleds[component] = []


def init_nb_leds(nb):
    NB_LEDS = nb


def display_component(component, color, cleds=component_leds):
    # display a component in a color
    if component in cleds:
        add(cleds[component], color)


def turn_off(color, cleds=component_leds):
    # turn off all LEDs that have been turned on for a specific color
    for component in cleds:
        remove(cleds[component], color)


def turn_all(color=0x000000, nb=NB_LEDS):
    # turn all LEDs to the color
    result = []
    for i in range(nb):
        result.append(to_color(color))
    return result


def display_error(message, color):
    # display an error
    return


def display_background(component, color, comps=components, backs=backgrounds):
    # change the background color of a component
    # print("display_background")
    #print(component, color, comps, backs)
    if component in comps:
        if component in backs:
            if color == backs[component]:
                del(backs[component])
        else:
            backs[component] = color
    #print(component, color, comps, backs)


def neo_write(t_color, sleep, nb=NB_LEDS):
    # write a table of colors to neopixel
    import machine
    from neopixel import NeoPixel
    leds = NeoPixel(machine.Pin(2), nb)
    for i, color in enumerate(t_color):
        leds[i] = color
    sleep(100)
    leds.write()


def to_color(color):
    # convert color to neopixel color
    r = color >> 16
    v = (0x00ff00 & color) >> 8
    b = (0x0000ff & color)
    return (r, v, b)


def to_neopixel(comps=components, cleds=component_leds, backs=backgrounds):
    result = []
    # print("to_neopixel")
    #print(comps, cleds, backs)
    for component in comps:
        bg = LED_OFF
        if component in backs:
            bg = to_color(backs[component])
        back_leds = [bg]*(5 - len(cleds[component]))
        result += back_leds
        for color in cleds[component]:
            neocolor = to_color(color)
            result += [neocolor]*2
        result += back_leds
    #print(comps, cleds, backs)
    return result


def flash(color, sleep):
    # flash all leds in the desired color
    neo_write(turn_all(color), sleep)
    sleep(1000)
    neo_write(turn_all(), sleep)


def add(colors, color):
    # add a color to a component
    if color == COLOR_BLACK:
        return
    if len(colors) == MAX_COLOR:
        return
    if color in colors:
        return
    colors.append(color)


def remove(colors, color):
    # remove a color from a component
    try:
        colors.remove(color)
    except:
        return
