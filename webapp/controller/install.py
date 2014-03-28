#encoding=UTF-8
#step 1:init the install
#add the tmp director 
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

logging=getlog('install','install.log')

class Login(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            item = ["item1","item2","item3"]
            self.render("main.html",title="集市自动化管理",item=item)
        except Exception ,e:
            logging.error(e)

    def post(self):
        try:
            if runshcommand("sh clurterinit.sh") == None:
                #the relative path/conf dir of the machines
                self.set_header("Content-Type","application/text")
                self.write("error")     
            else:
                paths={'ubuntu-64-bit':{'hadoop-2.2.0':'../../repo/hadoop-2.2.0,../tmp/hadoop-2.2.0,../tmp/hadoop-2.2.0/etc/hadoop'}}
                with open('../tmp/paths','w') as f:
                    pickle.dump(paths,f)
                self.set_header("Content-Type","application/text")
                self.write("success")
        except Exception ,e:
            logging.error(e)
            #redirect

class configureHandler(tornado.web.RequestHandler):
    """the configure html"""
    def get(self):
        item = os.listdir(os.path.abspath(os.curdir)+'/static/configure')
        self.render("configure.html",title="集市自动化管理",items=item)

class configuresHandler(tornado.web.RequestHandler):
    """find the contend in the """
    def get(self,filename):
        self.set_header("Content-Type", "application/json")
        paths='static/configure/'+filename
        con=HadoopConf(paths)
        dt=con.get()
        self.write(json.dumps(dt))
    def post(self,filename):
        try:
            paths='static/configure/'+filename.split('?')[0]
            con=HadoopConf(paths)
            con.setdt2(data) 
            self.set_header("Content-Type","application/text")
            self.set_status(201)
            self.write("保存成功!")
        except Exception, e:
            logging.error(e)
            self.set_header("Content-Type","application/text")
            self.set_status(201)
            self.write(e)

#create cluster
class createcluster(tornado.web.RequestHandler):
    def get(self):
        self.render("ctcluster.html")
    def post(self):
        try:
            self.set_header('Content-Type','application/text')
            #data=json.loads(self.request.body)
            clustername=str(self.get_argument("clustername","")).strip()
            clusteradress=str(self.get_argument("address","")).strip()
            clusters=cluster()
            if clustername == "" or clusteradress == "":
                self.write("输入不能为空值")        
            elif clusters.incluster(clustername):
                self.write('集群已经存在!')
            else:   
                clusters.addcluster(clustername,clusteradress)
                self.set_secure_cookie("crtcluster",clustername)
                if runshcommand("sh clurterinit.sh "+clustername) is not None:
                    self.write('添加成功!')
                    logging.info('add success')
                else:
                    self.write("添加出错!")
        except Exception, e:
            self.set_header('Content-Type','application/text')
            self.write('添加出错!')
            logging.error(e)

#step 2: add host                
class hostsHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie("crtcluster") is None:
            self.render("error.html",erroinfo="你还没有创建集群!",dirhref="/")
        else:
            self.render("hosts.html",title="添加hosts")
       
    def post(self):
        pass

#step 2:load data by ajax
class hostsloadHandler(tornado.web.RequestHandler):
    """
       handle the data by ajax
    """
    def get(self,paramer):
        try:
            hostsm=hostsmodel(self.get_secure_cookie("crtcluster"))
            hosts=hostsm.hosts
            self.set_header("Content-Type","application/json")
            self.write(json.dumps(hosts))

        except Exception, e:
            logging.error(e)
            self.set_header("Content-Type","application/text")
            self.write("error")

    def post(self,paramer):
        action=paramer.split('?')[0]
        self.set_header('Content-Type','application/text')
        if self.get_secure_cookie("crtcluster") is None:
            self.write("你还没有创建集群!")
            return
        hostm=hostsmodel(self.get_secure_cookie("crtcluster"))
        try:
            if action == 'save':
                data=json.loads(self.request.body)
                string='\n'.join(['\t'.join(x.values()) for x in data])
                hostm.save(string)
                
                self.write("success")
            else :
                if self.request.files.get('uploadfile',None):
                    uploadfile=self.request.files['uploadfile'][0]
                    hostm.save(uploadfile['body'])
                self.redirect('/hosts')
        except Exception, e:
            logging.error(e)
            self.write("error")        

#step 3:add cluster username and password
class addClusterUsername(tornado.web.RequestHandler):
    """docstring for addClusterUsername"""
    def get(self):
        try:
            path='tmp/unp'
            username=''
            password=''            
            with open(path,'r') as f:
                a=f.readline()
                if a != "":
                    a=a.strip().split('\t')                    
                    username=a[0]
                    password=a[1]
            self.render("clusterunp.html", title="添加用户以及用户名", user=username, password=password)
        except Exception, e:
            print e
            logging.error(e)

    def post(self):
        try:
            path='tmp/unp'
            username=self.get_argument("username",None)
            password=self.get_argument("password",None)
            print username
            if username and password:
                with open(path,'w') as f:
                    f.write(username+'\t'+password)
                self.redirect('/ChooseInstall')

        except Exception, e:
            logging.error(e)
            set_header('Content-Type','application/javascript')
            self.write("<script>alert('出错了!')</script>")

#step 4:choose the version of hadoop or the child level project of hadoop such as  to install
class ChooseInstallHandle(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie("crtcluster") is None:
            self.render("error.html",erroinfo="你还没有创建集群!",dirhref="/")
        else:
            machinesm=machinemodel(self.get_secure_cookie("crtcluster"))        
            self.render("chooseinstall.html",machines=machinesm.machines)

#step 4:load save data by ajax
class ChooseAjaxInstall(tornado.web.RequestHandler):
    def get(self,paramer):
        projectm=projectmodel(self.get_secure_cookie("crtcluster"))
        self.set_header("Content-Type","application/json")
        self.write(json.dumps(projectm.projects))

    def post(self,paramer):
        data=json.loads(self.request.body)
        #add the bash conf file
        data=['bashrc']+data
        installpm=installpmodel(self.get_secure_cookie("crtcluster"))
        self.set_header('Content-Type','application/text')
        try:
            #save data to promodel
            installpm.save(data)
            packagem=packagepathmodel(self.get_secure_cookie("crtcluster"))
            pathsofpack=packagem.packagepath
            for x in data[0:-1]:
                cpfromto=pathsofpack[data[-1]][x].split(',')
                runshcommand('cp -r '+cpfromto[0]+' '+'cluster/'+self.get_secure_cookie("crtcluster"))
            self.write('success')
        except Exception, e:
            logging.error(e)
            self.write('error')

#step 5:custom configure 
class CustomConfigure(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie("crtcluster") is None:
            self.render("error.html",erroinfo="你还没有创建集群!",dirhref="/")
        try:
            installm=installpmodel(self.get_secure_cookie("crtcluster"))
            packegpathm=packagepathmodel(self.get_secure_cookie("crtcluster"))
            showpath=[]
            #read the install project            
            chooseinstall=installm.installproject
            packetsp=packegpathm.packagepath
            for x in chooseinstall[0:-1]:
                confdir=packetsp[chooseinstall[-1]][x].split(',')[-1]
                if x !='bashrc':
                    confxml=[ i for i in os.listdir(confdir) if i.split('.')[-1] == 'xml']
                    showpath.append({'projectname':x,'projectdir':confxml})
                #handle the conf file
                else:
                    showpath.append({'projectname':x,'projectdir':['.bashrc']})

        except Exception, e:
            logging.error(e)        
        self.render('CustomConfigure.html',items=showpath)

#step 5:custom configure handle the data by ajax
class CustomConfigureAjax(tornado.web.RequestHandler):
    """handle the data by ajax"""
    def get(self,project,filename):
        try:
            installm=installpmodel(self.get_secure_cookie("crtcluster"))
            packegpathm=packagepathmodel(self.get_secure_cookie("crtcluster"))
            chooseinstall=installm.installproject
            packetsp=packegpathm.packagepath
            if filename.split('.')[-1] == 'xml':
                self.set_header('Content-Type','application/json')
                showpath=[]
                #read the install project
                confpath=packetsp[chooseinstall[-1]][project].split(',')[-1]+'/'+filename
                con=HadoopConf(confpath)
                dt=con.get()
                self.write(json.dumps(dt))
            else:
                self.set_header('Content-Type','application/text')
                datapath=packetsp[chooseinstall[-1]][project].split(',')[-1]+'/'+filename
                with open(datapath,'r') as f:
                    self.write(f.read())

        except Exception ,e:
            logging.error(e)
    def post(self,project,filename):
        try:
            self.set_header('Content-Type','application/json')
            installm=installpmodel(self.get_secure_cookie("crtcluster"))
            packegpathm=packagepathmodel(self.get_secure_cookie("crtcluster"))
            showpath=[]
            #read the install project
            chooseinstall=installm.installproject
            packetsp=packegpathm.packagepath
            #upload file
            if filename =="uploadfile":                
                if self.request.files.get('uploadfile',None):
                    uploadpath=packetsp[chooseinstall[-1]][project].split(',')[-1]+'/'+self.request.files['uploadfile'][0]['filename']
                    uploadfile=self.request.files['uploadfile'][0]
                    with open(uploadpath,'w') as f:
                        f.write(uploadfile['body'])
                self.redirect('/CustomConfigure')
            #save the xml file
            else:    
                confpath=packetsp[chooseinstall[-1]][project].split(',')[-1]+'/'+filename.split('?')[0]
                if filename.split('?')[0].split('.')[-1] == 'xml':
                    data=json.loads(self.request.body)
                    con=HadoopConf(confpath)
                    con.setdt2(data) 
                else:
                    with open(confpath,'w') as f:
                        f.write(self.request.body)
                self.set_header("Content-Type","application/text")
                self.set_status(201)
                self.write("保存成功!")
        except Exception ,e:
            logging.error(e)
            self.set_header("Content-Type","application/text")
            self.set_status(500)
            self.write(e)

#step 6:start install
class StartInstallHandle(tornado.web.RequestHandler):
    def get(self):
        self.render("StartInstall.html")
    def post(self):
        try:
            choosepath='tmp/chooseinstall'
            packegpath='tmp/paths'
            hostspath='tmp/hosts'
            unppath='tmp/unp'
            zipdir='tmp/project.tar.gz '
            zipproject='project.tar.gz'
            totals=0
            finish=0
            #read the install project
            with open(choosepath,'r') as f:
                chooseinstall=pickle.load(f)

            with open(packegpath,'r') as f:
                packetsp=pickle.load(f)

            with open(hostspath,'r') as f:
                hosts= [i.split('\t') for i in f.read().split('\n')]

            with open(unppath,'r') as f:
                unp=f.read().strip('\n').split('\t')

            #tar scp ssh untar
            totals= len(hosts)*2+1
            prodir = [packetsp[chooseinstall[-1]][x].split(',')[1] for x in chooseinstall[0:-1]]
            cmds='tar -zcf '+ zipdir+' '.join(prodir)+' '+'tmp/confclientpath.sh'
            clientrun='sh confclientpath.sh '+' '.join(chooseinstall[0:-1])
            if runshcommand(cmds) is not None:
                logging.info('tar the project success')
                finish+=1
                runshcommand('echo '+str(finish/totals*100)+' >done')

            #scp and ssh untar and stepup the project
            for x in hosts:
                cmds='scp '+zipdir+unp[0]+'@'+x[0]+':~/ 2>>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                cmds='ssh '+unp[0]+'@'+x[0]+' "tar -zxvf '+ zipproject +' && '+clientrun+'" 2>>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                logging.info(x[0]+" has finish install the project")

        except Exception ,e:
            logging.error(e)

#step 6:start install by ajax
class StartInstallAjax(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type","application/text")
        try:            
            with open("done",'r') as f:
                data=f.read().strip()
                self.write(data)

        except Exception ,e:
            logging(e)
            self.write("0")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header("Content-Type","application/text")
        try:
            clien=tornado.httpclient.AsyncHTTPClient()
            response= yield tornado.gen.Task(clien.fetch,"http://localhost:8887/Install")
            self.write("install "+response.body)
            self.finish()
        
        except Exception ,e:
            self.write("install error")

#upload project file
class uplprojectjar(tornado.web.RequestHandler):
    def get(self,projectname):
        if self.get_secure_cookie("crtcluster") is None:
            self.render("error.html",erroinfo="你还没有创建集群!",dirhref="/")
        else:
            route=projectname.split('/')
            if route[-1]=='loaddata':
                self.set_header('Content-Type','application/json')
                route.remove(route[-1])
                #get the projectname
                project=route[0]
                route.remove(route[0])
                dirpath='/'.join(route)
                #get the project which choose istall
                installpm=installpmodel(self.get_secure_cookie('crtcluster'))
                packegpathm=packagepathmodel(self.get_secure_cookie('crtcluster'))
                localpath=packegpathm.packagepath[installpm.installproject[-1]][project].split(',')[1]
                contend=os.walk(localpath+dirpath).next()
                #construct of dir:[ispath,pathname,pathhref]
                self.write(json.dumps([[True,x,'/'.join(['/uldprojectjar',project,dirpath,x])] for x in contend[1] ]+[[False,i] for i in contend[2]]))
            else:
                self.render("uplprojectjar.html",projectname=projectname,projecthref=projectname.split('/'))
            #installpm=installpmodel(self.get_secure_cookie("crtcluster"))

    def post(self,projectname):
        pass

class loadfiles(tornado.web.RequestHandler):
    def get(self,projectname):
        pass
    def post(self,projectname):
        pass