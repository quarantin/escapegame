#!/bin/bash

for F in */migrations/0*.py; do
	DIFF=$(git diff $F)
	COUNT=$(echo $DIFF | wc -l)
	if [ "$COUNT" -eq "10" ]; then
		git checkout $F
	else
		ADDS=$(echo $DIFF | grep '^+[^+]' | sed 's/^+//' | tail -n +2)
		DELS=$(echo $DIFF | grep '^-[^-]' | sed 's/^-//' | tail -n +2)

		if [ "$ADDS" == "$DELS" ]; then
			git checkout $F
		fi
	fi
done
