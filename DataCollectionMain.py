from MotorM import motorcontrol
from keyboardM import Keyboard1
from CameraM import OakDCamera
import time
import threading

def camera_stream(camera):
    # Function to run the camera stream in a separate thread
    camera.video_displayed(display=True)

def main():
    keyboard = Keyboard1()
    motor = motorcontrol()
    camera = OakDCamera()
    angle = 100
    ButtonE = 0
    record = 0

    # Start the camera stream in a new thread
    camera_thread = threading.Thread(target=camera_stream, args=(camera,))

    try:
        while True:
            if keyboard.getKey('e'):
                camera_thread.start()

            if jsM.getKey('z'):
                if record == 0:
                record = 1
                print('Recording started...')
                sleep(0.300)
                img = wM.getImg(True, size=[240,120])
                dcM.saveData(img, steering)
            else:
                print('Recording already started')

            elif jsM.getKey('x'):
                if record == 1:
                record = 0
                print('Recording stop...')
                sleep(0.300)
                dcM.saveLog()
                else:
                print('Recording already stopped')
                
            if keyboard.getKey('w'):
                angle = 100
                motor.move_forward(60)
                motor.reset_steering()
            elif keyboard.getKey('a'):
                motor.move_forward(40)
                angle -= 5
                if angle < 0:
                    angle = 0
                motor.set_steering_angle(angle)
            elif keyboard.getKey('d'):
                motor.move_forward(40)
                angle += 5
                if angle > 180:
                    angle = 180
                motor.set_steering_angle(angle)
                
            else:
                motor.stop_motor()
            
            # Print the steering angle
            print(angle)

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        motor.cleanup()
        # Stop the camera stream thread gracefully
        camera.close()

if __name__ == '__main__':
    main()
