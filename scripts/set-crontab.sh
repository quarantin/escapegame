#!/bin/bash

. $(dirname $0)/env.sh

CRONTAB=$(mktemp)

echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/django.ini" >> "${CRONTAB}"
echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/websocket.ini" >> "${CRONTAB}"
echo "@reboot ${ROOTDIR}/scripts/django-background-service.sh" >> "${CRONTAB}"

crontab "${CRONTAB}"
STATUS=$?
rm -f "${CRONTAB}"
if [ "${STATUS}" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully uwsgi for django"
	echo "[ + ] Installed successfully uwsgi for websockets"
	echo "[ + ] Installed successfully django-background-service.sh"
else
	echo "ERROR: failed to install crontab!"
fi
