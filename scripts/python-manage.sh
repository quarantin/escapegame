#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1

cd "${ROOTDIR}"

while true; do
	"${PYTHON}" manage.py $@
	if [ ${?} -eq 0 ]; then
		echo "Command \`${PYTHON} manage.py @@\` has quit, orderly exit (No challenge assigned to this Raspberry Pi)."
		break
	else
		echo "${PYTHON} died! Restarting command \`${PYTHON} manage.py $@\` in ${SLEEP} second(s)"
		sleep "${SLEEP}"
	fi
done
