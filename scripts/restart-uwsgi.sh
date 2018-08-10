#!/bin/bash

sudo killall -9 uwsgi

sleep 1

sudo uwsgi --ini /etc/uwsgi/apps-enabled/escapegame.ini
