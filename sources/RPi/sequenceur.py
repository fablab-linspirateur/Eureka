#!/usr/bin/python3

from threading import Thread
import paho.mqtt.client as mqtt
import os


broker_url = "localhost"
#broker_url = "192.168.1.2"
broker_port = 1883
def on_message(client, userdata, message):
	print("Test_Reçu:{}".format(message.payload))

def receptionMessages():
	client = mqtt.Client()
	client.connect(broker_url, broker_port)
	client.on_message = on_message
	client.subscribe("scanner/#")
	client.loop_start()
	while 1:
		pass

	
def Scan2Ident(scanvalue):
	"0010566601000 -> 105666"
	if len(scanvalue) == 13:
		return scanvalue[2:8]
	else:
		return None
		
class Machine(Thread):
	fini = False
	ident = ""
	df_idents ={}
	product_ident = None

	def explode_topic(self, topic):
		# retrieve type + info contained in a topic
		ttopic = topic.split(sep="/", maxsplit=1)
		print("explode_topic",ttopic)
		if len(ttopic) == 1:
			return {"base": ttopic[0], "info": ""}
		else:
			print({"base": ttopic[0], "info": Scan2Ident(ttopic[1])})
			return {"base": ttopic[0], "info": Scan2Ident(ttopic[1])}
			
	def on_message(self,client, userdata, message):
		print("Reçu:{}:{}".format(message.topic,message.payload))
		_id_produit = self.explode_topic(message.topic)["info"]
		_idents = self.identspour(_id_produit)
		print(_id_produit, _idents)
		print("publish: end:{}".format(message.payload))
		self.client.publish(topic="end", payload=message.payload, qos=0, retain=False)
		
		if _idents != None:	
			for ident in _idents:
				print("publish: search/{}:{}".format(ident,message.payload))
				self.client.publish(topic="search/{}".format(ident), payload=message.payload, qos=0, retain=False)
		
	def read_csv(self):
		f = open("idents.csv", "r")
		s = f.read().split("\n")
		for line in s[1:-1]:
			_idents = line.split(",")
			key = _idents[1]
			if key in self.df_idents:
				self.df_idents[key].append(_idents[0])
			else:	
				self.df_idents[key] = [_idents[0]]
		f.close()

	def __init__(self,NomIlot="Logistique"):
		Thread.__init__(self)
		self.NomIlot = NomIlot
		self.client = mqtt.Client()
		self.client.connect(broker_url, broker_port)
		self.client.on_message = self.on_message
		self.client.subscribe("scanner/#")
		
		self.state = "enCours"
		self.Etats={"enCours":{"Action":self.enCours,"EtatSuivant":"enCours"}}
		self.read_csv()#pd.read_csv("idents.csv",encoding='utf-8')
		
		self.client.loop_start()
	
	def identspour(self,ident_produit):
		print("recherche:{} dans {}".format(ident_produit,self.df_idents))
		_idents = self.df_idents[ident_produit]
		return _idents
		
	def enCours(self):
		pass #Attente d'un scan
		

	def run(self):
		while not self.fini:
			self.Etats[self.state]["Action"]()
			self.state = self.Etats[self.state]["EtatSuivant"]
			#self.client.loop() loop_start à la place ?
		self.client.loop_stop()
			
	
def testIdents():
	print("idents_pour(566606)",idents_pour(566606))
	print("idents_pour(566602)",idents_pour(566602))
	print("idents_pour(563457)",idents_pour(563457))

def testFunction():
	receptionMessages()
def testread_csv():
	df_idents={}
	f = open("idents.csv", "r")
	s = f.read().split("\n")
	for line in s[1:-1]:
		_idents = line.split(",")
		
		key = _idents[1]
		if key in df_idents:
			df_idents[key].append(_idents[0])
		else:	
			df_idents[key] = [_idents[0]]
	print(df_idents["448861"])
	f.close()

if __name__ == "__main__":
	#testFunction()
	#testIdents()
	#testread_csv()
	#idents_pour("438132")
	m=Machine()
	m.start()
