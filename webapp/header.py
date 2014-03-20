#encoding=UTF-8
import tornado.ioloop
import tornado.web
import os

class heaer(tornado.web.UIModule):
"""docstring for Header"""
    def render(self):
        return self.render_string(
            "heaer.html")

class footer(tornado.web.UIModule):
    """docstring for footer"""
    def render(self):
        return self.render_string(
            "footer.html")
        