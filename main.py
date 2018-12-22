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
                    self.app.update(questions)
                    
                
        except socket.error:
            pass    # this can happen when we close the stream
         
    def join(self, timeout=None):
        if self.sse:
            self.sse.close()
        self.stoprequest.set()
        super(RemoteThread, self).join(timeout)
        
        
        

class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        w,h = 650, 650
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        self.pack()
        
        if os.path.isfile('/path/to/file') == True:
            image_path = 'output/1.png'
        else:
            image_path = 'default/index.png'

        self.image = PhotoImage(file=image_path)
        self.imageLabel = Label(image=self.image,text="huhue",borderwidth=0)
        self.imageLabel.pack(padx=10)
        
        self.questionsLog = Listbox(width = 500, height = 500, takefocus=0)
        self.questionsLog.bind('<<ListboxSelect>>', self.onSelect)
        self.questionsLog.pack(padx=10,pady=10)
    
    def onSelect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        image_path = 'output/'+str(index + 1) + '.png'
        self.updateCurrentImage(image_path)

    def updateCurrentImage(self,image_path):
        
        im = PhotoImage(file=image_path)
        self.imageLabel.configure(image=im)
        self.imageLabel.image=im   

        
    def update(self,questions):
        im = PhotoImage(file='output/1.png')
        self.imageLabel.configure(image=im)
        self.imageLabel.image=im  
        
        self.questionsLog.delete(0,self.questionsLog.size()-1)
  
        for question in reversed(questions):
                self.questionsLog.insert(0, question)
        
        

if __name__ == '__main__':
    # Must be called before calling any function
    if not os.path.exists('output'):
        os.makedirs('output')
    else:
        for root, dirs, files in os.walk('output', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        
    inbound_queue = Queue()
    
    root = Tk()
    root.title("Utafiti")
    root.config(background = "#FFFFFF")
    app = GUI(master=root)
    
    remote_thread = RemoteThread(inbound_queue,app)
    remote_thread.daemon = True   
    remote_thread.start()
    
    app.mainloop()
    remote_thread.join()
    root.destroy()


        

    #parser = Parser();
    
    #stat = Statistique(parser.getQuestions());
    #stat.frequencyTableForQuestions()





