#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO


pin = 24
if len(sys.argv) > 1:
	pin = int(sys.argv[1])

print("Please ensure pin %d is wired directly to the challenge pin you want to test." % pin)
input("[ Press enter to continue when ready ]")

print("Configuring pin %d for output" % pin)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

i = -1

while True:

	i += 1

	state = ((i % 2) == 1) and GPIO.HIGH or GPIO.LOW

	print("Writing state: %s" % state)

	GPIO.output(pin, state)

	input("[ Press enter for next output ]")
