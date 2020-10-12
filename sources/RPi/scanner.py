#!/usr/bin/python3

import evdev
from evdev import ecodes
import asyncio
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883)
#client.connect("192.168.1.2", 1883)
client.loop_start()

r=0x10000
v=0x100
b=0x1
couleurs=[  0*r+200*v+0*b,0*r+0*v+200*b,250*r+50*v+100*b]

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u')', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'a', 17: u'z', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'^', 27: u'$', 28: u'CRLF', 29: u'LCTRL',
    30: u'q', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u'm',
    40: u'%', 41: u'*', 42: u'LSHFT', 43: u'<', 44: u'w', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u',', 51: u'.', 52: u':', 53: u'!', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

scanners={}

def getDevice():
    print("looking for scanners ...")
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for i,d in enumerate(devices):
        print(d)
        if "Scanner" in d.name:
            scanners[d.phys] = d
            scanners[d.phys].couleur = couleurs[i]
            yield d
            print("=============\nfound: {}".format(d.phys))
    print("finish")

def envoyerFin(dev):
    """ topic:end, payload:couleur courante """
    client.publish(topic="end", payload="{}".format(scanners[dev].couleur), qos=0, retain=False)

def envoyer(dev,scanvalue):
    """ topic:scanner/code, payload:couleur courante """
    print("scanner/{}".format(scanvalue), "payload={}".format(scanners[dev].couleur))
    client.publish(topic="scanner/{}".format(scanvalue), payload="{}".format(scanners[dev].couleur), qos=0, retain=False)

# def hoooputain(dev,couleur):
#     """ topic:end, payload:couleur courante passage à la nouvelle couleur """
#     print("hoooputain", dev,"<<<<",couleur)
#     couleur = couleur.split(".:")[-1] # remove "couleur. or couleur:"
#     client.publish(topic="end", payload="{}".format(scanners[dev].couleur), qos=0, retain=False)
#     scanners[dev].couleur = couleurs[couleur]

async def publishScan(dev):
    scanvalue = ""
    async for ev in dev.async_read_loop():
        if ev.type == ecodes.EV_KEY:
            #print(evdev.categorize(ev))
            data = evdev.categorize(ev)
            if data.keystate ==1 and data.scancode != 42 :
                if data.scancode == 28:
                    print(dev,"->",scanvalue)
                    if scanvalue == "effacer":
                        envoyerFin(dev.phys)
                    else:
                        envoyer(dev.phys,scanvalue)
                    scanvalue = ""
                else:
                    #print(scancodes[data.scancode])
                    scanvalue = scanvalue+scancodes[data.scancode]
    print("fin du scan")

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    devices = getDevice()
    print(">>>>>>",devices)
    for device in devices:
        asyncio.ensure_future(publishScan(device))
 
    loop.run_forever()
    client.loop_stop()
