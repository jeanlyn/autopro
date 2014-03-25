#!/usr/bin/env bash
if [ ! -d tornado-3.1.0 ];then
	echo "ERROR:have not the tornado package"
	exit 1
fi

if [ -z `which python` ];then
	echo "ERROR:hava not install python!"
fi
cd tornado-3.1.0
python setup.py build
sudo python setup.py install
