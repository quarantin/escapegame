#!/bin/bash

. $(dirname $0)/env.sh

APPS=(
	django
	websocket
)

CRONTAB=$(mktemp)


# UWSGI instances for django and websockets

for APP in "${APPS[@]}"; do
	echo "@reboot sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini:${APP}" >> "${CRONTAB}"
done


# Django background tasks

echo "@reboot ${ROOTDIR}/scripts/django-background-service.sh" >> "${CRONTAB}"


# Django websocket processes

echo "@reboot cd ${ROOTDIR} && ${PYTHON} manage.py websocket-1001-nuits"      >> "${CRONTAB}"
echo "@reboot cd ${ROOTDIR} && ${PYTHON} manage.py websocket-stranger-things" >> "${CRONTAB}"


crontab "${CRONTAB}"
STATUS=$?
rm -f "${CRONTAB}"
if [ "${STATUS}" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully uwsgi for django"
	echo "[ + ] Installed successfully uwsgi for websockets"
	echo "[ + ] Installed successfully django-background-service.sh"
	echo "[ + ] Installed successfully websocket-1001-nuits"
	echo "[ + ] Installed successfully websocket-stranger-things"
else
	echo "ERROR: failed to install crontab!"
fi
