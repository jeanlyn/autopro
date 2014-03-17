#!/usr/bin/sh
kill `netstat -anp|grep 8888|head -n1|awk '{split($7,array,"/");print array[1]}'`
