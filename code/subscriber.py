#!/usr/bin/python3

import time
import paho.mqtt.client as mqtt
import board
import neopixel
import pickle
from datetime import datetime

# configuration variable
NETWORK_PORT = 1883
BROKER_ADDRESS = "localhost"
KEEP_ALIVE = 120

# LED configuration
# TODO

pixels_1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

def on_connect(client, data, flags, rc):
    print("Connected with result code:\t", str(rc))
    client.subscribe(topic="midi-note.received", qos=1)

def on_message(client, data, message):
    message = pickle.loads(message.payload)
    delta_time = datetime.now() - message['sentAt']
    print("Audio received, delay time:\t", delta_time.total_seconds()*1000, ' ms')
    # print()
    pixels_1.fill((0, 6, 10))
    # time.sleep(0.18)
    pixels_1[10] = (0, 20, 255)
    pixels_1.fill((0, 0, 0))



client = mqtt.Client()
client. connect_async(BROKER_ADDRESS, NETWORK_PORT, KEEP_ALIVE)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()