#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

ENTRY=$(crontab -l 2>&1 | grep django-service)
if [ -z "$ENTRY" ]; then

	CRONTAB=$(mktemp)
	ROOTDIR=$(realpath "${SCRIPTDIR}/..")

	echo "@reboot ${ROOTDIR}/scripts/django-service.sh &" > "${CRONTAB}"
	crontab "${CRONTAB}"
	RES=$?
	rm -f "${CRONTAB}"
	if [ "$RES" = "0" ]; then
		crontab -l
		echo "[ + ] django-service.sh installed successfully."
	else
		echo "ERROR: failed to install django-service.sh!"
	fi

else
	crontab -l
	echo "[ + ] django-service.sh is already configured."
fi
