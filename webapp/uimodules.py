#encoding=UTF-8
import tornado.ioloop
import tornado.web
import os

class header(tornado.web.UIModule):
    """docstring for Header"""
    def render(self):
        return self.render_string(
            "header.html",title="集市自动化")

class footer(tornado.web.UIModule):
    """docstring for footer"""
    def render(self):
        return self.render_string(
            "footer.html")

class nav(tornado.web.UIModule):
    """docstring for footer"""
    def render(self,active=1):
        return self.render_string(
            "nav.html",active=active)