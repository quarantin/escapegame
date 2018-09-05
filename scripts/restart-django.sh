#!/bin/bash

. $(dirname $0)/env.sh

${ROOTDIR}/scripts/restart-uwsgi.sh

${ROOTDIR}/scripts/restart-django-services.sh
