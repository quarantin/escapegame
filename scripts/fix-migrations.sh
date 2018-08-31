#!/bin/bash

for F in */migrations/0*.py; do
	echo -n "Fixing $F..."
	DIFF=$(git diff $F)
	COUNT=$(git diff $F | wc -l)

	if [ "$COUNT" -eq "10" ] || [ "$COUNT" -eq "20" ]; then
		git checkout $F
		echo ' RESET'

	elif [ "$COUNT" -ne "0" ]; then
		echo ' MODIFIED'
	#	ADDS=$(echo $DIFF | grep '^+[^+]' | sed 's/^+//' | tail -n +2)
	#	DELS=$(echo $DIFF | grep '^-[^-]' | sed 's/^-//' | tail -n +2)
	#
	#	if [ "$ADDS" == "$DELS" ]; then
	#		git checkout $F
	#	fi
	else
		echo ' NOT TOUCHED'
	fi
done
