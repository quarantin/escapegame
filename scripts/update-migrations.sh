#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

rm -f */migrations/0*.py

echo "[ * ] Running ${PYTHON} manage.py makemigrations..."
${PYTHON} manage.py makemigrations

TRACKED=$(git status | grep deleted | awk '{ print $2 }')
UNTRACKED=$(git ls-files --others --exclude-standard | grep controllers/migrations/0002_auto_)

if [ ! -z "${TRACKED}" ] && [ ! -z "${UNTRACKED}" ]; then
	echo "Restoring deleted tracked file '${UNTRACKED}' => '${TRACKED}'"
	mv ${UNTRACKED} ${TRACKED}
fi

./scripts/fix-migrations.sh


echo "[ * ] Running ${PYTHON} manage.py migrate..."
${PYTHON} manage.py migrate
