#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

cd "${ROOTDIR}"

while true; do
	"${PYTHON}" manage.py runserver $HOSTNAME:80
	echo "${PYTHON} died! Restarting django background tasks in ${SLEEP} second(s)"
	sleep "${SLEEP}"
done
