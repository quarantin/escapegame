#!/bin/bash

. $(dirname $0)/env.sh

echo 'Restarting mysql...'
${ROOTDIR}/scripts/restart-mysql.sh

echo 'Restarting redis...'
${ROOTDIR}/scripts/restart-redis.sh

echo 'Restarting nginx...'
${ROOTDIR}/scripts/restart-nginx.sh

echo 'Restarting uwsgi...'
${ROOTDIR}/scripts/restart-uwsgi.sh

echo 'Restarting django services...'
${ROOTDIR}/scripts/restart-django-services.sh
