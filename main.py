'''
Created on Dec 18, 2018

@author: Hugues Kisita
'''
import firebase_admin

from firebase_admin import credentials
from parser import Parser
from statistique import Statistique



    
def initApp():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('/home/firebase/firebase/caritas-50fab-b10622860737.json')
    # Initialize the application with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://caritas-50fab.firebaseio.com/'})

if __name__ == '__main__':
    # Must be called before calling any function
    initApp()
    parser = Parser();
    
    stat = Statistique(parser.getQuestions());
    stat.frequencyTableForQuestions()





