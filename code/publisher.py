import rtmidi
import paho.mqtt.client as mqtt

## configuration variables
NETWORK_IP = "172.20.10.14"
NETWORK_PORT = 1884
KEEP_ALIVE = 60
DESTINATION_TOPIC = "midi-note.received"
MIDI_PORT = 0 # virtual bus midi port

def midi_publisher(midi_in):
    ## get the available midi input ports
    midi_ports = range(midi_in.getPortCount())
    
    ## establish mqtt connection
    # client = mqtt.Client()
    # client.connect(NETWORK_IP, NETWORK_PORT, KEEP_ALIVE)

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
    # client.disconnect()

def midi_handler(midi):
    if midi.isNoteOn():
        print('MIDI NOTE PUBLISHED')
        print('ON:\t', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity(), '\n')
        # publish message
        # TODO: parse and serialize midi messages
        # client.publish(DESTINATION_TOPIC, "hello world")

    elif midi.isNoteOff():
        print('OFF:\t', midi.getMidiNoteName(midi.getNoteNumber()))

    elif midi.isController():
        print('MIDI Controller Number:\t' + midi.getControllerNumber() + '\tMIDI Controller Value:\t' + midi.getControllerValue())


if __name__ == "__main__":
    midi_in = rtmidi.RtMidiIn()
    midi_publisher(midi_in)
    