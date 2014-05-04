#!/usr/bin/env bash
#
#

function print_usage(){
    echo "sh firststart.sh COMMAND"
    echo "where COMMAND is:"
    echo "-w|--webserver         the http address of webserver.default:http:0.0.0.0:8888"
    echo "-n|--cluster           the name of cluster"
    echo "-p|--port              the port of agent.default:8080"
    echo "-u|--username          the username for ssh"
}


if [ $# -lt 4 ]; then
    echo "you must input at least four arguments"
    exit 1
fi

rm agentserverport.txt clustername.txt sshuser.txt token.txt webserver.txt 2>/dev/null

cmd='python agentservicer.py'
while [ $# -gt 0 ]; do
    case $1 in
        -w|--webserver|-n|--cluster|-p|--port|-u|--username )
            cmd=${cmd}' '${1}
            shift
            if [ -z $1 ];then
                echo "input error!"
                exit 1
            fi
            cmd=${cmd}' '${1}
            shift
            ;;
        * )
            print_usage
            exit 1
        ;;
    esac
done

#echo $cmd
${cmd} &
python agentservicer.py &