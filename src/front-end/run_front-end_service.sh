#!/bin/bash

#export DISABLE_CACHE=
unset DISABLE_CACHE

if [ -z "$1" ]
then 
	export FRONTEND_HOST=127.0.0.1
else
	export FRONTEND_HOST=$1
fi
if [ -z "$2" ]
then 
	export CATALOG_HOST=127.0.0.1
else
	export CATALOG_HOST=$2
fi
if [ -z "$3" ]
then 
	export ORDER_HOST=127.0.0.1
else
	export ORDER_HOST=$3
fi
if [ -z "$4" ]
then 
	export ORDER_PORT_1=50054
else
	export ORDER_PORT_1=$4
fi
if [ -z "$5" ]
then 
	export ORDER_PORT_2=50055
else
	export ORDER_PORT_2=$5
fi
if [ -z "$6" ]
then 
	export ORDER_PORT_3=50056
else
	export ORDER_PORT_3=$6
fi
if [ -z "$7" ]
then 
	export ORDER_HOST_2=127.0.0.1
else
	export ORDER_HOST_2=$7
fi
if [ -z "$8" ]
then 
	export ORDER_HOST_3=127.0.0.1
else
	export ORDER_HOST_3=$8
fi

python3 frontend.py