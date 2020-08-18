import asyncio
import os
import paho.mqtt.client as mqtt
import finder

# constants
TOPIC_END = "end"
TOPIC_SEARCH_BASE = "search"
TOPIC_ERROR_NO_COMPONENTS = "error/no-components"

find = finder()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message):
    client.publish(topic=TOPIC_END, payload=message.payload,
                   qos=1, retain=False)
    etopic = find.explode_topic(message.topic)
    components = find.search_components(etopic["info"])
    if size(components) == 0:
        client.publish(topic=TOPIC_ERROR_NO_COMPONENTS,
                       payload=message.payload, qos=1, retain=False)
    else:
        for component in components:
            client.publish(topic=TOPIC_SEARCH_BASE + "/{}".format(component),
                           payload=message.payload, qos=1, retain=False)


def start_client():
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
    start_client
    asyncio.run(main())
