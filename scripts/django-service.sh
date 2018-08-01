#!/bin/bash

HOST=raspberrypi.local
PORT=80

PYTHON=python3
DJANGO="$( cd "$(dirname "$( dirname "${BASH_SOURCE[0]}" )" )" >/dev/null && pwd )"

cd "${DJANGO}" && while true; do
	"${PYTHON}" manage.py runserver "${HOST}:${PORT}"
	sleep 5
done

