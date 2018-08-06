#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1
PORT=80
LOGFILE='django.log'

cd "${ROOTDIR}"

echo -n > "${LOGFILE}"

while true; do
	"${PYTHON}" manage.py runserver "${HOSTNAME}:${PORT}" 2>&1 >> "${LOGFILE}"
	echo "${PYTHON} died! Restarting django in ${SLEEP}"  2>&1 >> "${LOGFILE}"
	sleep "${SLEEP}"
done
