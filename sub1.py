# python3.6

import random

from paho.mqtt import client as mqtt_client


username = input('Username: ')
password = input('Password: ')

if (username != "sub1" or password != "pass1"):
	print("User authentication failed")
	exit(0)
'''
username = "sub1"
password = "pass1"
'''


broker = 'broker.emqx.io'
port = 1883
topic = input("Enter topic (provide / to separate nested topics): ")
print("{user} has subscribed to {topic}".format(user=username,topic=topic))


# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
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

