#!/usr/bin/python3
"""
Name: Muhammad Khan
Date: 4/5/2021
"""
from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from gpiozero import DistanceSensor, LED
from threading import Thread

sensor = DistanceSensor(echo=20, trigger=21)
ledB = LED(16)
led1 = LED(13)
led2 = LED(19)
led3 = LED(26)
reading = True


def safe_exit(signum, frame):
    exit(1)


def read_distance():
    while reading:
        print("Distance: " + '{:1.2f}'.format(sensor.value*100) + " cm")
        if ((sensor.value*100) == 100):
            led1.on()
            led2.off()
            led3.off()
            ledB.off()
        elif (((sensor.value*100) < 100) and ((sensor.value*100) > 40)):
            led2.on()
            led3.off()
            led1.off()
            ledB.blink(0.5, 0.5)
            sleep(1)
        else:
            led3.on()
            led1.off()
            led2.off()
            ledB.on()

        sleep(0.1)


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    reader = Thread(target=read_distance, daemon=True)
    reader.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    sensor.close()
