#encoding=UTF-8
import pickle
import sys
import os
#from tool.log import *
from tool.log import *
from tool.tool import *
logger=getlog('installmodelog','installmodel.log')
class cluster():
    def __init__(self):
        self.datapath="models/data/cluster"
        if os.path.isfile(self.datapath):
            with open(self.datapath,"r") as f:
                self.clusters=pickle.load(f)
        else:
            self.clusters={}

    def incluster(self,clustername):
        return True if self.clusters.get(clustername,None) is not None else False

    def addcluster(self,clustername,url):
        if not self.incluster(clustername):
            self.clusters[clustername]=[url]
            try:
                with open(self.datapath,"w") as f:
                    pickle.dump(self.clusters,f)
            except Exception, e:
                logger.error(e)

    def modifyCluster(self,clustername,url):
        pass            

#handle the hosts file
class hostsmodel():
    def __init__(self,clustername):
        self.datapath="cluster/"+clustername+"/hosts"
        if os.path.isfile(self.datapath):
            with open(self.datapath,"r") as f:
                hoststring=runshcommand("cat "+self.datapath)
            if hoststring is not None:
                self.hosts=[x.split('\t') for x in hoststring]
        else:
            self.hosts=[]

    def save(self,data):
        with open(self.datapath,'w') as f:
            f.write(data)

class machinemodel():
    def __init__(self,clustername):
        self.machinepath="models/data/machines"        
        if os.path.isfile(self.machinepath):
            with open(self.machinepath,"r") as f:
                self.machines=pickle.load(f)
        else:
            self.machines=[{"machine":"ubuntu-64-bit"}]
       
class projectmodel():
    def __init__(self,clustername):
        self.projectpath="models/data/projects"
        if os.path.isfile(self.projectpath):
            with open(self.projectpath,"r") as f:
                self.projects=pickle.load(f)
        else:
            self.projects={"hadoop":["hadoop-2.2.0","hadoop-cdh4"],"hive":["hive-0.8","hive-0.12"]}

class installpmodel():
    def __init__(self,clustername):
        self.datapath="cluster/"+clustername+"/chooseinstall"
        if os.path.isfile(self.datapath):
            with open(self.datapath,"r") as f:
                self.installproject=pickle.load(f)
        else:
            self.installproject=[]
    def save(self,project):
        try:
            with open(self.datapath,"w") as f:
                pickle.dump(project,f)
        except Exception, e:
            logger.error(e)
    