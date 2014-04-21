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

def list_project(clustername):
    prohref=projecthref()
    im=installpmodel(clustername)
    if im.installproject==[]:
        return []
    projects=im.installproject
    projects.remove(projects[-1])
    return [[prohref[x],x] for x in projects]

class manage(tornado.web.RequestHandler):
    def get(self):
        self.render('manage.html',project=list_project(self.get_secure_cookie("crtcluster")))