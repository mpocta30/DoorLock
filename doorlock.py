import wiringpi
import time
import sys

class DoorLock:
	def __init__(self):
		self.delay_period = 0.01
		
		# use 'GPIO naming'
		wiringpi.wiringPiSetupGpio()

		# set #18 to be a PWM output
		wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

		# set the PWM mode to milliseconds stype
		wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

		# divide down clock
		wiringpi.pwmSetClock(192)
		wiringpi.pwmSetRange(2000)

	def moveServo(self, lower, upper, step):
		for pulse in range(lower, upper, step):
			wiringpi.pwmWrite(18, pulse)
			time.sleep(self.delay_period)