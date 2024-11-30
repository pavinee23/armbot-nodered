from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[9].angle = 0
time.sleep(2.5)
kit.servo[9].angle = 45
time.sleep(2.5)
kit.servo[9].angle = 90
time.sleep(2.5)
kit.servo[9].angle = 135
time.sleep(2.5)
kit.servo[9].angle = 180
time.sleep(2.5)
kit.servo[9].angle = 135
time.sleep(2.5)
kit.servo[9].angle = 90
time.sleep(2.5)
kit.servo[9].angle = 45
time.sleep(2.5)
kit.servo[9].angle = 0
time.sleep(2.5)
kit.servo[9].angle = 75

