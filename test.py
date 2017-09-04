__author__ = 'ESR'
# import ctypes
import time
import serial

class USB():
    def __init__(self):
        dia=raw_input('please input the serial port number such as 0,1,2...\n')
        try:
            port=int(dia)
            ser = serial.Serial(port, timeout=1)
        except:
            print 'Can not connect the target port, seaching now...'
            for i in range(30):
                print 'port',i,'test...',
                try:
                    ser = serial.Serial(i, timeout=1)
                    print 'succeed'
                    break
                except:
                    print 'fail'
                    continue
        self.ser=ser

    def read_old(self):
        # c_s = ctypes.c_char_p(s)
        ser=self.ser
        data=ser.read(64)
        # while data=='':
        #     data=ser.read(64)

        time.sleep(0.2)
        return data
        # # return repr(rc_s.raw)
        # return rc_s.rawa

    def write(self, s):
        ser=self.ser
        while ser.write(s) == 0:
            time.sleep(0.1)

        # rs = self.read()
        # return rs
    def read(self,s):
        ser=self.ser
        ser.write(s)
        data=ser.read(64)
        while data=='':
            while ser.write(s) == 0:
                time.sleep(0.1)
            data=ser.read(64)
        time.sleep(0.2)
        return data

if __name__ == '__main__':
    test_num = 500000
    dia=raw_input('please input the serial port number such as 0,1,2...\n')
    port=int(dia)
    ser = serial.Serial(port, timeout=2)
    while i < test_num:
        ser.write('*IDN?\n')
        data = ser.read(64)
        print(len(data), data)
        i += 1
    def write_test():
        a = time.clock()
        i = 0
        gaptime = 0
        while i < test_num:
            # print 'write'
            if ser.write("CONF:VOLT:DC C2,H\n")!=0:
                i += 1
            time.sleep(gaptime)
            print 'write times',i
        b = time.clock()
        print a, b, b - a
        print a, b, b - a
    def read_test():
        a = time.clock()
        i = 0
        gaptime = 0.2
        while i < test_num:
            # print i,'enter'
            ser.write('*IDN?\n')
            # ser.write('CONF:VOLT:DC D1,H\n')
            # ser.write('READ:REGI 0x00,0x1F\n')
            # ser.write("CONF:VOLT:DC C2,H\n")
            data = ser.read(64)
            print(len(data), data)
            # time.sleep(gaptime)
            # ser.write("CONF:VOLT:DC C2,L\n")
            # data = ser.read(64)
            # print(len(data), data)
            # time.sleep(gaptime)
            # print 'read times',i
            i += 1
        b = time.clock()
        print a, b, b - a
        print a, b, b - a
    ser.write('*IDN?\n')
    print(ser.read(64))
    import threading

    # thd = threading.Thread(target=write_test)
    # thd.start()
    thd = threading.Thread(target=read_test())
    thd.start()
    # dia=raw_input('please input the serial port number such as 0,1,2...\n')
    # import wx
    raw_input()
    # a = wx.App()
    # wx.MessageBox('ALDAKSDK')
    # a.MainLoop()
