#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> "${CRONTAB}"
done

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
