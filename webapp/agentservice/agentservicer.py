#encoding=UTF-8
import os
import sys
import json
import pickle

from controller.agentcontroller import *
from models.agentmodel import *

from optparse import OptionParser
from signal import SIGTERM

settings = {}

application = tornado.web.Application([
    (r"/update",updataHandler),
    (r"/uploadinstallpackage/(.+)",upload),    
    (r"/restart",restart),
    (r"/installcluster",installcluster),
    (r"/getinstallstate",getinstallstate),
],**settings)

if __name__ == "__main__":
    usage = "usage: %prog -w or --webservicer 192.168.1.1"
    parser = OptionParser(usage=usage)
    parser.add_option("-w", "--webserver", action="store", type="string", dest="webserver", default="0.0.0.0:8888", help="The IP address of the webserver to bind with, if not given, use 0.0.0.0")
    parser.add_option("-n","--cluster", action="store", type="string", dest="clustername", help="The clustername to bind with, it must given!")
    parser.add_option("-p", "--port", action="store", type="int", dest="port", default="8080", help="The port of the agentserver listen to")
    parser.add_option("-u","--username",action="store",type="string",dest="username",help="The username use for ssh")
    options, args = parser.parse_args()
    if len(sys.argv) == 1:
        print('Type python %s -h or --help for options help.' % sys.argv[0])
    else:
        if options.clustername == "":
            print('the -n paramer must be given')
            sys.exit(1)
        if options.username == "":
            print('the -u paramer muset be given')
            sys.exit(1)
        #set username clusetername
        sshum=sshuserModel()
        sshum.setusername(options.username)
        sm=serverModel()
        sm.setserver(options.webserver)
        sm.setclustername(options.clustername)
        application.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

