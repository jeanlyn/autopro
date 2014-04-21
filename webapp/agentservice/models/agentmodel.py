import os
import sys
import pickle
from tool.log import *
logger=getlog('agentmodel','agentmodel.log')
class serverModel():
    def __init__(self):
        self.path='webserver.txt'
        self.tokenpath='token.txt'
        self.clusterpath='clustername.txt'
        self.portpath='agentserverport.txt'
    #get the server address
    def getserver(self):
        if os.path.isfile(self.path):
            with open(self.path,'r') as f:
                return f.read().strip()
        else:
            return ''
    #set the server address
    def setserver(self,serveraddress):
        with open(self.path,'w') as f:
            f.write(serveraddress)

    def gettoken(self):
        if os.path.isfile(self.tokenpath):
            with open(self.tokenpath,'r') as f:
                return f.read().strip
        else:
            return ''
    def settoken(self,token):
        with open(self.tokenpath,'w') as f:
            f.write(token)

    #the address of update dir
    def getupdatead(self):
        return self.getserver()+'/static/agentservice.tar.gz'

    def getclustername(self):
        if os.path.isfile(self.clusterpath):
            with open(self.clusterpath,'r') as f:
                return f.read().strip()
        return ''

    def setclustername(self,name):
        with open(self.clusterpath,'w') as f:
            f.write(name)

    def getuploaddir(self):
        return self.getserver()+'/static/'

    def isnotexist(self):
        return not os.path.isfile(self.path)

    #get and set the agentserver port
    def getport(self):
        if os.path.isfile(self.portpath):
            with open(self.portpath) as f:
                return f.read().strip()
        else:
            return ''
    def setport(self,port):
        with open(self.portpath,'w') as f:
            f.write(port)



#the model used when install
class installModel():
    def __init__(self,clustername):
        self.path='cluster/'+clustername
        self.clustername=clustername

    def getinstall(self):
        if os.path.isdir(self.path):
            if os.path.isfile(self.path+'/chooseinstall'):
                with open(self.path+'/chooseinstall') as f:
                    install=pickle.load(f)
                    try:
                        install.remove(install[-1])
                        if install[0]=='bashrc':
                            install[0]='.bashrc'
                    except Exception, e:
                        logger.error(e)                    
                return install
            else:
                return None
        else:
            return None

    def getpropath(self):
        project=self.getinstall()
        if project is not None:
            return [ '/'.join(['cluster',self.clustername,x]) for x in project ]

    def gethosts(self):
        if os.path.isdir(self.path):
            if os.path.isfile(self.path+'/hosts'):
                with open(self.path+'/hosts') as f:
                    hosts=[x.split('\t') for x in f.read().split('\n')]
                return hosts
            else:
                return hosts
        else:
            return None

#the class for get or set the username to ssh 
class sshuserModel():
    def __init__(self):
        self.path="sshuser.txt"
    def getusername(self):
        if os.path.isfile(self.path):
            with open(self.path,'r') as f:
                return f.read().strip()
        return '-1'

    def setusername(self,username):
        with open(self.path,'w') as f:
            f.write(username)

