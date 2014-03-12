#encoding=UTF-8
import tornado.ioloop
import tornado.web
import os
import uimodules

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        item = ["item1","item2","item3"]
        self.render("main.html",title="集市自动化管理",item=item)

class configureHandler(tornado.web.RequestHandler):
    """the configure html"""
    def get(self):
        item = ["item1","item2","item3"]
        self.render("configure.html",title="集市自动化管理",item=item)
    
        
settings = {
    "ui_modules":uimodules,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/configure",configureHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
