#!/bin/bash

# Starts 3 replicas of the order service, all with a different port 
# to be used for their gRPC server

# Clear the RESTART environment variable if it's been set
unset RESTART

# First grab the port number argument or set it to the default value if no argument was given
if [ -z "$1" ]
then 
	export ORDER_PORT=50054
else
	export ORDER_PORT=$1
fi
# then the IP address for the order service
if [ -z "$2" ]
then 
	export ORDER_HOST=127.0.0.1
else
	export ORDER_HOST=$2
fi
# and finally the IP address for the catalog service
if [ -z "$3" ]
then 
	export CATALOG_HOST=127.0.0.1
else
	export CATALOG_HOST=$3
fi

# spin up 3 replicas, each with a different port number
for i in {0..2}
do
	echo "Starting order service replica #$i: $ORDER_HOST:$ORDER_PORT"
	python3 order_service.py &
	export ORDER_PORT=$(($ORDER_PORT+1))
done
