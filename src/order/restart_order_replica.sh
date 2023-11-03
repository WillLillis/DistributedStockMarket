#!/bin/bash

# TODO: test/finish this

export RESTART= # RESTART needs to be set, but doesn't need a value

# First grab the port number argument or set it to the default value if no argument was given
if [ -z "$1" ]
then 
	export ORDER_PORT_1=50054
else
	export ORDER_PORT_1=$1
fi
# First grab the port number argument or set it to the default value if no argument was given
if [ -z "$2" ]
then 
	export ORDER_PORT_2=50055
else
	export ORDER_PORT_2=$2
fi
# First grab the port number argument or set it to the default value if no argument was given
if [ -z "$3" ]
then 
	export ORDER_PORT_3=50056
else
	export ORDER_PORT_3=$3
fi
# then the IP address for the order service
if [ -z "$4" ]
then 
	export ORDER_HOST=127.0.0.1
else
	export ORDER_HOST=$4
fi
# and finally the IP address for the catalog service
if [ -z "$5" ]
then 
	export CATALOG_HOST=127.0.0.1
else
	export CATALOG_HOST=$5
fi

echo "Restarting order service replica: $ORDER_HOST:$ORDER_PORT_1"
python3 order_service.py &