#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)
GPIO_iR = 7  # 红外传感器GPIO
previousIR = 0 # IR前一个状态
iR = 0
def signalCollect():
    while True:
        signaliR()
    time.sleep(2)


def signaliR():
        global iR
        GPIO.setup(GPIO_iR, GPIO.IN)
        iR = GPIO.input(GPIO_iR)
        global previousIR
        if iR != previousIR:
            previousIR = iR
            print("Dang qian IR %s"%iR)

if __name__ == '__main__':
    GPIO.cleanup()
    t1 = threading.Thread(target=signalCollect, name='SignalCollect')
    t1.start()
