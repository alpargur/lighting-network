import paho.mqtt.client as mqtt
from mido import MidiFile
# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
    f = open('drum_patterns_2.mid', 'wb')
    f.write(msg.payload)
    print("audio Received")


    f.close()
    client.disconnect()
    
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message
mid = MidiFile('drum_patterns_2.mid', clip=True)
print(mid)
client.loop_forever()