#!/bin/bash

if [ -z "$1" ]
then 
	export CATALOG_HOST=127.0.0.1
else
	export CATALOG_HOST=$1
fi
if [ -z "$2" ]
then 
	export FRONTEND_HOST=127.0.0.1
else
	export FRONTEND_HOST=$1
fi

python3 catalog_service.py