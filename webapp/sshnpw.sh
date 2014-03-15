#!/usr/bin/env bash
NODE_LIST=tmp/hosts
MANAGE_LIST=tmp/manage
[ ! -d ~/.ssh] && ( mkdir ~/.ssh ) 
yes|ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

if [ ! -f $NODE_LIST ];then
    echo "ERROR: Can't not found the $NODE_LIST"
    exit 1
fi

HOST_NAME=`awk '{print $2}' $NODE_LIST`
MANAGE_NAME=`cat $MANAGE_LIST`
