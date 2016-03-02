# coding=utf-8
__author__ = 'Administrator'
print("hello")

import socket
import time
import sys
import threading
from time import ctime,sleep

HOST_IP = "110.192.166.96"
HOST_PORT = 9001

i = 0

def socketsocket(func):
    global i
    print("Starting socket: TCP...")
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
    host_addr = (HOST_IP, HOST_PORT)
    assert isinstance(socket_tcp, object)
    socket_tcp.bind(host_addr)
    socket_tcp.listen(1)
    while(True):
        print("aaaa")
        socket_con, addr  = socket_tcp.accept()
        t = threading.Thread(target=tcplink, args=(socket_con, addr))
        t.start()
        print("Connection accepted from %s:%s.." %addr)


threads = []
t1 = threading.Thread(target=socketsocket,args=(u'aaaaa',))
threads.append(t1)

#信息接收到回调
MessageRecive = {}

def tcplink(sock, addr):
    global buffer
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        #time.sleep(1)
        if data == 'exit' or not data:
            break
        dataReturn = MessageRecive(data)
        sendStr = ""
        for intt in dataReturn:
            sendStr +=chr(intt)
        sendTmp = str(sendStr)
        sock.send(sendTmp)

    sock.close()
    print 'Connection from %s:%s closed.' % addr



#开启监听程序
def linseningStart(sock, addr):
    global HOST_IP
    global HOST_PORT
    HOST_IP = sock
    HOST_PORT=addr

    for t in threads:
        t.setDaemon(True)
        t.start()

def UdpSend(sendIp, sendPort,sendData):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sendStr = ""
    for intt in sendData:
        sendStr +=chr(intt)
    sendTmp = str(sendStr)
    #send_addr = (sendIp, sendPort)
    s.sendto(sendTmp,  (sendIp, sendPort))
    s.close()

