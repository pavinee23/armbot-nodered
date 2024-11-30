from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[9].angle = 70
time.sleep(2.5)
kit.servo[5].angle = 100
time.sleep(2.5)
kit.servo[5].angle = 70
time.sleep(2.5)
kit.servo[5].angle = 50
time.sleep(2.5)
kit.servo[5].angle = 20
time.sleep(2.5)




