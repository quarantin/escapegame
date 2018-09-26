#!/bin/bash

. $(dirname $0)/env.sh

SERVICES=${@}
if [ -z "${SERVICES}" ]; then
	SERVICES=python-manage.sh
fi

for SERVICE in ${SERVICES}; do

	PIDS=$(ps axo pid,command | grep "${SERVICE}" | grep -v grep | awk '{ print $1 }')
	if [ -z "${PIDS}" ]; then
		echo "No $@ process found to kill."

	else
		for PID in ${PIDS}; do
			echo "Killing PID: ${PID}"
			kill -9 -${PID} 2>/dev/null || kill -9 ${PID}
		done
	fi
done
