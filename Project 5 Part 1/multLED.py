#!/usr/bin/python3
"""
Name: Muhammad Khan
Date: 4/5/2021
"""
from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import LED, Button
from threading import Thread
from time import sleep
from random import randrange
from rpi_lcd import LCD

leds = [LED(5), LED(19), LED(13), LED(27), LED(21), LED(20)]
button = Button(6)
lcd = LCD()

is_running = True
delay = 0.1

patterns = [
               [1, 0, 0, 0, 0, 0],
               [1, 1, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 0],
               [1, 1, 1, 1, 0, 0],
               [1, 1, 1, 1, 1, 0],
               [0, 0, 0, 0, 0, 1]
           ]
index = 0
led_in = 5
led_out = 0


def safe_exit(signum, frame):
    exit(1)


def show_pattern():
    while is_running:
        for i in range(6):
            leds[i].value = patterns[index][i]

        token = patterns[index].pop(led_out)
        patterns[index].insert(led_in, token)

        if led_in == 5:
            direction = "<<"
        else:
            direction = ">>"

        lcd.text("Pattern " + '{:d}'.format(index) + "/6 " + direction, 1)
        sleep(delay)


def change_direction():
    global led_in, led_out, index

    led_in, led_out = led_out, led_in

    while True:
        new_index = randrange(1, len(patterns))

        if new_index != index:
            index = new_index
            break


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    button.when_pressed = change_direction
    index = randrange(1, len(patterns))

    worker = Thread(target=show_pattern, daemon=True)
    worker.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    is_running = False
    sleep(1.5*delay)
    lcd.clear()

    for i in range(6):
        leds[i].close()
