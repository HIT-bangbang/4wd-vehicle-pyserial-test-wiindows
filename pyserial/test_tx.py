from ctypes import *
import serial #导入模块
import time
tx_buf = [0 for _ in range(15)]
test_data = [0 for _ in range(6)]
test_speed = [-2,20,0,0,0,0]
test_pid = [0,30,0,1,0,20]
"""
    ser:串口对象
    data：数据列表
    len:data的长度（注意仅仅是数据，不包括其他）
    type：数据帧的类型
"""
def UART_SendPacket(ser,data,len,type):
    checksum = 0
    if(len < 50):
        tx_buf[0] = 170
        tx_buf[1] = 85
        tx_buf[2] = len+5
        tx_buf[3] = type
        for a in range(len):
            tx_buf[4+a] = data[a]
        
        cnt = 4 + len  
        for a in range(cnt):
            checksum = checksum + tx_buf[a]
        tx_buf[a+1] = checksum & 0xff

        cnt = 5 + len
        for a in range(cnt):
            # print("testing")
            # ser.write(CHAR(tx_buf[a]))
            ser.write(c_char(tx_trans_type(tx_buf[a])))

#处理符号位，转变为补码
def tx_trans_type(data):
    if(data<0):
        pass
        return (256 + data)
    else:
        return data



try:
    #端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
    portx="COM21"
    #波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps=115200
    #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    timex=5
    # 打开串口，并得到串口对象
    ser=serial.Serial(portx,bps,timeout=timex)

    for a in range(20) :
        UART_SendPacket(ser,test_pid,6,0x12)
        print("send PID")
        time.sleep(0.02)


    while(True):
        # print("writing")
        # ser.write(CHAR(a))
        # time.sleep(0.1)
        UART_SendPacket(ser,test_speed,6,0x11)
        print("send speed")
        time.sleep(0.02)

except Exception as e:
    print("---异常---：",e)


