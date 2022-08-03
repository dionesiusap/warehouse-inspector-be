import paho.mqtt.client as mqtt
import datetime
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
payload_json = {
    "name": "Package D",
    "status": True,
    "position": "B2-5",
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
    "image": "https://media.istockphoto.com/photos/cardboard-box-isolated-on-white-background-with-clipping-path-picture-id1282219840?b=1&k=20&m=1282219840&s=170667a&w=0&h=FAo7lLqh8cmjPzAmXMjnsVx-fZxBn1iEmchcAH_jQTw=",
    "batch": 4
}
print(payload_json)
payload_msg = json.dumps(payload_json)
res = client.publish("drone", payload_msg, qos=1)
