#!/usr/bin/env sh 
usage(){
    echo ""
}
if [ $# -lt 2 ]; then
    echo "you must put two argument">&2
    exit 1
fi
kill `netstat -anp|grep 8080|head -n1|awk '{split($7,array,"/");print array[1]}'`
kill `netstat -anp|grep 8079|head -n1|awk '{split($7,array,"/");print array[1]}'`
python agentservicer.py -n $1 -u $2 &
python asynchandle.py &
