from bt_proximity import BluetoothRSSI
import time
import wiringpi
import time
import sys

class DoorLock:
	def __init__(self):
		self.rssi = -10
		self.open = False
		self.btaddr = 'D0:25:98:E3:79:37'
		self.btrssi = BluetoothRSSI(addr=self.btaddr)
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


if __name__ == '__main__':
	# Create item of type DoorLock
	lock = DoorLock()

	try:
		while True:
			lock.rssi = lock.btrssi.get_rssi()

			# If door is locked and phone comes close to lock
			if not lock.open and lock.rssi >= 0:
				lock.moveServo(50, 250, 1)
				lock.open = True
			elif lock.open and lock.rssi < 0:
				lock.moveServo(250, 50, -1)
				lock.open = False
	except:
		print("Thanks for trying our Lock!")
	
