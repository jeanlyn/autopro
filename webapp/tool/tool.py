#encoding=UTF-8
import os
import re
import commands
import logging
#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='web.log',filemode='w')

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
