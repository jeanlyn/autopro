#encoding=UTF-8
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.gen
import sys
import pickle
import json
import time
from tool.tool import *
from tool.log import *

from models.agentmodel import *

logging=getlog('agentlog','agent.log')

class updataHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/text')
        sm=serverModel()
        upad=sm.getupdatead()
        try:
            #1.wget
            if os.path.isfile('agentservice.tar.gz'):
                runshcommand('rm agentservice.tar.gz')
            runshcommand("wget "+upad)
            #2.tar
            runshcommand("tar -zxvf agentservice.tar.gz && cp -r -f agentservice/* ./ && rm -r agentservice")
            self.write("ok")
        except Exception, e:
            logging.error(e)
            self.write("error")

#download the install package
class upload(tornado.web.RequestHandler):
    def get(self,projectname):
        uploadad=serverModel().getuploaddir()+projectname
        sm=serverModel()
        filename=sm.getclustername()+'.tar.gz'
        if os.path.isfile(filename):
            runshcommand('rm '+filename)
        self.set_header('Content-Type','application/text')
        try:
            runshcommand("wget "+uploadad)
            self.write('success')
            runshcommand('rm -r cluster/')
            runshcommand("tar zxf "+projectname)
            
        except Exception, e:
            logging.error(e)
            self.write('error')
        

class restart(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/text')
        sm=serverModel()
        self.write("success")
        self.finish()
        time.sleep(1)
        runshcommand("sh restart.sh "+sm.getclustername())

#install        
class installcluster(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header('Content-Type','application/text')
        clien=tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(clien.fetch,'http://127.0.0.1:8079/installcluster')
        self.write(response.body)
        self.finish()
#get the process of install
class getinstallstate(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type","application/text")
        try:
            if os.path.isfile("done"):            
                with open("done",'r') as f:
                    data=f.read().strip()
                    self.write(data)
            else:
                self.write("0")
        except Exception ,e:
            logging(e)
            self.write("0")