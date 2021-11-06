
#该代码基于python3，在python2下部分代码（尤其是数据类型转换）会报错
import serial #导入模块
import time
rx_con = 0
rx_checksum = 0
rx_buf = [0 for _ in range(60)]
robot_speed = [0 for _ in range(30)]

#处理符号位，处理负数
def rxtype_trans_16(value):
    if value > 32767:
        return value-65536
    else:
        return value


try:
    #端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
    portx="COM9"
    #波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps=115200
    #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    timex=5
    # 打开串口，并得到串口对象
    ser=serial.Serial(portx,bps,timeout=timex)

    while(True):
        """
            注意python中的read().hex()读取的是16进制数，但是变量类型是str类型。
        """

        res = ser.read().hex()#读一个字节,16进制读取

        res = int(res,16)
        #int(str,Base)方法，将一个str表示的base进制的数字转换成对应的十进制
        #该方法不会考虑符号位，字符串中的数字按照无符号数处理
        #比如0xaa,其二进制为1010 1010，考虑符号位该值为负数补码表示，其值应为 -85
        #但是这里转换出来是170

        if(rx_con < 3):
            # print("rx_con < 3")
            if(rx_con == 0):
                # print("rx_con == 0")
                if(res == 170):
                    rx_buf[0] = res
                    rx_con = 1
                    # print("res = 170")
                else:
                    rx_con = 0
            elif(rx_con == 1):
                if(res == 85):
                    rx_buf[1] = res
                    rx_con = 2
                    # print("res = 85")
                else:
                    rx_con = 0
            else:
                # print('else')
                rx_buf[2] = res
                rx_con = 3
                rx_checksum = (170+85) + res
                # print(rx_buf[2])
        else:
            # print("here")
            if (rx_con < (rx_buf[2]-1)):
                # print("rx_con < (rx_buf[2]-1)")
                rx_buf[rx_con] = res
                rx_con = rx_con + 1
                rx_checksum = rx_checksum + res
            else:
                # print("rx_con !!!< (rx_buf[2]-1)")
                # print("res=",res)
                # print("rx_check = ",rx_checksum)
                if(res == (rx_checksum & 0xff)): #校验正确
                    print("校验正确")
                    if(rx_buf[3] == 6):
                        # robot_speed[0] = (int)(((rx_buf[42]<<8) | rx_buf[43]),16)
                        robot_speed[0] = (int)((rx_buf[22]<<8) | rx_buf[23])

                        print(rxtype_trans_16(robot_speed[0]))

                        pass
                        pass
                    rx_con = 0

            


    # ser.close()#关闭串口

except Exception as e:
    print("---异常---：",e)