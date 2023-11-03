#!/bin/bash

if [ -z "$1" ]
then 
	export FRONTEND_HOST=127.0.0.1
else
	export FRONTEND_HOST=$1
fi
if [ -z "$2" ]
then 
	p=1
else
	p=$2
fi
if [ -z "$3" ]
then 
	num_instances=5
else
	num_instances=$3
fi


for i in $( eval echo {1..$num_instances} )
do
	python3 client.py $p &
done