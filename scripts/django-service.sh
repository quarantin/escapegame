#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=5
PORT=80

cd "${ROOTDIR}"

while true; do
	"${PYTHON}" manage.py runserver "${HOSTNAME}:${PORT}"
	echo "${PYTHON} died! Restarting django in ${SLEEP}"
	sleep "${SLEEP}"
done

