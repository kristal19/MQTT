# python3.6

import random
from xmlrpc.client import SYSTEM_ERROR

from paho.mqtt import client as mqtt_client


username = input('Username: ')
password = input('Password: ')

if (username != "sub2" or password != "pass2"):
	print("User authentication failed")
	exit(0)
'''
username = "sub2"
password = "pass2"
'''


broker = 'broker.emqx.io'
port = 1883
topic = input("Enter topic (provide / to separate nested topics:) ")
print("{user} has subscribed to {topic}".format(user=username,topic=topic))


# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, transport = "websockets")
    client.username_pw_set(username, password)
    #client.ws_set_options(path = "/mqtt")
    client.on_connect = on_connect
    client.connect(broker, port=8083)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

