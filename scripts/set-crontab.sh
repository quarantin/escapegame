#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)


# Only the master needs these

if [ ${HOSTNAME} = ${MASTER_HOSTNAME} ]; then


	# Lift control management task

	echo "@reboot ${ROOTDIR}/scripts/python-manage.sh lift-control" >> ${CRONTAB}


	# Monitor the network to see which Raspberry Pis are alive

	echo "@reboot ${ROOTDIR}/scripts/python-manage.sh monitor-network" >> ${CRONTAB}


	# Django websocket timer process

	echo "@reboot ${ROOTDIR}/scripts/python-manage.sh websocket-timer" >> ${CRONTAB}
fi


# GPIO polling management task

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh poll-gpios" >> ${CRONTAB}


# Video player management task

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh video-player" >> ${CRONTAB}


# UWSGI instances for django and websockets

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> ${CRONTAB}
done


# Configure the crontab
crontab ${CRONTAB}

if [ "${?}" = '0' ]; then
	echo '[ + ] Crontab installed successfully:'
	crontab -l
else
	echo 'ERROR: failed to install crontab!'
fi


# Delete temporary file

rm -f ${CRONTAB}
