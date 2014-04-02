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

logger=getlog('agenthandle','agenthandle.log')
class updateagent(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/x-gzip")
        with open('agentservice.tar.gz','rb') as f:
            size=1024*1024
            content_cache=f.read(size)
            while content_cache:
                self.write(content_cache)
                content_cache=f.read(size)