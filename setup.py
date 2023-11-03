from setuptools import setup

setup(
    name="midi-lights",
    version="1.0.0",
    author="Alpar & Bach",
    description="A package to turn MIDI notes into LED lightning controls based on MQTT protocol.",
    packages=["midi-lights"],
    install_requires=[
        'mido',
        'paho-mqtt'
    ],
)