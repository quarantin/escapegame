#!/bin/bash

APPS=(
	django
	websocket
)

sudo killall -9 uwsgi

for APP in "${APPS[@]}"; do
	sudo uwsgi --ini "/etc/uwsgi/apps-enabled/uwsgi.ini:$APP"
done
