#!/bin/bash -e

. $(dirname $0)/env.sh

TEMP=$(mktemp)

${PYTHON} ${ROOTDIR}/manage.py munin-config > ${TEMP} && \
sudo chown root:root ${TEMP} && \
sudo chmod 644 ${TEMP} && \
sudo mv ${TEMP} /etc/munin/munin.conf && \
sudo /etc/init.d/munin restart
