#!/bin/bash

. $(dirname $0)/env.sh

ENTRY=$(crontab -l 2>&1 | grep django-background-service)
if [ -z "$ENTRY" ]; then

	CRONTAB=$(mktemp)

	echo "@reboot ${ROOTDIR}/scripts/django-service.sh &"            >> "${CRONTAB}"
	echo "@reboot ${ROOTDIR}/scripts/django-background-service.sh &" >> "${CRONTAB}"

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

else
	crontab -l
	echo "[ + ] Already configured django-service.sh"
	echo "[ + ] Already configured django-background-service.sh"
fi
