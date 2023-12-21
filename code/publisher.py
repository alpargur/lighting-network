#!/usr/bin/python3

import rtmidi
import paho.mqtt.client as mqtt
import pickle
from datetime import datetime

## configuration variables
NETWORK_IP = '172.20.10.2'
NETWORK_PORT = 1884
KEEP_ALIVE = 121
DESTINATION_TOPIC = "midi-note.received"
MIDI_PORT = 0 # virtual bus midi port

def midi_publisher(midi_in, client):
    ## get the available midi input ports
    midi_ports = range(midi_in.getPortCount())

    if not midi_ports:
        print("No MIDI input port's available.")
        return

    midi_in.openPort(MIDI_PORT)
    print("Listening to MIDI input on port: ", midi_in.getPortName(MIDI_PORT))

    ## set the callback function to handle incoming MIDI messages
    midi_in.setCallback(midi_handler)

    try:
        input("Press Enter to exit...\n")
    except KeyboardInterrupt:
        pass

    # Clean up
    midi_in.closePort()
    midi_in.cancelCallback()
    client.disconnect()

def midi_handler(midi):
    if midi.isNoteOn():
        # print('MIDI NOTE PUBLISHED')
        print('ON:\t', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity(), '\n')

        # publish message 
        # TODO: parse and serialize midi messages
        client.publish(topic=DESTINATION_TOPIC, payload=midi_serializer(midi), qos=1)

    elif midi.isNoteOff():
        print('OFF:\t', midi.getMidiNoteName(midi.getNoteNumber()), '\n')
        client.publish(DESTINATION_TOPIC, midi_serializer(midi))

    elif midi.isController():
        print('MIDI Controller Number:\t' + midi.getControllerNumber() + '\tMIDI Controller Value:\t' + midi.getControllerValue())

def midi_serializer(midi):
    midi_message = {
        'noteOn': midi.isNoteOn(),
        'key': midi.getMidiNoteName(midi.getNoteNumber()),
        'keyNumber': midi.getNoteNumber(),
        'velocity': midi.getVelocity(),
        'sentAt': datetime.now()
    }
    print(midi_message)
    return pickle.dumps(midi_message)

if __name__ == "__main__": 
    midi_in = rtmidi.RtMidiIn()
    ## establish mqtt connection 
    client = mqtt.Client()
    client.connect(NETWORK_IP, NETWORK_PORT, KEEP_ALIVE)
    midi_publisher(midi_in, client)
    