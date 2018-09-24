#!/bin/bash

IFS=$'\n'

TEMP=$(mktemp)
for F in */migrations/0*.py; do
	echo -n "Processing $F... "

	declare -a RAW_DIFF
	declare -a DIFF
	declare -a DIFF_PLUS
	declare -a DIFF_MINUS

	readarray RAW_DIFF   < <(git diff $F | grep '^[-+][^-+]')
	readarray DIFF       < <(git diff $F | grep '^[-+][^-+#]')
	readarray DIFF_PLUS  < <(git diff $F | grep '^[+][^+#]' | sed 's/^+//')
	readarray DIFF_MINUS < <(git diff $F | grep '^[-][^-#]' | sed 's/^-//')

	SAME_FILE=0
	DIFF_PLUS_LEN=${#DIFF_PLUS[@]}
	DIFF_MINUS_LEN=${#DIFF_MINUS[@]}
	if [ $DIFF_PLUS_LEN -ne $DIFF_MINUS_LEN ]; then
		SAME_FILE=1
	else
		for i in $(seq 0 $DIFF_PLUS_LEN); do

			if [ "${DIFF_PLUS[$i]}" != "${DIFF_MINUS[$i]}" ]; then
				SAME_FILE=1
				break
			fi
		done
	fi

	if [ ${#RAW_DIFF[@]} -eq 0 ]; then
		echo CLEAN
		continue

	elif [ ${#DIFF[@]} -eq 0 ]; then
		git checkout $F
		echo RESET
		#printf "%s" "${DIFF[@]}"

	elif [ $SAME_FILE -eq 0 ]; then
		git checkout $F
		echo RESET" (same file)"
		#printf "%s" "${DIFF[@]}"

	else
		echo MODIFIED
		#printf "%s" "${DIFF[@]}"
	fi
done
