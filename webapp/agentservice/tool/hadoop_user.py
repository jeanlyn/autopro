#encoding=UTF-8
import os
import re
import commands
import logging
from hconf import HadoopConf as HC
#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='web.log',filemode='w')
#返回数值说明[1:成功添加用户，-1用户目录已经存在，-2用户已经存在,-3：传入参数有误]
def adduser(username):
    if username == '':
        return -3
    cmdmkdir='hdfs dfs -mkdir /user/'+username
    cmdchown='hdfs dfs -chown '+username+' /user/'+username
    #user目录不存再
    if checkuserdir() != 1:
        return -1
    #用户已经存在
    elif checkuserisexist(username) != 1:
        return -2
    else:
        logging.info(cmdmkdir)
        statumk,resultr=commands.getstatusoutput(cmdmkdir)
        logging.info(cmdchown)
        statucm,resultn=commands.getstatusoutput(cmdchown)
        if statumk+statucm != 0:
            logging.error(reslutr+'\n'+resultn)
        elif addusertopolicy(username) == 1:
            return 1
        #在policy里面增加用户失败，需要把创建的目录删除
        else:
            cmd='hdfs dfs -rm -r /user/'+username
            statu,result=commands.getstatusoutput(cmd)
            if statu != 0:
                logging.erro('there is some error happen while remove the user home:'+result)

#返回值为数字,[1：检验成功，-1:user目录不存再，-2：命令有错]
def checkuserdir():
    com='hdfs dfs -ls /'
    statu,result=commands.getstatusoutput(com)
    if statu == 0:
        #把输出的结果弄成字符串数组
        results=[re.split(r'[ ]+',x) for x in result.strip().split('\n')]
        #获取hdfs根目录的文件夹
        rfloder=[t[-1] for t in results if t[-1][0]=='/']
        #判断user文件夹是够存在
        if "/user" not in rfloder:
            logging.error("the user's floder do not esists!")
            return -1
        else:
            return 1
    else:
        logging.error("the command run fail!"+result)
        return -2

def checkuserisexist(username):
    com='hdfs dfs -ls /user'
    statu,result=commands.getstatusoutput(com)
    if statu == 0:
        results=[re.split(r'[ ]+',x) for x in result.strip().split('\n')]
        #获取用户
        users=[t[-1].split('/')[-1] for t in results if t[-1][0]=='/']
        if username in users:
            logging.error("can'not add the user!the user is exists!")
            return -1
        else:
            return 1
    else:
        logging.error("the command run fail!"+result)
        return -2

def listuser():
    com='hdfs dfs -ls /user'
    statu,result=commands.getstatusoutput(com)
    if statu == 0:
        results=[re.split(r'[ ]+',x) for x in result.strip().split('\n')]
        #获取用户
        users=[t[-1].split('/')[-1] for t in results if t[-1][0]=='/']
        return users
    else:
        logging.error("the command run fail!"+result)

#SIMPLE模式 在hadoop-policy.xml 里面添加用户
#配置里面的字符串是user1，user2 group1，group2形式
def addusertopolicy(username):
    hadoopconfdir=os.environ['HADOOP_CONF_DIR']
    conf=HC(hadoopconfdir+'hadoop-policy.xml')
    dt=conf.get()
    aclname='security.client.protocol.acl'
    try:
        aclusers=dt.get(aclname,{"value":None})['value']
        if aclusers is not None and aclusers != '*':
            acluandg=aclusers.split(' ')
            if len(acluandg) == 2:
                if acluandg[0] not in ['','*']:
                    if username not in acluandg[0].split(','):
                        acluandg[0]=acluandg[0]+','+username
                else:
                    acluandg[0]=username
                aclusers=' '.join(acluandg)
            else:
                if username not in aclusers.split(','):
                    aclusers=aclusers+','+username
            dt[aclname]={"value":aclusers,"description":""}
        else:
            dt[aclname]={"value":aclusers,"description":""}
        conf.setdt(dt)
        #下面是格式化xml
        #com='sh format.sh '+hadoopconfdir+'hadoop-policy.xml'
        #statu,result=commands.getstatusoutput(com)
        #if statu != 0:
        #    logging.error('there is some error happen to format xml'+result)
        #    return -2
        #else:
        #    logging.info('format hadoop-policy.xml succeed')

        #使yarn更新servicer acl
        com='hadoop dfsadmin -refreshServiceAcl'
        statu,result=commands.getstatusoutput(com)
        if statu != 0:
            logging.error('refresh servoveacl fail!')
        return 1
    except Exception, e:
        return -3
    
    
