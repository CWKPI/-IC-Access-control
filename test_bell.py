#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO_open = 11  # 开门
GPIO_alert = 13  # 报警
GPIO_bell = 15  # 响铃
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_bell, GPIO.OUT)
GPIO.output(GPIO_bell, GPIO.HIGH)  #GPIO.LOW