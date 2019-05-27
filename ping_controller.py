# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import smbus
from time import sleep, time
import pyping

i2c = smbus.SMBus(1)  #bus number
addr01 = 0x3e #OLEDアドレス
_command = 0x00 #制御
_data = 0x40 #データ書き込み

# AQM0802Aの表示を初期化する
def initDisplay():
    i2c.write_i2c_block_data(addr01, _command, [0x38, 0x39, 0x14, 0x70, 0x56, 0x6c])
    sleep(0.2)
    i2c.write_i2c_block_data(addr01, _command, [0x38, 0x0c, 0x01])
    sleep(0.1)

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可。
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18 # start bit + single end bit
    commandout <<= 3 # LSBから8ビット目を送信するようにする
    
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    
    adcout = 0
    for i in range(13):
        #13ビット読む(null bit + 12bit data)
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

def appendIpOctet(channel):
    global ipOctet
    global ipOctetList
    ipOctetList.append(ipOctet)

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

# プルダウン抵抗を有効にする
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# ポジティブエッジの検出
GPIO.add_event_detect(24, GPIO.RISING, callback=appendIpOctet, bouncetime=200)

ipOctet = ""
ipOctetList = []

try:
    while True:
        # 0番から取得
        inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # 0 ~ 255の数字に変換
        ipOctet = str(int(inputVal0 / 16))

        initDisplay()
        if len(ipOctetList) == 0:
            i2c.write_i2c_block_data(addr01, _data, [ord(c) for c in list(ipOctet)])
            sleep(0.7)
            continue
        elif len(ipOctetList) == 4:
            break
        
        displayText = ".".join(ipOctetList) + "." + ipOctet

        # 1行目を出力
        i2c.write_i2c_block_data(addr01, _data, [ord(c) for c in list(displayText[:8])])
        if len(displayText) > 8:
            # 2行目を出力
            i2c.write_i2c_block_data(addr01, _command, [0xc0])
            sleep(0.1)
            i2c.write_i2c_block_data(addr01, _data, [ord(c) for c in list(displayText[8:])])
        sleep(0.7)

    GPIO.remove_event_detect(24)
    initDisplay()
    i2c.write_i2c_block_data(addr01, _data, [ord(c) for c in list("PING NOW")])

    # pingコマンド実行
    RPing = pyping.ping(".".join(ipOctetList))
    word = "        " + "AVG:" + str(RPing.avg_rtt) + "ms"
    wordIndex = 0
    while True:
        if GPIO.input(24) == GPIO.HIGH:
            # スイッチを押したら終了
            initDisplay()
            break
        
        showWordList = []
        for i in range(8):
            j = (wordIndex + i) % len(word)
            showWordList.append(ord(word[j]))
        initDisplay()
        i2c.write_i2c_block_data(addr01, _data, showWordList)
        sleep(0.7)
        wordIndex = (wordIndex + 1) % len(word)
    
except KeyboardInterrupt:
    initDisplay()

GPIO.cleanup()