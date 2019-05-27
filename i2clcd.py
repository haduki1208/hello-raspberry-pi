# -*- coding: utf-8 -*-
import smbus
from time import sleep
import subprocess

cmd_hostname = "hostname -I"
ipAddr = subprocess.check_output(cmd_hostname.split()).strip()
print("IP: " + ipAddr)

i2c = smbus.SMBus(1)  #bus number
addr01 = 0x3e #OLEDアドレス
_command = 0x00 #制御
_data = 0x40 #データ書き込み

def initDisplay():
    i2c.write_i2c_block_data(addr01, _command, [0x38, 0x39, 0x14, 0x70, 0x56, 0x6c])
    sleep(0.2)
    i2c.write_i2c_block_data(addr01, _command, [0x38, 0x0c, 0x01])
    sleep(0.1)

initDisplay()

try:
    word = "        " + ipAddr
    wordIndex = 0

    while True:
        showWordList = []
        for i in range(8):
            j = (wordIndex + i) % len(word)
            showWordList.append(ord(word[j]))
        # initDisplay()
        i2c.write_i2c_block_data(addr01, _command, [0x38, 0x0c, 0x01])
        sleep(0.1)
        i2c.write_i2c_block_data(addr01, _data, showWordList)
        sleep(0.9)
        wordIndex = (wordIndex + 1) % len(word)

except KeyboardInterrupt:
    initDisplay()

# 改行
# i2c.write_i2c_block_data(addr01, _command, [0xc0])
# sleep(0.1)
