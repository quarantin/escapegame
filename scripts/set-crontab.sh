#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)


# Celery

echo "@reboot sudo celery worker -A siteconfig --logfile /var/log/celery.log --statedb /var/run/celery/worker.state --uid 1000 --gid 1000 --workdir ${ROOTDIR}" >> ${CRONTAB}


# Django background tasks

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh process_tasks" >> ${CRONTAB}


# Django websocket timer process

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh websocket-timer" >> ${CRONTAB}


# UWSGI instances for django and websockets

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> ${CRONTAB}
done


crontab ${CRONTAB}
STATUS=$?
rm -f "${CRONTAB}"
if [ "${STATUS}" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully celery"
	echo "[ + ] Installed successfully process_tasks"
	echo "[ + ] Installed successfully websocket-timer"
	for APP in "${APPS[@]}"; do
		echo "[ + ] Installed successfully uwsgi for ${APP}"
	done
else
	echo "ERROR: failed to install crontab!"
fi
