#!/bin/bash

POSTURL='http://escapegame.local/admin/import-export/export/'
POSTDATA='export_date=on&software_version=on&escapegames=on&arduinos=on&raspberry_pis=on&remote_challenge_pins=on&remote_door_pins=on&remote_led_pins=on&images=on&videos=on'

wget -q -O- --post-data="${POSTDATA}" "${POSTURL}"
