#!/bin/bash

. $(dirname $0)/env.sh

POSTURL="http://${MASTER_HOSTNAME}/admin/json/export/"
POSTDATA='export_date=on&software_version=on&escapegames=on&rooms=on&challenges=on&gpios=on&raspberry_pis=on&images=on&videos=on'

wget -q -O- --post-data="${POSTDATA}" "${POSTURL}"
