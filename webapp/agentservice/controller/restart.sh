#!/usr/bin/env sh 
if [ $# -ne 1 ]; then
    echo "you must put one argument">&2
    exit 1
fi
kill `netstat -anp|grep 8080|head -n1|awk '{split($7,array,"/");print array[1]}'`
python agentservicer.py -n $1