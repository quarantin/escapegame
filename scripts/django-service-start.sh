#!/bin/bash

. $(dirname $0)/env.sh

COMMAND=$1

if [ -z "${COMMAND}" ]; then
	echo "Usage: ${0} <command>"
	exit
fi

echo -n "[ * ] Starting background task for management command ${COMMAND} "

${ROOTDIR}/scripts/python-manage.sh ${COMMAND} &

echo OK
