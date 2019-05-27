from picamera import PiCamera
from time import sleep

camera = PiCamera()

# カメラが画像の取得を開始する
camera.start_preview()

# 5秒待つ
sleep(5)

# 画像を収録して保存
camera.capture('tmp.jpg')

# カメラが画像の取得を停止する
camera.stop_preview()