# coding=utf-8
__author__ = 'Administrator'
print("hello")

import socket
import time
import sys
import threading
from time import ctime,sleep
import SocketVisitor
import MessageHandle
import DeviceControl

HOST_IP = "0.0.0.0"  # 10.192.167.25
HOST_PORT = 9001

sleepi = 0


#设备控制报文
def MessageDeviceControl(DeviceCode,ControlCode):
    if DeviceCode==1:
        DeviceControl.doorControl(ControlCode)
    else:
        DeviceControl.alertControl(ControlCode)
        # if ControlCode==1:
        #     print ""
        # else:
        #     print ""
    return 1

#查看猫眼请求
def MessageCatEyeVisitor():
    print("OUT MessageCatEyeVisitor ")
    return 1

#误报
def MessageMisInformation(AlarmCode):
    print("OUT MessageMisInformation AlarmCode:"+str(AlarmCode))
    return 1

#程序状态获取
def MessageGetProgramStatus():
    print("OUT MessageGetProgramStatus ")
    return 1

if __name__ == '__main__':
    global sleepi

    MessageHandle.CallbackDeviceControl = MessageDeviceControl
    MessageHandle.CallbackCatEyeVisitor = MessageCatEyeVisitor
    MessageHandle.CallbackMisInformation = MessageMisInformation
    MessageHandle.CallbackGetProgramStatus = MessageGetProgramStatus
    MessageHandle.linseningStart(HOST_IP,HOST_PORT)

    while(True):
          print("hello!!! %s" %sleepi)
          sleepi =sleepi+1
          if(sleepi == 5):
              MessageHandle.CallAlarm("192.168.12.102",8080,1)
          sleep(2)
