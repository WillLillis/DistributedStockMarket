#!/bin/bash

# Help from: https://stackoverflow.com/questions/3855127/find-and-kill-process-locking-port-3000-on-mac
if [[ $# -eq 0 ]]
then
	echo "Error! Usage: ./clean_by_port.sh <port_1> <port_2> ... <port_n>"
	exit 0
fi

for port in "$@"
do
	pid=$(lsof -i tcp:$port | grep LISTEN | awk '{ print $2 }')
	if [[ ! -z "$pid" ]]
	then
		#echo -n "Killing process with pid $pid..."
		/bin/echo -n "$port: Killing process with pid $pid..." # have to do this for the -n option to work on macOS
		kill $pid
		if [ "$?" -eq 0 ]
		then
			echo "Success"
		else
			echo "Failed! ($?)"
		fi
	else
		echo "No process found listening on $port"
	fi
done