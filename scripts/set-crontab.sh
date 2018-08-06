#!/bin/bash

. $(dirname $0)/env.sh

CRONTAB=$(mktemp)

LOGFILE_DJANGO="${ROOTDIR}/django.log"
LOGFILE_DJANGO_TASKS="${ROOTDIR}/django-tasks.log"

echo "@reboot ${ROOTDIR}/scripts/django-service.sh >>${LOGFILE_DJANGO} 2>&1" >> "${CRONTAB}"
echo "@reboot ${ROOTDIR}/scripts/django-background-service.sh >>${LOGFILE_DJANGO_TASKS} 2>&1" >> "${CRONTAB}"

crontab "${CRONTAB}"
STATUS=$?
rm -f "${CRONTAB}"
if [ "$STATUS" = "0" ]; then
	crontab -l
	echo "[ + ] Installed successfully django-service.sh"
	echo "[ + ] Installed successfully django-background-service.sh"
else
	echo "ERROR: failed to install django-service.sh!"
fi
