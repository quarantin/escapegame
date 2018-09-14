#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

GID=${UID}

LOG_FILE=/var/log/celery.log

STATE_DIR=/var/run/celery
STATE_FILE=${STATE_DIR}/worker.state

CELERY_WORKERS=15

cd ${ROOTDIR}

while true; do

	sudo sh -c "echo -n > ${LOG_FILE}"
	sudo chown ${UID}:${GID} ${LOG_FILE}

	sudo mkdir -p ${STATE_DIR}
	sudo chown ${UID}:${GID} ${STATE_DIR}

	sudo celery -A siteconfig -b redis://${MASTER_HOSTNAME} worker --statedb ${STATE_FILE} --uid ${UID} --gid ${GID} --logfile ${LOG_FILE} --concurrency ${CELERY_WORKERS}

	echo "celery died! Restarting celery in ${SLEEP} second(s)"
	sleep ${SLEEP}
done
