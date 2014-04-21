#!/usr/bin/env sh 
usage(){
    echo ""
}

port=`head -n 1 agentserverport.txt 2>/dev/null`
webserver=`head -n 1 webserver.txt 2>/dev/null`
clustername=`head -n 1 clustername.txt 2>/dev/null`
if [ -z $webserver ]; then
    if [ $# -lt 2 ]; then
        echo "you must put at least two argument -n and -u to figure out the clustername and the username of the cluster">&2
        exit 1
    fi
fi
cmd="python agentservicer.py "$@

pid=`netstat -anp|grep ${port}|head -n1|awk '{split($7,array,"/");print array[1]}' 2>/dev/null`
pid2=`netstat -anp|grep 8079|head -n1|awk '{split($7,array,"/");print array[1]}' 2>/dev/null`
kill $pid
kill $pid2


${cmd} &
python asynchandle.py &
