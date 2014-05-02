#encoding=UTF-8
import os
import sys
import json
import pickle
import tornado
import tornado.httpclient

from controller.agentcontroller import *
from models.agentmodel import *

from optparse import OptionParser
from signal import SIGTERM

import random
import urllib

settings = {}

application = tornado.web.Application([
    (r"/update",updataHandler),
    (r"/uploadinstallpackage/(.+)",upload),    
    (r"/restart",restart),
    (r"/installcluster",installcluster),
    (r"/getinstallstate",getinstallstate),
    (r"/geterrorhost",geterrorhost),
    (r"/geterrorinfo/(.+)",geterrorinfo),
],**settings)


#the first time start must add the option as follow list:
#1.webserver address. for example: -w http://192.168.1.12
#2.the clustername that represent this agent server. for example: -n jeanlyn
if __name__ == "__main__":
    usage = "usage: %prog -w or --webservicer 192.168.1.1"
    parser = OptionParser(usage=usage)
    parser.add_option("-w", "--webserver", action="store", type="string", dest="webserver", default="http://0.0.0.0:8888", help="The IP address of the webserver to bind with, if not given, use 0.0.0.0")
    parser.add_option("-n","--cluster", action="store", type="string", dest="clustername", help="The clustername to bind with, it must given!")
    parser.add_option("-p", "--port", action="store", type="int", dest="port", default="8080", help="The port of the agentserver listen to")
    parser.add_option("-u","--username",action="store",type="string",dest="username",help="The username use for ssh")
    options, args = parser.parse_args()
    
    #new the servermodel to handle the data
    sm=serverModel()
    sshum=sshuserModel()
    if sm.isnotexist() :
        if options.clustername == "":
            print('the -n paramer must be given')
            sys.exit(1)
        if options.username == "":
            print('the -u paramer muset be given')
            sys.exit(1)
        token=sm.gettoken() if sm.gettoken() != '' else str(random.randint(100000000,200000000))
        result=[]
        try:
            client = tornado.httpclient.HTTPClient()
            respond=client.fetch(options.webserver+"/regitcluster?"+urllib.urlencode({"name":options.clustername,"token":token,"port":options.port}))            
            result=result+json.loads(respond.body)
        except Exception, e:
            print("can't not connect the webserver!Please make sure the -w option is correct"+str(e))
        #response data:{0:success,1:'the clustername has exist'}
        
        if type(result) == type([]):
            if result[0] == 0:
                #set username clusetername,webserver,token to the file                
                sshum.setusername(options.username)
                sm.setserver(options.webserver)
                sm.setclustername(options.clustername)
                sm.setport(str(options.port))
                sm.settoken(token)
                print("add cluster success")
                application.listen(int(sm.getport()))
                tornado.ioloop.IOLoop.instance().start()
            else:
                print("fail to connect the webserver:%s"%(result[1]))   
    else:
        if sm.getport()!='':
            application.listen(int(sm.getport()))
            tornado.ioloop.IOLoop.instance().start() 

        

