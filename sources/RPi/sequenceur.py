#!/usr/bin/python3

from threading import Thread
import paho.mqtt.client as mqtt
import os

# constants
TOPIC_END = "end"
TOPIC_SEARCH_BASE = "search"
TOPIC_ERROR_NO_COMPONENTS = "error/no-components"
TOPIC_BACKGROUND_BASE = "bg"

broker_url = "localhost"
# broker_url = "192.168.1.2"
broker_port = 1883


def on_message(client, userdata, message):
    print("Test_Reçu:{}".format(message.payload))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def receptionMessages():
    client = mqtt.Client()
    client.connect(broker_url, broker_port)
    client.on_message = on_message
    client.subscribe("scanner/#")
    client.loop_start()
    while 1:
        pass


class Machine(Thread):
    fini = False
    ident = ""
    components = {}
    product_ident = None

    def __init__(self, NomIlot="Logistique"):
        Thread.__init__(self)
        self.NomIlot = NomIlot
        self.client = mqtt.Client()
        self.client.connect(broker_url, broker_port)
        self.client.on_message = self.on_message
        self.client.subscribe("scanner/#")

        self.state = "enCours"
        self.Etats = {"enCours": {
            "Action": self.enCours, "EtatSuivant": "enCours"}}
        self.read_csv()  # pd.read_csv("idents.csv",encoding='utf-8')

        self.client.loop_start()

	def is_compound(self, ident):
		return len(ident) == 13

	def is_component(self, ident):
		return len(ident) == 6

    def explode_topic(self, topic):
        # retrieve type + info contained in a topic
        ttopic = topic.split(sep="/", maxsplit=1)
        print("explode_topic", ttopic)
        if len(ttopic) == 1:
            return {"base": ttopic[0], "info": ""}
        else:
            print({"base": ttopic[0], "info": ttopic[1]})
            return {"base": ttopic[0], "info": ttopic[1]}

    def on_message(self, client, userdata, message):
        print("Reçu:{}:{}".format(message.topic, message.payload))
		ident = self.explode_topic(message.topic)["info"]
		if self.is_compound(ident):
			_compound = ident[2:8]
			_components = self.composantspour(_compound)
			print(_compound, _components)
            print("publish: {}:{}".format(TOPIC_END, message.payload))
            self.client.publish(
                topic=TOPIC_END, payload=message.payload, qos=0, retain=False)
			if _components != None:
				for ident in _components:
					print("publish: {}/{}:{}".format(TOPIC_SEARCH_BASE,
													ident, message.payload))
					self.client.publish(topic=TOPIC_SEARCH_BASE+"/{}".format(ident),
										payload=message.payload, qos=0, retain=False)
		elif self.is_component(ident):
			self.client.publish(topic=TOPIC_BACKGROUND_BASE+"/{}".format(ident),
										payload=message.payload, qos=0, retain=False)

    def read_csv(self):
        f = open("idents.csv", "r")
        s = f.read().split("\n")
        for line in s[1:-1]:
            _idents = line.split(",")
            key = _idents[1]
            if key in self.components:
                self.components[key].append(_idents[0])
            else:
                self.components[key] = [_idents[0]]
        f.close()

    def composantspour(self, compose):
        print("recherche:{} ".format(compose))
        _composants = self.components[compose]
        print("trouve: {}".format(_composants))
        return _composants

    def enCours(self):
        pass  # Attente d'un scan

    def run(self):
        while not self.fini:
            self.Etats[self.state]["Action"]()
            self.state = self.Etats[self.state]["EtatSuivant"]
            # self.client.loop() loop_start à la place ?
        self.client.loop_stop()


if __name__ == "__main__":
    m = Machine()
    m.start()
