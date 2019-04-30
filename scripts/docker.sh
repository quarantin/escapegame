#!/bin/bash

if [ -z "${1}" ]; then
	echo "Usage: ${0} <build|run>"
	exit
fi

ACTION="${1}"

if [ "${ACTION}" = "build" ]; then
	docker build -t escapegame:v01 -f conf/Dockerfile .
elif [ "${ACTION}" = "run" ]; then
	docker run -t escapegame:v01
else
	echo "Unknown action '${ACTION}'."
fi
