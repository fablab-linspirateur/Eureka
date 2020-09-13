def wlan_init(idnet, network, sleep_ms):
    # initialize wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("scanning wifi")
    _reseaux = wlan.scan()
    sleep_ms(2000)
    print("found: %s" % _reseaux)
    for n in _reseaux:
        if idnet in n[0]:
            print("network", idnet, "found")
            return wlan
    return None


def do_connect(wlan, idnet, password, sleep_ms):
    # connect to Wifi
    print("connecting to", idnet)
    wlan.connect(idnet, password)
    sleep_ms(5000)
