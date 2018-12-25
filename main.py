'''
Created on Dec 18, 2018

@author: Hugues Kisita
'''

from parser import Parser
from statistique import Statistique
from sseclient import SSEClient
from Queue import Queue
from Tkinter import *
import json
import threading
import socket
import os

URL   = 'https://caritas-50fab.firebaseio.com/survey.json'


class ClosableSSEClient(SSEClient):
    """
    Hack in some closing functionality on top of the SSEClient
    """

    def __init__(self, *args, **kwargs):
        self.should_connect = True
        super(ClosableSSEClient, self).__init__(*args, **kwargs)

    def _connect(self):
        if self.should_connect:
            super(ClosableSSEClient, self)._connect()
        else:
            raise StopIteration()

    def close(self):
        self.should_connect = False
        self.retry = 0
        # HACK: dig through the sseclient library to the requests library down to the underlying socket.
        # then close that to raise an exception to get out of streaming. I should probably file an issue w/ the
        # requests library to make this easier
        self.resp.raw._fp.fp._sock.shutdown(socket.SHUT_RDWR)
        self.resp.raw._fp.fp._sock.close()


class RemoteThread(threading.Thread):

    def __init__(self, message_queue,app_to_join):
        self.message_queue = message_queue
        self.app           = app_to_join
        super(RemoteThread, self).__init__()

    def run(self):
        try:
            print 'starting'
            stat = Statistique()
            self.sse = ClosableSSEClient(URL)
            for msg in self.sse:
                
                msg_data = json.loads(msg.data)
                
                if msg_data is not None :
                    parser = Parser();
                    stat.addQuestions(parser.getQuestions())
                    questions = stat.frequencyTableForQuestions()
                    if self.app is not None:
                        self.app.update(questions)
                    
                
        except socket.error:
            pass    # this can happen when we close the stream
         
    def join(self, timeout=None):
        super(RemoteThread, self).join(timeout)
        
        

if __name__ == '__main__':
    # Must be called before calling any function
        
    inbound_queue = Queue()
    
    remote_thread = RemoteThread(inbound_queue,None)
    remote_thread.daemon = True   
    remote_thread.start()
    remote_thread.join()

