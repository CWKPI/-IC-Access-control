#!/user/bin/env python
# coding=utf-8
__author__ = 'xzhao'
import RPi.GPIO as GPIO
import time
import threading
import IRStateMachine
import ShockStatemachine
import DeviceControl
import MessageHandle

GPIO.setmode(GPIO.BOARD)
GPIO_iR = 7  # 红外传感器GPIO
GPIO_shock = 12  # 振动传感器GPIO
GPIO_doorBell = 16  # 按下门铃

iR = 0           # 最终输出的信号值
shock = 0
doorBell = 0

iRSum = 0
shockSum = 0    # 把采集到的信号相加后 判断输出 0/1
bellSum = 0

iRi = 0
shocki = 0      # 采集的信号 每几下输出一次
belli = 0

previousIR = 0  # IR前一个状态
previousShock = 0  # Shock前一个状态
previousDoorBell = 0  # doorBell前一个状态

GPIO.setup(GPIO_iR, GPIO.IN)
GPIO.setup(GPIO_shock, GPIO.IN)
GPIO.setup(GPIO_doorBell, GPIO.IN)

bellSwitch = 0

tmp = "close"       # 暂时变量
timerIsStart = 0

def signalCollect():
    while True:
        signaliR()
        signalshock()
        signalDoorBell()
        time.sleep(0.05)  # IR 0.5s

# 红外信号搜集


def signaliR():
        global iRi
        global iRSum
        global iR
        global GPIO_iR
        if iRi != 5:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(GPIO_iR, GPIO.IN)
            iRSum = iRSum+GPIO.input(GPIO_iR)
            iRi += 1
        else:
            iRi = 0
            if iRSum >= 2:
                iR = 1
            else:
                iR = 0
            global previousIR
            if iR != previousIR:
                previousIR = iR
                print("Dang qian IR %s"%iR)
            iRSum = 0
            IRStateMachine.stateJudge(iR)


# 振动信号搜集


def signalshock():
        global shocki
        global shockSum
        global shock
        global GPIO_shock
        global timerIsStart
        if shocki != 5:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(GPIO_shock, GPIO.IN)
            shockSum = shockSum+GPIO.input(GPIO_shock)
            shocki += 1
        else:
            shocki = 0
            global shockTimer
            global tmp
            global timerIsStart
            if shockSum >= 2:
                shock = 1
                shockTimer.cancel()
                shockTimer = threading.Timer(5, shockDelay, [tmp])
                shockTimer.start()
                timerIsStart = 1
            else:
                global tmp
                global timerIsStart
                if timerIsStart == 0:
                    shockTimer = threading.Timer(5, shockDelay, [tmp])
                    shockTimer.start()
                    timerIsStart = 1

            global previousShock
            if shock != previousShock:
                previousShock = shock
                print("Dang qian shock %s" % shock)
            shockSum = 0
            ShockStatemachine.stateJudge(shock)


def shockDelay(s):
    global shock
    global timerIsStart
    if s == "close":
        shock = 0
        timerIsStart = 0


def timerinit():
    print('Timer is PrePare')

shockTimer = threading.Timer(0, timerinit,)


# 门铃信号搜集
def signalDoorBell():
    global doorBell
    global GPIO_doorBell
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_doorBell, GPIO.IN)
    doorBell = GPIO.input(GPIO_doorBell)
    if doorBell == 1:
        url = "192.168.1.101"
        port = 9001
        MessageHandle.CallAlarm(url, port, 1)
        DeviceControl.doorBell(doorBell)
        print("Dang qian doorBell %s" % doorBell)
    else:
        DeviceControl.doorBell(doorBell)


if __name__ == '__main__':
    GPIO.cleanup()
    t1 = threading.Thread(target=signalCollect, name='SignalCollect')
    t1.start()