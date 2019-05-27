# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

def my_callback(channel):
    global ledState
    if channel == 24:
        ledState = not ledState
        if ledState == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
        else:
            GPIO.output(25, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
# 消灯状態
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
# プルダウン抵抗を有効にする
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ポジティブエッジの検出
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=200)
#GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback, bouncetime=200)
#GPIO.add_event_detect(24, GPIO.BOTH, callback=my_callback, bouncetime=200)

ledState = GPIO.LOW

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()