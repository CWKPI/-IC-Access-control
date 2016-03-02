# coding=utf-8
__author__ = 'xzhao'

from threading import Timer
import MessageHandle
url = "192.168.12.101"  # 192.168.12.101
port = 9001

class State(object):
    @property
    def nomal(self):
        return "nomal"

    @property
    def preWarn(self):
        return "preWarn"

    @property
    def knockOr(self):
        return "knockOr"

    @property
    def knock(self):
        return "knock"

    @property
    def openDoor(self):
        return "openDoor"

    @property
    def openDoorWait(self):
        return "openDoorWait"

    @property
    def brokenDoor(self):
        return "brokenDoor"

    @property
    def brokenDoorWait(self):
        return "brokenDoorWait"


class CtState(object):
    def __init__(self):
        self._currentState = "nomal"

    @property
    def currentState(self):
        return self._currentState

    @currentState.setter
    def currentState(self, value):
        if value == st.preWarn:
            global timer1
            timerSwitch(timer1)
            timer1 = Timer(3, convert, [st.knockOr])
            timer1.start()
        elif value == st.knockOr:
            global timer2
            timerSwitch(timer2)
            timer2 = Timer(5, convert, [st.openDoor])
            timer2.start()
        elif value == st.openDoor:
            global timer3
            timerSwitch(timer3)
            timer3 = Timer(5, convert, [st.brokenDoor])
            timer3.start()
        elif value == st.brokenDoor:
            timerSwitch("")
            url = "192.168.1.101"
            port = 9001
            MessageHandle.CallAlarm(url, port, 2)
        elif value == st.openDoorWait or value == st.brokenDoorWait or value == st.knock or value == st.brokenDoor:
            global timer4
            timerSwitch(timer4)
            timer4 = Timer(5, convert, [st.nomal])
            timer4.start()
        elif value == st.nomal:
            timerSwitch("")
        self._currentState = value


# 当前状态
ctState = CtState()
# 所有状态类
st = State()
# 敲门标记次数
knockNum = 0


# 可供外部调用直接改变状态机状态


def convert(a):
    ctState.currentState = a
    if ctState.currentState != st.nomal:
        print("CurrentState %s" % a)
    if ctState.currentState == st.knockOr:
        global knockNum
        knockNum += 1
        if knockNum == 2:
            ctState.currentState = st.knock
    if ctState.currentState == st.knock:
        # url = "192.168.12.101"
        # port = 9001
        # MessageHandle.CallAlarm(url, port, 1)
        print "Tong zhi Yong hu :you ren qiao men"




# Timer初始化


def timerinit():
    print('Timer is PrePare')


timer1 = Timer(0, timerinit, )
timer2 = Timer(0, timerinit, )
timer3 = Timer(0, timerinit, )
timer4 = Timer(0, timerinit, )


# Timer切换


def timerSwitch(timer):
    if timer == timer1:
        timer2.cancel()
        timer3.cancel()
        timer4.cancel()
    elif timer == timer2:
        timer1.cancel()
        timer3.cancel()
        timer4.cancel()
    elif timer == timer3:
        timer1.cancel()
        timer2.cancel()
        timer4.cancel()
    elif timer == timer4:
        timer1.cancel()
        timer2.cancel()
        timer3.cancel()
    else:
        timer1.cancel()
        timer2.cancel()
        timer3.cancel()
        timer4.cancel()


# 状态判断函数

def stateJudge(shock):
    if shock == 1:
        if ctState.currentState == st.nomal:
            convert(st.preWarn)
        elif ctState.currentState == st.openDoorWait:
            convert(st.openDoor)
        elif ctState.currentState == st.brokenDoorWait:
            convert(st.brokenDoor)
    else:
        if ctState.currentState == st.nomal:
            convert(st.nomal)
        elif ctState.currentState == st.preWarn:
            convert(st.nomal)
        elif ctState.currentState == st.knockOr:
            convert(st.preWarn)
        elif ctState.currentState == st.openDoor:
            convert(st.openDoorWait)
        elif ctState.currentState == st.brokenDoor:
            convert(st.brokenDoorWait)
        elif ctState.currentState == st.openDoorWait:
            print "System is Still in openDoorWait"
        elif ctState.currentState == st.brokenDoorWait:
            print "System is Still in brokenDoorWait"

