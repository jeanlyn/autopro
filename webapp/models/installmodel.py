#encoding=UTF-8
import pickle
import sys
import os
#from tool.log import *
from tool.log import *
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
            