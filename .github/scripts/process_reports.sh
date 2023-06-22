#!/usr/bin/env bash

for d in $(find reports/anvil-$1/tool-tests -type d -name "$2") ; do
	#echo $d
	python .github/scripts/process_reports.py $d
done

