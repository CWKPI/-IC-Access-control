#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO_open = 11  # 开门
GPIO_alert = 13  # 报警
GPIO_bell = 15  # 响铃
open = 0
alert = 0
bell = 0




def doorControl(open):
    global GPIO_open
    GPIO.setup(GPIO_open, GPIO.OUT)
    if open == 1:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_open, GPIO.LOW)
    else:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_open, GPIO.HIGH)


def alertControl(alert):
    global GPIO_alert
    GPIO.setup(GPIO_alert, GPIO.OUT)
    if alert == 1:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_alert, GPIO.LOW)
    else:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_alert, GPIO.HIGH)


def doorBell(bell):
    global GPIO_bell
    GPIO.setup(GPIO_bell, GPIO.OUT)
    if bell == 1:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_bell, GPIO.LOW)
    else:
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(GPIO_bell, GPIO.HIGH)
