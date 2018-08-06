#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1
LOGFILE='django-tasks.log'

cd "${ROOTDIR}"

echo -n > "${LOGFILE}"

while true; do
	"${PYTHON}" manage.py process_tasks                  2>&1 >> "${LOGFILE}"
	echo "${PYTHON} died! Restarting django background tasks in ${SLEEP}" 2>&1 >> "${LOGFILE}"
	sleep "${SLEEP}"
done
