#!/usr/bin/env sh
if [ $# -lt 1 ]; then
    echo "you must put at lease one argument!" >&2
    exit 1
fi
rm project.tar.gz
cat cluster/${1}/.bashrc >> ~/.bashrc
source ~/.bashrc
cp -r -f cluster/${1}/* ~/
