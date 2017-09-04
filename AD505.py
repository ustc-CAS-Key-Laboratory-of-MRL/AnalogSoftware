import wx
import wx.xrc
import analog
import time
import os
import sys
import ctypes
import pprint
import pickle
import string
import threading

from decimal import Decimal

ImagePath = 'resource/image/'
PdfPath = 'resource/data sheet/'
FilePath = 'resource/initial parameter/'
Link_9516 = None
add_9139 = []
add_9516 = []
reg_91391 = []
reg_91392 = []
reg_9516 = []
MainFrameLink = None
###########################################################################
## Class MyFrame1
###########################################################################
DefaultSaveFilePath = os.getcwd()
num = '0123456789'
num1 = '0123456789.-'
usb = analog.USB()
base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A') + 6)]


# def fun():
# os.system(E:\XYJ\xyj Document\AD9139.pdf)
def openfile_9139():
    os.system(PdfPath + 'AD9139.pdf')


def openfile_9516():
    os.system(PdfPath + 'AD9516_3.pdf')


def openfile_5732():
    os.system(PdfPath + 'AD5722R_5732R_5752R.pdf')


def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))


def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))


def bin2dec(string_num):
    return str(int(string_num, 2))


def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 16)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])


def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))


def Find_9139(k):
    global add_9139
    k = int(k, 16)
    for i in range(0, 58):
        if add_9139[i] == k:
            return i


def binary_float(x, n=100):
    a = Decimal(x) * 2
    r = []
    for i in xrange(n):
        if a >= 1:
            r.append("1")
            a -= 1
        else:
            r.append("0")
        a = a * 2
    return "0." + "".join(r)


def InitialParameter_5732():
    try:
        f = open(FilePath + 'default_ad5732.txt', 'r')
    except:
        return -1
    data = f.readlines()
    for i in range(1, len(data)):
        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
        substance = data[i][-3] + data[i][-2]
        WriteReg(5732, site, substance)
        OnPanelChange_5732(site, substance)


def InitialParameter_91391():
    global MainFrameLink
    data = []
    try:
        # f = open(FilePath + 'default_ad9139_1.txt', 'r')
        f = open(FilePath + 'default_ad9139_1.txt', 'r')
    except:
        return -1

    data = f.readlines()
    for i in range(1, len(data)):
        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
        substance = data[i][-3] + data[i][-2]
        WriteReg(91391, site, substance)
        OnPanelChange_91391(site, substance)
    f.close()


def OnPanelChange_91391(site, substance):
    global reg_91391
    x = Find_9139(site)
    # reg_91391[x].content=int(substance,16)
    if site == '0001':
        if reg_91391[x].content == 64:
            MainFrameLink.d9139.channel1.ON_OFF.SetLabel('ON')
        if reg_91391[x].content == 192:
            MainFrameLink.d9139.channel1.ON_OFF.SetLabel('OFF')
    if site == '0028':
        if reg_91391[x].content == 0:
            MainFrameLink.d9139.channel1.m_radioBox1.SetSelection(0)
        if reg_91391[x].content == 128:
            MainFrameLink.d9139.channel1.m_radioBox1.SetSelection(1)
    if site == '0027':
        if reg_91391[x].content / 128 == 0:
            MainFrameLink.d9139.channel1.Inv.SetLabel('Disable')
        if reg_91391[x].content / 128 == 1:
            MainFrameLink.d9139.channel1.Inv.SetLabel('Enable')

    if site == '000D' or site == '005E' or site == '005F':
        x = Find_9139('000D')
        y = Find_9139('005E')
        z = Find_9139('005F')

        if reg_91391[x].content == 6 and reg_91391[y].content == 0 and reg_91391[z].content == 96:
            MainFrameLink.d9139.channel1.choice1.SetSelection(0)
        if reg_91391[x].content == 6 and reg_91391[y].content == 128 and reg_91391[z].content == 103:
            MainFrameLink.d9139.channel1.choice1.SetSelection(1)
        if reg_91391[x].content == 6 and reg_91391[y].content == 240 and reg_91391[z].content == 103:
            MainFrameLink.d9139.channel1.choice1.SetSelection(2)
        if reg_91391[x].content == 6 and reg_91391[y].content == 254 and reg_91391[z].content == 103:
            MainFrameLink.d9139.channel1.choice1.SetSelection(3)
    if site == '000A' or site == '000D':
        x = Find_9139('000A')
        y = Find_9139('000D')

        if reg_91391[x].content == 192 and reg_91391[y].content == 134:
            MainFrameLink.d9139.channel1.dll.SetLabel('Enable')
            MainFrameLink.d9139.channel1.choice1.Enable(False)
            MainFrameLink.d9139.channel1.choice2.Enable(True)
        if reg_91391[x].content == int('40', 16) and reg_91391[y].content == 6:
            MainFrameLink.d9139.channel1.dll.SetLabel('Disable')
            MainFrameLink.d9139.channel1.choice2.Enable(False)
            MainFrameLink.d9139.channel1.choice1.Enable(True)

    if site == '000A':
        x = Find_9139('000A')
        temp = '%X' % reg_91391[x].content
        if temp[-2] == 'C':
            if temp[-1] == 'A':
                MainFrameLink.d9139.channel1.choice2.SetSelection(0)
            if temp[-1] == 'B':
                MainFrameLink.d9139.channel1.choice2.SetSelection(1)
            if temp[-1] == 'C':
                MainFrameLink.d9139.channel1.choice2.SetSelection(2)
            if temp[-1] == 'D':
                MainFrameLink.d9139.channel1.choice2.SetSelection(3)
            if temp[-1] == 'E':
                MainFrameLink.d9139.channel1.choice2.SetSelection(4)
            if temp[-1] == 'F':
                MainFrameLink.d9139.channel1.choice2.SetSelection(5)
            if temp[-1] == '0':
                MainFrameLink.d9139.channel1.choice2.SetSelection(6)
            if temp[-1] == '1':
                MainFrameLink.d9139.channel1.choice2.SetSelection(7)
            if temp[-1] == '2':
                MainFrameLink.d9139.channel1.choice2.SetSelection(8)
            if temp[-1] == '3':
                MainFrameLink.d9139.channel1.choice2.SetSelection(9)
            if temp[-1] == '4':
                MainFrameLink.d9139.channel1.choice2.SetSelection(10)
            if temp[-1] == '5':
                MainFrameLink.d9139.channel1.choice2.SetSelection(11)
            if temp[-1] == '6':
                MainFrameLink.d9139.channel1.choice2.SetSelection(12)
    if site == '0027':
        x = Find_9139('0027')
        temp = bin(reg_91391[x].content)
        temp = temp[2:]
        # print temp
        # print len(temp),temp[0]
        ####### Enable #####
        if (len(temp) == 8 and temp[2] == '1'):
            MainFrameLink.d9139.channel1.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel1.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel1.textCtrl_2.Enable(True)
        elif (len(temp) == 7 and temp[1] == '1'):
            MainFrameLink.d9139.channel1.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel1.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel1.textCtrl_2.Enable(True)
        elif (len(temp) == 6 and temp[0] == '1'):
            # print '6'
            MainFrameLink.d9139.channel1.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel1.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel1.textCtrl_2.Enable(True)
        ####### Disable ######
        else:
            # print 'else'
            MainFrameLink.d9139.channel1.gainbutton.SetLabel('Disable')
            MainFrameLink.d9139.channel1.textCtrl_1.Enable(False)
            MainFrameLink.d9139.channel1.textCtrl_2.Enable(False)
    if site == '003F':
        x = Find_9139('003F')
        temp = bin(reg_91391[x].content)
        temp = temp[2:]
        if len(temp) == 5:
            temp = '0' + temp[2:]
        if len(temp) == 4:
            temp = '00' + temp[2:]
        if len(temp) == 3:
            temp = '000' + temp[2:]
        if len(temp) == 2:
            temp = '0000' + temp[2:]
        if len(temp) == 1:
            temp = '00000' + temp[-1]
        if len(temp) == 0:
            temp = '000000'
        # print temp[0]
        # print temp[1]
        # print temp[5]
        value = int(temp[0]) + int(temp[1]) * 0.5 + int(temp[2]) * 0.25 + int(temp[3]) * 0.125 + int(
            temp[4]) * 0.0625 + int(temp[5]) * 0.03125
        MainFrameLink.d9139.channel1.textCtrl_1.SetValue(str(value))
    if site == '003B' or site == '003C':
        x = Find_9139('003B')
        y = Find_9139('003C')
        value = '%X' % reg_91391[y].content
        if len(value) == 1:
            value = '0' + value
        value2 = '%X' % reg_91391[x].content
        if len(value2) == 1:
            value2 = '0' + value2
        # temp=hex2bin(value)
        value = value + value2
        temp = hex2dec(value)
        MainFrameLink.d9139.channel1.textCtrl_2.SetValue(temp)


def OnPanelChange_91392(site, substance):
    x = Find_9139(site)
    if site == '0001':
        if reg_91392[x].content == 64:
            MainFrameLink.d9139.channel2.ON_OFF.SetLabel('OFF')
            MainFrameLink.d9139.channel2.ON_OFF.SetValue(False)
        if reg_91392[x].content == 192:
            MainFrameLink.d9139.channel2.ON_OFF.SetLabel('ON')
            MainFrameLink.d9139.channel2.ON_OFF.SetValue(True)
    if site == '0028':
        if reg_91392[x].content == 0:
            MainFrameLink.d9139.channel2.m_radioBox1.SetSelection(0)
        if reg_91392[x].content == 128:
            MainFrameLink.d9139.channel2.m_radioBox1.SetSelection(1)
    if site == '0027':
        if reg_91392[x].content / 128 == 0:
            MainFrameLink.d9139.channel2.Inv.SetLabel('Disable')
        if reg_91392[x].content / 128 == 1:
            MainFrameLink.d9139.channel2.Inv.SetLabel('Enable')

    if MainFrameLink.d9139.channel2.dll.GetLabel() == 'Diable':
        if site == '000D' or site == '005E' or site == '005F':
            x = Find_9139('000D')
            y = Find_9139('005E')
            z = Find_9139('005F')

            if reg_91392[x].content == 6 and reg_91392[y].content == 0 and reg_91392[z].content == 96:
                MainFrameLink.d9139.channel2.choice1.SetSelection(0)
            if reg_91392[x].content == 6 and reg_91392[y].content == 128 and reg_91392[z].content == 103:
                MainFrameLink.d9139.channel2.choice1.SetSelection(1)
            if reg_91392[x].content == 6 and reg_91392[y].content == 240 and reg_91392[z].content == 103:
                MainFrameLink.d9139.channel2.choice1.SetSelection(2)
            if reg_91392[x].content == 6 and reg_91392[y].content == 254 and reg_91392[z].content == 103:
                MainFrameLink.d9139.channel2.choice1.SetSelection(3)

    if site == '000A' or site == '000D':
        x = Find_9139('000A')
        y = Find_9139('000D')
        if reg_91392[x].content == 192 and reg_91392[y].content == 134:
            MainFrameLink.d9139.channel2.dll.SetLabel('Enable')
            MainFrameLink.d9139.channel2.choice1.Enable(False)
            MainFrameLink.d9139.channel2.choice2.Enable(True)
        if reg_91392[x].content == int('40', 16) and reg_91392[y].content == 6:
            MainFrameLink.d9139.channel2.dll.SetLabel('Disable')
            MainFrameLink.d9139.channel2.choice2.Enable(False)
            MainFrameLink.d9139.channel2.choice1.Enable(True)
    if site == '000A':
        x = Find_9139('000A')
        temp = '%X' % reg_91392[x].content
        if temp[-2] == 'C':
            if temp[-1] == 'A':
                MainFrameLink.d9139.channel2.choice2.SetSelection('0')
            if temp[-1] == 'B':
                MainFrameLink.d9139.channel2.choice2.SetSelection('1')
            if temp[-1] == 'C':
                MainFrameLink.d9139.channel2.choice2.SetSelection('2')
            if temp[-1] == 'D':
                MainFrameLink.d9139.channel2.choice2.SetSelection('3')
            if temp[-1] == 'E':
                MainFrameLink.d9139.channel2.choice2.SetSelection('4')
            if temp[-1] == 'F':
                MainFrameLink.d9139.channel2.choice2.SetSelection(5)
            if temp[-1] == '0':
                MainFrameLink.d9139.channel2.choice2.SetSelection(6)
            if temp[-1] == '1':
                MainFrameLink.d9139.channel2.choice2.SetSelection(7)
            if temp[-1] == '2':
                MainFrameLink.d9139.channel2.choice2.SetSelection(8)
            if temp[-1] == '3':
                MainFrameLink.d9139.channel2.choice2.SetSelection(9)
            if temp[-1] == '4':
                MainFrameLink.d9139.channel2.choice2.SetSelection(10)
            if temp[-1] == '5':
                MainFrameLink.d9139.channel2.choice2.SetSelection(11)
            if temp[-1] == '6':
                MainFrameLink.d9139.channel2.choice2.SetSelection(12)
    if site == '003F':
        x = Find_9139('003F')
        temp = bin(reg_91392[x].content)
        temp = temp[2:]
        if len(temp) == 5:
            temp = '0' + temp[2:]
        if len(temp) == 4:
            temp = '00' + temp[2:]
        if len(temp) == 3:
            temp = '000' + temp[2:]
        if len(temp) == 2:
            temp = '0000' + temp[2:]
        if len(temp) == 1:
            temp = '00000' + temp[-1]
        if len(temp) == 0:
            temp = '000000'
        # print temp[0]
        # print temp[1]
        # print temp[5]
        value = int(temp[0]) + int(temp[1]) * 0.5 + int(temp[2]) * 0.25 + int(temp[3]) * 0.125 + int(
            temp[4]) * 0.0625 + int(temp[5]) * 0.03125
        MainFrameLink.d9139.channel2.textCtrl_1.SetValue(str(value))
    if site == '0027':
        x = Find_9139('0027')
        temp = bin(reg_91392[x].content)
        temp = temp[2:]
        # print temp
        # print len(temp),temp[0]
        ####### Enable #####
        if (len(temp) == 8 and temp[2] == '1'):
            MainFrameLink.d9139.channel2.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel2.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(True)
        elif (len(temp) == 7 and temp[1] == '1'):
            MainFrameLink.d9139.channel2.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel2.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(True)
        elif (len(temp) == 6 and temp[0] == '1'):
            # print '6'
            MainFrameLink.d9139.channel2.gainbutton.SetLabel('Enable')
            MainFrameLink.d9139.channel2.textCtrl_1.Enable(True)
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(True)
        ####### Disable ######
        else:
            # print 'else'
            MainFrameLink.d9139.channel2.gainbutton.SetLabel('Disable')
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(False)
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(False)
            MainFrameLink.d9139.channel2.textCtrl_1.Enable(False)

    if site == '003B' or site == '003C':
        x = Find_9139('003B')
        y = Find_9139('003C')
        value = '%X' % reg_91392[y].content
        if len(value) == 1:
            value = '0' + value
        value2 = '%X' % reg_91392[x].content
        if len(value2) == 1:
            value2 = '0' + value2
        # temp=hex2bin(value)
        value = value + value2
        temp = hex2dec(value)
        MainFrameLink.d9139.channel2.textCtrl_2.SetValue(temp)


def InitialParameter_91392():
    global MainFrameLink
    data = []
    try:
        f = open(FilePath + 'default_ad9139_2.txt', 'r')
    except:
        return -1
    data = f.readlines()
    for i in range(1, len(data)):
        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
        substance = data[i][-3] + data[i][-2]
        WriteReg(91392, site, substance)
        OnPanelChange_91392(site, substance)
    f.close()


def InitialParameter_9516():
    global MainFrameLink
    data = []
    ############# 9516 ##############
    ############# 9516 ##############
    try:
        f = open(FilePath + 'default_ad9516.txt', 'r')
    except:
        return -1
    data = f.readlines()
    # print len(data)
    for i in range(1, len(data)):
        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
        substance = data[i][-3] + data[i][-2]
        WriteReg(9516, site, substance)
        # print site
        if site == '01E1':
            # print 'eee'
            if substance == '01':
                MainFrameLink.d9516.spdtbutton.SetValue(False)
            elif substance == '02':
                # print 'en'
                MainFrameLink.d9516.spdtbutton.SetValue(True)
        ####### P combobox########
        elif site == '0016':
            if substance == '00':
                MainFrameLink.d9516.comboBox_P.SetSelection(0)
            if substance == '01':
                MainFrameLink.d9516.comboBox_P.SetSelection(1)
            if substance == '02':
                MainFrameLink.d9516.comboBox_P.SetSelection(2)
            if substance == '07':
                MainFrameLink.d9516.comboBox_P.SetSelection(3)
            if substance == '03':
                MainFrameLink.d9516.comboBox_P.SetSelection(4)
            if substance == '04':
                MainFrameLink.d9516.comboBox_P.SetSelection(5)
            if substance == '05':
                MainFrameLink.d9516.comboBox_P.SetSelection(6)
            if substance == '06':
                MainFrameLink.d9516.comboBox_P.SetSelection(7)
        ######### REF-CLK combobox #########3
        elif site == '001C':
            if substance == '82':
                MainFrameLink.d9516.comboBox_ref_clk.SetSelection(1)
            if substance == 'C4':
                MainFrameLink.d9516.comboBox_ref_clk.SetSelection(0)
        ####### Out button ######
        elif site == '00F0':
            if substance == '0C':
                MainFrameLink.d9516.out_button0.SetLabel('ON')
                MainFrameLink.d9516.out_button0.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button0.SetLabel('OFF')
                MainFrameLink.d9516.out_button0.SetValue(False)
        elif site == '00F1':
            if substance == '0C':
                MainFrameLink.d9516.out_button1.SetLabel('ON')
                MainFrameLink.d9516.out_button1.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button1.SetLabel('OFF')
                MainFrameLink.d9516.out_button1.SetValue(False)
        elif site == '00F2':
            if substance == '0C':
                MainFrameLink.d9516.out_button2.SetLabel('ON')
                MainFrameLink.d9516.out_button2.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button2.SetLabel('OFF')
                MainFrameLink.d9516.out_button2.SetValue(False)
        elif site == '00F3':
            if substance == '0C':
                MainFrameLink.d9516.out_button3.SetLabel('ON')
                MainFrameLink.d9516.out_button3.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button3.SetLabel('OFF')
                MainFrameLink.d9516.out_button3.SetValue(False)
        elif site == '00F4':
            if substance == '0C':
                MainFrameLink.d9516.out_button4.SetLabel('ON')
                MainFrameLink.d9516.out_button4.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button4.SetLabel('OFF')
                MainFrameLink.d9516.out_button4.SetValue(False)
        elif site == '00F5':
            if substance == '0C':
                MainFrameLink.d9516.out_button5.SetLabel('ON')
                MainFrameLink.d9516.out_button5.SetValue(True)
            if substance == '0E':
                MainFrameLink.d9516.out_button5.SetLabel('OFF')
                MainFrameLink.d9516.out_button5.SetValue(False)

        elif site == '0140':
            if substance == '02':
                MainFrameLink.d9516.out_button6.SetLabel('ON')
                MainFrameLink.d9516.out_button6.SetValue(True)
            if substance == '03':
                MainFrameLink.d9516.out_button6.SetLabel('OFF')
                MainFrameLink.d9516.out_button6.SetValue(False)
        elif site == '0141':
            if substance == '02':
                MainFrameLink.d9516.out_button7.SetLabel('ON')
                MainFrameLink.d9516.out_button7.SetValue(True)
            if substance == '03':
                MainFrameLink.d9516.out_button7.SetLabel('OFF')
                MainFrameLink.d9516.out_button7.SetValue(False)
        elif site == '0142':
            if substance == '02':
                MainFrameLink.d9516.out_button8.SetLabel('ON')
                MainFrameLink.d9516.out_button8.SetValue(True)
            if substance == '03':
                MainFrameLink.d9516.out_button8.SetLabel('OFF')
                MainFrameLink.d9516.out_button8.SetValue(False)
        elif site == '0143':
            if substance == '02':
                MainFrameLink.d9516.out_button9.SetLabel('ON')
                MainFrameLink.d9516.out_button9.SetValue(True)
            if substance == '03':
                MainFrameLink.d9516.out_button9.SetLabel('OFF')
                MainFrameLink.d9516.out_button9.SetValue(False)
        ############ VCO Diveder ###############
        elif site == '01E0':
            if substance == '00':
                MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(0)
            if substance == '01':
                MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(1)
            if substance == '02':
                MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(2)
            if substance == '03':
                MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(3)
            if substance == '04':
                MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(4)
        ######## A Text ###############
        elif site == '0013':
            MainFrameLink.d9516.textCtrl_A.SetLabel(str(int(substance, 16)))
        ######## B Text ###############
        elif site == '0014':
            for j in range(1, 60):
                site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                substance2 = data[j][-3] + data[j][-2]
                if site2 == '0015':
                    value_B = str(int(substance2 + substance, 16))
                    MainFrameLink.d9516.textCtrl_B.SetLabel(value_B)
        ########## R_dil ############
        elif site == '0011':
            for j in range(1, 60):
                site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                substance2 = data[j][-3] + data[j][-2]
                if site2 == '0012':
                    MainFrameLink.d9516.textCtrl_R_dil.SetLabel(str(int(substance2 + substance, 16)))
                    # print(str(int(substance2 + substance, 16)))
        ######### Text 1 ###############
        elif site == '0191':
            if substance == '80':
                MainFrameLink.d9516.textCtrl_1.SetLabel('1')
            elif substance == '00':
                for j in range(1, 60):
                    site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                    substance2 = data[j][-3] + data[j][-2]
                    if site2 == '0190':
                        if substance2[-1] == substance2[-2]:
                            temp_value = int(substance2[-1], 16)
                            temp_value = 2 + 2 * temp_value
                            MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_value))
                        elif substance2[-1] != substance2[-2]:
                            # print 'C=',int(substance2[-1],16)
                            # print 'D=',int(substance2[-2],16)
                            temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                            MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_value))
        ######### Text 2 ###############
        elif site == '0194':
            if substance == '80':
                MainFrameLink.d9516.textCtrl_2.SetLabel('1')
            elif substance == '00':
                for j in range(1, 60):
                    site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                    substance2 = data[j][-3] + data[j][-2]
                    if site2 == '0193':
                        if substance2[-1] == substance2[-2]:
                            temp_value = int(substance2[-1], 16)
                            temp_value = 2 + 2 * temp_value
                            MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_value))
                        elif substance2[-1] != substance2[-2]:
                            # print 'C=',int(substance2[-1],16)
                            # print 'D=',int(substance2[-2],16)
                            temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                            MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_value))
        ######### Text 3 ###############
        elif site == '0197':
            if substance == '80':
                MainFrameLink.d9516.textCtrl_3.SetLabel('1')
            elif substance == '00':
                for j in range(1, 60):
                    site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                    substance2 = data[j][-3] + data[j][-2]
                    if site2 == '0196':
                        if substance2[-1] == substance2[-2]:
                            temp_value = int(substance2[-1], 16)
                            temp_value = 2 + 2 * temp_value
                            MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_value))
                        elif substance2[-1] != substance2[-2]:
                            # print 'C=',int(substance2[-1],16)
                            # print 'D=',int(substance2[-2],16)
                            temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                            MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_value))
        ######### Text 4 ###############
        elif site == '019C':
            if substance == '30':
                MainFrameLink.d9516.textCtrl_4.SetLabel('1')
            elif substance == '20':
                for j in range(1, 60):
                    site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                    substance2 = data[j][-3] + data[j][-2]
                    if site2 == '0199':
                        if substance2[-1] == substance2[-2]:
                            temp_value = int(substance2[-1], 16)
                            temp_value = 2 + 2 * temp_value
                            MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_value))
                        elif substance2[-1] != substance2[-2]:
                            # print 'C=',int(substance2[-1],16)
                            # print 'D=',int(substance2[-2],16)
                            temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                            MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_value))
                            ######### Text 5 ###############
        elif site == '01A1':
            if substance == '30':
                MainFrameLink.d9516.textCtrl_5.SetLabel('1')
            elif substance == '20':
                for j in range(1, 60):
                    site2 = data[j][12] + data[j][13] + data[j][17] + data[j][18]
                    substance2 = data[j][-3] + data[j][-2]
                    if site2 == '019E':
                        if substance2[-1] == substance2[-2]:
                            temp_value = int(substance2[-1], 16)
                            temp_value = 2 + 2 * temp_value
                            MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_value))
                        elif substance2[-1] != substance2[-2]:
                            # print 'C=',int(substance2[-1],16)
                            # print 'D=',int(substance2[-2],16)
                            temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                            MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_value))
    f.close()


def OnPanelChange_5732(site, substance):
    global MainFrameLin
    # print site[0:2]
    if site[0:2] == '00':
        temp = site[2:4]
        temp = temp + substance
        temp = hex2bin(temp)
        while 16 - len(temp) != 0:
            temp = '0' + temp
        temp = temp[0:14]

        if temp[0] == '0':
            temp = bin2dec(temp)
        elif temp[0] == '1':

            k = len(temp) - 1
            if temp[k] == '0':
                temp = temp[0:k] + '1'
            k = k - 1
            while temp[k] == '0' and k > 0:
                temp = temp[0:k] + '1' + temp[k + 1:]
                k = k - 1
            temp = temp[0:k] + '0' + temp[k + 1:]
            k = 1
            while k < len(temp) - 1:
                if temp[k] == '0':
                    temp = temp[0:k] + '1' + temp[k + 1:]
                if temp[k] == '1':
                    temp = temp[0:k] + '0' + temp[k + 1:]
                k = k + 1
            if temp[k] == '0':
                temp = temp[0:k] + '1'
            elif temp[k] == '1':
                temp = temp[0:k] + '0'
            temp = bin2dec(temp)
        a = int(temp) * 4.096 / 32768
        # print 'a=',a
        MainFrameLink.d5732.m_textCtrl8.SetValue(str(a))
    if site[0:2] == '02':
        # print 'enter'
        temp = site[2:4]
        temp = temp + substance
        temp = hex2bin(temp)
        while 16 - len(temp) != 0:
            temp = '0' + temp
        temp = temp[0:14]

        if temp[0] == '0':
            temp = bin2dec(temp)
        elif temp[0] == '1':

            k = len(temp) - 1
            if temp[k] == '0':
                temp = temp[0:k] + '1'
            k = k - 1
            while temp[k] == '0' and k > 0:
                temp = temp[0:k] + '1' + temp[k + 1:]
                k = k - 1
            temp = temp[0:k] + '0' + temp[k + 1:]
            k = 1
            while k < len(temp) - 1:
                if temp[k] == '0':
                    temp = temp[0:k] + '1' + temp[k + 1:]
                if temp[k] == '1':
                    temp = temp[0:k] + '0' + temp[k + 1:]
                k = k + 1
            if temp[k] == '0':
                temp = temp[0:k] + '1'
            elif temp[k] == '1':
                temp = temp[0:k] + '0'
            temp = bin2dec(temp)
        a = int(temp) * 4.096 / 32768
        # print a
        MainFrameLink.d5732.m_textCtrl10.SetValue(str(a))


def OnPanelChange_9516(site, substance):
    global MainFrameLink, reg_9516, add_9516
    # ##### SPDF##### 
    if site == '01E1':
        if substance == '01':
            MainFrameLink.d9516.spdtbutton.SetValue(False)
        elif substance == '02':
            MainFrameLink.d9516.spdtbutton.SetValue(True)
    ####### P combobox########
    elif site == '0016':
        if substance == '00':
            MainFrameLink.d9516.comboBox_P.SetSelection(0)
        if substance == '01':
            MainFrameLink.d9516.comboBox_P.SetSelection(1)
        if substance == '02':
            MainFrameLink.d9516.comboBox_P.SetSelection(2)
        if substance == '07':
            MainFrameLink.d9516.comboBox_P.SetSelection(3)
        if substance == '03':
            MainFrameLink.d9516.comboBox_P.SetSelection(4)
        if substance == '04':
            MainFrameLink.d9516.comboBox_P.SetSelection(5)
        if substance == '05':
            MainFrameLink.d9516.comboBox_P.SetSelection(6)
        if substance == '06':
            MainFrameLink.d9516.comboBox_P.SetSelection(7)
    ######### REF-CLK combobox #########3
    elif site == '001C':
        if substance == '82':
            MainFrameLink.d9516.comboBox_ref_clk.SetSelection(1)
        if substance == 'C4':
            MainFrameLink.d9516.comboBox_ref_clk.SetSelection(0)
    ####### Out button ######
    elif site == '00F0':
        if substance == '0C':
            MainFrameLink.d9516.out_button0.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button0.SetLabel('OFF')
    elif site == '00F1':
        if substance == '0C':
            MainFrameLink.d9516.out_button1.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button1.SetLabel('OFF')
    elif site == '00F2':
        if substance == '0C':
            MainFrameLink.d9516.out_button2.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button2.SetLabel('OFF')
    elif site == '00F3':
        if substance == '0C':
            MainFrameLink.d9516.out_button3.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button3.SetLabel('OFF')
    elif site == '00F4':
        if substance == '0C':
            MainFrameLink.d9516.out_button4.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button4.SetLabel('OFF')
    elif site == '00F5':
        if substance == '0C':
            MainFrameLink.d9516.out_button5.SetLabel('ON')
        if substance == '0E':
            MainFrameLink.d9516.out_button5.SetLabel('OFF')

    elif site == '0140':
        if substance == '02':
            MainFrameLink.d9516.out_button6.SetLabel('ON')
        if substance == '03':
            MainFrameLink.d9516.out_button6.SetLabel('OFF')
    elif site == '0141':
        if substance == '02':
            MainFrameLink.d9516.out_button7.SetLabel('ON')
        if substance == '03':
            MainFrameLink.d9516.out_button7.SetLabel('OFF')
    elif site == '0142':
        if substance == '02':
            MainFrameLink.d9516.out_button8.SetLabel('ON')
        if substance == '03':
            MainFrameLink.d9516.out_button8.SetLabel('OFF')
    elif site == '0143':
        if substance == '02':
            MainFrameLink.d9516.out_button9.SetLabel('ON')
        if substance == '03':
            MainFrameLink.d9516.out_button9.SetLabel('OFF')
    ############ VCO Diveder ###############
    elif site == '01E0':
        if substance == '00':
            MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(0)
        if substance == '01':
            MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(1)
        if substance == '02':
            MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(2)
        if substance == '03':
            MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(3)
        if substance == '04':
            MainFrameLink.d9516.comboBox_VCO_DIVIDER.SetSelection(4)
    ######## A Text ###############
    elif site == '0013':
        MainFrameLink.d9516.textCtrl_A.SetLabel(str(int(substance, 16)))
    ######## B Text ###############
    elif site == '0014':
        for j in range(0, 64):
            if add_9516[j] == int('15', 16):
                substance2 = '%X' % reg_9516[j].content
                value_B = str(int(substance2 + substance, 16))
                MainFrameLink.d9516.textCtrl_B.SetLabel(value_B)
    ########## R_dil ############
    elif site == '0011':
        for j in range(0, 64):
            if add_9516[j] == 12:
                substance2 = '%X' % reg_9516[j].content
                MainFrameLink.d9516.textCtrl_R_dil.SetLabel(str(int(substance2 + substance, 16)))
    ######### Text 1 ###############
    elif site == '0191':
        if substance == '80':
            MainFrameLink.d9516.textCtrl_1.SetLabel('1')
        elif substance == '00':
            for j in range(0, 64):
                if add_9516[j] == int('190', 16):
                    substance2 = '%X' % reg_9516[j].content
                    if len(substance2) == 1:
                        substance2 = '0' + substance2
                    if substance2[-1] == substance2[-2]:

                        temp_value = int(substance2[-1], 16)
                        temp_value = 2 + 2 * temp_value
                        MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_value))
                    elif substance2[-1] != substance2[-2]:
                        # print 'C=',int(substance2[-1],16)
                        # print 'D=',int(substance2[-2],16)
                        temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                        MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_B + 2))
    elif site == '0190' and reg_9516[42].content == 0:
        if substance[-1] == substance[-2]:
            temp_value = int(substance[-1], 16)
            temp_value = 2 + 2 * temp_value
            MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_value))
        elif substance[-1] != substance[-2]:
            # print 'C=',int(substance2[-1],16)
            # print 'D=',int(substance2[-2],16)
            temp_B = int(substance[-1], 16) + int(substance[-2], 16)
            MainFrameLink.d9516.textCtrl_1.SetLabel(str(temp_B + 2))
    ######### Text 2 ###############
    elif site == '0194':
        if substance == '80':
            MainFrameLink.d9516.textCtrl_2.SetLabel('1')
        elif substance == '00':
            for j in range(0, 64):
                if add_9516[j] == int('193', 16):
                    substance2 = '%X' % reg_9516[j].content
                    if len(substance2) == 1:
                        substance2 = '0' + substance2
                    if substance2[-1] == substance2[-2]:
                        temp_value = int(substance2[-1], 16)
                        temp_value = 2 + 2 * temp_value
                        MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_value))
                    elif substance2[-1] != substance2[-2]:
                        # print 'C=',int(substance2[-1],16)
                        # print 'D=',int(substance2[-2],16)
                        temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                        MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_B + 2))
    elif site == '0193' and reg_9516[45].content == 0:
        if substance[-1] == substance[-2]:
            temp_value = int(substance[-1], 16)
            temp_value = 2 + 2 * temp_value
            MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_value))
        elif substance[-1] != substance[-2]:
            # print 'C=',int(substance2[-1],16)
            # print 'D=',int(substance2[-2],16)
            temp_B = int(substance[-1], 16) + int(substance[-2], 16)
            MainFrameLink.d9516.textCtrl_2.SetLabel(str(temp_B + 2))
    ######### Text 3 ###############
    elif site == '0197':
        if substance == '80':
            MainFrameLink.d9516.textCtrl_3.SetLabel('1')
        elif substance == '00':
            for j in range(0, 64):
                if add_9516[j] == int('196', 16):
                    substance2 = '%X' % reg_9516[j].content
                    if len(substance2) == 1:
                        substance2 = '0' + substance2
                    if substance2[-1] == substance2[-2]:
                        temp_value = int(substance2[-1], 16)
                        temp_value = 2 + 2 * temp_value
                        MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_value))
                    elif substance2[-1] != substance2[-2]:
                        # print 'C=',int(substance2[-1],16)
                        # print 'D=',int(substance2[-2],16)
                        temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                        MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_B + 2))
    elif site == '0196' and reg_9516[48].content == 0:
        if substance[-1] == substance[-2]:
            temp_value = int(substance[-1], 16)
            temp_value = 2 + 2 * temp_value
            MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_value))
        elif substance[-1] != substance[-2]:
            # print 'C=',int(substance2[-1],16)
            # print 'D=',int(substance2[-2],16)
            temp_B = int(substance[-1], 16) + int(substance[-2], 16)
            MainFrameLink.d9516.textCtrl_3.SetLabel(str(temp_B + 2))
    ######### Text 4 ###############
    elif site == '019C':
        if substance == '30':
            MainFrameLink.d9516.textCtrl_4.SetLabel('1')
        elif substance == '20':
            for j in range(0, 64):
                if add_9516[j] == int('199', 16):
                    substance2 = '%X' % reg_9516[j].content
                    if len(substance2) == 1:
                        substance2 = '0' + substance2
                    if substance2[-1] == substance2[-2]:
                        temp_value = int(substance2[-1], 16)
                        temp_value = 2 + 2 * temp_value
                        MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_value))
                    elif substance2[-1] != substance2[-2]:
                        # print 'C=',int(substance2[-1],16)
                        # print 'D=',int(substance2[-2],16)
                        temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                        MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_B + 2))
    elif site == '0199' and reg_9516[53].content == int('20', 16):
        if substance[-1] == substance[-2]:
            temp_value = int(substance[-1], 16)
            temp_value = 2 + 2 * temp_value
            MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_value))
        elif substance[-1] != substance[-2]:
            # print 'C=',int(substance2[-1],16)
            # print 'D=',int(substance2[-2],16)
            temp_B = int(substance[-1], 16) + int(substance[-2], 16)
            MainFrameLink.d9516.textCtrl_4.SetLabel(str(temp_B + 2))
            ######### Text 5 ###############
    elif site == '01A1':
        if substance == '30':
            MainFrameLink.d9516.textCtrl_5.SetLabel('1')
        elif substance == '20':
            for j in range(0, 64):
                if add_9516[j] == int('019E', 16):
                    substance2 = '%X' % reg_9516[j].content
                    if len(substance2) == 1:
                        substance2 = '0' + substance2
                    if substance2[-1] == substance2[-2]:
                        temp_value = int(substance2[-1], 16)
                        temp_value = 2 + 2 * temp_value
                        MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_value))
                    elif substance2[-1] != substance2[-2]:
                        # print 'C=',int(substance2[-1],16)
                        # print 'D=',int(substance2[-2],16)
                        temp_B = int(substance2[-1], 16) + int(substance2[-2], 16)
                        MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_B + 2))
                        # for j in range(0,64):
                        # if add_9516[j]==int('019C',16):
                        # print j
                        # break
    if site == '019E' and reg_9516[58].content == int('20', 16):
        # print 'enter'
        if substance[-1] == substance[-2]:
            temp_value = int(substance[-1], 16)
            temp_value = 2 + 2 * temp_value
            MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_value))
        elif substance[-1] != substance[-2]:
            # print 'C=',int(substance2[-1],16)
            # print 'D=',int(substance2[-2],16)
            temp_B = int(substance[-1], 16) + int(substance[-2], 16)
            MainFrameLink.d9516.textCtrl_5.SetLabel(str(temp_B + 2))


def OnCheckLegal(s, handle):
    for i in s:
        if i not in num:
            handle.SetValue('')
            temp = wx.MessageBox("Please input integer ", "Sorry")
            return False
    a = int(s)
    if a < 1 or a > 32:
        handle.SetValue('')
        temp = wx.MessageBox("Please input integer between 0 and 32 ", "Sorry")
        return False
    return True


def OnChangeToggleButton(handle):
    s = handle.GetLabel()
    if s == "ON":
        handle.SetLabel('OFF')
    if s == 'OFF':
        handle.SetLabel('ON')


def WriteReg2(no, addr, substance):
    global reg_9516, add_9516
    addr = str(addr)
    tempadd = int(addr, 16)
    usb.write('CONF:VOLT:DC D1,H\n')
    usb.write('CONF:REGI 0x' + addr[-4] + addr[-3] + ',0x' + addr[-2] + addr[-1] + ',0x' + substance[-2] + substance[
        -1] + '\n')
    usb.write('CONF:REGI 0x00,0x18,0x06\n')
    usb.write('CONF:REGI 0x02,0x32,0x01\n')
    usb.write('CONF:REGI 0x00,0x18,0x07\n')
    usb.write('CONF:REGI 0x02,0x32,0x01\n')
    for k in range(0, 64):
        if add_9516[k] == tempadd:
            value = int(substance, 16)
            reg_9516[k].ChangeLabel(value, tempadd)
            break


def WriteReg(no, addr, substance):
    global reg_91391, reg_91392, add_9139, add_9516, reg_9516
    addr = str(addr)
    tempadd = int(addr, 16)
    if no == 9516:
        # print "Def WriteReg  addr=(10 num)",int(addr,16),addr
        usb.write('CONF:VOLT:DC D1,H\n')
        usb.write(
            'CONF:REGI 0x' + addr[-4] + addr[-3] + ',0x' + addr[-2] + addr[-1] + ',0x' + substance[-2] + substance[
                -1] + '\n')
        usb.write('CONF:REGI 0x02,0x32,0x01\n')
        try:
            k = add_9516.index(tempadd)
            if add_9516[k] == tempadd:
                value = int(substance, 16)
                reg_9516[k].ChangeLabel(value, tempadd)
        except:
            pass

    elif no == 91391:
        # print "Def WriteReg  addr=(10 num)",int(addr,16)
        usb.write('CONF:VOLT:DC D0,H\n')
        usb.write(
            'CONF:REGI 0x' + addr[-4] + addr[-3] + ',0x' + addr[-2] + addr[-1] + ',0x' + substance[-2] + substance[
                -1] + '\n')
        for k in range(0, 58):
            if add_9139[k] == tempadd:
                tempp = int(str(int(addr, 16)) + '1')
                # print "Def WriteReg  temp=(10 num)",tempp
                reg_91391[k].ChangeLabel(int(substance, 16), tempp)
                break
    elif no == 91392:
        usb.write('CONF:VOLT:DC D2,H\n')
        usb.write(
            'CONF:REGI 0x' + addr[-4] + addr[-3] + ',0x' + addr[-2] + addr[-1] + ',0x' + substance[-2] + substance[
                -1] + '\n')

        for k in range(0, 58):
            if add_9139[k] == tempadd:
                reg_91392[k].ChangeLabel(int(substance, 16), int(str(int(addr, 16)) + '2'))
                break
    elif no == 5732:
        usb.write('CONF:VOLT:DC D3,H\n')
        usb.write('CONF:REGI 0x0C,0x00,0x03\n')
        usb.write('CONF:REGI 0x1C,0x00,0x00\n')
        usb.write('CONF:REGI 0x1D,0x00,0x00\n')
        usb.write('CONF:REGI 0x10,0x00,0x05\n')
        usb.write(
            'CONF:REGI 0x' + addr[-4] + addr[-3] + ',0x' + addr[-2] + addr[-1] + ',0x' + substance[-2] + substance[
                -1] + '\n')


class Status_Button2(wx.ToggleButton):
    image1 = None
    image2 = None
    bitmap1 = None
    bitmap2 = None

    def __init__(self, parent, pos=wx.DefaultPosition, size=(20, 20)):
        if Status_Button2.bitmap1 is None:
            Status_Button2.image1 = wx.Image(ImagePath + "status2.jpg", wx.BITMAP_TYPE_ANY)
            Status_Button2.image1.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)
            Status_Button2.image2 = wx.Image(ImagePath + "status_off.jpg", wx.BITMAP_TYPE_ANY)
            Status_Button2.image2.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

            Status_Button2.bitmap1 = wx.BitmapFromImage(Status_Button2.image1)
            Status_Button2.bitmap2 = wx.BitmapFromImage(Status_Button2.image2)
        wx.ToggleButton.__init__(self, parent, -1, '', pos=pos, size=size, style=wx.BU_AUTODRAW | wx.NO_BORDER)
        self.SetBitmap(Status_Button2.bitmap1)
        self.SetBitmapSelected(Status_Button2.bitmap2)


class SPDT_Button(wx.ToggleButton):
    def __init__(self, parent, pos=(600, 10), size=(120, 100)):
        self.name = 'SPDT'
        self.image1 = wx.Image(ImagePath + "SPDT1.jpg", wx.BITMAP_TYPE_ANY)
        self.image1.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)
        self.image2 = wx.Image(ImagePath + "SPDT2.jpg", wx.BITMAP_TYPE_ANY)
        self.image2.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

        self.bitmap1 = wx.BitmapFromImage(self.image1)
        self.bitmap2 = wx.BitmapFromImage(self.image2)
        # buttons.GenBitmapToggleButton.__init__(self,parent, id, self.bitmap1 ,style=wx.BU_AUTODRAW|wx.NO_BORDER)
        wx.ToggleButton.__init__(self, parent, -1, '', pos=pos, size=size, style=wx.BU_AUTODRAW | wx.NO_BORDER)
        self.SetBitmap(self.bitmap1)
        self.SetBitmapSelected(self.bitmap2)

        # self.SetInitialSize()


class Register_Button(wx.ToggleButton):
    image1 = None
    image2 = None
    bitmap1 = None
    bitmap2 = None

    def __init__(self, parent, pos=wx.DefaultPosition, size=(15, 15)):
        if Register_Button.bitmap1 is None:
            Register_Button.image1 = wx.Image(ImagePath + "register_off.jpg", wx.BITMAP_TYPE_ANY)
            Register_Button.image1.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)
            Register_Button.image2 = wx.Image(ImagePath + "register_on.jpg", wx.BITMAP_TYPE_ANY)
            Register_Button.image2.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

            Register_Button.bitmap1 = wx.BitmapFromImage(Register_Button.image1)
            Register_Button.bitmap2 = wx.BitmapFromImage(Register_Button.image2)
        # buttons.GenBitmapToggleButton.__init__(self,parent, id, self.bitmap1 ,style=wx.BU_AUTODRAW|wx.NO_BORDER)
        wx.ToggleButton.__init__(self, parent, -1, '', pos=pos, size=size, style=wx.BU_AUTODRAW | wx.NO_BORDER)
        self.SetBitmap(Register_Button.bitmap1)
        # self.add=addr
        self.SetBitmapSelected(Register_Button.bitmap2)

        # self.SetInitialSize()


class Status_Button(wx.ToggleButton):
    def __init__(self, parent, pos=(600, 10), size=(60, 60)):
        self.name = 'SPDT'
        self.image1 = wx.Image(ImagePath + "status_on.jpg", wx.BITMAP_TYPE_ANY)
        self.image1.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)
        self.image2 = wx.Image(ImagePath + "status_off.jpg", wx.BITMAP_TYPE_ANY)
        self.image2.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

        self.bitmap1 = wx.BitmapFromImage(self.image1)
        self.bitmap2 = wx.BitmapFromImage(self.image2)
        # buttons.GenBitmapToggleButton.__init__(self,parent, id, self.bitmap1 ,style=wx.BU_AUTODRAW|wx.NO_BORDER)
        wx.ToggleButton.__init__(self, parent, -1, '', pos=pos, size=size, style=wx.BU_AUTODRAW | wx.NO_BORDER)
        self.SetBitmap(self.bitmap1)
        self.SetBitmapSelected(self.bitmap2)


class Reset_Button(wx.ToggleButton):
    def __init__(self, parent, pos=(600, 10), size=(30, 30)):
        self.name = 'SPDT'
        self.image1 = wx.Image(ImagePath + "reset1.jpg", wx.BITMAP_TYPE_ANY)
        self.image1.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)
        self.image2 = wx.Image(ImagePath + "reset2.jpg", wx.BITMAP_TYPE_ANY)
        self.image2.Rescale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

        self.bitmap1 = wx.BitmapFromImage(self.image1)
        self.bitmap2 = wx.BitmapFromImage(self.image2)
        # buttons.GenBitmapToggleButton.__init__(self,parent, id, self.bitmap1 ,style=wx.BU_AUTODRAW|wx.NO_BORDER)
        wx.ToggleButton.__init__(self, parent, -1, '', pos=pos, size=size, style=wx.BU_AUTODRAW | wx.NO_BORDER)
        self.SetBitmap(self.bitmap1)
        self.SetBitmapSelected(self.bitmap2)


class OUT_Button(wx.ToggleButton):
    def __init__(self, parent, label, pos=(600, 10), size=(400, 30)):
        self.name = 'OUT'
        # self.image1=wx.Image("OUT2.jpg", wx.BITMAP_TYPE_ANY )
        # self.image1.Rescale(size[0],size[1],quality=wx.IMAGE_QUALITY_HIGH )
        # self.image2=wx.Image("OUT1.jpg", wx.BITMAP_TYPE_ANY )
        # self.image2.Rescale(size[0],size[1],quality=wx.IMAGE_QUALITY_HIGH)

        # self.bitmap1=wx.BitmapFromImage(self.image1)
        # self.bitmap2=wx.BitmapFromImage(self.image2)

        wx.ToggleButton.__init__(self, parent, -1, label, pos=pos, size=wx.Size(50, 30), style=wx.BU_AUTODRAW)
        # |wx.NO_BORDER
        # self.SetBitmap(self.bitmap1)
        # self.SetBitmapSelected(self.bitmap2)


class Register_RAW_9139(wx.Panel):
    SIZEK = (15, 15)

    def __init__(self, parent, i):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.content = 0
        self.chip = 0
        gSizer1 = wx.GridSizer(1, 10, 2, 2)
        self.addr = i
        str_i = '%X' % i
        len_str = len(str_i)
        if len_str == 1:
            str_i = '0' + str_i

        m_staticText1 = wx.StaticText(self, wx.ID_ANY, str_i, wx.DefaultPosition, Register_RAW_9139.SIZEK, 0)
        m_staticText1.Wrap(-1)
        gSizer1.Add(m_staticText1, 0, wx.ALL, 0)

        self.m_toggleBtn1 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn1.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton7Click)
        gSizer1.Add(self.m_toggleBtn1, 0, wx.ALL, 0)

        self.m_toggleBtn2 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn2.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton6Click)
        gSizer1.Add(self.m_toggleBtn2, 0, wx.ALL, 0)

        self.m_toggleBtn3 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn3.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton5Click)
        gSizer1.Add(self.m_toggleBtn3, 0, wx.ALL, 0)

        self.m_toggleBtn4 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn4.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton4Click)
        gSizer1.Add(self.m_toggleBtn4, 0, wx.ALL, 0)

        self.m_toggleBtn5 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn5.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton3Click)
        gSizer1.Add(self.m_toggleBtn5, 0, wx.ALL, 0)

        self.m_toggleBtn6 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn6.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton2Click)
        gSizer1.Add(self.m_toggleBtn6, 0, wx.ALL, 0)

        self.m_toggleBtn7 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn7.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton1Click)
        gSizer1.Add(self.m_toggleBtn7, 0, wx.ALL, 0)

        self.m_toggleBtn8 = Register_Button(self, wx.DefaultPosition, Register_RAW_9139.SIZEK)
        self.m_toggleBtn8.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton0Click)
        gSizer1.Add(self.m_toggleBtn8, 0, wx.ALL, 0)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"00", wx.DefaultPosition, Register_RAW_9139.SIZEK, 0)
        self.m_staticText2.Wrap(-1)

        gSizer1.Add(self.m_staticText2, 0, wx.ALL, 0)
        self.SetSizer(gSizer1)

    def ChangeLabel(self, s, addr):
        # print addr
        global reg_91391, reg_91392, add_9139
        if addr % 2 == 1:
            addr = str(addr)
            if addr != '1':
                addr = addr[:-1]
                if len(addr) != 0:
                    addr = int(addr)
            elif addr == '1':
                addr = 0
            for j in range(0, 58):
                if add_9139[j] == addr:
                    reg_91391[j].content = s
                    reg_91391[j].addr = addr
                    reg_91391[j].m_staticText2.SetLabel('%X' % s)
                    break

            tempcontent = reg_91391[j].content
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn8.GetValue() == True:
                reg_91391[j].m_toggleBtn8.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn8.GetValue() == False:
                reg_91391[j].m_toggleBtn8.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn7.GetValue() == True:
                reg_91391[j].m_toggleBtn7.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn7.GetValue() == False:
                reg_91391[j].m_toggleBtn7.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn6.GetValue() == True:
                reg_91391[j].m_toggleBtn6.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn6.GetValue() == False:
                reg_91391[j].m_toggleBtn6.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn5.GetValue() == True:
                reg_91391[j].m_toggleBtn5.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn5.GetValue() == False:
                reg_91391[j].m_toggleBtn5.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn4.GetValue() == True:
                reg_91391[j].m_toggleBtn4.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn4.GetValue() == False:
                reg_91391[j].m_toggleBtn4.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn3.GetValue() == True:
                reg_91391[j].m_toggleBtn3.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn3.GetValue() == False:
                reg_91391[j].m_toggleBtn3.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn2.GetValue() == True:
                reg_91391[j].m_toggleBtn2.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn2.GetValue() == False:
                reg_91391[j].m_toggleBtn2.SetValue(True)

            tempcontent = tempcontent / 2
            if tempcontent % 2 == 0 and reg_91391[j].m_toggleBtn1.GetValue() == True:
                reg_91391[j].m_toggleBtn1.SetValue(False)
            if tempcontent % 2 == 1 and reg_91391[j].m_toggleBtn1.GetValue() == False:
                reg_91391[j].m_toggleBtn1.SetValue(True)

        elif addr % 2 == 0:
            addr = str(addr)
            addr = addr[:-1]
            if len(addr) != 0:
                addr = int(addr)
                for j in range(0, 58):
                    if add_9139[j] == addr:
                        reg_91392[j].content = s
                        reg_91392[j].addr = addr
                        reg_91392[j].m_staticText2.SetLabel('%X' % s)
                        break

                tempcontent = reg_91392[j].content
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn8.GetValue() == True:
                    reg_91392[j].m_toggleBtn8.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn8.GetValue() == False:
                    reg_91392[j].m_toggleBtn8.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn7.GetValue() == True:
                    reg_91392[j].m_toggleBtn7.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn7.GetValue() == False:
                    reg_91392[j].m_toggleBtn7.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn6.GetValue() == True:
                    reg_91392[j].m_toggleBtn6.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn6.GetValue() == False:
                    reg_91392[j].m_toggleBtn6.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn5.GetValue() == True:
                    reg_91392[j].m_toggleBtn5.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn5.GetValue() == False:
                    reg_91392[j].m_toggleBtn5.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn4.GetValue() == True:
                    reg_91392[j].m_toggleBtn4.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn4.GetValue() == False:
                    reg_91392[j].m_toggleBtn4.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn3.GetValue() == True:
                    reg_91392[j].m_toggleBtn3.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn3.GetValue() == False:
                    reg_91392[j].m_toggleBtn3.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn2.GetValue() == True:
                    reg_91392[j].m_toggleBtn2.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn2.GetValue() == False:
                    reg_91392[j].m_toggleBtn2.SetValue(True)

                tempcontent = tempcontent / 2
                if tempcontent % 2 == 0 and reg_91392[j].m_toggleBtn1.GetValue() == True:
                    reg_91392[j].m_toggleBtn1.SetValue(False)
                if tempcontent % 2 == 1 and reg_91392[j].m_toggleBtn1.GetValue() == False:
                    reg_91392[j].m_toggleBtn1.SetValue(True)


class Register_RAW_9516(wx.Panel):
    SIZEJ = (22, 22)
    global Link_9516

    def __init__(self, parent, i):

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        Link_9516 = self
        self.content = 0
        gSizer1 = wx.GridSizer(1, 10, 2, 2)
        self.addr = i
        self.chip = 0

        str_i = '%X' % i
        len_str = len(str_i)
        if len_str == 2:
            str_i = '0' + str_i

        if len_str == 1:
            str_i = '00' + str_i

        m_staticText1 = wx.StaticText(self, wx.ID_ANY, str_i, wx.DefaultPosition, Register_RAW_9516.SIZEJ, 0)
        m_staticText1.Wrap(-1)
        gSizer1.Add(m_staticText1, 0, wx.ALL, 0)

        self.m_toggleBtn1 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn1.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton7Click)
        gSizer1.Add(self.m_toggleBtn1, 0, wx.ALL, 0)

        self.m_toggleBtn2 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn2.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton6Click)
        gSizer1.Add(self.m_toggleBtn2, 0, wx.ALL, 0)

        self.m_toggleBtn3 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn3.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton5Click)
        gSizer1.Add(self.m_toggleBtn3, 0, wx.ALL, 0)

        self.m_toggleBtn4 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn4.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton4Click)
        gSizer1.Add(self.m_toggleBtn4, 0, wx.ALL, 0)

        self.m_toggleBtn5 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn5.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton3Click)
        gSizer1.Add(self.m_toggleBtn5, 0, wx.ALL, 0)

        self.m_toggleBtn6 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn6.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton2Click)
        gSizer1.Add(self.m_toggleBtn6, 0, wx.ALL, 0)

        self.m_toggleBtn7 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn7.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton1Click)
        gSizer1.Add(self.m_toggleBtn7, 0, wx.ALL, 0)

        self.m_toggleBtn8 = Register_Button(self, wx.DefaultPosition, Register_RAW_9516.SIZEJ)
        self.m_toggleBtn8.Bind(wx.EVT_TOGGLEBUTTON, Event().OnRegisterButton0Click)
        gSizer1.Add(self.m_toggleBtn8, 0, wx.ALL, 0)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"00", wx.DefaultPosition, Register_RAW_9516.SIZEJ, 0)
        self.m_staticText2.Wrap(-1)

        gSizer1.Add(self.m_staticText2, 0, wx.ALL, 0)

        self.SetSizer(gSizer1)

    def ChangeLabel(self, s, addr):
        global reg_9516
        global add_9516
        for j in range(0, 64):
            if add_9516[j] == addr:
                reg_9516[j].content = s
                reg_9516[j].addr = addr
                reg_9516[j].m_staticText2.SetLabel('%X' % s)
                break

        tempcontent = reg_9516[j].content
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn8.GetValue() == True:
            reg_9516[j].m_toggleBtn8.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn8.GetValue() == False:
            reg_9516[j].m_toggleBtn8.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn7.GetValue() == True:
            reg_9516[j].m_toggleBtn7.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn7.GetValue() == False:
            reg_9516[j].m_toggleBtn7.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn6.GetValue() == True:
            reg_9516[j].m_toggleBtn6.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn6.GetValue() == False:
            reg_9516[j].m_toggleBtn6.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn5.GetValue() == True:
            reg_9516[j].m_toggleBtn5.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn5.GetValue() == False:
            reg_9516[j].m_toggleBtn5.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn4.GetValue() == True:
            reg_9516[j].m_toggleBtn4.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn4.GetValue() == False:
            reg_9516[j].m_toggleBtn4.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn3.GetValue() == True:
            reg_9516[j].m_toggleBtn3.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn3.GetValue() == False:
            reg_9516[j].m_toggleBtn3.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn2.GetValue() == True:
            reg_9516[j].m_toggleBtn2.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn2.GetValue() == False:
            reg_9516[j].m_toggleBtn2.SetValue(True)

        tempcontent /= 2
        if tempcontent % 2 == 0 and reg_9516[j].m_toggleBtn1.GetValue() == True:
            reg_9516[j].m_toggleBtn1.SetValue(False)
        if tempcontent % 2 == 1 and reg_9516[j].m_toggleBtn1.GetValue() == False:
            reg_9516[j].m_toggleBtn1.SetValue(True)


class Register_Panel_9139(wx.Panel):
    global add_9139, reg_91391

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(643, 335),
                          style=wx.TAB_TRAVERSAL)
        gSizer = wx.GridSizer(1, 0, 0, 0)
        gSizer0 = wx.GridSizer(0, 1, 0, 0)
        gSizer01 = wx.GridSizer(0, 1, 0, 0)
        gSizer02 = wx.GridSizer(0, 1, 0, 0)
        gSizer03 = wx.GridSizer(0, 1, 0, 0)

        staticText_9139_1 = wx.StaticText(self, wx.ID_ANY, u"9139 1", wx.DefaultPosition, wx.DefaultSize, 0)
        staticText_9139_1.Wrap(-1)
        gSizer0.Add(staticText_9139_1, 0, wx.ALL, 5)
        num = 0
        list_9139 = [0, 1, 3, 11, 13, 14, 16, 18, 20, 25, 28, 40, 57, 57, 59, 60, 63, 63, 65, 68, 94, 104, 106, 108,
                     127, 127]
        for j in range(0, len(list_9139)):
            if j % 2 == 0:
                for k in range(list_9139[j], list_9139[j + 1] + 1):
                    handle = Register_RAW_9139(self, k)
                    handle.chip = 91391
                    reg_91391.append(handle)
                    # print 'handle.addr=',handle.addr
                    num = num + 1
                    add_9139.append(k)
                    if num < 28:
                        gSizer0.Add(reg_91391[-1], 1, wx.ALL, 0)
                    if num >= 28 and num < 60:
                        gSizer01.Add(reg_91391[-1], 1, wx.ALL, 0)
                        # if num>=50 and num<75:
                        # gSizer02.Add(reg_9516[-1],1,wx.ALL, 0)
        staticText_9139_2 = wx.StaticText(self, wx.ID_ANY, u"9139 2", wx.DefaultPosition, wx.DefaultSize, 0)
        staticText_9139_2.Wrap(-1)
        gSizer02.Add(staticText_9139_2, 0, wx.ALL, 5)
        num = 0
        for j in range(0, len(list_9139)):
            if j % 2 == 0:
                for k in range(list_9139[j], list_9139[j + 1] + 1):

                    handle = Register_RAW_9139(self, k)

                    handle.chip = 91392
                    reg_91392.append(handle)
                    num = num + 1
                    if num < 28:
                        gSizer02.Add(reg_91392[-1], 1, wx.ALL, 0)
                    if num >= 28 and num < 60:
                        gSizer03.Add(reg_91392[-1], 1, wx.ALL, 0)

        gSizer.Add(gSizer0, 2, wx.EXPAND, 5)
        gSizer.Add(gSizer01, 2, wx.EXPAND, 5)
        gSizer.Add(gSizer02, 2, wx.EXPAND, 5)
        gSizer.Add(gSizer03, 2, wx.EXPAND, 5)
        self.SetSizer(gSizer)
        self.Layout()


class Register_Panel_9516(wx.Panel):
    global add_9516
    global reg_9516

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(643, 335),
                          style=wx.TAB_TRAVERSAL)
        gSizer = wx.GridSizer(1, 0, 0, 0)
        gSizer0 = wx.GridSizer(0, 1, 0, 0)
        gSizer01 = wx.GridSizer(0, 1, 0, 0)
        gSizer02 = wx.GridSizer(0, 1, 0, 0)
        gSizer03 = wx.GridSizer(0, 1, 0, 0)
        # gSizer04 = wx.GridSizer( 0, 1, 0, 0)
        list_9516 = [0, 0, 3, 4, 16, 31, 160, 171, 240, 245, 320, 323, 400, 418, 480, 481, 560, 560, 562, 562]
        # xx=0
        num = 0
        for j in range(0, len(list_9516)):
            if j % 2 == 0:
                for k in range(list_9516[j], list_9516[j + 1] + 1):
                    handle = Register_RAW_9516(self, k)
                    handle.chip = 9516
                    reg_9516.append(handle)
                    num = num + 1
                    add_9516.append(k)
                    # print len(reg_9516)
                    # print 'add',k
                    if num < 21:
                        gSizer0.Add(reg_9516[-1], 1, wx.ALL, 0)
                    if num >= 21 and num < 43:
                        gSizer01.Add(reg_9516[-1], 1, wx.ALL, 0)
                    if num >= 43 and num < 65:
                        gSizer02.Add(reg_9516[-1], 1, wx.ALL, 0)
        gSizer.Add(gSizer0, 1, wx.EXPAND, 5)
        gSizer.Add(gSizer01, 1, wx.EXPAND, 5)
        gSizer.Add(gSizer02, 1, wx.EXPAND, 5)
        # gSizer.Add(gSizer02,1,wx.EXPAND, 5)

        # gSizer.Add(gSizer04,1,wx.EXPAND, 5)
        self.SetSizer(gSizer)
        self.Layout()


class Event:
    def __init__(self):
        self.Theard_Flag = False

    def OnToolBarClick(self, evt):
        toolbar = evt.GetEventObject()
        id = evt.GetId()
        pos = toolbar.GetToolPos(id)
        global DefaultSaveFilePath, MainFrameLink, reg_9516, add_9516
        if pos == 0:
            ll = []
            filestyle = "Data files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(MainFrameLink.d9516, message="Open file ...", defaultDir=DefaultSaveFilePath,
                                defaultFile="", wildcard=filestyle, style=wx.OPEN)
            result = dlg.ShowModal()
            # dlg.Destroy()

            if result == wx.ID_OK:
                path = dlg.GetPaths()
                f = file(path[0], 'r')
                judge = f.readline()
                data = f.readlines()

                if judge == 'CONF:VOLT:DC D1,H\n':
                    # print len(data)
                    for i in range(0, len(data)):
                        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
                        substance = data[i][-3] + data[i][-2]
                        WriteReg(9516, site, substance)
                        OnPanelChange_9516(site, substance)

                elif judge == 'CONF:VOLT:DC D0,H\n':

                    for i in range(0, len(data)):
                        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
                        substance = data[i][-3] + data[i][-2]
                        WriteReg(91391, site, substance)
                        OnPanelChange_91391(site, substance)

                elif judge == 'CONF:VOLT:DC D2\n':

                    for i in range(0, len(data)):
                        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
                        substance = data[i][-3] + data[i][-2]
                        WriteReg(91392, site, substance)
                        OnPanelChange_91392(site, substance)

                elif judge == 'CONF:VOLT:DC D3,H\n':

                    for i in range(0, len(data)):
                        site = data[i][12] + data[i][13] + data[i][17] + data[i][18]
                        substance = data[i][-3] + data[i][-2]
                        # print 'site,substance',site,substance
                        WriteReg(5732, site, substance)
                        OnPanelChange_5732(site, substance)
                f.close()

        elif pos == 1:
            filestyle = "Data files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(MainFrameLink.d9516, message="Save file as ...", defaultDir=DefaultSaveFilePath,
                                defaultFile="", wildcard=filestyle, style=wx.SAVE)
            result = dlg.ShowModal()
            # dlg.Destroy()
            if result == wx.ID_OK:
                path = dlg.GetPath()
                # print path
                f = file(path, 'w')
                f.write('CONF:VOLT:DC D1,H\n')

                for i in range(0, 64):
                    site = '%X' % add_9516[i]
                    while 4 - len(site) != 0:
                        site = '0' + site
                    substance = '%X' % reg_9516[i].content
                    if len(substance) == 1:
                        substance = '0' + substance
                    f.write('CONF:REGI 0x' + site[0:2] + ',0x' + site[2:4] + ',0x' + substance + '\n')
                f.close()
        elif pos == 2:
            filestyle = "Data files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(MainFrameLink.d9516, message="Save file as ...", defaultDir=DefaultSaveFilePath,
                                defaultFile="", wildcard=filestyle, style=wx.SAVE)
            result = dlg.ShowModal()
            # dlg.Destroy()
            if result == wx.ID_OK:
                path = dlg.GetPath()
                # print path
                f = file(path, 'w')
                f.write('CONF:VOLT:DC D0,H\n')

                for i in range(0, 58):
                    site = '%X' % add_9139[i]
                    while 4 - len(site) != 0:
                        site = '0' + site
                    substance = '%X' % reg_91391[i].content
                    if len(substance) == 1:
                        substance = '0' + substance
                    f.write('CONF:REGI 0x' + site[0:2] + ',0x' + site[2:4] + ',0x' + substance + '\n')
                f.close()
        elif pos == 3:
            filestyle = "Data files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(MainFrameLink.d9516, message="Save file as ...", defaultDir=DefaultSaveFilePath,
                                defaultFile="", wildcard=filestyle, style=wx.SAVE)
            result = dlg.ShowModal()
            # dlg.Destroy()
            if result == wx.ID_OK:
                path = dlg.GetPath()
                # print path
                f = file(path, 'w')
                f.write('CONF:VOLT:DC D2,H\n')

                for i in range(0, 58):
                    site = '%X' % add_9139[i]
                    while 4 - len(site) != 0:
                        site = '0' + site
                    substance = '%X' % reg_91392[i].content
                    if len(substance) == 1:
                        substance = '0' + substance
                    f.write('CONF:REGI 0x' + site[0:2] + ',0x' + site[2:4] + ',0x' + substance + '\n')
                f.close()
        elif pos == 4:
            a = MainFrameLink.d5732.m_textCtrl8.GetValue()
            a = string.atof(a)
            # print a
            a = int(a / 4.096 * 32768)
            temp = bin(a)
            if a > 0:
                # print '0'
                temp = temp[2:] + '00'
                while (16 - len(temp)) is not 0:
                    temp = '0' + temp
                # print len(temp)

                temp = bin2hex(temp)
                # print temp,temp
                if len(temp) == 1:
                    # print '0'
                    temp = '000' + temp
                if len(temp) == 2:
                    temp = '00' + temp
                if len(temp) == 3:
                    temp = '0' + temp
                    # print 'final=',temp
            elif a == 0:
                temp = '0000'
            elif a < 0:
                temp = temp[3:]
                for k in range(0, len(temp)):
                    if temp[k] == '0':
                        temp = temp[:k] + '1' + temp[k + 1:]
                    elif temp[k] == '1':
                        temp = temp[:k] + '0' + temp[k + 1:]
                # print 'reverse=',temp
                k = len(temp) - 1
                while (temp[k] == '1' and k > 0):
                    temp = temp[:k] + '0' + temp[k + 1:]
                    k = k - 1
                # print 'k=',k
                temp = temp[:k] + '1' + temp[k + 1:]
                temp = temp + '00'
                while ((15 - len(temp)) != 0):
                    temp = '0' + temp
                temp = '1' + temp
                # print len(temp)
                temp = bin2hex(temp)
                if len(temp) == 1:
                    temp = '000' + temp
                if len(temp) == 2:
                    temp = '00' + temp
                if len(temp) == 3:
                    temp = '0' + temp

            a = MainFrameLink.d5732.m_textCtrl10.GetValue()
            a = string.atof(a)
            a = int(a / 4.096 * 32768)
            tempp = bin(a)
            if a > 0:
                # print '0'
                tempp = tempp[2:] + '00'
                while (16 - len(tempp)) is not 0:
                    tempp = '0' + tempp
                # print len(tempp)

                tempp = bin2hex(tempp)
                # print tempp,tempp
                if len(tempp) == 1:
                    # print '0'
                    tempp = '000' + tempp
                if len(tempp) == 2:
                    tempp = '00' + tempp
                if len(tempp) == 3:
                    tempp = '0' + tempp
                    # print 'final=',tempp
            elif a == 0:
                tempp = '0000'
            elif a < 0:
                tempp = tempp[3:]
                for k in range(0, len(tempp)):
                    if tempp[k] == '0':
                        tempp = tempp[:k] + '1' + tempp[k + 1:]
                    elif tempp[k] == '1':
                        tempp = tempp[:k] + '0' + tempp[k + 1:]
                # print 'reverse=',tempp
                k = len(tempp) - 1
                while tempp[k] == '1' and k > 0:
                    tempp = tempp[:k] + '0' + tempp[k + 1:]
                    k -= 1
                # print 'k=',k
                tempp = tempp[:k] + '1' + tempp[k + 1:]
                tempp += '00'
                while (15 - len(tempp)) != 0:
                    tempp = '0' + tempp
                tempp = '1' + tempp
                # print len(tempp)
                tempp = bin2hex(tempp)
                if len(tempp) == 1:
                    tempp = '000' + tempp
                if len(tempp) == 2:
                    tempp = '00' + tempp
                if len(temp) == 3:
                    tempp = '0' + tempp
            filestyle = "Data files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(MainFrameLink.d9516, message="Save file as ...", defaultDir=DefaultSaveFilePath,
                                defaultFile="", wildcard=filestyle, style=wx.SAVE)
            result = dlg.ShowModal()
            # dlg.Destroy()
            f = None
            if result == wx.ID_OK:
                path = dlg.GetPath()
                # print path
                f = file(path, 'w')
                f.write('CONF:VOLT:DC D3,H\n')
                f.write('CONF:REGI 0x00,0x' + temp[0:2] + ',0x' + temp[2:4] + '\n')
                f.write('CONF:REGI 0x02,0x' + tempp[0:2] + ',0x' + tempp[2:4] + '\n')
            f.close()

        elif pos == 5:
            thd = threading.Thread(target=openfile_9516, args=())
            thd.start()

        elif pos == 6:
            thd = threading.Thread(target=openfile_9139, args=())
            thd.start()

        elif pos == 7:
            thd = threading.Thread(target=openfile_5732, args=())
            thd.start()

    def OnRegisterButton7Click(self, evt):
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
            # #####content#########
        if a:
            hand.content += 128
            temp_value = int(temp_value, 16) + 128
        if not a:
            hand.content -= 128
            temp_value = int(temp_value, 16) - 128
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton6Click(self, evt):
        # print 'enter 6'
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        # print 'hand.addr=',hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
            ######content#########
        if a == True:
            hand.content = hand.content + 64
            temp_value = int(temp_value, 16) + 64
        if a == False:
            hand.content = hand.content - 64
            temp_value = int(temp_value, 16) - 64
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton5Click(self, evt):
        # print '2'
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a
        hand = RegButton.GetParent()
        # print 'hand.addr=',hand.addr
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
        ######content#########
        if a == True:
            hand.content = hand.content + 32
            temp_value = int(temp_value, 16) + 32
        if a == False:
            hand.content = hand.content - 32
            temp_value = int(temp_value, 16) - 32
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton4Click(self, evt):
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
            ######content#########
        if a == True:
            hand.content = hand.content + 16
            temp_value = int(temp_value, 16) + 16
        if a == False:
            hand.content = hand.content - 16
            temp_value = int(temp_value, 16) - 16
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton3Click(self, evt):
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
        ######content#########
        if a == True:
            hand.content = hand.content + 8
            temp_value = int(temp_value, 16) + 8
        if a == False:
            hand.content = hand.content - 8
            temp_value = int(temp_value, 16) - 8
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton2Click(self, evt):
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        # print a  
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
            ######content#########
        if a == True:
            hand.content = hand.content + 4
            temp_value = int(temp_value, 16) + 4
        if a == False:
            hand.content = hand.content - 4
            temp_value = int(temp_value, 16) - 4
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton1Click(self, evt):
        # print '6'
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        site = str(site)
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
        ######content#########
        if a == True:
            hand.content = hand.content + 2
            temp_value = int(temp_value, 16) + 2
        if a == False:
            hand.content = hand.content - 2
            temp_value = int(temp_value, 16) - 2
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnRegisterButton0Click(self, evt):
        RegButton = evt.GetEventObject()
        a = RegButton.GetValue()
        hand = RegButton.GetParent()
        temp_value = hand.m_staticText2.GetLabel()
        site = '%X' % hand.addr
        if len(site) == 3:
            site = '0' + site
        if len(site) == 2:
            site = '00' + site
        if len(site) == 1:
            site = '000' + site
            ######content#########
        if a == True:
            hand.content = hand.content + 1
            temp_value = int(temp_value, 16) + 1
        if a == False:
            hand.content = hand.content - 1
            temp_value = int(temp_value, 16) - 1
        temp_value = '%X' % temp_value
        hand.m_staticText2.SetLabel(temp_value)

        substance = '%X' % hand.content
        # substance=str(substance)
        if len(substance) == 1:
            substance = '0' + substance
        if hand.chip == 9516:
            WriteReg(9516, site, substance)
            OnPanelChange_9516(site, substance)
        if hand.chip == 91391:
            WriteReg(91391, site, substance)
            OnPanelChange_91391(site, substance)
        if hand.chip == 91392:
            WriteReg(91392, site, substance)
            OnPanelChange_91392(site, substance)

    def OnReset_ButtonClick(self, evt):
        toggleb = evt.GetEventObject()
        # a=toggleb.GetValue()


        # WriteReg(9516,'0000','3C')
        # WriteReg(9516,'0000','18')
        # toggleb.SetValue(False)
        InitialParameter_9516()
        toggleb.SetValue(False)

    def OnSPDTButtonClick(self, evt):
        toggleb = evt.GetEventObject()
        a = toggleb.GetValue()
        # print a
        if a == True:
            WriteReg2(9516, '01E1', '02')
        if a == False:
            WriteReg2(9516, '01E1', '01')

    def OnOut0ButtonClick(self, evt):
        toggleb = evt.GetEventObject()

        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F0', '0C')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F0', '0E')

    def OnOut1ButtonClick(self, evt):
        toggleb = evt.GetEventObject()

        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F1', '0C')

        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F1', '0E')

    def OnOut2ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F2', '0C')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F2', '0E')

    def OnOut3ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F3', '0C')

        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F3', '0E')

    def OnOut4ButtonClick(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F4', '0C')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F4', '0E')

    def OnOut5ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '00F5', '0C')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '00F5', '0E')

    def OnOut6ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '0140', '03')
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '0140', '02')

    def OnOut7ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '0141', '03')
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '0141', '02')

    def OnOut8ButtonClick(self, evt):

        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '0142', '02')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '0142', '03')

    def OnOut9ButtonClick(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        a = toggleb.GetLabel()
        if a == "ON":
            toggleb.SetValue(True)
            WriteReg(9516, '0043', '02')
        if a == "OFF":
            toggleb.SetValue(False)
            WriteReg(9516, '0043', '03')

    def OnSelectComboValue_VCO_DIVIDER(self, evt):

        combo_p = evt.GetEventObject()
        a = combo_p.GetStringSelection()
        if a == '2':
            WriteReg(9516, '00E0', '00')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x01,0xE0,0x00')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')
        if a == "3":
            WriteReg(9516, '00E0', '01')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x01,0xE0,0x01')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "4":
            WriteReg(9516, '00E0', '02')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x01,0xE0,0x02')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "5":
            WriteReg(9516, '00E0', '03')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x01,0xE0,0x03')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "6":
            WriteReg(9516, '00E0', '04')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x01,0xE0,0x04')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')       

    def OnSelectComboValue_p(self, evt):

        combo_p = evt.GetEventObject()
        a = combo_p.GetStringSelection()
        # combo_p.SetSelection(1)
        if a == '1 FD(VCO Max 300MHz)':
            WriteReg2(9516, '0016', '00')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x00')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')
        if a == "2 FD(VCO Max 600MHz)":
            WriteReg2(9516, '0016', '01')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x01')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "2 DM(VCO Max 200MHz)":
            WriteReg2(9516, '0016', '02')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x02')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "3 FD(VCO Max 900MHz)":
            WriteReg2(9516, '0016', '07')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x07')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n') 
        if a == "4 DM(VCO Max 1000MHz":
            WriteReg2(9516, '0016', '03')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x03')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')  
        if a == "8 DM(VCO Max 2400MHz)":
            WriteReg2(9516, '0016', '04')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x04')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')   
        if a == "16 DM(VCO Max 3000MHz)":
            WriteReg2(9516, '0016', '05')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x05')
            # usb.write('CONF:REGI 0x02,0x32,0x05\n') 
        if a == "32 DM(VCO Max 3000MHz)":
            WriteReg2(9516, '0016', '06')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x16,0x06')
            # usb.write('CONF:REGI 0x02,0x32,0x06\n') 
        PP = MainFrameLink.d9516.comboBox_P.GetSelection()
        # print PP
        if PP == 0:
            P = 1
        elif PP == 1:
            P = 2
        elif PP == 2:
            P = 2
        elif PP == 3:
            P = 3
        elif PP == 4:
            P = 4
        elif PP == 5:
            P = 8
        elif PP == 6:
            P = 16
        elif PP == 7:
            P = 32
        R = int(MainFrameLink.d9516.textCtrl_R_dil.GetValue())
        A = int(MainFrameLink.d9516.textCtrl_A.GetValue())
        B = int(MainFrameLink.d9516.textCtrl_B.GetValue())
        result = (10.00 / R) * (P * B + A)
        if result - int(result) != 0:
            # print result-int(result)
            float = (result - int(result)) * 100
            if float - int(float) < 0.5:
                result = int(result) + int(float) / 100.0
            elif float - int(float) >= 0.5:
                result = int(result) + (int(float) + 1) / 100.0
        MainFrameLink.d9516.formula.SetLabel(str(result) + 'MHz')

    def OnSelectComboValue_Ref(self, evt):

        combo_p = evt.GetEventObject()
        a = combo_p.GetStringSelection()
        if a == 'Int_10MHz':
            WriteReg2(9516, '001C', '82')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x1C,0x82\n')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')
        if a == 'Ext_10MHz':
            WriteReg2(9516, '001C', 'C4')
            # usb.write('CONF:VOLT:DC D1,H\n')
            # usb.write('CONF:REGI 0x00,0x1C,0xC4\n')
            # usb.write('CONF:REGI 0x02,0x32,0x01\n')

    def Ontoggle1_left_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    def Ontoggle1_right_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    def Ontoggle2_left_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    def Ontoggle2_right_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    def Ontoggle3_left_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    def Ontoggle3_right_Click(self, evt):
        toggleb = evt.GetEventObject()
        OnChangeToggleButton(toggleb)
        pass

    ############## TextCtrl Def #######################
    def OnChangeTextCtrl_Value_Div1(self, evt):

        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        if OnCheckLegal(s, textctrl_Div1) == True:
            s = int(s)
            if s == 1:
                WriteReg(9516, '0191', '80')
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x91,0x80\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 == s / (2.0):
                c = (s - 2) / 2
                t2 = '%X' % c
                WriteReg(9516, '0191', '00')
                WriteReg(9516, '0190', t2 + t2)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x91,0x00\n')
                # usb.write('CONF:REGI 0x01,0x90,0x'+ t2+t2+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 != s / (2.0):
                b = s - 2
                c = b / 2
                d = b / 2 + 1
                t2 = '%X' % c
                t3 = '%X' % d
                WriteReg(9516, '0191', '00')
                WriteReg(9516, '0190', t2 + t3)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x91,0x00\n')
                # usb.write('CONF:REGI 0x01,0x90,0x'+ t2+t3+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

    def OnChangeTextCtrl_Value_Div2(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        if OnCheckLegal(s, textctrl_Div1) == True:
            s = int(s)
            if s == 1:
                WriteReg(9516, '0194', '80')

                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x94,0x80\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 == s / (2.0):
                c = (s - 2) / 2
                t2 = '%X' % c
                WriteReg(9516, '0194', '00')
                WriteReg(9516, '0193', t2 + t2)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x94,0x00\n')
                # usb.write('CONF:REGI 0x01,0x93,0x'+ t2+t2+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 != s / (2.0):
                b = s - 2
                c = b / 2
                d = b / 2 + 1
                t2 = '%X' % c
                t3 = '%X' % d
                WriteReg(9516, '0194', '00')
                WriteReg(9516, '0193', t2 + t3)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x94,0x00\n') 

    def OnChangeTextCtrl_Value_Div3(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        if OnCheckLegal(s, textctrl_Div1) == True:
            s = int(s)
            if s == 1:
                WriteReg(9516, '0197', '80')

                # usb.write('CONF:REGI 0x01,0x93,0x'+ t2+t3+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x97,0x80\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 == s / (2.0):
                c = (s - 2) / 2
                t2 = '%X' % c
                WriteReg(9516, '0197', '00')
                WriteReg(9516, '0196', t2 + t2)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x97,0x00\n')
                # usb.write('CONF:REGI 0x01,0x96,0x'+ t2+t2+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 != s / (2.0):
                b = s - 2
                c = b / 2
                d = b / 2 + 1
                t2 = '%X' % c
                t3 = '%X' % d
                WriteReg(9516, '0197', '00')
                WriteReg(9516, '0196', t2 + t3)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x97,0x00\n')
                # usb.write('CONF:REGI 0x01,0x96,0x'+ t2+t3+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

    def OnChangeTextCtrl_Value_Div4(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        if OnCheckLegal(s, textctrl_Div1) == True:
            s = int(s)
            if s == 1:
                WriteReg(9516, '019C', '30')
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x9C,0x30\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 == s / (2.0):
                c = (s - 2) / 2
                t2 = '%X' % c
                WriteReg(9516, '019C', '20')
                WriteReg(9516, '0199', t2 + t2)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x9C,0x20\n')
                # usb.write('CONF:REGI 0x01,0x99,0x'+ t2+t2+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 != s / (2.0):
                b = s - 2
                c = b / 2
                d = b / 2 + 1
                t2 = '%X' % c
                t3 = '%X' % d
                WriteReg(9516, '019C', '20')
                WriteReg(9516, '0199', t2 + t3)

                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0x9C,0x20\n')
                # usb.write('CONF:REGI 0x01,0x99,0x'+ t2+t3+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

    def OnChangeTextCtrl_Value_Div5(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        if OnCheckLegal(s, textctrl_Div1) == True:
            s = int(s)
            if s == 1:
                WriteReg(9516, '01A1', '30')
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0xA1,0x30\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 == s / (2.0):
                c = (s - 2) / 2
                t2 = '%X' % c
                WriteReg(9516, '01A1', '20')
                WriteReg(9516, '019E', t2 + t2)
                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0xA1,0x20\n')
                # usb.write('CONF:REGI 0x01,0x9E,0x'+ t2+t2+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

            elif s / 2 != s / (2.0):
                b = s - 2
                c = b / 2
                d = b / 2 + 1
                t2 = '%X' % c
                t3 = '%X' % d
                WriteReg(9516, '01A1', '00')
                WriteReg(9516, '019E', t2 + t3)

                # usb.write('CONF:VOLT:DC D1,H\n')
                # usb.write('CONF:REGI 0x01,0xA1,0x00\n')
                # usb.write('CONF:REGI 0x01,0x9E,0x'+ t2+t3+'\n')
                # usb.write('CONF:REGI 0x02,0x32,0x01\n')

    def OnChangeTextCtrl_Value_B(self, evt):
        # print 'enter'
        global reg_9516, add_9516
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        s = str(s)
        for i in s:
            if i not in num:
                textctrl_Div1.SetValue(25)
                temp = wx.MessageBox("Please input integer", "Sorry")
                temp.Destroy()
                # print 'wrong1'
                return
        a = int(s)
        if a < 0 or a > 8191:
            # print 'wrong2'
            textctrl_Div1.SetValue(25)
            temp = wx.MessageBox("Please input integer between 0 and 8191", "Sorry")
            temp.Destroy()
            return
        t2 = '%X' % a
        if len(t2) == 1:
            t2 = '000' + t2
        if len(t2) == 2:
            t2 = '00' + t2
        if len(t2) == 3:
            t2 = '0' + t2
        # WriteReg2(9516,'0014', t2[-2]+t2[-1])
        # WriteReg2(9516,'0015', t2[-4]+t2[-3])


        usb.write('CONF:VOLT:DC D1,H\n')
        usb.write('CONF:REGI 0x00,0x14,0x' + t2[-2] + t2[-1] + '\n')
        usb.write('CONF:REGI 0x00,0x15,0x' + t2[-4] + t2[-3] + '\n')
        usb.write('CONF:REGI 0x00,0x18,0x06\n')
        usb.write('CONF:REGI 0x02,0x32,0x01\n')
        usb.write('CONF:REGI 0x00,0x18,0x07\n')
        usb.write('CONF:REGI 0x02,0x32,0x01\n')

        addr = '0014'
        substance = t2[-2] + t2[-1]
        # print 'len=',len(substance)
        tempadd = int(addr, 16)
        for k in range(0, 64):
            if add_9516[k] == tempadd:
                value = int(substance, 16)
                reg_9516[k].ChangeLabel(value, tempadd)
                break
        addr = '0015'
        substance = t2[-4] + t2[-3]
        # print 'len=',len(substance)
        tempadd = int(addr, 16)
        for k in range(0, 64):
            if add_9516[k] == tempadd:
                value = int(substance, 16)
                reg_9516[k].ChangeLabel(value, tempadd)
                break

        PP = MainFrameLink.d9516.comboBox_P.GetSelection()
        if PP == 0:
            P = 1
        elif PP == 1:
            P = 2
        elif PP == 2:
            P = 2
        elif PP == 3:
            P = 3
        elif PP == 4:
            P = 4
        elif PP == 5:
            P = 8
        elif PP == 6:
            P = 16
        elif PP == 7:
            P = 32
        R = int(MainFrameLink.d9516.textCtrl_R_dil.GetValue())
        A = int(MainFrameLink.d9516.textCtrl_A.GetValue())
        B = int(MainFrameLink.d9516.textCtrl_B.GetValue())
        result = (10.00 / R) * (P * B + A)
        if result - int(result) != 0:
            # print result-int(result)
            float = (result - int(result)) * 100
            if float - int(float) < 0.5:
                result = int(result) + int(float) / 100.0
            elif float - int(float) >= 0.5:
                result = int(result) + (int(float) + 1) / 100.0
        MainFrameLink.d9516.formula.SetLabel(str(result) + 'MHz')

    def OnChangeTextCtrl_Value_A(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')

        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        # print s
        s = str(s)
        for i in s:
            if i not in num:
                textctrl_Div1.SetValue(0)
                temp = wx.MessageBox("Please input integer ", "Sorry")
                temp.Destroy()
                # print 'wrong1'
                return
        a = int(s)
        if a < 0 or a > 63:
            # print 'wrong2'
            textctrl_Div1.SetValue(0)
            temp = wx.MessageBox("Please input integer between 0 and 63", "Sorry")
            temp.Destroy()
        t2 = '%X' % a
        if len(t2) == 1:
            t2 = '000' + t2
        if len(t2) == 2:
            t2 = '00' + t2
        if len(t2) == 3:
            t2 = '0' + t2
        WriteReg2(9516, '0013', t2[-2] + t2[-1])
        # print 'begin'
        PP = MainFrameLink.d9516.comboBox_P.GetSelection()
        if PP == 0:
            P = 1
        elif PP == 1:
            P = 2
        elif PP == 2:
            P = 2
        elif PP == 3:
            P = 3
        elif PP == 4:
            P = 4
        elif PP == 5:
            P = 8
        elif PP == 6:
            P = 16
        elif PP == 7:
            P = 32
        R = int(MainFrameLink.d9516.textCtrl_R_dil.GetValue())
        A = int(MainFrameLink.d9516.textCtrl_A.GetValue())
        B = int(MainFrameLink.d9516.textCtrl_B.GetValue())
        result = (10.00 / R) * (P * B + A)
        if result - int(result) != 0:
            # print result-int(result)
            float = (result - int(result)) * 100
            if float - int(float) < 0.5:
                result = int(result) + int(float) / 100.0
            elif float - int(float) >= 0.5:
                result = int(result) + (int(float) + 1) / 100.0
        MainFrameLink.d9516.formula.SetLabel(str(result) + 'MHz')

    def OnChangeTextCtrl_Value_R_dil(self, evt):
        # usb.write('CONF:VOLT:DC D1,H\n')
        textctrl_Div1 = evt.GetEventObject()
        s = textctrl_Div1.GetValue()
        # print s
        s = str(s)
        for i in s:
            if i not in num:
                textctrl_Div1.SetValue(25)
                temp = wx.MessageBox("Please input integer ", "Sorry")
                temp.Destroy()
                return
        a = int(s)
        if a < 1 or a > 16384:
            textctrl_Div1.SetValue(25)
            temp = wx.MessageBox("Please input integer between 1 and 16383", "Sorry")
            temp.Destroy()
            return
        t2 = '%X' % a
        if len(t2) == 1:
            t2 = '000' + t2
        if len(t2) == 2:
            t2 = '00' + t2
        if len(t2) == 3:
            t2 = '0' + t2
        WriteReg2(9516, '0011', t2[-2] + t2[-1])
        WriteReg2(9516, '0012', t2[-4] + t2[-3])

        PP = MainFrameLink.d9516.comboBox_P.GetSelection()
        if PP == 0:
            P = 1
        elif PP == 1:
            P = 2
        elif PP == 2:
            P = 2
        elif PP == 3:
            P = 3
        elif PP == 4:
            P = 4
        elif PP == 5:
            P = 8
        elif PP == 6:
            P = 16
        elif PP == 7:
            P = 32
        R = int(MainFrameLink.d9516.textCtrl_R_dil.GetValue())
        A = int(MainFrameLink.d9516.textCtrl_A.GetValue())
        B = int(MainFrameLink.d9516.textCtrl_B.GetValue())
        result = (10.00 / R) * (P * B + A)
        if result - int(result) != 0:
            # print result-int(result)
            float = (result - int(result)) * 100
            if float - int(float) < 0.5:
                result = int(result) + int(float) / 100.0
            elif float - int(float) >= 0.5:
                result = int(result) + (int(float) + 1) / 100.0
        MainFrameLink.d9516.formula.SetLabel(str(result) + 'MHz')

    def OnChangeTextCtrl_Enter(self, evt):
        textctrl = evt.GetEventObject()
        if textctrl == MainFrameLink.entertext:
            a = textctrl.GetValue()

            if a[:2] == 'D0':
                WriteReg(91391, a[3:7], a[8:10])
                OnPanelChange_91391(a[3:7], a[8:10])
            if a[:2] == 'D1':
                WriteReg(9516, a[3:7], a[8:10])
                OnPanelChange_9516(a[3:7], a[8:10])
            if a[:2] == 'D2':
                WriteReg(91392, a[3:7], a[8:10])
                OnPanelChange_91392(a[3:7], a[8:10])
            if a[:2] == 'D3':
                WriteReg(5732, a[3:7], a[8:10])
                # OnPanelChange_91391(a[3:7],a[8:10])                

    def OnChangeTextCtrl_Value_Voltage(self, evt):
        textctrl_Div1 = evt.GetEventObject()
        a = textctrl_Div1.GetValue()

        # print 'num=',a
        for i in a:
            if i not in num1:
                textctrl_Div1.SetValue('')
                temp = wx.MessageBox("Please input Arabic numerals", "Sorry")
                # temp.Destroy()
                return

        a = string.atof(a)
        if a < -0.5 or a > 0.5:
            textctrl_Div1.SetValue('')
            temp = wx.MessageBox("Please input between -0.5 and 0.5", "Sorry")
            # temp.Destroy()
            return
        # print int(a/4.096*8192)
        #### left ####
        if textctrl_Div1 == MainFrameLink.d5732.m_textCtrl8:
            a = a - 0.22054 * a + 0.00414
            a = a + 0.04937 * a - 0.000000009
        #### right ####
        elif textctrl_Div1 == MainFrameLink.d5732.m_textCtrl10:
            a = a - 0.22133 * a + 0.00502
            a = a + 0.0497 * a - 0.00109

        a = int(a / 4.096 * 8192)
        # print a
        temp = bin(int(a))
        # print 'after multi bin=',temp[2:]
        if a > 0:
            # print '0'
            temp = temp[2:] + '00'
            while ((16 - len(temp)) is not 0):
                temp = '0' + temp
            # print len(temp)
            # print 'bin=', temp[0:14]
            temp = bin2hex(temp)
            # print temp,temp
            if len(temp) == 1:
                # print '0'
                temp = '000' + temp
            if len(temp) == 2:
                temp = '00' + temp
            if len(temp) == 3:
                temp = '0' + temp
                # print 'final=',temp
        elif a == 0:

            temp = '0000'
        elif a < 0:
            temp = temp[3:]
            while len(temp) != 13:
                temp = '0' + temp
            temp = '1' + temp
            # print 'orign bin=',temp
            for k in range(1, len(temp)):
                if temp[k] == '0':
                    temp = temp[:k] + '1' + temp[k + 1:]
                elif temp[k] == '1':
                    temp = temp[:k] + '0' + temp[k + 1:]
            # print 'reverse=',temp
            k = len(temp) - 1
            while (temp[k] == '1' and k > 0):
                temp = temp[:k] + '0' + temp[k + 1:]
                k = k - 1
            temp = temp[:k] + '1' + temp[k + 1:]
            temp = temp + '00'

            # print 'bin=', temp[0:14]
            temp = bin2hex(temp)
            if len(temp) == 1:
                temp = '000' + temp
            if len(temp) == 2:
                temp = '00' + temp
            if len(temp) == 3:
                temp = '0' + temp

        if textctrl_Div1 == MainFrameLink.d5732.m_textCtrl8:
            WriteReg(5732, '00' + temp[0] + temp[1], temp[2] + temp[3])
            print '00' + temp[0] + temp[1], temp[2] + temp[3]
        if textctrl_Div1 == MainFrameLink.d5732.m_textCtrl10:
            WriteReg(5732, '02' + temp[0] + temp[1], temp[2] + temp[3])

    def Reset_Click(self, evt):
        InitialParameter_5732()

    def OnUpdate(self, evt):
        framehand = evt.GetEventObject()
        if not self.Theard_Flag:
            thd = threading.Thread(target=self.Start_Theard, args=(framehand,))
            thd.start()

    def Start_Theard(self, framehand):
        self.Theard_Flag = True
        # ######### 9516 ##########
        usb.write('CONF:VOLT:DC D1,H\n')
        raw = usb.read('READ:REGI 0x00,0x1F\n')
        xx = ord(raw[0])
        temp = int(xx) % 2
        print 'Lock:', temp != 0

        framehand.d9516.statusbutton.SetValue(True) if temp == 0 else framehand.d9516.statusbutton.SetValue(False)

        # 9516
        updatelist_9516 = ['0003', '001F']
        usb.write('CONF:VOLT:DC D1,H\n')
        raw = usb.read('READ:REGI 0x00,0x03\n')
        substance = dec2hex(ord(raw[0]))
        k = add_9516.index(3)
        compare = dec2hex(reg_9516[k].content)
        if compare != substance:
            print '0003 9516 change'
        while len(substance) != 2:
            substance = '0' + substance
        WriteReg(9516, '0003', str(substance))

        usb.write('CONF:VOLT:DC D1,H\n')
        raw = usb.read('READ:REGI 0x00,0x1F\n')
        substance = dec2hex(ord(raw[0]))
        k = add_9516.index(31)
        compare = dec2hex(reg_9516[k].content)
        if compare != substance:
            print '001F 9516 change'
        while len(substance) != 2:
            substance = '0' + substance
        WriteReg(9516, '001F', str(substance))

        self.Theard_Flag = False

    def Update9139(self, framehand):
        ############# 91391 7 @ 8 @ 16  #########
        # usb.write('CONF:VOLT:DC D0,H\n')
        # usb.write('CONF:REGI 0x00,0x0C,0x03\n')

        usb.write('CONF:VOLT:DC D0,H\n')
        raw = usb.read('READ:REGI 0x00,0x0E\n')
        tem = ord(raw[0])
        tem = str(tem)
        while 8 - len(tem) != 0:
            tem = '0' + tem
        if tem[0] == '1':
            framehand.d9139.channel1.lock_Button.SetValue(False)
            pass
        if tem[0] == '0':
            # print 'enter'
            framehand.d9139.channel1.lock_Button.SetValue(True)
            # print framehand.d9139.channel1.lock_Button.GetValue()
            pass
        if tem[1] == '0':
            framehand.d9139.channel1.warning_Button.SetValue(True)
        elif tem[1] == '1':
            framehand.d9139.channel1.warning_Button.SetValue(False)

        ############# 91392  7@8 @ 16  #########
        usb.write('CONF:VOLT:DC D2,H\n')
        raw = usb.read('READ:REGI 0x00,0x0E\n')
        tem = ord(raw[0])
        tem = str(tem)
        while (8 - len(tem) != 0):
            tem = '0' + tem
        # print 'temp[0]=',tem[0]
        if tem[0] == '0':
            framehand.d9139.channel2.lock_Button.SetValue(True)
        elif tem[0] == '1':
            framehand.d9139.channel2.lock_Button.SetValue(False)
        if tem[1] == '0':
            framehand.d9139.channel2.warning_Button.SetValue(True)
        elif tem[1] == '1':
            framehand.d9139.channel2.warning_Button.SetValue(False)
            # if tem[-3]==0:
            # framehand.d9139.channel2.DCI_Button.SetValue(True)
            # elif tem[-3]==1:
            # framehand.d9139.channel2.DCI_Button.SetValue(False)

        ############# 91391 10 #########
        usb.write('CONF:VOLT:DC D0,H\n')
        raw = usb.read('READ:REGI 0x00,0x25\n')
        tem = ord(raw[0])
        tem = str(tem)
        while (8 - len(tem) != 0):
            tem = '0' + tem
        if tem[-2] == '0':
            framehand.d9139.channel1.SPI_Button.SetValue(True)
        elif tem[-2] == '1':
            framehand.d9139.channel1.SPI_Button.SetValue(False)
            ############# 91392  10 #########
        usb.write('CONF:VOLT:DC D2,H\n')
        raw = usb.read('READ:REGI 0x00,0x25\n')
        tem = ord(raw[0])
        tem = str(tem)
        while (8 - len(tem) != 0):
            tem = '0' + tem
        if tem[-2] == '0':
            framehand.d9139.channel2.SPI_Button.SetValue(True)
        elif tem[-2] == '1':
            framehand.d9139.channel2.SPI_Button.SetValue(False)

        ############# 91391 11 @ 12  #########
        usb.write('CONF:VOLT:DC D0,H\n')
        raw = usb.read('READ:REGI 0x00,0x06\n')
        tem = ord(raw[0])
        tem = str(tem)
        while (8 - len(tem) != 0):
            tem = '0' + tem
        if tem[-2] == '0':
            framehand.d9139.channel1.Overflow_Button.SetValue(True)
        elif tem[-2] == '1':
            framehand.d9139.channel1.Overflow_Button.SetValue(False)
        if tem[-3] == '0':
            framehand.d9139.channel1.Underflow_Button.SetValue(True)
        elif tem[-3] == '1':
            framehand.d9139.channel1.Underflow_Button.SetValue(False)
        ############# 91392  11@12 #########
        usb.write('CONF:VOLT:DC D2,H\n')
        raw = usb.read('READ:REGI 0x00,0x06\n')
        tem = ord(raw[0])
        tem = str(tem)
        while (8 - len(tem) != 0):
            tem = '0' + tem
        if tem[-2] == '0':
            framehand.d9139.channel2.Overflow_Button.SetValue(True)
        elif tem[-2] == '1':
            framehand.d9139.channel2.Overflow_Button.SetValue(False)
        if tem[-3] == '0':
            framehand.d9139.channel2.Underflow_Button.SetValue(True)
        elif tem[-3] == '1':
            framehand.d9139.channel2.Underflow_Button.SetValue(False)

        # register
        updatelist_9139 = [5, 6, 14, 22, 23, 29, 30, 31, 36, 107, 108, 127]
        for i in updatelist_9139:
            add = dec2hex(i)
            while len(add) != 4:
                add = '0' + add
            usb.write('CONF:VOLT:DC D0,H\n')
            # usb.write('READ:REGI 0x' + add[0:2] + ',0x' + add[2:4] + '\n')
            raw = usb.read('READ:REGI 0x' + add[0:2] + ',0x' + add[2:4] + '\n')
            substance = dec2hex(ord(raw[0]))
            k = add_9139.index(i)
            compare = dec2hex(reg_91391[k].content)
            if compare != substance:
                print add + ' 91391 change'
            while len(substance) != 2:
                substance = '0' + substance
            WriteReg(91391, str(add), str(substance))

            usb.write('CONF:VOLT:DC D2,H\n')
            # usb.write('READ:REGI 0x' + add[0:2] + ',0x' + add[2:4] + '\n')
            raw = usb.read('READ:REGI 0x' + add[0:2] + ',0x' + add[2:4] + '\n')
            substance = dec2hex(ord(raw[0]))
            k = add_9139.index(i)
            compare = dec2hex(reg_91392[k].content)
            if compare != substance:
                print add + ' 91392 change'
            while len(substance) != 2:
                substance = '0' + substance
            WriteReg(91392, str(add), str(substance))

    def ON_OFF_Click(self, evt):
        toggleb = evt.GetEventObject()
        a = toggleb.GetLabel()
        if a == 'OFF':
            toggleb.SetLabel('ON')
            toggleb.SetValue(True)
            if toggleb == MainFrameLink.d9139.channel1.ON_OFF:
                WriteReg(91391, '0001', '40')
            if toggleb == MainFrameLink.d9139.channel2.ON_OFF:
                WriteReg(91392, '0001', '40')
        if a == 'ON':
            toggleb.SetLabel('OFF')
            toggleb.SetValue(False)
            if toggleb == MainFrameLink.d9139.channel1.ON_OFF:
                WriteReg(91391, '0001', 'C0')
            if toggleb == MainFrameLink.d9139.channel2.ON_OFF:
                WriteReg(91392, '0001', 'C0')

    def OnRadioBox_Click(self, evt):
        toggleb = evt.GetEventObject()
        a = toggleb.GetSelection()
        if toggleb == MainFrameLink.d9139.channel1.m_radioBox1:
            if a == 0:
                WriteReg(91391, '0028', '00')
            if a == 1:
                WriteReg(91391, '0028', '80')

        if toggleb == MainFrameLink.d9139.channel2.m_radioBox1:
            if a == 0:
                WriteReg(91392, '0028', '00')
            if a == 1:
                WriteReg(91392, '0028', '80')

    def OnToggleButton_Click(self, evt):
        toggleb = evt.GetEventObject()
        a = toggleb.GetLabel()
        if toggleb == MainFrameLink.d9139.channel1.Inv:
            if a == 'Enable':
                toggleb.SetLabel("Disable")
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91391[k].m_toggleBtn1.GetValue() == False:
                            pass
                        if reg_91391[k].m_toggleBtn1.GetValue() == True:
                            substance = '%X' % (reg_91391[k].content - 128)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91391, '0027', substance)

            if a == 'Disable':
                toggleb.SetLabel('Enable')

                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91391[k].m_toggleBtn1.GetValue() == True:
                            pass
                        if reg_91391[k].m_toggleBtn1.GetValue() == False:
                            # print 'should change'
                            substance = '%X' % (reg_91391[k].content + 128)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91391, '0027', substance)

        if toggleb == MainFrameLink.d9139.channel2.Inv:
            if a == 'Disable':
                toggleb.SetLabel("Enable")
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91392[k].m_toggleBtn1.GetValue() == True:
                            pass
                        if reg_91392[k].m_toggleBtn1.GetValue() == False:
                            substance = '%X' % (reg_91392[k].content + 128)
                            # print '000000=',reg_91391[k].content
                            # print '000000001=',int(substance,16)
                            WriteReg(91392, '0027', substance)
                            # reg_91391[k].ChansgeLabel(reg_91391[k].content+128,391)
            if a == 'Enable':
                toggleb.SetLabel('Disable')
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91392[k].m_toggleBtn1.GetValue() == False:
                            pass
                        if reg_91392[k].m_toggleBtn1.GetValue() == True:
                            substance = '%X' % (reg_91392[k].content - 128)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91392, '0027', substance)
        if toggleb == MainFrameLink.d9139.channel1.dll:
            # print 'enter'
            if a == 'Disable':
                # print 'Enabel'
                toggleb.SetLabel("Enable")
                WriteReg(91391, '000A', 'C0')
                WriteReg(91391, '000D', '86')
                MainFrameLink.d9139.channel1.choice1.Enable(False)
                MainFrameLink.d9139.channel1.choice2.Enable(True)
            if a == 'Enable':
                # print 'Disabel'
                toggleb.SetLabel('Disable')
                WriteReg(91391, '000A', '40')
                WriteReg(91391, '000D', '06')
                MainFrameLink.d9139.channel1.choice1.Enable(True)
                MainFrameLink.d9139.channel1.choice2.Enable(False)
        if toggleb == MainFrameLink.d9139.channel2.dll:
            if a == 'Enable':
                toggleb.SetLabel("Disable")
                WriteReg(91392, '000A', '40')
                WriteReg(91392, '000D', '06')
                MainFrameLink.d9139.channel2.choice1.Enable(True)
                MainFrameLink.d9139.channel2.choice2.Enable(False)
            if a == 'Disable':
                toggleb.SetLabel('Enable')
                WriteReg(91392, '000A', 'C0')
                WriteReg(91392, '000D', '86')
                MainFrameLink.d9139.channel2.choice1.Enable(False)
                MainFrameLink.d9139.channel2.choice2.Enable(True)
        if toggleb == MainFrameLink.d9139.channel1.STATUS_Button:
            # toggleb.SetLabel('Reset')
            WriteReg(91391, '0025', '00')
            WriteReg(91391, '0025', '01')
            WriteReg(91391, '0025', '00')
        if toggleb == MainFrameLink.d9139.channel2.STATUS_Button:
            # toggleb.SetLabel('Reset')
            WriteReg(91392, '0025', '00')
            WriteReg(91392, '0025', '01')
            WriteReg(91392, '0025', '00')
        if toggleb == MainFrameLink.d9139.channel1.gainbutton:
            if a == 'Enable':
                toggleb.SetLabel("Disable")
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91391[k].m_toggleBtn3.GetValue() == False:
                            pass
                        if reg_91391[k].m_toggleBtn3.GetValue() == True:
                            substance = '%X' % (reg_91391[k].content - 32)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91391, '0027', substance)
                MainFrameLink.d9139.channel1.textCtrl_1.Enable(False)
                MainFrameLink.d9139.channel1.textCtrl_2.Enable(False)
            if a == 'Disable':
                toggleb.SetLabel('Enable')
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91391[k].m_toggleBtn3.GetValue() == True:
                            pass
                        if reg_91391[k].m_toggleBtn3.GetValue() == False:
                            substance = '%X' % (reg_91391[k].content + 32)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91391, '0027', substance)
                MainFrameLink.d9139.channel1.textCtrl_2.Enable(True)
                MainFrameLink.d9139.channel1.textCtrl_1.Enable(True)
        if toggleb == MainFrameLink.d9139.channel2.gainbutton:
            if a == 'Enable':
                toggleb.SetLabel("Disable")
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91392[k].m_toggleBtn3.GetValue() == False:
                            pass
                        if reg_91392[k].m_toggleBtn3.GetValue() == True:
                            substance = '%X' % (reg_91392[k].content - 32)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91392, '0027', substance)
            MainFrameLink.d9139.channel2.textCtrl_1.Enable(False)
            MainFrameLink.d9139.channel2.textCtrl_2.Enable(False)
            if a == 'Disable':
                toggleb.SetLabel('Enable')
                for k in range(0, 58):
                    if add_9139[k] == 39:
                        if reg_91392[k].m_toggleBtn3.GetValue() == True:
                            pass
                        if reg_91392[k].m_toggleBtn3.GetValue() == False:
                            substance = '%X' % (reg_91392[k].content + 32)
                            if len(substance) == 1:
                                substance = '0' + substance
                            WriteReg(91392, '0027', substance)
                MainFrameLink.d9139.channel2.textCtrl_1.Enable(True)
                MainFrameLink.d9139.channel2.textCtrl_2.Enable(True)

    def ResetButtonClick(self, evt):
        toggleb = evt.GetEventObject()
        a = toggleb.GetValue()
        if a == True:
            if toggleb == MainFrameLink.d9139.channel1.Reset:
                WriteReg(91391, '0000', '20')
                InitialParameter_91391()
            if toggleb == MainFrameLink.d9139.channel2.Reset:
                WriteReg(91392, '0000', '20')
                InitialParameter_91392()
            toggleb.SetValue(False)

    def OnSelectComboValue(self, evt):
        combo = evt.GetEventObject()
        a = combo.GetSelection()
        if combo == MainFrameLink.d9139.channel1.choice1:
            if a == 0:
                WriteReg(91391, '000D', '06')
                WriteReg(91391, '005E', '00')
                WriteReg(91391, '005F', '60')
            if a == 1:
                WriteReg(91391, '000D', '06')
                WriteReg(91391, '005E', '80')
                WriteReg(91391, '005F', '67')
            if a == 2:
                WriteReg(91391, '000D', '06')
                WriteReg(91391, '005E', 'F0')
                WriteReg(91391, '005F', '67')
            if a == 3:
                WriteReg(91391, '000D', '06')
                WriteReg(91391, '005E', 'FE')
                WriteReg(91391, '005F', '67')
        if combo == MainFrameLink.d9139.channel2.choice1:
            if a == 0:
                WriteReg(91392, '000D', '06')
                WriteReg(91392, '005E', '00')
                WriteReg(91392, '005F', '60')
            if a == 1:
                WriteReg(91392, '000D', '06')
                WriteReg(91392, '005E', '80')
                WriteReg(91392, '005F', '67')
            if a == 2:
                WriteReg(91392, '000D', '06')
                WriteReg(91392, '005E', 'F0')
                WriteReg(91392, '005F', '67')
            if a == 3:
                WriteReg(91392, '000D', '06')
                WriteReg(91392, '005E', 'FE')
                WriteReg(91392, '005F', '67')
        if combo == MainFrameLink.d9139.channel1.choice2:
            if a == 0:
                WriteReg(91391, '000A', 'CA')
            if a == 1:
                WriteReg(91391, '000A', 'CB')
            if a == 2:
                WriteReg(91391, '000A', 'CC')
            if a == 3:
                WriteReg(91391, '000A', 'CD')
            if a == 4:
                WriteReg(91391, '000A', 'CE')
            if a == 5:
                WriteReg(91391, '000A', 'CF')
            if a == 6:
                WriteReg(91391, '000A', 'C0')
            if a == 7:
                WriteReg(91391, '000A', 'C1')
            if a == 8:
                WriteReg(91391, '000A', 'C2')
            if a == 9:
                WriteReg(91391, '000A', 'C3')
            if a == 10:
                WriteReg(91391, '000A', 'C4')
            if a == 11:
                WriteReg(91391, '000A', 'C5')
            if a == 12:
                WriteReg(91391, '000A', 'C6')

            phase = str(90 + (int(a) - 6) * 11.25)
            MainFrameLink.d9139.channel1.phaseoffset.SetValue(phase)

        if combo == MainFrameLink.d9139.channel2.choice2:
            if a == 0:
                WriteReg(91392, '000A', 'CA')
            if a == 1:
                WriteReg(91392, '000A', 'CB')
            if a == 2:
                WriteReg(91392, '000A', 'CC')
            if a == 3:
                WriteReg(91392, '000A', 'CD')
            if a == 4:
                WriteReg(91392, '000A', 'CE')
            if a == 5:
                WriteReg(91392, '000A', 'CF')
            if a == 6:
                WriteReg(91392, '000A', 'C0')
            if a == 7:
                WriteReg(91392, '000A', 'C1')
            if a == 8:
                WriteReg(91392, '000A', 'C2')
            if a == 9:
                WriteReg(91392, '000A', 'C3')
            if a == 10:
                WriteReg(91392, '000A', 'C4')
            if a == 11:
                WriteReg(91392, '000A', 'C5')
            if a == 12:
                WriteReg(91392, '000A', 'C6')
            phase = str(90 + (int(a) - 6) * 11.25)
            MainFrameLink.d9139.channel2.phaseoffset.SetValue(phase)

    def OnChangeTextCtrl_Digital(self, evt):
        combo = evt.GetEventObject()
        s = combo.GetValue()
        # print s
        for i in s:
            if i not in num1:
                combo.SetValue('')
                temp = wx.MessageBox("Please input Arabic numerals", "Sorry")
                # temp.Destroy()
                return
        if combo == MainFrameLink.d9139.channel1.textCtrl_1:
            a = string.atof(s)
            if a <= 0 or a > 1:
                combo.SetValue('')
                temp = wx.MessageBox("Please input between (0,1]", "Sorry")
                # temp.Destroy()
                return
            s = str(a)
            # print s
            temp = str(binary_float(s, 5))
            # print temp
            temp = '00' + temp[0] + temp[2] + temp[3] + temp[4] + temp[5]
            temp = '%X' % int(temp)
            WriteReg(91391, '003F', '0' + temp)
        if combo == MainFrameLink.d9139.channel2.textCtrl_1:
            a = string.atof(s)
            if a < 0 or a > 65535:
                combo.SetValue('')
                temp = wx.MessageBox("Please input between [0,65535]", "Sorry")
                # temp.Destroy()
                return
            s = str(a)
            temp = str(binary_float(s, 5))
            temp = '00' + temp[0] + temp[2] + temp[3] + temp[4] + temp[5]
            temp = '%X' % int(temp)
            WriteReg(91392, '003F', '0' + temp)
        if combo == MainFrameLink.d9139.channel1.textCtrl_2:
            value = '%X' % int(s)
            # value=value[2:]
            if len(value) == 1:
                value = '0' + value
            WriteReg(91391, '003B', value[-2:])
            WriteReg(91391, '003C', value[0] + value[1])
        if combo == MainFrameLink.d9139.channel2.textCtrl_2:
            # value=bin(int(s))
            value = '%X' % int(s)
            # value=value[2:]
            if len(value) == 1:
                value = '0' + value
            WriteReg(91392, '003B', value[-2:])
            WriteReg(91392, '003C', value[0] + value[1])


class MyPanel0(wx.Panel):
    bitmap1 = None
    image1 = None

    def __init__(self, parent, size=wx.Size(800, 500)):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, size, wx.NO_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        if MyPanel0.bitmap1 is None:
            MyPanel0.image1 = wx.Image(ImagePath + "show2.jpg", wx.BITMAP_TYPE_ANY)
            MyPanel0.image1.Rescale(size[0], size[1] * 0.85, quality=wx.IMAGE_QUALITY_HIGH)
            MyPanel0.bitmap1 = wx.BitmapFromImage(self.image1)
        # self.SetBackgroundColour((255,0,0))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        pos = (100, 135)
        self.vco = wx.StaticText(self, wx.ID_ANY, u"Vco", pos, wx.Size(20, 20), 0)
        self.vco.Wrap(-1)

        pos = (250, 110)
        self.p = wx.StaticText(self, wx.ID_ANY, u"P:", pos, wx.DefaultSize, 0)
        self.p.Wrap(-1)

        pos = (243, 135)
        self.b = wx.StaticText(self, wx.ID_ANY, u" B:", pos, wx.Size(30, 20), 0)
        self.b.Wrap(-1)

        pos = (250, 160)
        self.a = wx.StaticText(self, wx.ID_ANY, u"A:", pos, wx.DefaultSize, 0)
        self.a.Wrap(-1)

        ref_clk_choice = [u"Ext_10MHz", u"Int_10MHz"]
        self.comboBox_ref_clk = wx.ComboBox(self, wx.ID_ANY, u"332", (100, 240), wx.Size(100, 50), ref_clk_choice,
                                            wx.CB_READONLY)
        self.comboBox_ref_clk.SetSelection(0)
        self.comboBox_ref_clk.Bind(wx.EVT_COMBOBOX, Event().OnSelectComboValue_Ref)
        self.ref_clk = wx.StaticText(self, wx.ID_ANY, u"Ref_Clk", (100, 220), wx.DefaultSize, 0)

        pos = (450, 204)
        self.pd = wx.StaticText(self, wx.ID_ANY, u"PD", pos, wx.DefaultSize, 0)
        self.pd.Wrap(-1)

        pos = (210, 373)
        self.lowpassfiller = wx.StaticText(self, wx.ID_ANY, u"Low Pass Filler", pos, wx.DefaultSize, 0)
        self.lowpassfiller.Wrap(-1)

        pos = (370, 15)
        self.spdtlabel = wx.StaticText(self, wx.ID_ANY, u'SPDT', pos, wx.DefaultSize, 0)
        self.spdtlabel.Wrap(-1)

        # choice1Choices =("2", u"4","8","16","32" )
        pos = (278, 110)
        comboBox1Choices = ["1 FD(VCO Max 300MHz)", "2 FD(VCO Max 600MHz)", "2 DM(VCO Max 200MHz)",
                            "3 FD(VCO Max 900MHz)", "4 DM(VCO Max 1000MHz)", "8 DM(VCO Max 2400MHz)",
                            "16 DM(VCO Max 3000MHz)", "32 DM(VCO Max 3000MHz)"]
        self.comboBox_P = wx.ComboBox(self, wx.ID_ANY, u"1", pos, wx.Size(180, 26), comboBox1Choices, 0)

        self.comboBox_P.Bind(wx.EVT_COMBOBOX, Event().OnSelectComboValue_p)
        ###########   later add  ############
        ###########   later add  ############
        ###########   later add  ############

        self.comboBox_VCO_DIVIDER = wx.ComboBox(self, wx.ID_ANY, u"1", (160, 115), wx.Size(50, 26),
                                                ["2", "3", "4", "5", "6"], 0)

        self.comboBox_VCO_DIVIDER.Bind(wx.EVT_COMBOBOX, Event().OnSelectComboValue_VCO_DIVIDER)
        self.statictext_VCO_DIVIDER = wx.StaticText(self, wx.ID_ANY, u"VCO_DIVIDER", (140, 100), wx.DefaultSize, 0)

        self.statusbutton = Status_Button(self, pos=(120, 300), size=(50, 50))

        self.resetbutton = Reset_Button(self, pos=(15, 80), size=(50, 34))
        self.resetbutton.Bind(wx.EVT_TOGGLEBUTTON, Event().OnReset_ButtonClick)

        ######### center PBA TextCtrl##########
        ######### center PBA TextCtrl##########
        # self.textCtrl_B = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, (278,135), wx.Size(80,26), wx.TE_PROCESS_ENTER )
        self.textCtrl_B = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, (278, 135), wx.Size(80, 26), wx.TE_PROCESS_ENTER,
                                      0, 8192, 25)
        # self.textCtrl_B.SetValue(temp_value)
        self.textCtrl_B.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_B)
        self.textCtrl_B.Bind(wx.EVT_SPINCTRL, Event().OnChangeTextCtrl_Value_B)
        self.textCtrl_B.SetToolTipString("[0,8191]")

        self.textCtrl_A = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, (278, 160), wx.Size(80, 26), wx.TE_PROCESS_ENTER,
                                      0, 64, 0)
        self.textCtrl_A.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_A)
        self.textCtrl_A.Bind(wx.EVT_SPINCTRL, Event().OnChangeTextCtrl_Value_A)
        self.textCtrl_A.SetToolTipString("[0,63]")
        ###########  formula #########
        self.formula_1 = wx.StaticText(self, wx.ID_ANY, u"=", (277, 195), wx.DefaultSize, 0)
        self.formula = wx.StaticText(self, wx.ID_ANY, u"0MHz", (290, 195), wx.DefaultSize, 0)

        ############ R_dil #############
        ############ R_dil #############
        self.R_dil = wx.StaticText(self, wx.ID_ANY, u"R", (235, 220), wx.DefaultSize, 0)
        self.textCtrl_R_dil = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, (230, 245), wx.Size(65, 20),
                                          wx.TE_PROCESS_ENTER, 0, 8191, 1)
        # self.textCtrl_R_dil = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, (230,245), wx.Size(45,20), wx.TE_PROCESS_ENTER )
        self.textCtrl_R_dil.Bind(wx.EVT_SPINCTRL, Event().OnChangeTextCtrl_Value_R_dil)
        self.textCtrl_R_dil.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_R_dil)
        self.textCtrl_R_dil.SetToolTipString("[1,16383]")
        self.SetSizer(sizer)
        self.SetInitialSize()

        statictext_ext = wx.StaticText(self, wx.ID_ANY, u" Ext_Sample_Clock", (80, 40), wx.Size(60, 20), 0)
        statictext_ext.Wrap(-1)
        self.spdtbutton = SPDT_Button(self, pos=(370, 30), size=(140, 80))
        self.spdtbutton.Bind(wx.EVT_TOGGLEBUTTON, Event().OnSPDTButtonClick)

        ######### right TextCtrl#########
        ######### right TextCtrl#########
        statictext_1 = wx.StaticText(self, wx.ID_ANY, u" Div 1", (560, 47), wx.Size(60, 20), 0)
        statictext_1.Wrap(-1)

        statictext_2 = wx.StaticText(self, wx.ID_ANY, u" Div 2", (560, 107), wx.Size(60, 20), 0)
        statictext_2.Wrap(-1)

        statictext_3 = wx.StaticText(self, wx.ID_ANY, u" Div 3", (560, 167), wx.Size(60, 20), 0)
        statictext_3.Wrap(-1)

        statictext_4 = wx.StaticText(self, wx.ID_ANY, u" Div 4", (560, 227), wx.Size(60, 20), 0)
        statictext_4.Wrap(-1)

        statictext_5 = wx.StaticText(self, wx.ID_ANY, u" Div 5", (560, 287), wx.Size(60, 20), 0)
        # statictext_5.Wrap( -1 )

        self.textCtrl_1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 67), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_1.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Div1)
        self.textCtrl_1.SetToolTipString("[1,32]")
        # textCtrl_1.Bind(wx.EVT_TEXT_ENTER,Event().OnChaaaaaangeTextCtrl_Value_Div1)

        self.textCtrl_2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 127), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_2.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Div2)
        self.textCtrl_2.SetToolTipString("[1,32]")

        self.textCtrl_3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 187), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_3.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Div3)
        self.textCtrl_3.SetToolTipString("[1,32]")

        self.textCtrl_4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 247), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_4.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Div4)
        self.textCtrl_4.SetToolTipString("[1,32]")

        self.textCtrl_5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 307), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_5.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Div5)
        self.textCtrl_5.SetToolTipString("[1,32]")

        ########## right togglebutton##########
        ########## right togglebutton##########
        ########## right togglebutton##########
        ########## right togglebutton##########

        self.out_button0 = OUT_Button(self, 'OUT 0', pos=(665, 40), size=wx.Size(50, 30))
        self.out_button0.SetLabel('ON')
        self.out_button0.SetValue(True)
        self.out_button0.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut0ButtonClick)

        self.out_button1 = OUT_Button(self, 'OUT 1', pos=(665, 70), size=wx.Size(50, 30))
        self.out_button1.SetLabel('ON')
        self.out_button1.SetValue(True)
        self.out_button1.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut1ButtonClick)

        self.out_button2 = OUT_Button(self, 'OUT 2', pos=(665, 105), size=wx.Size(50, 30))
        self.out_button2.SetLabel('ON')
        self.out_button2.SetValue(True)
        self.out_button2.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut2ButtonClick)

        self.out_button3 = OUT_Button(self, 'OUT 3', pos=(665, 135), size=wx.Size(50, 30))
        self.out_button3.SetLabel('ON')
        self.out_button3.SetValue(True)
        self.out_button3.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut3ButtonClick)

        self.out_button4 = OUT_Button(self, 'OUT 4', pos=(665, 170), size=wx.Size(50, 30))
        self.out_button4.SetLabel('ON')
        self.out_button4.SetValue(True)
        self.out_button4.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut4ButtonClick)

        self.out_button5 = OUT_Button(self, 'OUT 5', pos=(665, 200), size=wx.Size(50, 30))
        self.out_button5.SetLabel('ON')
        self.out_button5.SetValue(True)
        self.out_button5.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut5ButtonClick)

        self.out_button6 = OUT_Button(self, 'OUT 6', pos=(665, 232), size=wx.Size(50, 30))
        self.out_button6.SetLabel('ON')
        self.out_button6.SetValue(True)
        self.out_button6.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut6ButtonClick)

        self.out_button7 = OUT_Button(self, 'OUT 7', pos=(665, 262), size=wx.Size(50, 30))
        self.out_button7.SetLabel('ON')
        self.out_button7.SetValue(True)
        self.out_button7.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut7ButtonClick)

        self.out_button8 = OUT_Button(self, 'OUT 8', pos=(665, 295), size=wx.Size(50, 30))
        self.out_button8.SetLabel('ON')
        self.out_button8.SetValue(True)
        self.out_button8.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut8ButtonClick)

        self.out_button9 = OUT_Button(self, 'OUT 9', pos=(665, 325), size=wx.Size(50, 30))
        self.out_button9.SetLabel('ON')
        self.out_button9.SetValue(True)
        self.out_button9.Bind(wx.EVT_TOGGLEBUTTON, Event().OnOut9ButtonClick)
        # self.out_button9.Bind(wx.EVT_TOGGLEBUTTON,Event().OnToggleButton)

        ########## right StaticText###############
        ########## right StaticText###############
        ########## right StaticText###############
        ########## right StaticText###############

        self.REF1 = wx.StaticText(self, wx.ID_ANY, u"REF 1", (720, 40), wx.DefaultSize, 0)
        self.REF2 = wx.StaticText(self, wx.ID_ANY, u"REF 2", (720, 70), wx.DefaultSize, 0)

        self.DAC1 = wx.StaticText(self, wx.ID_ANY, u"DAC 1", (720, 170), wx.DefaultSize, 0)
        self.DAC2 = wx.StaticText(self, wx.ID_ANY, u"DAC 1", (720, 200), wx.DefaultSize, 0)

        self.DCO = wx.StaticText(self, wx.ID_ANY, u"DCO", (720, 232), wx.DefaultSize, 0)
        self.DCO = wx.StaticText(self, wx.ID_ANY, u"DCO", (720, 262), wx.DefaultSize, 0)

        self.Frame1 = wx.StaticText(self, wx.ID_ANY, u"Frame 1", (720, 292), wx.DefaultSize, 0)
        self.Frame2 = wx.StaticText(self, wx.ID_ANY, u"Frame 2", (720, 325), wx.DefaultSize, 0)

        # global MyPanel0Link
        # MyPanel0Link=MyPanel0(self)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.SetPen(wx.Pen('BLACK'))
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        # dc.SetBackground(wx.Brush(HighlightText))
        dc.Clear()
        # print 'draw!!!!!'
        dc.DrawBitmap(MyPanel0.bitmap1, 0, 0)
        # print 'get!!!!!'
        dc.EndDrawing()


class MyPanel1(wx.Panel):
    image1 = None
    bitmap1 = None

    def __init__(self, parent, Nostr):
        size = (390, 700)
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, size, wx.TAB_TRAVERSAL, Nostr)

        # Total_sizer = wx.wx.BoxSizer( wx.VERTICAL )
        ############# No1 ###############
        ############# No1 ###############
        box1_title = wx.StaticBox(self, -1, " Channel                 " + Nostr)
        Total_sizer = wx.StaticBoxSizer(box1_title, wx.VERTICAL)
        ############### ON/OFF #############
        self.ON_OFF_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ON_OFF1_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.output = wx.StaticText(self, wx.ID_ANY, u'        Output', wx.DefaultPosition, wx.DefaultSize, 0)
        self.ON_OFF = wx.ToggleButton(self, -1, 'ON')
        self.ON_OFF.SetValue(True)
        self.ON_OFF.Bind(wx.EVT_TOGGLEBUTTON, Event().ON_OFF_Click)

        self.Reset = Reset_Button(self, wx.DefaultPosition, size=(30, 30))
        self.Reset.Bind(wx.EVT_TOGGLEBUTTON, Event().ResetButtonClick)
        # self.Resetspace=wx.StaticText( self, wx.ID_ANY, u'       ', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ON_OFF1_Sizer.Add(self.output, 1, wx.ALL, )
        self.ON_OFF1_Sizer.Add(self.ON_OFF, 1, wx.ALL, 0)

        self.ON_OFF_Sizer.Add(self.ON_OFF1_Sizer, 2, wx.FIXED_MINSIZE | wx.RIGHT, 5)
        self.ON_OFF_Sizer.Add(self.Reset, 1, wx.FIXED_MINSIZE | wx.RIGHT, 5)

        # No1.Add( self.ON_OFF_Sizer, 0, wx.ALL, 0)

        ################# No2 Basic Digital Functions ############
        ################# No2 Basic Digital Functions ############
        box2_title = wx.StaticBox(self, -1, "Basic Digital Functions", wx.DefaultPosition, size=(300, 200))
        Basic_Sizer = wx.StaticBoxSizer(box2_title, wx.VERTICAL)
        In_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        In_right_Sizer = wx.BoxSizer(wx.VERTICAL)

        m_radioBox1Choices = [u"2x", u"1x"]
        self.m_radioBox1 = wx.RadioBox(self, wx.ID_ANY, u"Interpolation", wx.DefaultPosition, wx.DefaultSize,
                                       m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS)

        self.m_radioBox1.Bind(wx.EVT_RADIOBOX, Event().OnRadioBox_Click)
        self.m_radioBox1.SetSelection(1)

        self.static_Inv = wx.StaticText(self, wx.ID_ANY, "Invsinc Enable", wx.DefaultPosition, wx.DefaultSize, 0)

        self.Inv = wx.ToggleButton(self, -1, 'Disable')
        self.Inv.Bind(wx.EVT_TOGGLEBUTTON, Event().OnToggleButton_Click)
        # self.Inv = wx.RadioButton(self,-1,'Disable')
        # self.Inv.Bind(wx.EVT_RADIOBUTTON,Event().OnToggleButton_Click)

        In_right_Sizer.Add(self.static_Inv, 0, wx.ALL, 0)
        In_right_Sizer.Add(self.Inv, 0, wx.ALL, 0)

        In_Sizer.Add(self.m_radioBox1, 0, wx.FIXED_MINSIZE | wx.RIGHT, 40)
        In_Sizer.Add(In_right_Sizer, 0, wx.FIXED_MINSIZE | wx.RIGHT, 40)

        Basic_Sizer.Add(In_Sizer, 0, wx.ALL, 0)

        ##############  No3  INTER  #######################
        ##############  No3  INTER  #######################
        DLL_PhaseSizer = wx.BoxSizer(wx.HORIZONTAL)
        DLL_EnableSizer = wx.BoxSizer(wx.HORIZONTAL)

        Lamp_t = wx.BoxSizer(wx.HORIZONTAL)
        Lamp1 = wx.BoxSizer(wx.HORIZONTAL)
        Lamp2 = wx.BoxSizer(wx.HORIZONTAL)
        box3_title = wx.StaticBox(self, -1, "Interface Control", wx.DefaultPosition, size=(300, 400))
        box3 = wx.StaticBoxSizer(box3_title, wx.VERTICAL)

        self.DelayLine = wx.StaticText(self, wx.ID_ANY, u"Delay Line (Must set when DCI<250MHz)", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.DelayLine.Wrap(-1)

        choice1Choices = ['0', '1', '2', '3']
        self.choice1 = wx.ComboBox(self, wx.ID_ANY, u"choice1", wx.DefaultPosition, wx.Size(55, 20), choice1Choices, 0)
        self.choice1.Bind(wx.EVT_COMBOBOX, Event().OnSelectComboValue)

        self.static_dll_enable = wx.StaticText(self, wx.ID_ANY, "DLL Enable", wx.DefaultPosition, wx.DefaultSize, 0)
        self.dll = wx.ToggleButton(self, -1, 'Disable')
        self.dll.Bind(wx.EVT_TOGGLEBUTTON, Event().OnToggleButton_Click)
        self.DLL_Phase = wx.StaticText(self, wx.ID_ANY, u"DLL Phase Setting", wx.DefaultPosition, wx.DefaultSize, 0)
        self.DLL_Phase.Wrap(-1)

        choice2Choices = ['-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6']
        self.choice2 = wx.ComboBox(self, wx.ID_ANY, u"choice1", wx.DefaultPosition, wx.Size(55, 20), choice2Choices, 0)
        self.choice2.Bind(wx.EVT_COMBOBOX, Event().OnSelectComboValue)

        self.phaseoffset = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(40, 20),
                                       style=wx.TE_READONLY)

        self.phaseoffsetsta = wx.StaticText(self, wx.ID_ANY, u"Phase Offset", wx.DefaultPosition, wx.DefaultSize, 0)

        self.dll_lock = wx.StaticText(self, wx.ID_ANY, u"DLL Lock", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lock_Button = Status_Button2(self)
        # self.lock_Button.SetValue(True)


        self.dll_warning = wx.StaticText(self, wx.ID_ANY, u"DLL Warning", wx.DefaultPosition, wx.DefaultSize, 0)
        self.warning_Button = Status_Button2(self)

        Lamp1.Add(self.dll_lock, 0, wx.RIGHT, 15)
        Lamp1.Add(self.lock_Button, 0, wx.RIGHT, 15)

        Lamp2.Add(self.dll_warning, 0, wx.RIGHT, 15)
        Lamp2.Add(self.warning_Button, 0, wx.RIGHT, 15)

        Lamp_t.Add(Lamp1, 0, wx.RIGHT, 15)
        Lamp_t.Add(Lamp2, 0, wx.RIGHT, 15)

        DLL_EnableSizer.Add(self.static_dll_enable, 0, wx.RIGHT, 35)
        DLL_EnableSizer.Add(self.dll, 0, wx.RIGHT, 35)

        DLL_PhaseSizer.Add(self.DLL_Phase, 0, wx.RIGHT, 5)
        DLL_PhaseSizer.Add(self.choice2, 0, wx.RIGHT, 5)
        DLL_PhaseSizer.Add(self.phaseoffsetsta, 0, wx.RIGHT, 5)
        DLL_PhaseSizer.Add(self.phaseoffset, 0, wx.RIGHT, 5)

        box3.Add(self.DelayLine, 0, wx.ALL, 0)
        box3.Add(self.choice1, 0, wx.ALL, 0)
        box3.Add(DLL_EnableSizer, 0, wx.ALL, 0)
        box3.Add(DLL_PhaseSizer, 0, wx.ALL, 0)
        box3.Add(Lamp_t, 0, wx.ALL, 0)

        ############ No 4 FIFO ##############
        ############ No 4 FIFO ##############
        box4_title = wx.StaticBox(self, -1, "FIFO Control", wx.DefaultPosition, size=(300, 300))
        FIFO_Sizer_Total = wx.StaticBoxSizer(box4_title, wx.VERTICAL)
        STATUS_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        SPI_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Flow_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Flow_Sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        Flow_Sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.STATUS_TextCtrl = wx.StaticText(self, wx.ID_ANY, u"FIFO SPI Reset Request", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.STATUS_TextCtrl.Wrap(-1)
        self.STATUS_Button = wx.Button(self, -1, 'Reset')
        self.STATUS_Button.Bind(wx.EVT_BUTTON, Event().OnToggleButton_Click)

        self.SPI_TextCtrl = wx.StaticText(self, wx.ID_ANY, u"FIFO SPI Reset Ack", wx.DefaultPosition, wx.DefaultSize, 0)
        self.SPI_TextCtrl.Wrap(-1)
        self.SPI_Button = Status_Button2(self)

        overflow = wx.StaticText(self, wx.ID_ANY, u"FIFO Over Flow", wx.DefaultPosition, wx.DefaultSize, 0)
        underflow = wx.StaticText(self, wx.ID_ANY, u"FIFO Under Flow", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Overflow_Button = Status_Button2(self)

        self.Underflow_Button = Status_Button2(self)

        STATUS_Sizer.Add(self.STATUS_TextCtrl, 0, wx.FIXED_MINSIZE | wx.RIGHT, 22)
        STATUS_Sizer.Add(self.STATUS_Button, 0, wx.FIXED_MINSIZE | wx.RIGHT, 22)

        SPI_Sizer.Add(self.SPI_TextCtrl, 0, wx.FIXED_MINSIZE | wx.RIGHT, 22)
        SPI_Sizer.Add(self.SPI_Button, 0, wx.FIXED_MINSIZE | wx.RIGHT, 22)

        Flow_Sizer1.Add(overflow, 0, wx.RIGHT, 15)
        Flow_Sizer1.Add(self.Overflow_Button, 0, wx.RIGHT, 15)
        Flow_Sizer2.Add(underflow, 0, wx.RIGHT, 15)
        Flow_Sizer2.Add(self.Underflow_Button, 0, wx.RIGHT, 15)

        Flow_Sizer.Add(Flow_Sizer1, 0, wx.RIGHT, 15)
        Flow_Sizer.Add(Flow_Sizer2, 0, wx.RIGHT, 15)

        FIFO_Sizer_Total.Add(STATUS_Sizer, 0, wx.ALL, 0)
        FIFO_Sizer_Total.Add(SPI_Sizer, 0, wx.ALL, 0)
        FIFO_Sizer_Total.Add(Flow_Sizer, 0, wx.ALL, 0)

        ########### No 5 ################
        ########### No 5 ################
        box5_title = wx.StaticBox(self, -1, "Digital Path Control", wx.DefaultPosition, size=(500, 200))
        Digital_Sizer = wx.StaticBoxSizer(box5_title, wx.VERTICAL)
        Gain_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Gain_left_Sizer = wx.BoxSizer(wx.VERTICAL)
        Gain_right_Sizer = wx.BoxSizer(wx.VERTICAL)
        Gain_ADJ_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Gain_DC_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ADJ_TextCtrl = wx.StaticText(self, wx.ID_ANY, u"   Gain ADJ ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.textCtrl_1_fanwei = wx.StaticText(self, wx.ID_ANY, u" (0,1]", wx.DefaultPosition, wx.DefaultSize, 0)
        self.DC_TextCtrl = wx.StaticText(self, wx.ID_ANY, u"Dc Offset ADJ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.textCtrl_2_fanwei = wx.StaticText(self, wx.ID_ANY, u"[0,65535]", wx.DefaultPosition, wx.DefaultSize, 0)

        self.gainbutton = wx.ToggleButton(self, -1, 'Disable')
        self.gainbutton.Bind(wx.EVT_TOGGLEBUTTON, Event().OnToggleButton_Click)

        self.gain_radio_text = wx.StaticText(self, wx.ID_ANY, u"Gain Dc offset ADJ Enable", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.textCtrl_1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 187), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_1.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Digital)
        self.textCtrl_2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, (560, 187), wx.Size(60, 20), wx.TE_PROCESS_ENTER)
        self.textCtrl_2.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Digital)

        Gain_ADJ_Sizer.Add(self.ADJ_TextCtrl, 0, wx.wx.FIXED_MINSIZE, 0)
        Gain_ADJ_Sizer.Add(self.textCtrl_1, 0, wx.wx.FIXED_MINSIZE, 0)
        Gain_ADJ_Sizer.Add(self.textCtrl_1_fanwei, 0, wx.wx.FIXED_MINSIZE, 0)

        Gain_DC_Sizer.Add(self.DC_TextCtrl, 0, wx.wx.FIXED_MINSIZE, 0)
        Gain_DC_Sizer.Add(self.textCtrl_2, 0, wx.wx.FIXED_MINSIZE, 0)
        Gain_DC_Sizer.Add(self.textCtrl_2_fanwei, 0, wx.FIXED_MINSIZE, 0)

        Gain_right_Sizer.Add(Gain_ADJ_Sizer, 0, wx.ALL, 2)
        Gain_right_Sizer.Add(Gain_DC_Sizer, 0, wx.ALL, 2)

        Gain_left_Sizer.Add(self.gain_radio_text, 0, wx.ALL, 0)
        Gain_left_Sizer.Add(self.gainbutton, 0, wx.ALL, 0)

        Gain_Sizer.Add(Gain_left_Sizer, 0, wx.ALL, 0)
        Gain_Sizer.Add(Gain_right_Sizer, 0, wx.ALL, 0)

        Digital_Sizer.Add(Gain_Sizer, 0, wx.ALL, 0)

        Total_sizer.Add(self.ON_OFF_Sizer, 1, wx.ALL, 3)
        Total_sizer.Add(Basic_Sizer, 1, wx.ALL, 3)
        Total_sizer.Add(box3, 3, wx.ALL, 3)
        # Total_sizer.Add(Inter_Total_sizer,0, wx.ALL, 5 )
        Total_sizer.Add(FIFO_Sizer_Total, 2, wx.ALL, 3)
        Total_sizer.Add(Digital_Sizer, 2, wx.ALL, 3)
        # if MyPanel1.bitmap1 is None:
        # MyPanel1.image1=wx.Image( "show1.png", wx.BITMAP_TYPE_ANY )
        # MyPanel1.image1.Rescale(size[0],size[1],quality=wx.IMAGE_QUALITY_HIGH )
        # MyPanel1.bitmap1=wx.BitmapFromImage(self.image1)

        # self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.SetSizer(Total_sizer)
        self.Layout()

        # Total_sizer.Fit( self )
        def OnPaint(self, evt):
            dc = wx.BufferedPaintDC(self)
            dc.SetPen(wx.Pen('BLACK'))
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            dc.DrawBitmap(MyPanel1.bitmap1, 0, 0)
            dc.EndDrawing()


class MyPanel1_1(wx.Panel):
    def __init__(self, parent, size=wx.Size(800, 500)):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, size, wx.NO_BORDER)

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.channel1 = MyPanel1(self, '1')
        self.channel2 = MyPanel1(self, '2')
        Sizer.Add(self.channel1, 0, wx.ALL, 0)
        Sizer.Add(self.channel2, 0, wx.ALL, 0)
        self.SetSizer(Sizer)
        self.Layout()


###########################################################################
## Class MyPanel2
###########################################################################

class MyPanel2(wx.Panel):
    def __init__(self, parent, size=wx.Size(840, 500)):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, size, wx.TAB_TRAVERSAL)

        fgSizer2 = wx.FlexGridSizer(0, 2, 5, 35)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.channel1 = wx.StaticText(self, wx.ID_ANY, u"channel1 offset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.channel1.Wrap(-1)
        fgSizer2.Add(self.channel1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.channel2 = wx.StaticText(self, wx.ID_ANY, u"channel2 offset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.channel2.Wrap(-1)
        fgSizer2.Add(self.channel2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.voltage1 = wx.StaticText(self, wx.ID_ANY, u"Voltage", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl10_fanwei = wx.StaticText(self, wx.ID_ANY, u"V (-0.5V,0.5V)", wx.DefaultPosition, wx.DefaultSize,
                                                 0)
        self.m_textCtrl10_fanwei1 = wx.StaticText(self, wx.ID_ANY, u"V (-0.5V,0.5V)", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.voltage1.Wrap(-1)
        bSizer3.Add(self.voltage1, 0, wx.ALL, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                       wx.TE_PROCESS_ENTER)
        self.m_textCtrl8.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Voltage)
        bSizer3.Add(self.m_textCtrl8, 0, wx.ALL, 5)

        bSizer3.Add(self.m_textCtrl10_fanwei1, 0, wx.ALL, 5)

        fgSizer2.Add(bSizer3, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.voltage2 = wx.StaticText(self, wx.ID_ANY, u"Voltage", wx.DefaultPosition, wx.DefaultSize, 0)
        self.voltage2.Wrap(-1)
        bSizer4.Add(self.voltage2, 0, wx.ALL, 5)

        self.m_textCtrl10 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                        wx.TE_PROCESS_ENTER)
        self.m_textCtrl10.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Value_Voltage)

        bSizer4.Add(self.m_textCtrl10, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        bSizer4.Add(self.m_textCtrl10_fanwei, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        self.resetbutton1 = Reset_Button(self, wx.DefaultPosition, size=(50, 34))
        self.resetbutton1.Bind(wx.EVT_TOGGLEBUTTON, Event().Reset_Click)

        fgSizer2.Add(bSizer4, 1, wx.EXPAND, 5)
        fgSizer2.Add(self.resetbutton1, 1, wx.EXPAND, 5)

        self.SetSizer(fgSizer2)
        self.Layout()


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='anolog', pos=wx.DefaultPosition, size=wx.Size(800, 640),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook6 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.d9516 = MyPanel0(self.m_notebook6)
        self.m_notebook6.AddPage(self.d9516, u"AD9516", True)
        self.d9139 = MyPanel1_1(self.m_notebook6)
        self.m_notebook6.AddPage(self.d9139, u"AD9139", False)
        self.d5732 = MyPanel2(self.m_notebook6)
        self.m_notebook6.AddPage(self.d5732, u"AD5732", False)

        self.register_2 = Register_Panel_9516(self.m_notebook6)
        self.m_notebook6.AddPage(self.register_2, u"Register_9516", False)
        self.register_1 = Register_Panel_9139(self.m_notebook6)
        self.m_notebook6.AddPage(self.register_1, u"Register_9139", False)

        bSizer2.Add(self.m_notebook6, 1, wx.EXPAND | wx.ALL, 5)
        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        # self.toolbar = wx.ToolBar(self, style= (wx.TB_HORIZONTAL| wx.NO_BORDER| wx.TB_FLAT))
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.toolbar.SetToolBitmapSize(wx.DefaultSize)

        self.tool1 = self.toolbar.AddLabelTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(ImagePath + "open_folder.png", wx.BITMAP_TYPE_ANY))
        # self.tool1.SetShortHelp('Save Current Experiment Data')
        # self.tool2 = self.toolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap("save.png", wx.BITMAP_TYPE_ANY ) )
        # self.tool2.SetShortHelp('Save Past Experiment Data')

        self.tool4 = self.toolbar.AddLabelTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(ImagePath + "0_9516.png", wx.BITMAP_TYPE_ANY))
        self.tool3 = self.toolbar.AddLabelTool(wx.NewId(), "tool",
                                               wx.Bitmap(ImagePath + "0_91391.png", wx.BITMAP_TYPE_ANY))
        self.tool3.SetShortHelp('Compare Data')
        self.tool5 = self.toolbar.AddLabelTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(ImagePath + "0_91392.png", wx.BITMAP_TYPE_ANY))
        self.tool6 = self.toolbar.AddLabelTool(wx.NewId(), "tool",
                                               wx.Bitmap(ImagePath + "0_5732.png", wx.BITMAP_TYPE_ANY))

        self.tool7 = self.toolbar.AddLabelTool(wx.NewId(), "tool",
                                               wx.Bitmap(ImagePath + "help_9516.png", wx.BITMAP_TYPE_ANY))
        self.tool8 = self.toolbar.AddLabelTool(wx.NewId(), "tool",
                                               wx.Bitmap(ImagePath + "help_9139.png", wx.BITMAP_TYPE_ANY))
        self.tool8 = self.toolbar.AddLabelTool(wx.NewId(), "tool",
                                               wx.Bitmap(ImagePath + "help_5732.png", wx.BITMAP_TYPE_ANY))

        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.entertext = wx.TextCtrl(self.toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PROCESS_ENTER)
        self.entertext.Bind(wx.EVT_TEXT_ENTER, Event().OnChangeTextCtrl_Enter)
        self.expla = wx.StaticText(self.toolbar, wx.ID_ANY, u" eg:D0,000C,FF", wx.DefaultPosition, wx.DefaultSize, 0)
        self.toolbar.AddControl(self.entertext)
        self.toolbar.AddControl(self.expla)

        self.toolbar.Realize()

        self.toolbar.Bind(wx.EVT_TOOL, Event().OnToolBarClick)

        self.UpdateTimer = wx.Timer()
        self.UpdateTimer.SetOwner(self, wx.ID_ANY)
        self.UpdateTimer.Start(1000)

        self.Bind(wx.EVT_TIMER, Event().OnUpdate, id=wx.ID_ANY)
        self.Bind(wx.EVT_CLOSE, self.Onclose)

    def Onclose(self, event):
        event.Skip()


if __name__ == '__main__':
    a = wx.App()
    b = MyFrame1(None)
    MainFrameLink = b
    b.Show()
    InitialParameter_9516()
    InitialParameter_91391()
    InitialParameter_91392()
    InitialParameter_5732()
    print 'Initial end.'
    a.MainLoop()
