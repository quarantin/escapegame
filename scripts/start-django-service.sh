#!/bin/bash

. $(dirname $0)/env.sh

SERVICES=$@

if [ -z "${SERVICES}" ]; then
	SERVICES=$(echo lift-control video-player monitor-network poll-gpios websocket-timer)
fi

for SERVICE in ${SERVICES}; do
	echo -n "[ * ] Starting background task for management command ${SERVICE} "

	${ROOTDIR}/scripts/python-manage.sh ${SERVICE} &

	echo OK
done
