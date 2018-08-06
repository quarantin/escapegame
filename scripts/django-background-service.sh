#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

cd "${ROOTDIR}"

while true; do
	"${PYTHON}" manage.py process_tasks
	echo "${PYTHON} died! Restarting django background tasks in ${SLEEP} second(s)"
	sleep "${SLEEP}"
done
