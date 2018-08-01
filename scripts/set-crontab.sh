#!/bin/bash

. env.sh

ENTRY=$(crontab -l 2>&1 | grep django-service)
if [ -z "$ENTRY" ]; then

	CRONTAB=$(mktemp)

	echo "@reboot ${ROOTDIR}/scripts/django-service.sh &" > "${CRONTAB}"
	crontab "${CRONTAB}"
	STATUS=$?
	rm -f "${CRONTAB}"
	if [ "$STATUS" = "0" ]; then
		crontab -l
		echo "[ + ] django-service.sh installed successfully."
	else
		echo "ERROR: failed to install django-service.sh!"
	fi

else
	crontab -l
	echo "[ + ] django-service.sh is already configured."
fi
