import RPi.GPIO as GPIO
from time import sleep


class Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # 모터 상태
        self.STOP = 0
        self.FORWARD = 1
        self.BACKWARD = 2
        # 모터 채널
        self.CH1 = 0
        self.CH2 = 1

        # PIN 입출력 설정
        self.OUTPUT = 1
        self.INPUT = 0

        # PIN 설정
        self.HIGH = 1
        self.LOW = 0
        # 실제 핀 정의
        self.ENA = 26
        self.ENB = 0

        self.IN1 = 19
        self.IN2 = 13
        self.IN3 = 6
        self.IN4 = 5

        self.pwmA = self.set_pin_config(self.ENA, self.IN1, self.IN2)
        self.pwmB = self.set_pin_config(self.ENB, self.IN3, self.IN4)

    def set_pin_config(self, en, ina, inb):
        GPIO.setup(en, GPIO.OUT)
        GPIO.setup(ina, GPIO.OUT)
        GPIO.setup(inb, GPIO.OUT)
        pwm = GPIO.PWM(en, 100)
        pwm.start(0)
        return pwm

    def set_motor_control(self, pwm, ina, inb, speed, stat):
        pwm.ChangeDutyCycle(speed)

        if stat == self.FORWARD:
            GPIO.output(ina, self.HIGH)
            GPIO.output(inb, self.LOW)

        elif stat == self.BACKWARD:
            GPIO.output(ina, self.LOW)
            GPIO.output(inb, self.HIGH)

        elif stat == self.STOP:
            GPIO.output(ina, self.LOW)
            GPIO.output(inb, self.LOW)

    def set_motor(self, ch, speed, stat):
        if ch == self.CH1:
            self.set_motor_control(self.pwmA, self.IN1, self.IN2, speed, stat)
        else:
            self.set_motor_control(self.pwmB, self.IN3, self.IN4, speed, stat)

    def go_forward(self, speed):
        self.set_motor(self.CH1, speed, self.FORWARD)
        self.set_motor(self.CH2, speed, self.FORWARD)

    def go_backward(self, speed):
        self.set_motor(self.CH1, speed, self.BACKWARD)
        self.set_motor(self.CH2, speed, self.BACKWARD)

    def run(self, speed):
        if speed < 0:
            speed = min(100, -speed)
            self.go_backward(speed)
        else:
            speed = min(100, speed)
            self.go_forward(speed)

    def stop(self):
        self.set_motor(self.CH1, 0, self.STOP)
        self.set_motor(self.CH2, 0, self.STOP)


if __name__ == "__main__":
    motor = Motor()
    try:
        while True:
            motor.go_forward(50)
            sleep(1)
            motor.go_backward(50)
            sleep(1)
    except KeyboardInterrupt:
        motor.stop()
        GPIO.cleanup()
