import paho.mqtt.client as mqtt
import time 
import board 
import neopixel

pixels_1 = neopixel. NeoPixel(board. D18, 55, brightness=1)
x = 0

def on_connect(client, data, flags, rc):
    print("Connected with result code:\t", str(rc))
    client.subscribe("midi-note.received")

def on_message(client, data, message):
    print("Audio received:\t", message.payload)
    pixels_1.fill((0, 220, 0))
    pixels_1[10] = (0, 20, 255)
    pixels_1.fill((0, 0, 0))


broker = "localhost"
port = 1884
client = mqtt.Client()
client. conect_async(broker, port, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()