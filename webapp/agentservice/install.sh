#!/usr/bin/env sh
rm *.txt
rm -rf cluster
if [ $# -lt 2 ]; then
    echo "you must put at least two argument: -n and -u to figure out the clustername and the username for ssh of the cluster"
    exit
fi
python agentservicer.py $@ &
python asynchandle.py &