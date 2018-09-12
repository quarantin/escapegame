#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

GID=${UID}
LOG_FILE=/var/log/celery.log
STATE_DIR=/var/run/celery
STATE_FILE=${STATE_DIR}/worker.state

cd ${ROOTDIR}

while true; do
	sudo mkdir -p ${STATE_DIR}
	sudo chown ${UID}:${GID} ${STATE_DIR}
	sudo celery -A siteconfig -b redis://${MASTER_HOSTNAME} worker --statedb ${STATE_FILE} --uid ${UID} --gid ${GID} --logfile ${LOG_FILE}
	echo "celery died! Restarting celery in ${SLEEP} second(s)"
	sleep ${SLEEP}
done
