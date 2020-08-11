import asyncio
import pandas as pd
import os
import paho.mqtt.client as mqtt


def initialise_idents(csv_filename="idents.csv"):
    return pd.read_csv(csv_filename, encoding='utf-8')


def idents_pour(id_produit):
    DF_Idents = initialise_idents()
    return list(DF_Idents["ident"][DF_Idents["ID objet"] == id_produit])


def Scan2Ident(scanvalue):
    "43487459001056660600010000001000"
    if len(scanvalue) == 32:
        return int(scanvalue[12:18])
    else:
        return None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

product_ident = None

def on_message(client, userdata, message):
    if message.payload == b"fin d'of":
        client.publish(topic="/stat/end/{}".format(NomIlot), payload=str(product_ident), qos=1,retain=False)
        client.publish(topic="/{}/off".format(NomIlot), payload="1", qos=0, retain=False)
        product_ident = None
    else:
        _id = Scan2Ident(message.payload)
        if _id != None:
            if _id == product_ident:
                client.publish(topic="/{}/blink".format(NomIlot), payload="1", qos=0, retain=False)
            else:
                product_ident = _id
                scan()


def scan():
    _idents = list(df_idents["ident"][df_idents["ID objet"] == product_ident])
    client.publish(topic="/stat/start/{}/of/".format(NomIlot), payload="{}".format(product_ident), qos=0,
                   retain=False)  # fait par scanner
    for _id in _idents:
        client.publish(topic="/{}/{}".format(NomIlot, _id), payload=b"0,0,0,100", qos=0, retain=False)

def startClient(client):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()


async def main():
    while 1:
        print("task", end=" ")
        await  asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
