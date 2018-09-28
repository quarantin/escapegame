#!/bin/bash

. $(dirname $0)/env.sh

${ROOTDIR}/scripts/stop-django-service.sh

${ROOTDIR}/scripts/start-django-service.sh
