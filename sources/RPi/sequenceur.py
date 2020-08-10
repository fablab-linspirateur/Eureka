import paho.mqtt.client as mqtt
import asyncio


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
