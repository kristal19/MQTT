# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


username = input('Username: ')
password = input('Password: ')

if (username != "pub1" or password != "pass1"):
	print("User authentication failed")
	exit(0)
'''
username = "pub1"
password = "pass1"
'''


broker = 'broker.emqx.io'
port = 1883
topic = input("Enter topic (provide / to separate nested topics): ")
nested= topic.split("/")
print("{user} has subscribed to {topic}".format(user=username,topic=topic))


# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt():
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
    print(client)
    return client


def publish(client):
    msg_count = 0
    while msg_count <10:
        time.sleep(1)
        msg = input("enter message: ")
        
        j= nested[0] #j=dance
        for i in range(1, len(nested)+1): #i=2
        	result = client.publish(j, msg) #j= dance
        	status = result[0]
        	if status == 0:
        		print(f"Send `{msg}` to topic `{j}`")
        	else:
        		print(f"Failed to send message to topic {j}")
        	msg_count += 1
        	if i<len(nested):
        		j= j + "/" + nested[i] #j=dance/hiphop
        
        '''
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
        	print(f"Send `{msg}` to topic `{topic}`")
        else:
        	print(f"Failed to send message to topic {topic}")
        msg_count += 1
        '''  


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

