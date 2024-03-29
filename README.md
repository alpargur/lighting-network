# lighting-network
Lighting Network for Audiovisual System <br>

## About The Project
This project is a MIDI-based real-time audiovisual system for live-shows and installations. <br>
It's done as a part of Advanced Multimedia Communications course offered at [Cologne University of Applied Sciences](https://www.th-koeln.de/studium/technische-informatik-master_1197.php) by Prof. Dr. Andreas Grebe in Fall Semester 2023/24.

## System Architecture
> 💡 Attention
>
> Unlike many LED controlling systems. Lighting-Network is built on the wireless network connection. 
<br>

- The setup's heart is the master node. It contains the components to generate sound (DAW) and transmit MIDI signals (publisher). Broker's machine is trivial.
- MIDI note transmission is based on Message Queuing Telemetry Transport (MQTT). A subscriber on the controller receives the MIDIs and use the data to control the lighting.
    - The publisher in the master node. It listens to the MIDI interface and publishes the messages to the topic.
    - On the otherside, a subscriber listens to the published MIDI messages, parses the content and uses it to illumunate the LED.

![Lighting Network System Architecture](./assets/img/Lighting-Network-System-Architecture.png)

## Get Started
To get started you will need a couple of tools ready. Here is a list of tools you will need. Note that these are the tools we have used in the project. This documentation is solely based in the development with these mentioned tools. Overall, they delivered a satisfying job. If you want to go with an alternative, it is advised to look in detail for compatability, pros and cons.

|Tools|Description|
| --- | --- |
| [Raspberry Pi 4](https://www.raspberrypi.com/) | Single-board computer, used to control LEDs |
| [Controllable LEDs (WS2812B)](https://www.amazon.de/dp/B088BNNP63?psc=1&ref=ppx_yo2ov_dt_b_product_details) | They should be controllable |
| [Power Supply (5V)](https://www.amazon.de/dp/B09KNFD38L?psc=1&ref=ppx_yo2ov_dt_b_product_details) | Above 5V may roast the LEDs |
| [Jumper Wires](https://www.amazon.de/dp/B01EV70C78?psc=1&ref=ppx_yo2ov_dt_b_product_details) | Connects LEDs with the Raspberry Pi |
| [Female Connector](https://www.amazon.de/dp/B0BR4S7J23?psc=1&ref=ppx_yo2ov_dt_b_product_details) | Connects LEDs with the power supply |
| [Ableton Live](https://www.ableton.com/de/shop/?mtm_campaign=20778045271&mtm_kwd=ableton%20live&mtm_source=google&mtm_medium=cpc&mtm_cid=20778045271&mtm_group={AdGroupName}&gclid=Cj0KCQiAtaOtBhCwARIsAN_x-3KUQOT1SvdGork4GlHiQg3X-D_RstrnO8lcREZIC4rGUKvB2Q534vYaAnNqEALw_wcB) | DAW to generate and transmit MIDI data |

<br>

> 💡 Remark
> 
> Ableton Live has the ability to export MIDI data. If you want to use a DAW of your choice make sure that this
> feature is available. The system listens to a virtual MIDI bus. It is essential to lead MIDI to this interface for
> end-to-end connection.

## Set-up Development Environment
Make sure you have Python installed on your machine before executing the steps below. For the event-based system to run properly, both the machine with DAW and the Raspberry Pi must be equipped with `paho-mqtt` package. For convenience, you can simply create virtual environment in both machines.

```bash
# Go to the root directory

$ pip show virtualenv # check if you have virtualenv package installed
$ pip install virtualenv # if not install virtualenv
$ python -m venv venv # create a virtualenv named venv
$ source venv/bin/activate # activate virtualenv
$ pip install -r requirements.txt # download dependencies

$ deactivate # close the virtualenv
```

## Start Mosquitto Broker
Mosquitto broker needs to be up and running so that the producer can publish into the topic and the subscriber can consume the mesages.

- Install mosquitto => `sudo apt install -y mosquitto`
- For a quick setup, create a custom configuration and enable anonymous connections =>
    ```bash
    $ sudo nano /path/to/custom.conf # create and edit custom config file

    # add following lines to the config file
    $ allow_anonymous true 
    $ listener 1883
    ```
    This config allows anonymous connections and starts the mosquitto service on port 1883.
- Start mosquitto with the custom config in the background: `mosquitto -c /path/to/custom.conf -d` 

## Troubleshoot
- If you are trying to install the packages on your global environment and your Pi is equipped with a recent OS version you might encounter with a failure of package installation. <br> In that case, you can enable `--allow-breaking-changes` flag.
- If you haven't shutdown Pi properly this may cause some hardware issues in the board. So shutting it properly down is highly suggested!

## LED Control Logic
Visualization of MIDI notes is an art in its own way. For demo purposes, we configured an LED strip with 60 LEDs to be controlled by a drum machine with 10 elements. Each element is assigned to 6 consecutive LEDs in a serial fashion. Plus, the unique `keyNumber` of each element is used for color mapping. For details, check out the [configuration.py](./code/configuration.py).
Following table depicts the mapping used in transforming MIDI information to visual feedback.

| MIDI Attribute | Control Type |
| --- | --- |
| noteOn (boolean) | Turns LEDs on/off |
| key (string) | Chooses which LEDs to be controlled (NYI) |
| keyNumber (numeric) | Chooses which LEDs to be controlled |
| velocity (numeric)  | Adjusts the LEDs' brightness |

<br>

## Milestones
1. Build the end-to-end architecture
    - Hardware Setup
    - Network Setup (Implementation of MQTT based communication)
    - End-to-End Testing (MIDI signal is successfully transmitted and LED is successfully lit up)
2. Implementation LED controlling program
3. Scale up the lighting network (optional)
4. Create report
5. Presentation

## Task Distribution
| Task                                   | Assignee        |
|----------------------------------------|-----------------|
| [x] Build the end-to-end architecture     | Alpar, Bach  |
| [x] Implementation LED controlling        | Alpar        |
| [x] QoS Measurements                      | Alpar, Bach  |
| [x] Create report                         | Alpar, Bach  |
| [] Presentation                          | Alpar, Bach   |


# Wireshark Analysis
We analyzed the network for the three QoS levels and investigated network throughput and latency (expect QoS 0) for two different MIDI message types (single-shot & drum beat).

## QoS 0
This level uses fire and forget mechanism.
### Throughput
- **Single-Shot:** Throughput stays the same for single-shot play in a ~1 second interval (308 bytes/sec). 
- **Drum Beat:** Drum beat consists of multiple drum elements sending MIDI notes frequently and the throughput varies along.

### Delay
- End-to-End delay measured at 70ms.

## QoS 1
This level ensures that a message is delivered at least once and sender receives an acknowledgement message about the message status.
### Throughput
- **Single-Shot:** Throughput stays the same for impulse with a slight increase in the throughput size due to additional ACK packets. (390 bytes/sec). 
- **Drum Beat:** After `messageId = 20` MQTT switches automatically back to QoS 0. Following measure depicts the values before the switch. This is due to a Mosquitto MQTT broker problem described [in this issue](https://github.com/eclipse/mosquitto/issues/1821) or [this] (https://github.com/eclipse/mosquitto/issues/1517).

## QoS 2
This level enures that a message is delivered exactly ones, sender receives an acknowledgement message about the message status.
### Throughput
- **Single-Shot:** Throughput stays the same for impulse with a slight inrease in the throughput size due to additional ACK packets. (390 bytes/sec). 
- **Drum Beat:** The same issue from QoS 1 is observed here too. 

For conveniency, we decided to stick to only QoS 0 for further experiments.

## Throughput Analysis with QoS 0
- Each triggered MIDI note sends two messages in total. First when the note is on and the second when it is off. The throughput of each note is 3.26 kbps.
- If only 2 MIDI notes are being sent, the total throughput is equal to the summation of both MIDI notes' throughput.
- If 3 or more notes are sent, MQTT will sent message as follows:
    - The first instrument which has the lowest `keyNumber` will be sent first. In case you want to prioritize the end-to-end transmission of a specific drum element, `keyNumber` can be adjusted.
    - The rest will either be sent in one message or split into two or more messages containing multiple notes with different patterns each time.
Therefore, when 3 or more MIDI notes are being sent simultaneously, the total throughput is smaller than the aggregation of each element's single throughput.