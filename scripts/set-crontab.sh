#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)


# Celery

echo "@reboot ${ROOTDIR}/scripts/python-celery.sh" >> ${CRONTAB}


# Django background tasks

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh process_tasks" >> ${CRONTAB}


# Django websocket timer process

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh websocket-timer" >> ${CRONTAB}


# Monitor the network to see which Raspberry Pis are alive

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh monitor-network" >> ${CRONTAB}


# UWSGI instances for django and websockets

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> ${CRONTAB}
done


# Configure the crontab
crontab ${CRONTAB}

if [ "${?}" = "0" ]; then
	echo '[ + ] Crontab installed successfully'
else
	echo 'ERROR: failed to install crontab!'
fi


# Delete temporary file

rm -f "${CRONTAB}"
