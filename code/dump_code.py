import rtmidi


def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())


def midi_input_callback(message, time_stamp):
    print(f"Received MIDI message: {message} at time {time_stamp}")


def parse_midi_message(message_bytes):
    status_byte = message_bytes[0]
    data_bytes = message_bytes[1:]

    if 128 <= status_byte <= 239:
        message_type = (status_byte >> 4) & 0xF  # Extract the message type (e.g., note on, note off)
        channel = status_byte & 0xF  # Extract the MIDI channel
        return f"Message Type: {message_type}, Channel: {channel}, Data: {data_bytes}"
    return "Unknown MIDI Message"


def listen_to_midi_port(midi_in):
    # Get the available input ports
    available_ports = range(midi_in.getPortCount())

    if not available_ports:
        print("No MIDI input ports available.")
        return

    # Open the first available input port
    print("Opening port 0!")
    midi_in.openPort(1)

    # Set the callback function to handle incoming MIDI messages
    midi_in.setCallback(midi_input_callback)

    print(f"Listening to MIDI input on port: {available_ports[0]}")

    try:
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        pass

    # Clean up
    midi_in.closePort()
    midi_in.cancelCallback()


if __name__ == "__main__":
    midi_in = rtmidi.RtMidiIn()
    listen_to_midi_port(midi_in)

