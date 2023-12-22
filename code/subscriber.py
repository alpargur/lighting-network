#!/usr/bin/python3

import time
import paho.mqtt.client as mqtt
import board
import neopixel
import pickle
from datetime import datetime

from configuration import drum_kit

# configuration variable
NETWORK_PORT = 1883
BROKER_ADDRESS = 'localhost'
KEEP_ALIVE = 120 # in seconds
SOURCE_TOPIC = "midi-note.received"

# LED configuration
GIO_PIN = board.D18
LED_COUNT = 60
BRIGHTNESS = 20
OFF = (0, 0, 0)
QOS = 0 # Quality of Service level, possible values => 0, 1, 2

led_strip = neopixel.NeoPixel(GIO_PIN, LED_COUNT, brightness=BRIGHTNESS)


def on_connect(client, data, flags, rc):
    print("Connected with result code:\t", str(rc))
    client.subscribe((SOURCE_TOPIC, QOS))

def on_message(client, data, message):
    message = pickle.loads(message.payload)
    midi_key = message['keyNumber']
    note_on = message['noteOn']

    print(type(midi_key))
    # light_up(note_on, drum_kit[midi_key])

def light_up(note_on, drum_element):

    color = led_strip[i] = OFF
    if note_on:
        color = drum_element['color']

    for i in drum_element['range']:
        led_strip[i] = color
    led_strip.show()

def calculate_delay(sent_at):
    delta_time = datetime.now() - sent_at
    print("Midi received, delay time:\t", delta_time.total_seconds()*1000, " ms")

def get_qos(messasge):
    print("QoS:\t", str(message.qos))
client = mqtt.Client(client_id='midi-lights', clean_session=False)
client.connect_async(BROKER_ADDRESS, NETWORK_PORT, KEEP_ALIVE)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()