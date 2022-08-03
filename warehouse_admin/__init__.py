from . import mqtt

client = mqtt.MQTTClient("localhost", 1883, 60, "drone")
client.run()