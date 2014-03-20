#!/usr/bin/env bash
if [ $# -lt 1 ];then
    echo "[Error]:need at least one arguments";
    exit 1
fi
#hadoop2.2.0 confi
hadoopconf()
{
    curdir=`pwd`
    hadoophome=${curdir}/${1}
    echo "export HADOOP_DEV_HOME=${hadoophome}
export PATH=$PATH:${hadoophome}/bin
export PATH=$PATH:${hadoophome}/sbin
export HADOOP_MAPARED_HOME=${hadoophome}
export HADOOP_COMMON_HOME=${hadoophome}
export HADOOP_HDFS_HOME=${hadoophome}
export YARN_HOME=${hadoophome}
export HADOOP_CONF_DIR=${hadoophome}/etc/hadoop
    ">>~/.bashrc
    source ~/.bashrc
}

while [ $# -ne 0 ]; do
    case $1 in
        hadoop* )
            hadoopconf $1
            ;;
        hive* )
        echo $1
            ;;
    esac
    shift
done

