#encoding=UTF-8
import tornado.ioloop
import tornado.web
import os
import uimodules
import sys
from tool.hconf import HadoopConf
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        item = ["item1","item2","item3"]
        self.render("main.html",title="集市自动化管理",item=item)

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
    (r"/", MainHandler),
    (r"/configure",configureHandler),
    (r'/configure/(.+)',configuresHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
