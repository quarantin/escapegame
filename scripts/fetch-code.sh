#!/bin/bash

ORIGIN=corentin
BRANCH=master

OUTPUT=$(git status --porcelain)
MODIFIED=$(echo "${OUTPUT}" | grep '^ M ' | wc -l)
if [ "${MODIFIED}" -gt "0" ]; then
	git status
	exit
fi

git fetch "${ORIGIN}" && git pull "${ORIGIN}" "${BRANCH}"
