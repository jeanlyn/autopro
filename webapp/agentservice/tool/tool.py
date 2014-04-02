#encoding=UTF-8
import os
import re
import commands

from log import *
logging=getlog('tool','tool.log')
#日志配置
def runshcommand(cmd):
    status,result=commands.getstatusoutput(cmd)
    if status !=0 :
        logging.error("there is someting wrong:"+result)
        return None
    else:
        return result.split('\n')

def readhosts():
    path='tmp/hosts'
    hosts={}
    hostf=[]
    with open(path,"r") as f:
        hostf=runshcommand("cat "+path)
    return [x.split('\t') for x in hostf]
