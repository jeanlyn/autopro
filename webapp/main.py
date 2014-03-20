#encoding=UTF-8
import tornado.ioloop
import tornado.web
import os
import uimodules
import sys
from tool.hconf import HadoopConf
from tool.tool import *
import json
import logging
import pickle
#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='web.log',filemode='w')

#step 1:init the install
#add the tmp director 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        item = ["item1","item2","item3"]
        self.render("main.html",title="集市自动化管理",item=item)

    def post(self):
        try:
            if runshcommand("sh clurterinit.sh") == None:
                #the relative path/conf dir of the machines
                self.set_header("Content-Type","application/text")
                self.write("error")     
            else:
                paths={'ubuntu-64-bit':{'hadoop-2.2.0':'../hadoop-2.2.0,tmp/hadoop-2.2.0,tmp/hadoop-2.2.0/etc/hadoop'}}
                with open('tmp/paths','w') as f:
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
            data=json.loads(self.request.body)
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
#step 2: add host                
class hostsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            self.render("hosts.html",title="添加hosts")
        except Exception, e:
            logging.error(e)
        
    def post(self):
        pass

#step 2:load data by ajax
class hostsloadHandler(tornado.web.RequestHandler):
    """
       handle the data by ajax
    """
    def get(self,paramer):
        try:
            hosts=readhosts()
            self.set_header("Content-Type","application/json")
            self.write(json.dumps(hosts))

        except Exception, e:
            print(e)
            logging.error(e)
            self.set_header("Content-Type","application/text")
            self.write("error")

    def post(self,paramer):
        action=paramer.split('?')[0]
        path='tmp/hosts'
        try:
            if action == 'save':
                data=json.loads(self.request.body)
                string='\n'.join(['\t'.join(x.values()) for x in data])
                with open(path,'w') as f:
                    f.write(string)
                self.set_header('Content-Type','application/text')
                self.write("success")
            else :
                if self.request.files.get('uploadfile',None):
                    uploadfile=self.request.files['uploadfile'][0]
                    with open(path,'w') as f:
                        f.write(uploadfile['body'])
                self.redirect('/hosts')
        except Exception, e:
            logging.error(e)
            self.set_header('Content-Type','application/text')
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
        machines=[{"machine":"ubuntu-64-bit","id":1}]
        self.render("chooseinstall.html",machines=machines)

#step 4:load data by ajax
class ChooseAjaxInstall(tornado.web.RequestHandler):
    def get(self,paramer):
        projects=[["hadoop-2.2.0","hadoop-cdh4"],["hive-0.8","hive-0.12"]]
        self.set_header("Content-Type","application/json")
        self.write(json.dumps(projects))

    def post(self,paramer):
        data=json.loads(self.request.body)
        path='tmp/chooseinstall'
        packegpath='tmp/paths'
        self.set_header('Content-Type','application/text')
        try:
            with open(path,'w') as f:
                pickle.dump(data,f)
            with open(packegpath,'r') as f:
                pathsofpack=pickle.load(f)
            if packegpath is not None:
                for x in data[0:-1]:
                    cpfromto=pathsofpack[data[-1]][x].split(',')
                    runshcommand('cp -r '+cpfromto[0]+' '+'tmp/')
            self.write('success')
        except Exception, e:
            logging.error(e)
            self.write('error')

#step 5:custom configure 
class CustomConfigure(tornado.web.RequestHandler):
    def get(self):
        try:
            choosepath='tmp/chooseinstall'
            packegpath='tmp/paths'
            showpath=[]
            #read the install project
            with open(choosepath,'r') as f:
                chooseinstall=pickle.load(f)
            with open(packegpath,'r') as f:
                packetsp=pickle.load(f)
            for x in chooseinstall[0:-1]:
                confdir=packetsp[chooseinstall[-1]][x].split(',')[-1]
                confxml=[ i for i in os.listdir(confdir) if i.split('.')[-1] == 'xml']
                showpath.append({'projectname':x,'projectdir':confxml})

        except Exception, e:
            logging.error(e)        
        self.render('CustomConfigure.html',items=showpath)

#step 5:custom configure handle the data by ajax
class CustomConfigureAjax(tornado.web.RequestHandler):
    """handle the data by ajax"""
    def get(self,project,filename):
        try:
            self.set_header('Content-Type','application/json')
            choosepath='tmp/chooseinstall'
            packegpath='tmp/paths'
            showpath=[]
            #read the install project
            with open(choosepath,'r') as f:
                chooseinstall=pickle.load(f)
            with open(packegpath,'r') as f:
                packetsp=pickle.load(f)
            confpath=packetsp[chooseinstall[-1]][project].split(',')[-1]+'/'+filename
            con=HadoopConf(confpath)
            dt=con.get()
            self.write(json.dumps(dt))
        except Exception ,e:
            logging.error(e)
    def post(self,project,filename):
        try:
            self.set_header('Content-Type','application/json')
            choosepath='tmp/chooseinstall'
            packegpath='tmp/paths'
            showpath=[]
            #read the install project
            with open(choosepath,'r') as f:
                chooseinstall=pickle.load(f)
            with open(packegpath,'r') as f:
                packetsp=pickle.load(f)
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
                data=json.loads(self.request.body)
                con=HadoopConf(confpath)
                con.setdt2(data) 
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

class StartInstallAjax(tornado.web.RequestHandler):
    def get(self):
        pass
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
            self.set_header("Content-Type","application/json")
            self.write("success")

        except Exception ,e:
            logging.error(e)

class test(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")
        self.write("hello")
#setting for application
settings = {
    "ui_modules":uimodules,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

#routing
application = tornado.web.Application([
    (r"/",MainHandler),    
    (r"/\?.+",MainHandler),
    (r"/clusterunp.*",addClusterUsername),
    (r"/hosts",hostsHandler),
    (r"/hosts/(.+)",hostsloadHandler),
    (r"/configure",configureHandler),
    (r'/configure/(.+)',configuresHandler),
    (r"/ChooseInstall",ChooseInstallHandle),
    (r"/ChooseInstall/(.+)",ChooseAjaxInstall),
    (r"/CustomConfigure",CustomConfigure),
    (r"/CustomConfigure/([^/]+)/(.+)",CustomConfigureAjax),
    (r"/StartInstall",StartInstallHandle),
    (r"/StartInstall/.+",StartInstallAjax),
    (r'/test',test),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
