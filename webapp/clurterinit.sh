#!/usr/bin/env bash
if [ -d tmp ] ; then
    rm -rf tmp
fi
mkdir -p tmp
touch tmp/hosts
touch tmp/manage
touch tmp/unp
touch tmp/chooseinstall
cp confclientpath.sh tmp/confclientpath.sh