#!/bin/bash

if (( $# > 0 ))
then
	source activate "$@"
	echo "Installing to Environment" "$@"
	conda env list
	pip install -r requirements.txt
else
	echo "Installing to default Python Environment"
	pip install -r requirements.txt
fi
