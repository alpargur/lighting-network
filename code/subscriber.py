#!/usr/bin/python3

import pickle
import paho.mqtt.client as mqtt
import board 
import neopixel

# configuration variable
NETWORK_PORT = 1883
BROKER_ADDRESS = "localhost"
KEEP_ALIVE = 60

# LED configuration
# TODO

pixels_1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

def on_connect(client, data, flags, rc):
    print("Connected with result code:\t", str(rc))
    client.subscribe("midi-note.received")

def on_message(client, data, message):
    print("Audio received:\t", pickle.loads(message.payload))
    pixels_1.fill((0, 220, 0))
    # pixels_1[10] = (0, 20, 255)
    pixels_1.fill((0, 0, 0))



client = mqtt.Client()
client. connect_async(BROKER_ADDRESS, NETWORK_PORT, KEEP_ALIVE)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()