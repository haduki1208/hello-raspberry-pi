# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep, time

# 長押しを検知するために使用
timer = -1

def doSettingTimer(channel):
    global timer
    if timer < 0:
        startTimer()
    else:
        stopTimer()

def startTimer():
    global timer
    timer = time()

def stopTimer():
    global timer
    if time() - timer >= 1:
        GPIO.output(25, GPIO.HIGH)
    else:
        GPIO.output(25, GPIO.LOW)
    timer = -1

GPIO.setmode(GPIO.BCM)
# 消灯状態
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
# プルダウン抵抗を有効にする
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# イベントの検出
GPIO.add_event_detect(24, GPIO.BOTH, callback=doSettingTimer, bouncetime=50)

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()