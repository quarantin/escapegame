#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

#rm -f */migrations/0*.py

echo "[ * ] Running ${PYTHON} manage.py makemigrations..."
${PYTHON} manage.py makemigrations

ESCAPEGAME_TRACKED=$(git status | grep deleted.*escapegame/migrations/0002_auto_ | awk '{ print $2 }')
ESCAPEGAME_UNTRACKED=$(git ls-files --others --exclude-standard | grep escapegame/migrations/0002_auto_)

CONTROLLER_TRACKED=$(git status | grep deleted.*controllers/migrations/0002_auto_ | awk '{ print $2 }')
CONTROLLER_UNTRACKED=$(git ls-files --others --exclude-standard | grep controllers/migrations/0002_auto_)

if [ ! -z "${CONTROLLER_TRACKED}" ] && [ ! -z "${CONTROLLER_UNTRACKED}" ]; then
	echo "Restoring deleted tracked file '${CONTROLLER_UNTRACKED}' => '${CONTROLLER_TRACKED}'"
	mv ${CONTROLLER_UNTRACKED} ${CONTROLLER_TRACKED}
fi

if [ ! -z "${ESCAPEGAME_TRACKED}" ] && [ ! -z "${ESCAPEGAME_UNTRACKED}" ]; then
	echo "Restoring deleted tracked file '${ESCAPEGAME_UNTRACKED}' => '${ESCAPEGAME_TRACKED}'"
	mv ${ESCAPEGAME_UNTRACKED} ${ESCAPEGAME_TRACKED}
fi

./scripts/fix-migrations.sh


if [ "${1}" = 'migrate' ]; then
	echo "[ * ] Running ${PYTHON} manage.py migrate..."
	${PYTHON} manage.py migrate
fi
