#!/bin/bash

HOST=raspberrypi.local
PORT=80

PYTHON=python3
DJANGO=/home/pi/escapegame.git

cd "${DJANGO}" && while true; do
	"${PYTHON}" manage.py runserver "${HOST}:${PORT}"
	sleep 5
done

