#!/bin/bash

if [ -z "$1" ]
then 
	export FRONTEND_HOST=127.0.0.1
else
	export FRONTEND_HOST=$1
fi
if [ -z "$2" ]
then 
	python3 client.py 1
else
	python3 client.py $2
fi