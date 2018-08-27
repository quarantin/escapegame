#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)


# Django background tasks

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh process_tasks"             >> "${CRONTAB}"


# Django websocket processes

echo "@reboot ${ROOTDIR}/scripts/python-manage.sh websocket-1001-nuits"      >> "${CRONTAB}"
echo "@reboot ${ROOTDIR}/scripts/python-manage.sh websocket-stranger-things" >> "${CRONTAB}"


# UWSGI instances for django and websockets

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> "${CRONTAB}"
done


crontab "${CRONTAB}"
STATUS=$?
rm -f "${CRONTAB}"
if [ "${STATUS}" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully django-background-service.sh"
	echo "[ + ] Installed successfully websocket-1001-nuits"
	echo "[ + ] Installed successfully websocket-stranger-things"
	echo "[ + ] Installed successfully uwsgi for django"
	echo "[ + ] Installed successfully uwsgi for websockets"
else
	echo "ERROR: failed to install crontab!"
fi
