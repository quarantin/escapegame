#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

rm -f */migrations/0*.py

${PYTHON} manage.py makemigrations
