#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

GID=${UID}
LOG_FILE=/var/log/celery.log
STATE_FILE=/var/run/celery/worker.state

cd ${ROOTDIR}

while true; do
	sudo celery -A siteconfig --uid ${UID} --gid ${GID} --logfile ${LOG_FILE} --statedb ${STATE_FILE} worker
	echo "celery died! Restarting celery in ${SLEEP} second(s)"
	sleep ${SLEEP}
done
