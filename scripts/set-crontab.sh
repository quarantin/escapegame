#!/bin/bash

. $(dirname $0)/env.sh

CRONTAB=$(mktemp)

echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/escapegame.ini" >> "${CRONTAB}"
echo "@reboot ${ROOTDIR}/scripts/django-background-service.sh" >> "${CRONTAB}"

crontab "${CRONTAB}"
STATUS=$?
rm -f "${CRONTAB}"
if [ "${STATUS}" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully uwsgi"
	echo "[ + ] Installed successfully django-background-service.sh"
else
	echo "ERROR: failed to install crontab!"
fi
