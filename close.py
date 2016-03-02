#!/user/bin/env python
# coding=utf-8
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO_open = 11  # 开门
GPIO_alert = 13  # 报警
GPIO.setup(GPIO_open, GPIO.OUT)
GPIO.setup(GPIO_alert, GPIO.OUT)
GPIO.output(GPIO_open, GPIO.LOW)
GPIO.output(GPIO_alert, GPIO.LOW)
