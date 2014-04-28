#encoding=UTF-8
import os
import uimodules
import sys
from tool.hconf import HadoopConf
from tool.tool import *
from controller.install import *
from controller.agent import *
from controller.manage import *
import json
import pickle

#setting for application
settings = {
    "ui_modules":uimodules,
    "template_path":os.path.join(os.path.dirname(__file__),"view"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

#routing
application = tornado.web.Application([
    (r"/",MainHandler),    
    (r"/\?.+",MainHandler),#install
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
    (r"/StartInstall/(.+)",StartInstallAjax),
    (r"/CreateCluster.*",createcluster),
    (r"/login",Login),
    (r"/uldprojectjar/(.+)",uplprojectjar),
    (r"/updateagent",updateagent),
    (r"/regitcluster",registercluster),
    (r"/choosecluster/?(.*)",choosecluster),#install end
    (r"/manage",manage),
    (r"/overview/?(.*)",overview),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
