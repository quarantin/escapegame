#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

rm -f */migrations/0*.py

${PYTHON} manage.py makemigrations

TRACKED=$(git status | grep deleted | awk '{ print $2 }')
UNTRACKED=$(git ls-files --others --exclude-standard | grep controllers/migrations/0002_auto_)

if [ ! -z "${TRACKED}" ] && [ ! -z "${UNTRACKED}" ]; then
	echo "Restoring untracked file '${UNTRACKED}' => '${TRACKED}'"
	mv ${UNTRACKED} ${TRACKED}
fi

${ROOTDIR}/scripts/reset-migrations.sh
