#!/usr/bin/python3

import sys
import RPi.GPIO as GPIO

pin = 12
if len(sys.argv) > 1:
	pin = int(sys.argv[1])

print("Configuring pin %d for output" % pin)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

for i in range(0, 10):
	state = ((i % 2) == 0) and GPIO.HIGH or GPIO.LOW
	print("Writing state: %s" % state)
	GPIO.output(pin, state)
	input("Press enter for next output...")
