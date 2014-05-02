#encoding=UTF-8
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.gen
import sys
import pickle
import json
from tool.hconf import HadoopConf
from tool.log import *
from tool.tool import *
from models.installmodel import *

logging=getlog('manage','manage.log')

#获取现在管理集群里面选择安装了的项目
def manage_list_project(clustername):
    #在model获取project的链接
    prohref=projecthref()

    im=installpmodel(clustername)
    if im.installproject==[]:
        return []
    projects=im.installproject
    projects.remove(projects[-1])
    return [[prohref[x],x] for x in projects]

#传入项目名字以及集群的名字,获取配置文件
def manage_get_conf_file(clustername,projectname):
    installm=installpmodel(clustername)
    packegpathm=packagepathmodel(clustername)
    packetsp=packegpathm.packagepath
    chooseinstall=installm.installproject
    confdir=packetsp[chooseinstall[-1]][projectname].split(',')[-1]
    #列出后缀不包含以下的文件
    excluded=['example','template']
    confdir=[ i for i in os.listdir(confdir) if i.split('.')[-1] not in excluded ]

    return {'projectname':projectname,'projectdir':confdir } 

#管理页面的默认页面的controller默认是选择hadoop
class manage(tornado.web.RequestHandler):
    def get(self):
        projects=manage_list_project(self.get_secure_cookie("crtcluster"))
        #获取hadoop选择安装的版本文字
        projectname=[ x[1] for x in projects if 'hadoop' in x[1] ][0]
 
        xmls=manage_get_conf_file(self.get_secure_cookie("crtcluster"),projectname)
        self.render('manage.html',project=projects,xmls=xmls)

class overview(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self,projectname):   
        if self.get_secure_cookie("crtcluster") is None:
            self.set_header("Content-Type","application/text")
            self.write("你应该先选择集群,再进行操作!")     
        
        else:
            #获取相应的路径信息
            installm=installpmodel(self.get_secure_cookie("crtcluster"))
            packegpathm=packagepathmodel(self.get_secure_cookie("crtcluster"))
            chooseinstall=installm.installproject
            packetsp=packegpathm.packagepath
            yarnpath=packetsp[chooseinstall[-1]][projectname].split(',')[-1]+'/yarn-site.xml'
            hdfspath=packetsp[chooseinstall[-1]][projectname].split(',')[-1]+'/hdfs-site.xml'
            clusterpath='cluster/'+self.get_secure_cookie("crtcluster")
            rtvalue={}
            resourcemanage="yarn.resourcemanager.address"
            nameservices="dfs.nameservices"
            defaultFS="fs.defaultFS"
            if os.path.isfile(yarnpath) and os.path.isfile(hdfspath):
                yarncon=HadoopConf(yarnpath)
                hdfscon=HadoopConf(hdfspath)
                yarndt=yarncon.get()
                hdfsdt=hdfscon.get()
                if hdfsdt.get(nameservices,None) is not None:
                    rtvalue['nameservices']=hdfsdt.get(nameservices)
                else:
                    rtvalue['nameservices']=HadoopConf(packetsp[chooseinstall[-1]][projectname].split(',')[-1]+'/core-site.xml').get().get(defaultFS)
                rtvalue['resourcemanager']=yarndt.get(resourcemanage,"")
                #列出安装失败的节点信息
                clien=tornado.httpclient.AsyncHTTPClient()
                clusterurl=cluster().getclusterurl(self.get_secure_cookie('crtcluster'))
                response=yield tornado.gen.Task(clien.fetch,clusterurl[0]+'/geterrorhost')
                errorhost=json.loads(response.body)
                if len(errorhost) != 0:
                    if os.path.isfile(clusterpath+"/hosts"):
                        cmd="grep -E '"+"|".join(errorhost)+"' "+clusterpath+"/hosts"
                        ips=runshcommand(cmd)
                        #format ips:["ip\thost",......]
                        if ips is not None:
                            rtvalue['hosts']=[[x.split('\t')[0],x.split('\t')[1]] for x in ips]
                    else:
                        rtvalue['hosts']=[]
                else:
                    rtvalue['hosts']=[]
                self.set_header('Content-Type','application/json')
                self.write(json.dumps(rtvalue))
                self.finish()
            else:
                self.set_header('Content-Type','application/text')
                logging.error("path error:"+yarnpath+","+hdfspath)
                self.write("error!")

#已安装的host
class installhost(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            #获取已安装host
            hostsm=hostsmodel(self.get_secure_cookie("crtcluster"))
            hosts=hostsm.hosts
            #获取失败host
            clien=tornado.httpclient.AsyncHTTPClient()
            clusterurl=cluster().getclusterurl(self.get_secure_cookie('crtcluster'))
            response=yield tornado.gen.Task(clien.fetch,clusterurl[0]+'/geterrorhost')
            errorhost=json.loads(response.body)
            #得到形式为[[ip,hosts,fasle]] 最后一个元素表示安装成功或者失败
            rtvalue=map(lambda x:x+[False] if x[0] in errorhost else x+[True],hosts)
            self.set_header("Content-Type","application/json")
            self.write(json.dumps(rtvalue))
            self.finish()

        except Exception, e:
            logging.error(e)
            self.set_header("Content-Type","application/text")
            self.write("error")

class geterrorinfo(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self,ip):
        if self.get_secure_cookie('crtcluster') is None:
            self.set_header("Content-Type","application/text")
            return
        clien=tornado.httpclient.AsyncHTTPClient()
        clusterurl=cluster().getclusterurl(self.get_secure_cookie('crtcluster'))
        response=yield tornado.gen.Task(clien.fetch,clusterurl[0]+'/geterrorinfo/'+ip)
        self.set_header("Content-Type","application/text")
        self.write(response.body)
        self.finish()