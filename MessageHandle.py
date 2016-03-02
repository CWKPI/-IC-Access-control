# coding=utf-8
__author__ = 'Administrator'
import SocketVisitor

# 下行报文设备控制报文的回调
CallbackDeviceControl = {}
# 下行报文猫眼请求的回调
CallbackCatEyeVisitor = {}
# 下行报文误报的回调
CallbackMisInformation = {}
# 下行报文程序状态获取的回调
CallbackGetProgramStatus = {}


# 接收到消息
def MessageRecive(data):
    clusid = ord(data[4])
    if (clusid == 0x21):
        # 设备控制报文
        return MessageDeviceControl(data)
    else:
        if (clusid == 0x22):
            # 查看猫眼请求
            return MessageCatEyeVisitor(data)
        else:
            if (clusid == 0x23):
                # 误报
                return MessageMisInformation(data)
            else:
                if (clusid == 0x24):
                    # 程序状态获取
                    return MessageGetProgramStatus(data)
                else:
                    print("CantRecognizeMessage " + str(ord(data[4])))
    return b"abc"


# 设备控制报文
def MessageDeviceControl(data):
    print("MessageDeviceControl ")
    DeviceCode = ord(data[19])
    ControlCode = ord(data[20])
    ControlResult = CallbackDeviceControl(DeviceCode, ControlCode)
    result = UpMessageDeviceControl(DeviceCode, ControlResult)
    result = AddPackgeHead(result)
    return result


# 设备控制回复上行报文
def UpMessageDeviceControl(DeviceCode, ControlResult):
    result = []
    # 簇ID
    result.append(0x13)
    # 硬件ID
    result.append(0x11)
    result.append(0x22)
    result.append(0x33)
    result.append(0x44)
    result.append(0x55)
    result.append(0x66)
    # 客户端ID
    result.append(0x66)
    result.append(0x55)
    result.append(0x44)
    result.append(0x33)
    result.append(0x22)
    result.append(0x11)
    # 回复KEY
    result.append(0x12)
    result.append(0x34)
    # 受控硬件码
    result.append(DeviceCode)
    # 控制结果
    result.append(ControlResult)
    # 硬件状态
    result.append(0x01)
    # 预留字段
    result.append(0x00)
    result.append(0x00)
    return result


# 查看猫眼请求
def MessageCatEyeVisitor(data):
    print("MessageCatEyeVisitor ")
    Result = CallbackCatEyeVisitor()
    result = UpMessageCatEyeVisitor()
    result = AddPackgeHead(result)
    return result


# 查看猫眼回复
def UpMessageCatEyeVisitor():
    result = []
    # 簇ID
    result.append(0x12)
    # 硬件ID
    result.append(0x11)
    result.append(0x22)
    result.append(0x33)
    result.append(0x44)
    result.append(0x55)
    result.append(0x66)
    # 客户端ID
    result.append(0x66)
    result.append(0x55)
    result.append(0x44)
    result.append(0x33)
    result.append(0x22)
    result.append(0x11)
    # 回复KEY
    result.append(0x12)
    result.append(0x34)
    # 预留字段
    result.append(0x00)
    result.append(0x00)
    return result


# 误报
def MessageMisInformation(data):
    print("MessageMisInformation ")
    AlarmCode = ord(data[21])
    Result = CallbackMisInformation(AlarmCode)
    result = UpMessageMisInformation(AlarmCode)
    result = AddPackgeHead(result)
    return result


# 误报上行回复
def UpMessageMisInformation(AlarmCode):
    result = []
    # 簇ID
    result.append(0x14)
    # 硬件ID
    result.append(0x11)
    result.append(0x22)
    result.append(0x33)
    result.append(0x44)
    result.append(0x55)
    result.append(0x66)
    # 客户端ID
    result.append(0x66)
    result.append(0x55)
    result.append(0x44)
    result.append(0x33)
    result.append(0x22)
    result.append(0x11)
    # 回复KEY
    result.append(0x12)
    result.append(0x34)
    # 报警类型
    result.append(AlarmCode)
    # 预留字段
    result.append(0x00)
    result.append(0x00)
    return result


# 程序状态获取
def MessageGetProgramStatus(data):
    print("MessageGetProgramStatus ")
    Result = CallbackGetProgramStatus()
    result = UpMessageGetProgramStatus()
    result = AddPackgeHead(result)
    return result


def UpMessageGetProgramStatus():
    result = []
    # 簇ID
    result.append(0x15)
    # 硬件ID
    result.append(0x11)
    result.append(0x22)
    result.append(0x33)
    result.append(0x44)
    result.append(0x55)
    result.append(0x66)
    # 客户端ID
    result.append(0x66)
    result.append(0x55)
    result.append(0x44)
    result.append(0x33)
    result.append(0x22)
    result.append(0x11)
    # 回复KEY
    result.append(0x12)
    result.append(0x34)
    # 状态保温网版本
    result.append(0x01)
    # 程序版本
    result.append(0x01)
    result.append(0x01)
    # 振动传感器状态机状态
    result.append(0x01)
    # 红外传感器状态机状态
    result.append(0x01)
    # 预留字段
    result.append(0x00)
    result.append(0x00)
    return result


# 添加包头
def AddPackgeHead(data):
    result = []
    # FE
    result.append(0xFE)
    # 版本
    result.append(0x01)
    # 字节数
    result.append(0x00)
    result.append(data.count(data))
    # 添加数据包
    for byte in data:
        result.append(byte)
    # 校验和
    result.append(0x55)
    return result


# 纯上行报警报文  报警码   1为敲门   2为撬门   3为徘徊报警
def CallAlarm(sock, addr, AlarmCode):
    result = UpMessageAlarm(AlarmCode)
    result = AddPackgeHead(result)
    SocketVisitor.UdpSend(sock, addr, result)


def UpMessageAlarm(AlarmCode):
    result = []
    # 簇ID
    result.append(0x11)
    # 硬件ID
    result.append(0x11)
    result.append(0x22)
    result.append(0x33)
    result.append(0x44)
    result.append(0x55)
    result.append(0x66)
    # 客户端ID
    result.append(0x66)
    result.append(0x55)
    result.append(0x44)
    result.append(0x33)
    result.append(0x22)
    result.append(0x11)
    # 报警KEY
    result.append(0x12)
    result.append(0x34)
    # 报警类型
    result.append(AlarmCode)
    # 预留字段
    result.append(0x00)
    result.append(0x00)
    return result


# 开启监听程序
def linseningStart(sock, addr):
    SocketVisitor.MessageRecive = MessageRecive
    SocketVisitor.linseningStart(sock, addr)
