#!/usr/bin/env bash
if [ $# -ne 1 ]; then
    echo "must has one argument!" 1>&2
    exit 1
fi
dir="cluster/$1"
if [ -d $dir ]; then
    rm -rf $dir
fi
mkdir -p $dir
touch $dir/hosts
#if [ -d tmp ] ; then
#    rm -rf tmp
#fi
#mkdir -p tmp
#touch tmp/hosts
#touch tmp/manage
#touch tmp/unp
#touch tmp/chooseinstall
#cp confclientpath.sh tmp/confclientpath.sh