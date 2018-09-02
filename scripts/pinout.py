#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO


# See:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Checking%20function%20of%20GPIO%20channels/

FUNCTIONS = {
	GPIO.IN: 'GPIO.IN',
	GPIO.OUT: 'GPIO.OUT',
	GPIO.SPI: 'GPIO.SPI',
	GPIO.I2C: 'GPIO.I2C',
	GPIO.HARD_PWM: 'GPIO.HARD_PWM',
	GPIO.SERIAL: 'GPIO.SERIAL',
	GPIO.UNKNOWN: 'GPIO.UNKNOWN',
}

verbose = False
if '-v' in sys.argv[1:]:
	verbose = True

GPIO.setmode(GPIO.BOARD)
for pin in range(1, 41):

	try:
		func = GPIO.gpio_function(pin)
		if func in FUNCTIONS:
			func = FUNCTIONS[func]

		print("PIN %d = %s" % (pin, func))

	except Exception as err:
		err = str(err)
		if err.startswith('The channel sent is invalid on a Raspberry Pi'):
			if verbose:
				print("PIN %d is not a GPIO" % pin)
		else:
			print('Error: %s' % err)
