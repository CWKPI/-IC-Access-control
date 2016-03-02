#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'
import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BOARD)
GPIO_shock = 12  # 振动传感器GPIO
shock = 0
shocki = 0
shockSum = 0
previousShock = 0  #Shock前一个状态
GPIO.setup(GPIO_shock, GPIO.IN)


def signalCollect():
    while True:
        signalshock()
        time.sleep(0.05)


# 振动信号搜集


def signalshock():
        global shocki
        global shockSum
        global shock
        global GPIO_shock
        if shocki != 5:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(GPIO_shock, GPIO.IN)
            shockSum = shockSum+GPIO.input(GPIO_shock)
            shocki += 1
        else:
            shocki = 0
            if shockSum >=2:
                shock = 1
            else:
                shock = 0
            global previousShock
            if shock != previousShock:
                previousShock = shock
                print("Dang qian shock %s" % shock)
            shockSum = 0


if __name__ == '__main__':
    GPIO.cleanup()
    t1 = threading.Thread(target=signalCollect, name='SignalCollect')
    t1.start()