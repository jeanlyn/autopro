#encoding=UTF-8

import os
import uimodules
import sys
from tool.hconf import HadoopConf
from tool.tool import *
from view import *
from controller.install import *
import json
import logging
import pickle


#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='web.log',filemode='w')

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
    (r"/StartInstall.+",StartInstallAjax),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
