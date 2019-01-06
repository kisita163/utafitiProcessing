'''
Created on Dec 18, 2018

@author: Hugues Kisita
'''

from parser import Parser
from statistique import Statistique
from sseclient import SSEClient
import json
import socket

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

         
def run():
    try:
        print 'starting'
        stat = Statistique()
        sse = ClosableSSEClient(URL)
        for msg in sse:

            msg_data = json.loads(msg.data)

            if msg_data is not None :
                parser = Parser();
                parser.dropRawData()
                stat.addQuestions(parser.getQuestions())
                stat.frequencyTableForQuestions()


    except socket.error:
        pass    # this can happen when we close the stream
    
    except KeyboardInterrupt:
        print 'Program stopped'

        

if __name__ == '__main__':
    run()
