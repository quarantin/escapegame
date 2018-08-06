#!/usr/bin/python3

import sys
import RPi.GPIO as GPIO

pin = 24
if len(sys.argv) > 1:
	pin = int(sys.argv[1])

print("Please ensure pin %d is wired directly to the challenge pin you want to test." % pin)
input("[ Press enter to continue when ready ]")

GPIO.setmode(GPIO.BOARD)

print("Configuring pin %d for output" % pin)

gpio_type = GPIO.gpio_function(pin)
if gpio_type != GPIO.OUT:
	GPIO.setup(pin, GPIO.OUT)

i = -1

while True:

	i += 1

	state = ((i % 2) == 0) and GPIO.HIGH or GPIO.LOW

	print("Writing state: %s" % state)

	GPIO.output(pin, state)

	input("[ Press enter for next output ]")