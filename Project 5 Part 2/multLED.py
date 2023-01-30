#!/usr/bin/python3
"""
Name: Muhammad Khan
Date: 4/5/2021
"""
from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import Button, PWMLED
from threading import Thread
from time import sleep
from random import randrange
from rpi_lcd import LCD
from smbus import SMBus
from math import log10


leds = [PWMLED(5), PWMLED(19), PWMLED(22), PWMLED(27), PWMLED(20), PWMLED(16)]
button = Button(17)
bus = SMBus(1)
lcd = LCD()
is_running = True
step = 255
fade_factor = (step * log10(2))/(log10(step))
messege = ""
messege2 = ""
delay = 0.1

patterns = [
               [1, 0, 0, 0, 0, 0],
               [1, 1, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 0],
               [1, 1, 1, 1, 0, 0],
               [1, 1, 1, 1, 1, 0],
               [0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 1, 1],
               [0, 0, 0, 1, 1, 1]
           ]
index = 0
led_in = 5
led_out = 0


def safe_exit(signum, frame):
    exit(1)


def show_pattern():
    global messege, delay

    while is_running:
        for i in range(6):
            leds[i].value = patterns[index][i]

        token = patterns[index].pop(led_out)
        patterns[index].insert(led_in, token)

        if led_in == 5:
            direction = "<<"
        else:
            direction = ">>"

        messege = "Pattern " + '{:d}'.format(index) + "/8 " + direction
        sleep(delay)


def change_direction():
    global led_in, led_out, index

    led_in, led_out = led_out, led_in

    while True:
        new_index = randrange(1, len(patterns))

        if new_index != index:
            index = new_index
            break


ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]


def read_ads7830(input):
    bus.write_byte(0x4b, 0xc4+input)
    return bus.read_byte(0x4b)


def read2_ads7830(input):
    bus.write_byte(0x4b, 0x84+input)
    return bus.read_byte(0x4b)


def bright_adj(input):
    global messege2, brightness

    while is_running:
        value = read2_ads7830(input)
        brightness = (pow(2, (value/fade_factor))-1)/step
        for id in range(6):
            leds[id].value = patterns[index][id]*brightness
        messege2 = f"B:{brightness*100:3.0f}% D:{delay:2.2f}s"
        sleep(0.01)


def speed_adj(input):
    while is_running:
        for id in range(6):
            leds[id].value = patterns[index][id]*brightness
        value = read_ads7830(input)
        delay = 0.01+0.4*value/255
        sleep(0.01)


def display_stuff():
    while is_running:
        sleep(0.01)
        lcd.text(messege, 1)
        lcd.text(messege2, 2)


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    button.when_pressed = change_direction
    index = randrange(1, len(patterns))

    display = Thread(target=display_stuff, daemon=True)
    display.start()

    worker = Thread(target=show_pattern, daemon=True)
    worker.start()

    bright_adj(0)
    worker2 = Thread(target=bright_adj, daemon=True)

    speed_adj(0)
    worker3 = Thread(target=bright_adj, daemon=True)

    worker = Thread(target=show_pattern, daemon=True)

    worker2.start()
    worker3.start()
    pause()

except KeyboardInterrupt:
    pass

finally:
    is_running = False
    sleep(1.5*delay)
    lcd.clear()

    for i in range(6):
        leds[i].close()
