'''
Created on Dec 18, 2018

@author: Hugues Kisita
'''

from parser import Parser
from statistique import Statistique


if __name__ == '__main__':
    # Must be called before calling any function
    parser = Parser();
    
    stat = Statistique(parser.getQuestions());
    stat.frequencyTableForQuestions()





