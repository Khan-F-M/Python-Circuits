#!/usr/bin/python3
"""
Name: Muhammad Khan
Date: 3/20/2021
"""
from time import sleep
from gpiozero import LED, Button
from signal import pause, signal, SIGTERM, SIGHUP


blink_state = False
blink_inv = 1


def safe_exit(signum, frame):
    exit(1)


def turn_on():
    led1.blink(blink_inv, blink_inv*3)
    sleep(blink_inv)
    led2.blink(blink_inv, blink_inv)
    sleep(blink_inv)
    led3.blink(blink_inv, blink_inv*3)


def turn_off():
    led1.off()
    led2.off()
    led3.off()


def go_blink():
    global blink_state

    if blink_state:
        turn_off()
    else:
        turn_on()

    blink_state = not blink_state


def blink_speed():
    global blink_inv

    if blink_inv == 1:
        blink_inv = 0.2
    else:
        blink_inv = 1

    if blink_state:
        turn_off()
        turn_on()


button1 = Button(21)
button2 = Button(16)

led1 = LED(13)
led2 = LED(19)
led3 = LED(26)

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    button1.when_pressed = go_blink
    button2.when_pressed = blink_speed
    pause()

except KeyboardInterrupt:
        pass
