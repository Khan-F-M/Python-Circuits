#!/usr/bin/python3
"""
Name: Muhammad Khan
Date: 4/5/2021
"""
from signal import signal, SIGTERM, SIGHUP, pause
from smbus import SMBus
from gpiozero import PWMLED
from time import sleep
from math import log10

bus = SMBus(1)
led = PWMLED(13)
steps = 255
fade_factor = (steps * log10(2))/(log10(steps))


def safe_exit(signum, frame):
    exit(1)


ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def values(input):
    while True:
        value = read_ads7830(input)
        print(value)
        yield (pow(2, (value/fade_factor))-1)/steps
        sleep(0.05)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    led.source_delay = 0.05
    led.source = values(0)
    pause()

except KeyboardInterrupt:
    pass

finally:
    led.close()
