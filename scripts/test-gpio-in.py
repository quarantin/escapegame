#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO


if len(sys.argv) < 2:
	print('Usage: %s <pin>' % sys.argv[0])

pin = int(sys.argv[1])

print("Configuring pin %d for input" % pin)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

i = -1

while True:

	state = GPIO.input(pin)

	print("Read state: %s" % state)

	input("[ Press enter for next read ]")
