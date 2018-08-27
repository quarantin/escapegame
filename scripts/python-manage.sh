#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

cd "${ROOTDIR}"

while true; do
	"${PYTHON}" manage.py $@
	echo "${PYTHON} died! Restarting command `${PYTHON} manage.py $@` in ${SLEEP} second(s)"
	sleep "${SLEEP}"
done
