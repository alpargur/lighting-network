#!/usr/bin/python3

import time
import paho.mqtt.client as mqtt
import board
import neopixel
import pickle
from datetime import datetime

# configuration variable
NETWORK_PORT = 1884
BROKER_ADDRESS = 'localhost'
KEEP_ALIVE = 120 # in seconds
SOURCE_TOPIC = "midi-note.received"

# LED configuration
GIO_PIN = board.D18
LED_COUNT = 60
BRIGHTNESS = 20
QOS = 1 # Quality of Service level, possible values => 0, 1, 2

led_strip = neopixel.NeoPixel(GIO_PIN, LED_COUNT, brightness=BRIGHTNESS)

# midi key and led mappings
drum_kit = {
    'ride': 51, 'crash': 49, 'hi-tom': 47, 'open-hi-hat': 46, 'mid-tom': 45, 'low-tom': 44, 'snare-drum': 43, 
    'clap': 39, 'rim-shot': 37, 'bass-drum': 36
}



def on_connect(client, data, flags, rc):
    print("Connected with result code:\t", str(rc))
    client.subscribe(SOURCE_TOPIC, QOS)

def on_message(client, data, message):
    message = pickle.loads(message.payload)
    # delta_time = datetime.now() - message['sentAt']
    # print("Audio received, delay time:\t", delta_time.total_seconds()*1000, ' ms')
    midi_key = message['keyNumber']

    if midi_key == drum_kit['bass-drum'] :
        led_strip[:5].fill((255, 0, 0))
        time.sleep(0.18)
        led_strip[:5].fill((0, 0, 0))

    elif midi_key == drum_kit['clap'] :
        led_strip[5:11] = ((255, 255, 0))
        time.sleep(0.18)
        led_strip[17:23].fill((0, 0, 0))

    elif midi_key == drum_kit['crash'] :
        led_strip[11:17] = ((255, 0, 255))
        time.sleep(0.18)
        led_strip[17:23].fill((0, 0, 0))

    elif midi_key == drum_kit['hi-tom'] :
        led_strip[17:23] = ((0, 0, 255))
        time.sleep(0.18)
        led_strip[17:23].fill((0, 0, 0))
    
    # print()
    # led_strip.fill((0, 6, 10))
    # time.sleep(0.18)
    # led_strip[10] = (0, 20, 255)
    # led_strip.fill((0, 0, 0))



client = mqtt.Client()
client. connect_async(BROKER_ADDRESS, NETWORK_PORT, KEEP_ALIVE)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()