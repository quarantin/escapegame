#!/bin/bash

. $(dirname $0)/env.sh

if [ $HOSTNAME == $MASTER_HOSTNAME ]; then

	${ROOTDIR}/scripts/restart-mysql.sh

	${ROOTDIR}/scripts/restart-redis.sh
fi

${ROOTDIR}/scripts/restart-nginx.sh

${ROOTDIR}/scripts/restart-uwsgi.sh

${ROOTDIR}/scripts/restart-django-services.sh
