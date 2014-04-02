#encoding=UTF-8
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.gen
import os
import sys
from tool.tool import *
import json
import logging
import pickle
#日志配置
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='asynservice.log',filemode='w')


class SendPackage(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type","application/text")
        try:
            choosepath='tmp/chooseinstall'
            packegpath='tmp/paths'
            hostspath='tmp/hosts'
            unppath='tmp/unp'
            zipdir='tmp/project.tar.gz '
            zipproject='project.tar.gz'
            totals=0
            finish=0
            #read the install project
            with open(choosepath,'r') as f:
                chooseinstall=pickle.load(f)

            with open(packegpath,'r') as f:
                packetsp=pickle.load(f)

            with open(hostspath,'r') as f:
                hosts= [i.split('\t') for i in f.read().split('\n')]

            with open(unppath,'r') as f:
                unp=f.read().strip('\n').split('\t')

            #tar scp ssh untar
            totals = len(hosts)*2+1
            prodir = [packetsp[chooseinstall[-1]][x].split(',')[1] for x in chooseinstall[0:-1]]
            cmds='tar -zcf '+ zipdir+' '.join(prodir)+' '+'tmp/confclientpath.sh'
            clientrun='sh tmp/confclientpath.sh '+' '.join(chooseinstall[0:-1])
            if runshcommand(cmds) is not None:
                logging.info('tar the project success')
                finish+=1
                runshcommand('echo '+str(finish*100/totals)+' >done')

            #scp and ssh untar and stepup the project
            for x in hosts:
                cmds='scp '+zipdir+unp[0]+'@'+x[0]+':~/ 2>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                    runshcommand('echo '+str(float(finish/totals)*100)+' >done')
                    logging.info(x[0]+" scp success!")
                else:
                    logging.error(x[0]+" scp error!")
                cmds='ssh '+unp[0]+'@'+x[0]+' "tar -zxvf '+ zipproject +' && '+clientrun+'" 2>>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                    runshcommand('echo '+str(float(finish/totals)*100)+' >done')
                    logging.info(x[0]+" has finished install the project")
                else:
                    logging.error(x[0]+" has failed to install the project")
            
            if finish==totals:
                self.write("success")
            else:
                self.write("error")

        except Exception ,e:
            runshcommand('echo "-1" >done')
            logging.error(e)
            self.write("error")

    def resetinstall(self):
        runshcommand('rm done')

settings = {
    "template_path":os.path.join(os.path.dirname(__file__),"view"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

#routing
application = tornado.web.Application([
    (r"/Install",SendPackage),    
],**settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
