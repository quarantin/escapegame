#!/bin/bash

. $(dirname $0)/env.sh

LOGFILE='django.log'
PORT=80

cd "${ROOTDIR}"

echo -n > "${LOGFILE}"

while true; do
	"${PYTHON}" manage.py runserver "${HOSTNAME}:${PORT}" 2>&1 >> "${LOGFILE}"
	sleep 5
done

