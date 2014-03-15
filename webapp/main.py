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
#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='web.log',filemode='w')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        item = ["item1","item2","item3"]
        self.render("main.html",title="集市自动化管理",item=item)

    def post(self):
        if runshcommand("sh clurterinit.sh") == None:   
            self.set_header("Content-Type","application/text")
            self.write("error")     
        else:
            self.set_header("Content-Type","application/text")
            self.write("success")
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

#setting for application
settings = {
    "ui_modules":uimodules,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

#luyou yinshe
application = tornado.web.Application([
    (r"/",MainHandler),
    (r"/\?.+",MainHandler),
    (r"/hosts",hostsHandler),
    (r"/hosts/(.+)",hostsloadHandler),
    (r"/configure",configureHandler),
    (r'/configure/(.+)',configuresHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
