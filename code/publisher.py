import rtmidi
import paho.mqtt.client as mqtt

## configuration variables
network_ip = "172.20.10.14"
network_port = 1884
keep_alive = 60
topic = "midi-note.received"

## establish mqtt connection
client = mqtt.Client()
client.connect(network_ip, network_port, keep_alive)

## create a midi-in channel
midi_in = rtmidi.RtMidiIn()

def publish_message(midi):
    if midi.isNoteOn():
        print('ON:\t', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
        # publish message
        client.publish(topic, "hello world")
        print('MIDI NOTE PUBLISHED')

    elif midi.isNoteOff():
        print('OFF:\t', midi.getMidiNoteName(midi.getNoteNumber()))

    elif midi.isController():
        print('MIDI Controller Number:\t', midi.getControllerNumber(), '\tMIDI Controller Value:\t' midi.getControllerValue())


midi_ports = range(midi_in.getPortCount())
if midi_ports:
    for midi_port in midi_ports:
        print(midi_in.getPortName(midi_port))
    print("Opening port 0!")
    midi_in.openPort(0)

    while True:
        message = midi_in.getMessage(2500) # some timeout in ms
        if message:
            print_message(message)
else:
    print('No available MIDI input port found. Check the port.')

client.disconnect()
    