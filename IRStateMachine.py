# coding=utf-8
__author__ = 'xzhao'


from threading import Timer
import MessageHandle


class State(object):
    @property
    def nomal(self):
        return "nomal"

    @property
    def preWarn(self):
        return "preWarn"

    @property
    def shortStay(self):
        return "shortStay"

    @property
    def longStay(self):
        return "longStay"

    @property
    def wait(self):
        return "wait"

    @property
    def wander(self):
        return "wander"


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
            timer1 = Timer(5, convert, [st.shortStay])
            timer1.start()
        elif value == st.shortStay:
            global timer2
            timerSwitch(timer2)
            timer2 = Timer(5, convert, [st.longStay])
            timer2.start()
        elif value == st.longStay:
            timerSwitch("")
            print "you ren chang zhu,tong zhi yonghu"
            url = "192.168.1.101"
            port = 9001
            MessageHandle.CallAlarm(url, port, 3)
            global timer3
            timerSwitch(timer3)
            timer3 = Timer(5, convert, [st.nomal])
            timer3.start()
        # elif value == st.wander:
        #     timerSwitch("")
        #     print "you ren pai huai,tong zhi yonghu"
        #     url = "192.168.1.101"
        #     port = 9001
        #     MessageHandle.CallAlarm(url, port, 3)
        #     global timer3
        #     timerSwitch(timer3)
        #     timer3 = Timer(5, convert, [st.nomal])
        #     timer3.start()
        elif value == st.nomal:
            timerSwitch("")
        self._currentState = value


# 当前状态
ctState = CtState()
# 所有状态类
st = State()

wanderNum = 0
# 可供外部调用直接改变状态机状态


def convert(a):
    ctState.currentState = a
    if ctState.currentState != st.nomal:
        print("CurrentState %s" % a)
    # if ctState._currentState == st.preWarn:
    #     global wanderNum
    #     wanderNum += 1
    #     if wanderNum >= 2:
    #         ctState.currentState = st.wander
    #         print("CurrentState %s" % ctState.currentState)
    # if ctState._currentState != st.preWarn:
    #     wanderNum = 0





def timerinit():
    print("Timer is PrePare")


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

def stateJudge(ir):
    if ir == 1:
        if ctState.currentState == st.nomal:
            convert(st.preWarn)
    else:
        if ctState.currentState == st.nomal:
            convert(st.nomal)
        elif ctState.currentState == st.preWarn:
            convert(st.nomal)
        elif ctState.currentState == st.shortStay:
            convert(st.preWarn)
        elif ctState.currentState == st.wait:
            convert(st.shortStay)
