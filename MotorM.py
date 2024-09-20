import RPi.GPIO as GPIO
import time

class motorcontrol:
    def __init__(self, L_PWM=12, R_PWM=16, L_EN=27, R_EN=17, L2_PWM=21, R2_PWM=13, L2_EN=26, R2_EN=19, SteeringPin=18):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.L_PWM = L_PWM
        self.R_PWM = R_PWM
        self.L_EN = L_EN
        self.R_EN = R_EN
        self.L2_PWM = L2_PWM
        self.R2_PWM = R2_PWM
        self.L2_EN = L2_EN
        self.R2_EN = R2_EN
        self.SteeringPin = SteeringPin

        GPIO.setup(self.L_PWM, GPIO.OUT)
        GPIO.setup(self.R_PWM, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.R_EN, GPIO.OUT)
        GPIO.setup(self.L2_PWM, GPIO.OUT)
        GPIO.setup(self.R2_PWM, GPIO.OUT)
        GPIO.setup(self.L2_EN, GPIO.OUT)
        GPIO.setup(self.R2_EN, GPIO.OUT)
        GPIO.setup(self.SteeringPin, GPIO.OUT)

        self.left_motor_pwm = GPIO.PWM(self.L_PWM, 1000)
        self.right_motor_pwm = GPIO.PWM(self.R_PWM, 1000)
        self.left2_motor_pwm = GPIO.PWM(self.L2_PWM, 1000)
        self.right2_motor_pwm = GPIO.PWM(self.R2_PWM, 1000)

        self.left_motor_pwm.start(0)
        self.right_motor_pwm.start(0)
        self.left2_motor_pwm.start(0)
        self.right2_motor_pwm.start(0)

        self.steeringPin_pwm = GPIO.PWM(self.SteeringPin, 50)
        self.steeringPin_pwm.start(0)

        GPIO.output(self.L_EN, GPIO.HIGH)
        GPIO.output(self.R_EN, GPIO.HIGH)
        GPIO.output(self.L2_EN, GPIO.HIGH)
        GPIO.output(self.R2_EN, GPIO.HIGH)

    def move_forward(self, speed=60):
        self.left_motor_pwm.ChangeDutyCycle(speed)
        self.right_motor_pwm.ChangeDutyCycle(0)
        self.left2_motor_pwm.ChangeDutyCycle(speed)
        self.right2_motor_pwm.ChangeDutyCycle(0)
        #print('Moving Forward')

    def move_backward(self, speed=50):
        self.left_motor_pwm.ChangeDutyCycle(0)
        self.right_motor_pwm.ChangeDutyCycle(speed)
        self.left2_motor_pwm.ChangeDutyCycle(0)
        self.right2_motor_pwm.ChangeDutyCycle(speed)
        print('Moving Backward')

    def set_steering_angle(self, angle):
        if 0 <= angle <= 180:
            duty = 2 + (angle / 18)
            self.steeringPin_pwm.ChangeDutyCycle(duty)
            #print(f'Steering angle set to {angle} degrees')
        else:
            print("Angle out of range!")

    def turn_left(self):
        self.set_steering_angle(70)
        print("Turning Left")

    def turn_right(self):
        self.set_steering_angle(130)
        print('Turning Right')

    def stop_motor(self):
        self.left_motor_pwm.ChangeDutyCycle(0)
        self.right_motor_pwm.ChangeDutyCycle(0)
        self.left2_motor_pwm.ChangeDutyCycle(0)
        self.right2_motor_pwm.ChangeDutyCycle(0)
        #print('Motor Stopped')

    def reset_steering(self):
        self.set_steering_angle(100)
        #print('Steering reset to 90 degrees')

    def cleanup(self):
        self.reset_steering()
        self.left_motor_pwm.stop()
        self.right_motor_pwm.stop()
        self.left2_motor_pwm.stop()
        self.right2_motor_pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    motor = motorcontrol()

    try:
        print("Testing motor control...")
        
        # Move forward
        motor.move_forward(speed=70)
        time.sleep(2)

        # Stop
        motor.stop_motor()
        time.sleep(1)

        # Move backward
        motor.move_backward(speed=70)
        time.sleep(2)

        # Stop
        motor.stop_motor()
        time.sleep(1)

        # Turn left
        motor.turn_left()
        time.sleep(2)

        # Turn right
        motor.turn_right()
        time.sleep(2)

        # Reset steering
        motor.reset_steering()
        time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        motor.cleanup()
