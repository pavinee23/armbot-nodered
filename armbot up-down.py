from adafruit_servokit import ServoKit
import time
from picamera2 import Picamera2
import numpy as np
import cv2

def main():
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (2580, 2280)})
        picam2.configure(config)
        picam2.start()
        
        
        return picam2
    except Picamera2Error as e:
        print(f"Error initializing Picamera2: {e}")
        return None
    except IndexError as e:
        print("No camera found or index error: Ensure the camera is properly connected.")
        return None

servo_channel = 0
kit = ServoKit(channels=16)

def capture_and_process(picam2):
    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Armbot Control A00001", frame_bgr)

        ArmbotA00001 = frame_bgr[:2580, :2280]
        hsv = cv2.cvtColor(ArmbotA00001, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 100:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)
                    cv2.putText(frame, f"({cX}, {cY})", (cX + 10, cY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    move_servo_to_position(cX, cY)
                    close_gripper()

                    arm_x_range = 2580
                    arm_y_range = 2280  
                    release_x = arm_x_range // 2
                    release_y = arm_y_range // 2
                    move_servo_to_position(release_x, release_y)
                    open_gripper()

                    break

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

def move_servo_to_position(x, y):
    angle = int(x / 640 * 180)
    kit.servo[servo_channel].angle = angle
    time.sleep(1)

def close_gripper():
    kit.servo[servo_channel].angle = 90
    time.sleep(2)
    detach_servo()

def open_gripper():
    kit.servo[servo_channel].angle = 0
    time.sleep(2)
    detach_servo()

def detach_servo():
    kit.servo[servo_channel].angle = None

if __name__ == "__main__":
    picam2 = main()
    if picam2:
        try:
            capture_and_process(picam2)

            print("Opening gripper...")
            open_gripper()
            time.sleep(4.5)

            print("Closing gripper...")
            close_gripper()
            time.sleep(4.5)
        except KeyboardInterrupt:
            print("Program interrupted...")
        finally:
            close_gripper()
            print("Closed")
            picam2.stop()
            cv2.destroyAllWindows()
    else:
        print("Failed to initialize the camera.")