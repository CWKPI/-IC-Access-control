#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'
import RPi.GPIO as GPIO
import time
import threading
import DeviceControl


GPIO_doorBell = 16  #按下
doorBell = 0
bellSwitch = 0
previousDoorBell = 0  # doorBell前一个状态
belli = 0
bellSum = 0



def signalCollect():
    while True:
        signalDoorBell()
        time.sleep(0.01)


def signalDoorBell():
    global doorBell
    global belli
    global bellSum
    global previousDoorBell
    global GPIO_doorBell
    global GPIO_bell
    if belli != 15:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_doorBell, GPIO.IN)
        bellSum = bellSum + GPIO.input(GPIO_doorBell)
        belli += 1
    else:
        belli = 0
        if bellSum >= 15:
            doorBell = 1
        else:
            doorBell = 0
        if doorBell != previousDoorBell:
            previousDoorBell = doorBell
            DeviceControl.doorBell(doorBell)
            print("Dang qian doorBell %s" % doorBell)
        bellSum = 0


if __name__ == '__main__':
    GPIO.cleanup()
    DeviceControl.doorBell(0)
    signalCollect()
