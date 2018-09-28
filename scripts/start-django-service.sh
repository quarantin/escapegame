#!/bin/bash

. $(dirname $0)/env.sh

SERVICES=$@

if [ -z "${SERVICES}" ]; then

	if [ ${HOSTNAME} = ${MASTER_HOSTNAME} ]; then

		SERVICES=$(echo lift-control video-player monitor-network poll-gpios websocket-timer)
	else

		SERVICES=$(echo video-player poll-gpios)
	fi
fi

for SERVICE in ${SERVICES}; do
	echo -n "[ * ] Starting background task for management command ${SERVICE} "

	${ROOTDIR}/scripts/python-manage.sh ${SERVICE} &

	echo OK
done
