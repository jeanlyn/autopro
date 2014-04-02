#encoding=UTF-8
import os
import sys
from tool.tool import *
import json
import pickle
from tool.log import *
from models.agentmodel import *

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.gen

logging=getlog('asynhandler','asynhandler.log')

class installcluster(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/text')
        sm=serverModel()
        im=installModel(sm.getclustername())
        hosts=im.gethosts()
        project=im.getpropath()
        zipdir='project.tar.gz '        
        finish=0
        '''todo'''
        totals=len(hosts)*2+1
        clientrun='sh nodeinstall.sh '+sm.getclustername()
        runshcommand('echo "0" > done')
        user=sshuserModel().getusername()
        try:
            cmds='tar zcf '+zipdir+' '.join(project)+' nodeinstall.sh'
            if runshcommand(cmds) is not None:
                logging.info('tar the project success')
                finish+=1
                runshcommand('echo '+str(finish*100/totals)+' >done')
            #1.scp and 2.ssh untar 3.run nodeinstall.sh
            for x in hosts:
                #scp
                cmds='scp '+zipdir+user+'@'+x[0]+':~/ 2>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                    runshcommand('echo '+str(float(finish/totals)*100)+' >done')
                    logging.info(x[0]+" scp success!")
                else:
                    logging.error(x[0]+" scp error!")
                #ssh untar
                cmds='ssh '+user+'@'+x[0]+' "tar -zxvf '+ zipdir +' && '+clientrun+'" 2>>'+x[0]+'.error'
                if runshcommand(cmds) is not None:
                    finish+=1
                    runshcommand('echo '+str(float(finish/totals)*100)+' >done')
                    logging.info(x[0]+" has finished install the project")
                else:
                    logging.error(x[0]+" has failed to install the project")
        except Exception, e:
            logging.error(e)        

        if finish == totals:
            self.write("success")
        else:
            runshcommand('rm done')
            self.write("error")

#setting for application
settings = {
   
}

#routing
application = tornado.web.Application([
    (r"/installcluster",installcluster),    
    
],**settings)

if __name__ == "__main__":
    application.listen(8079)
    tornado.ioloop.IOLoop.instance().start()