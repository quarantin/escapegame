#!/bin/bash

. $(dirname $0)/env.sh

SLEEP=1
LOGFILE=/var/log/django-service-${1}.info.log
ERRFILE=/var/log/django-service-${1}.err.log

cd ${ROOTDIR}

while true; do
	#sudo sh -c "echo \"# Restarting service ${1} $(date)\" > ${LOGFILE}"
	#sudo sh -c "echo -n > ${ERRFILE}"
	#sudo chmod 644 ${LOGFILE}
	#sudo chmod 644 ${ERRFILE}
	#sudo chown ${PI_UID}:${PI_GID} ${LOGFILE} ${ERRFILE}

	${PYTHON} manage.py ${1} #2>${ERRFILE} >>${LOGFILE}
	if [ ${?} -eq 0 ]; then
		echo "Command \`${PYTHON} manage.py @@\` has quit, orderly exit (Probably no challenge assigned to this Raspberry Pi)."
		break
	else
		echo "${PYTHON} died! Restarting command \`${PYTHON} manage.py $@\` in ${SLEEP} second(s)"
		sleep ${SLEEP}
	fi
done
