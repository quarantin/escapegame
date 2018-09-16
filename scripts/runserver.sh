#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

cd "${ROOTDIR}"

sudo /etc/init.d/nginx stop

while true; do
	"${PYTHON}" manage.py runserver $HOSTNAME:80
	echo "${PYTHON} died! Restarting django in ${SLEEP} second(s)"
	sleep "${SLEEP}"
done
