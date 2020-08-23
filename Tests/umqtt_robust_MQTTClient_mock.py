class MQTTClient():
    def __init__(self, name, broker, port):
        self.name = name
        self.broker = broker
        self.port = port
        self.is_connected = False
        self.topics = []
        self.callback = None

    def connect(self):
        self.is_connected = True
        return not self.is_connected

    def subscribe(self, topic):
        self.topics.append(topic)

    def set_callback(self, callback):
        self.callback = callback
