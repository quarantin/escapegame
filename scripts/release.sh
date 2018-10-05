#!/bin/bash

RELEASE='v0.1'
MESSAGE='First version'

if [ ! -z "${2}" ]; then
	MESSAGE="${2}"
fi

if [ ! -z "${1}" ]; then
	RELEASE="${1}"
fi

git push --delete origin ${RELEASE}
git tag -d ${RELEASE}
git tag -a ${RELEASE} -m "${MESSAGE}"
git push origin ${RELEASE}
