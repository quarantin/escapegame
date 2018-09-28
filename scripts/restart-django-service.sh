#!/bin/bash

. $(dirname $0)/env.sh

${ROOTDIR}/scripts/django-service-stop.sh

for SERVICE in lift-control video-player monitor-network poll-gpios websocket-timer; do
	${ROOTDIR}/scripts/stop-django-service.sh ${SERVICE}
done
