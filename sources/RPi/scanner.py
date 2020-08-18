#!/usr/bin/python3

import asyncio
import evdev
import paho.mqtt.client as mqtt
from evdev import ecodes

# constants
TOPIC_END = "end"
TOPIC_SEARCH_BASE = "search"
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}


# connexion (async) to mqtt broker
client = mqtt.Client()
client.connect("localhost", 1883)
client.loop_start()


def getDevice():
    # get the list of all scanning devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for d in devices:
        print(d)
        if "Scanner" in d.name:
            yield d
            print("found: {}".format(d))


async def publishScan(dev):
    # read the value scanned by a device and publish a topic on mqtt broker
    scanvalue = ""
    async for ev in dev.async_read_loop():
        if ev.type == ecodes.EV_KEY:
            # print(evdev.categorize(ev))
            data = evdev.categorize(ev)
            if data.keystate == 1 and data.scancode != 42:
                if data.scancode == 28:
                    if scanvalue == "fin d4of":
                        # TODO payload should be the color associated to the device, not the device itself
                        client.publish(topic=TOPIC_END,
                                       payload="{}".format(dev), qos=0, retain=False)
                    else:
                        # TODO payload should be the color associated to the device, not the device itself
                        compound = read_compound(scanvalue)
                        client.publish(topic=TOPIC_SEARCH_BASE + "/{}".format(compound),
                                       payload="{}".format(dev), qos=0, retain=False)
                    scanvalue = ""
                else:
                    # print(scancodes[data.scancode])
                    scanvalue = scanvalue+scancodes[data.scancode]
    print("fin du scan")


def read_compound(barcode):
    if len(barcode) == 32:
        return int(barcode[12:18])
    else:
        return None


loop = asyncio.get_event_loop()

if __name__ == "__main__":

    # create async task for all scanner devices
    devices = getDevice()
    for device in devices:
        asyncio.ensure_future(publishScan(device))

    # execute the callbacks forever
    loop.run_forever()

    client.loop_stop()
