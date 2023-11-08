#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("localhost",1883,60)

f = open("drum_patterns.mid", "rb")
imagestring = f.read()
f.close()
byteArray = bytearray(imagestring)


client.publish("topic/test", byteArray)


client.disconnect()