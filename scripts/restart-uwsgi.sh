#!/bin/bash

APPS=(
	django
	websocket
)

sudo killall -9 uwsgi

for APP in "${APPS[@]}"; do
	LOGFILE=/var/log/uwsgi.${APP}.log
	sudo sh -c "echo \"# Restarting uwsgi app ${APP}\" > ${LOGFILE}"
	sudo chmod 644 ${LOGFILE}

	sudo uwsgi --ini "/etc/uwsgi/apps-enabled/uwsgi.ini:$APP"
done
